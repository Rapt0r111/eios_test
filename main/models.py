import time
import uuid
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.deconstruct import deconstructible
import os
from django.utils.safestring import mark_safe
from pytils.translit import slugify


@deconstructible
class PathAndRename():

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = "{}.{}".format(filename.split(".")[0] + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class Speciality(models.Model):
    speciality = models.CharField("Название специальности", max_length=8)

    def __str__(self):
        return self.speciality

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class CustomUser(AbstractUser):
    content = models.TextField('Описание', max_length=500, blank=True)
    email = models.EmailField('Email', unique=True)
    avatar = models.ImageField("Фотография профиля", upload_to="images/avatars/", blank=True,
                               default='/images/avatars/user.png')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     self.username = self.username.lower()
    #     return super(CustomUser, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150"  />' % (self.avatar))

    image_tag.short_description = 'Текущая'


class Lessons(models.Model):
    name = models.CharField("Название предмета", max_length=100, db_index=True)
    photo = models.ImageField("Фотография предмета", upload_to="images/lessons/")
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def get_absolute_url(self):
        return reverse('lessons', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        x = self.slug
        self.slug = slugify(self.name+'-'+str(self.speciality))
        LessonsDescriptions.objects.filter(lesson_id=x).update(lesson_id=self.slug)
        super(Lessons, self).save(*args, **kwargs)


class LessonsDescriptions(models.Model):
    topic = models.CharField(max_length=100, verbose_name='Тема')
    lesson = models.ForeignKey('Lessons', on_delete=models.CASCADE, verbose_name='Урок',to_field='slug')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Files(models.Model):
    EDUCATION_TYPES = (
        ('', 'Ничего не выбрано'),
        ('resources/icons/word.ico', 'Word'),
        ('resources/icons/pdf.ico', 'PDF'),
        (' ', 'Другой формат'),
    )
    lesDesc = models.ForeignKey(LessonsDescriptions, on_delete=models.CASCADE)
    name = models.CharField("Название файла",max_length=100, default='Неизвестный')
    topic_content = models.FileField("Файл", upload_to=PathAndRename("resources/lessons/"))
    file_type = models.FileField("Тип файла",choices=EDUCATION_TYPES, null=True, blank=True)

    def filename(self):
        filename = "{}".format(self.topic_content.name.split(".")[0])
        return os.path.basename(filename[:-17])

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'



