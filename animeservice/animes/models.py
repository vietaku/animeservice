import datetime
from django.db import models
from tinymce.models import HTMLField
from django.conf import settings

class Studio(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, update_firebase=True, *args, **kwargs):
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
    
    class Meta:
        ordering = ("rank", "popularity", "mean")

    def __str__(self):
        return self.title

    def save(self, update_firebase=True, *args, **kwargs):
        super(Anime, self).save(*args, **kwargs)

# class AnimeQuery(models.Model):
#     name = models.CharField(max_length=50, null=True, blank=True)

#     # Path Parameters
#     year = models.IntegerField(default=datetime.date.today().year)
#     ANIME_SEASON_CHOICES = [
#         ('winter', 'Winter'),
#         ('spring', 'Spring'),
#         ('summer', 'Summer'),
#         ('fall', 'Fall')
#     ]
#     season = models.CharField(max_length=10, default='winter', choices=ANIME_SEASON_CHOICES)

#     # Query Parameters
#     SORT_CHOICES = [
#         ('anime_score', 'Anime Score'),
#         ('anime_num_list_users', 'Anime Number List Users'),
#     ]
#     sort = models.CharField(max_length=20, default='anime_score', choices=SORT_CHOICES)
#     get_all_available_animes = models.BooleanField(default=True)
#     limit = models.IntegerField(default=100, null=True, blank=True)
#     offset = models.IntegerField(default=0, null=True, blank=True)

#     # Fields Parameters
#     get_all_fields = models.BooleanField(default=True)
#     overide_value = models.BooleanField(default=True)
#     title = models.BooleanField(default=False)
#     main_picture = models.BooleanField(default=False)
#     alternative_titles = models.BooleanField(default=False)
#     start_date = models.BooleanField(default=False)
#     end_date = models.BooleanField(default=False)
#     synopsis = models.BooleanField(default=False)
#     mean = models.BooleanField(default=False)
#     rank = models.BooleanField(default=False)
#     popularity = models.BooleanField(default=False)
#     genres = models.BooleanField(default=False)
#     media_type = models.BooleanField(default=False)
#     status = models.BooleanField(default=False)
#     num_episodes = models.BooleanField(default=False)
#     start_season = models.BooleanField(default=False)
#     broadcast = models.BooleanField(default=False)
#     source = models.BooleanField(default=False)
#     average_episode_duration = models.BooleanField(default=False)
#     studios = models.BooleanField(default=False)
#     nsfw = models.BooleanField(default=False)
#     rating = models.BooleanField(default=False)

#     def get_fields_char(self):
#         if self.get_all_fields:
#             return 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw,genres,media_type,status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,studios'
#         fields = ""
#         if self.main_picture: fields += 'main_picture,'
#         if self.alternative_titles: fields += 'alternative_titles,'
#         if self.start_date: fields += 'start_date,'
#         if self.end_date: fields += 'end_date,'
#         if self.synopsis: fields += 'synopsis,'
#         if self.mean: fields += 'mean,'
#         if self.rank: fields += 'rank,'
#         if self.popularity: fields += 'popularity,'
#         if self.genres: fields += 'genres,'
#         if self.media_type: fields += 'media_type,'
#         if self.status: fields += 'status,'
#         if self.num_episodes: fields += 'num_episodes,'
#         if self.start_season: fields += 'start_season,'
#         if self.broadcast: fields += 'broadcast,'
#         if self.source: fields += 'source,'
#         if self.average_episode_duration: fields += 'average_episode_duration,'
#         if self.studios: fields += 'studios,'
#         if self.nsfw: fields += 'nsfw,'
#         if self.rating: fields += 'rating,'
#         if self.title: fields += 'title,'
#         fields += 'id'
#         return 