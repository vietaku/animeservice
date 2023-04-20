import pytz
import requests
from animeservice.animes.models import Anime, Studio, Tag, Url
from animeservice.animes.utils import AnimeSeason, update_or_create_anime
from django.core.management.base import BaseCommand
from datetime import datetime
import urllib.parse

# initial url to fetch animes from MAL
def get_url(id):
    fields = "pictures,background,related_anime,related_manga,recommendations,statistics"
    url = f"https://api.myanimelist.net/v2/anime/{id}?fields={fields}"
    
    return url

def get_current_url_object():
    url_object, created = Url.objects.get_or_create(id=2)

    if created:
        url_object.url = 1
        url_object.save()

    return url_object

def get_anime_object_by_id(id):
    anime_object = Anime.objects.get(mal_id=id)
    return anime_object

def get_next_anime_id(id):
    url_object = Anime.objects.filter(mal_id__gt=id).order_by('mal_id').first()
    if url_object is None:
        return None
    return url_object.mal_id

def is_all_animes_fetched():
    url_object = get_current_url_object()
    return url_object.url == "done"

def fetch_anime(process):
    if is_all_animes_fetched():
            process.stdout.write(process.style.WARNING("All animes fetched"))
            return

    process.stdout.write("Fetching animes")

    url_object = get_current_url_object()
    anime_object = get_anime_object_by_id(url_object.url)

    headers = {
        "X-MAL-CLIENT-ID": "4a17101ff85b13ca8baaa4c6ede7d567",
    }

    url = get_url(anime_object.mal_id)
    process.stdout.write(f"Fetching {anime_object.title}")
    response = requests.get(url, headers=headers)
    data = response.json()

    anime_object.pictures = data["pictures"]
    anime_object.background = data["background"]
    anime_object.related_anime = data["related_anime"]
    anime_object.related_manga = data["related_manga"]
    anime_object.recommendations = data["recommendations"]
    anime_object.statistics = data["statistics"]
    anime_object.save()

    next_id = get_next_anime_id(anime_object.mal_id)

    if next_id is None:
        url_object.url = "done"
        url_object.save()
        process.stdout.write(process.style.SUCCESS("Reached the end of the list"))
    else:
        url_object.url = next_id
        url_object.save()
        process.stdout.write(process.style.WARNING("Saved next url"))

# Fetch animes from MAL if it's the first day of the month
class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        for i in range(25):
            fetch_anime(self)

        self.stdout.write(self.style.SUCCESS("FINISHED FETCHING DATA, UPDATED TO DB"))