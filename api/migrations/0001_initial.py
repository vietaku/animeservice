# Generated by Django 4.1.7 on 2023-03-11 04:15

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('name_translated', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('is_translated', models.BooleanField(default=False)),
                ('mal_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('main_picture', models.JSONField(blank=True, null=True)),
                ('alternative_titles', models.JSONField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('synopsis', tinymce.models.HTMLField(blank=True, null=True)),
                ('translated_synopsis2', tinymce.models.HTMLField(blank=True, null=True)),
                ('translated_synopsis', models.TextField(blank=True, null=True)),
                ('mean', models.FloatField(blank=True, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('popularity', models.IntegerField(blank=True, null=True)),
                ('media_type', models.CharField(blank=True, max_length=10)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('num_episodes', models.IntegerField(blank=True)),
                ('start_season', models.JSONField(blank=True, null=True)),
                ('broadcast', models.JSONField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=20, null=True)),
                ('average_episode_duration', models.IntegerField(blank=True, null=True)),
                ('nsfw', models.CharField(blank=True, max_length=20, null=True)),
                ('rating', models.CharField(blank=True, max_length=20, null=True)),
                ('studios', models.ManyToManyField(blank=True, to='api.studio')),
                ('tags', models.ManyToManyField(blank=True, to='api.tag')),
            ],
        ),
    ]
