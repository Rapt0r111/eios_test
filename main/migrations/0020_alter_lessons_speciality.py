# Generated by Django 4.0.2 on 2022-04-27 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_files_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.speciality'),
        ),
    ]
