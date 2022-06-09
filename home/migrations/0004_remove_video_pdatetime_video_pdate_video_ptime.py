# Generated by Django 4.0.5 on 2022-06-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_video_pdatetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='pdatetime',
        ),
        migrations.AddField(
            model_name='video',
            name='pdate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='ptime',
            field=models.TimeField(auto_now=True),
        ),
    ]