# Generated by Django 4.1.7 on 2023-03-21 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='translated_synopsis',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='translated_synopsis2',
        ),
        migrations.AddField(
            model_name='anime',
            name='translated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
