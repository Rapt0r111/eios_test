# Generated by Django 4.0.2 on 2022-04-19 11:49

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_files_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='topic_content',
            field=models.FileField(blank=True, upload_to=main.models.PathAndRename('resources/lessons/')),
        ),
    ]