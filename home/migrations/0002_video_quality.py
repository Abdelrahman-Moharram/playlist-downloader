# Generated by Django 4.0.5 on 2022-06-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='quality',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
