# Generated by Django 4.0.2 on 2022-04-14 21:20

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Название предмета')),
                ('photo', models.ImageField(upload_to='images/lessons/', verbose_name='Фотография предмета')),
                ('course', models.PositiveSmallIntegerField(default=1, verbose_name='Номер курса предмета(Целое положительное число не больше 10)')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=8, verbose_name='Название специальности')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
            },
        ),
        migrations.CreateModel(
            name='LessonsDescriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Тема')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.lessons', verbose_name='Урок')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.AddField(
            model_name='lessons',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.speciality'),
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Неизвестный', max_length=100)),
                ('topic_content', models.FileField(upload_to=main.models.PathAndRename('resources/lessons/'))),
                ('file_type', models.FileField(choices=[('resources/icons/word.ico', 'Word'), ('resources/icons/pdf.ico', 'PDF')], null=True, upload_to='')),
                ('lesDesc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.lessonsdescriptions')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('content', models.TextField(blank=True, max_length=500, verbose_name='Описание')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('avatar', models.ImageField(blank=True, default='/images/avatars/user.png', upload_to='images/avatars/', verbose_name='Фотография профиля')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.speciality')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
