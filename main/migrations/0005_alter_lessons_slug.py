# Generated by Django 4.0.2 on 2022-04-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_lessons_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
