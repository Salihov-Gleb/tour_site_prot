from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse

from main_app.models import Post, Comment, Photos
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.admin.views.decorators import staff_member_required
from main_app.forms import PostForm, CommentForm, UserLoginForm, UserSignupForm


class PostList(ListView):
    model = Post
    template_name = 'main_app/post_list.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Предложения'}


class CurrentUserPostList(ListView):
    model = Post
    template_name = 'main_app/post_list.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Мои объявления'}

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.id)


class UserPostList(ListView):
    model = Post
    template_name = 'main_app/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.get['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Объявления пользователя {user.username}'
        return context


class SearchResultView(ListView):
    model = Post
    template_name = 'main_app/post_list.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Результаты поиска'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(
            Q(title__icontains=query) | Q(address__icontains=query) | Q(description__icontains=query)
        )


class PostDetail(DetailView):
    model = Post
    template_name = 'main_app/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(self.request.POST or None)
        return context


class CommentCreate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['pk'])
        if form.is_valid():
            if len(post.comment_set.filter(author=request.user)) != 0:
                messages.error(request, 'Вы уже оставили отзыв')
                return redirect(post.get_absolute_url())
            if request.user == post.owner:
                messages.error(request, 'Нельзя оставлять отзыв под своей записью')
                return redirect(post.get_absolute_url())
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.post = post
            new_comment.save()
            print(post)
            post.calculate_mean_rate()
            return redirect(post.get_absolute_url())
        messages.error(request, 'Не удалось оставить комментарий')
        return redirect(post.get_absolute_url())


class CommentDelete(DeleteView):
    model = Comment
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != Comment.objects.get(pk=kwargs['pk']).author.pk:
            return HttpResponseForbidden()
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object.post
        response = super().delete(request, *args, **kwargs)
        post.calculate_mean_rate()
        return response

    def get_success_url(self):
        post = self.object.post
        return post.get_absolute_url()


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'main_app/create_post.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        post = form.save()
        for f in self.request.FILES.getlist('photos'):
            data = f.read()
            photo = Photos(post=post)
            photo.photo.save(f.name, ContentFile(data))
            photo.save()
        return redirect(post.get_absolute_url())


class EditPost(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'main_app/update_post.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.owner == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise Http404
        return super(EditPost, self).dispatch(request, *args, **kwargs)


class PostDelete(DeleteView):
    model = Post
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.model.objects.get(pk=kwargs['pk']).owner.pk:
            return HttpResponseForbidden()
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('my_posts')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'main_app/login.html', context={'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна')
            return redirect('main')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserSignupForm()
    return render(request, 'main_app/signup.html', context={'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
