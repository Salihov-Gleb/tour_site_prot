# Generated by Django 3.2.8 on 2021-11-26 14:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Название')),
                ('image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Изображение')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Обновление')),
                ('mean_rate', models.FloatField(blank=True, verbose_name='Оценка')),
                ('contacts', models.CharField(blank=True, max_length=100, verbose_name='Контакты')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ('-update_date', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Фотография')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.post', verbose_name='Объявление')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], validators=[django.core.validators.MaxValueValidator(5)])),
                ('text', models.TextField(blank=True, max_length=300, verbose_name='Текст')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.post', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-datetime',),
            },
        ),
    ]
