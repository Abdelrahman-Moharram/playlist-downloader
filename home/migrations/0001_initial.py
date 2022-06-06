# Generated by Django 4.0.5 on 2022-06-05 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('url', models.CharField(max_length=500)),
                ('d_datetime', models.CharField(max_length=50)),
                ('local_src', models.FileField(upload_to=home.models.save_video)),
                ('thumbnail', models.CharField(max_length=300)),
                ('file_type', models.IntegerField(default=1)),
                ('link_type', models.IntegerField(default=1)),
                ('length', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
