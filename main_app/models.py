from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=80, verbose_name='Название')
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Изображение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    update_date = models.DateField(auto_now_add=True, verbose_name='Обновление')
    mean_rate = models.FloatField(blank=True, verbose_name='Оценка', null=True)
    contacts = models.CharField(blank=True, max_length=100, verbose_name='Контакты')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def calculate_mean_rate(self):
        print(len(self.comment_set.all()))
        if len(self.comment_set.all()) == 0:
            self.mean_rate = None
        else:
            self.mean_rate = round(sum([x.rate for x in self.comment_set.all()]) / len(self.comment_set.all()), 1)
        print(self.mean_rate)
        self.save()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-update_date', 'title')


class Photos(models.Model):
    photo = models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Фотография')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление', related_name='photos')


class Comment(models.Model):
    RATE_CHOICES = [
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично')
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, validators=[MaxValueValidator(5)], verbose_name='Оценка')
    text = models.TextField(blank=True, max_length=300, verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    datetime = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-datetime',)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.post.calculate_mean_rate()
