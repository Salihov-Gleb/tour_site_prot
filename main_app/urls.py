from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.PostList.as_view(), name='main'),
    path('my_posts/', views.CurrentUserPostList.as_view(), name='my_posts'),
    path('user_posts/<int:pk>/', views.UserPostList.as_view(), name='user_posts'),
    path('search/', views.SearchResultView.as_view(), name='search_post'),
    path('post_detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('edit_post/<int:pk>/', views.EditPost.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', views.PostDelete.as_view(), name='delete_post'),
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('create_comment/<int:pk>/', views.CommentCreate.as_view(), name='create_comment'),
    path('delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='delete_comment'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]