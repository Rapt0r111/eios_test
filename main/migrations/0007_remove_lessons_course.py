# Generated by Django 4.0.2 on 2022-04-16 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_lessons_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='course',
        ),
    ]
