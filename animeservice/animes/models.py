import datetime
from django.db import models
from tinymce.models import HTMLField
from django.conf import settings

class Studio(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Studio, self).save(*args, **kwargs)

class Tag(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    name_translated = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return str(self.name_translated) + " (" + self.name + ")"

    def save(self, update_firebase=True, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)

class Anime(models.Model):
    # Added Fields
    is_translated = models.BooleanField(default=False)
    translated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    # Fields from MAL
    mal_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    main_picture = models.JSONField(null=True, blank=True)
    alternative_titles = models.JSONField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    synopsis = HTMLField(null=True, blank=True)
    mean = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    media_type = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, blank=True)
    num_episodes = models.IntegerField(blank=True)
    start_season = models.JSONField(null=True, blank=True)
    broadcast = models.JSONField(null=True, blank=True)
    source = models.CharField(max_length=20, null=True, blank=True)
    average_episode_duration = models.IntegerField(null=True, blank=True)
    studios = models.ManyToManyField(Studio, blank=True)
    nsfw = models.CharField(max_length=20, null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    pictures = models.JSONField(null=True, blank=True)
    background = HTMLField(null=True, blank=True)
    related_anime = models.JSONField(null=True, blank=True)
    related_manga = models.JSONField(null=True, blank=True)
    recommendations = models.JSONField(null=True, blank=True)
    statistics = models.JSONField(null=True, blank=True)


    class Meta:
        ordering = ("rank", "popularity", "mean")

    def __str__(self):
        return self.title
    
    def save(self, update_firebase=True, *args, **kwargs):
        super(Anime, self).save(*args, **kwargs)

class Url(models.Model):
    id = models.IntegerField(primary_key=True)
    # url text field
    url = models.TextField(null=True, blank=True)