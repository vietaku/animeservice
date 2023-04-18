import pytz
import requests
from animeservice.animes.models import Anime, Studio, Tag, Url
from animeservice.animes.utils import AnimeSeason, update_or_create_anime
from django.core.management.base import BaseCommand
from datetime import datetime
import urllib.parse

# initial url to fetch animes from MAL
def initial_url():
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw\
    ,genres,media_type,status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,studios"

    MAX_LIMIT_NUMBER_OF_ANIME = 500

    params  = {
        "ranking_type": "all",
        "limit": MAX_LIMIT_NUMBER_OF_ANIME,
        "offset": "0",
        "fields": fields,
    }

    url = "https://api.myanimelist.net/v2/anime/ranking?"+urllib.parse.urlencode(params)
    
    return url

def get_or_create_url_object():
    url_object, created = Url.objects.get_or_create(id=1)

    if created:
        url = initial_url() 
        url_object.url = url
        url_object.save()

    return url_object

def is_all_animes_fetched():
    url_object = get_or_create_url_object()
    return url_object.url == "done"

# Fetch animes from MAL if it's the first day of the month
class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        if is_all_animes_fetched():
            self.stdout.write(self.style.WARNING("All animes fetched"))
            return

        self.stdout.write("Fetching animes ranking")

        url_object = get_or_create_url_object()

        headers = {
            "X-MAL-CLIENT-ID": "4a17101ff85b13ca8baaa4c6ede7d567",
        }

        for i in range(100):
            url = url_object.url
            self.stdout.write(f"Fetching {url}")

            response = requests.get(url, headers=headers)
            jsonResponse = response.json()

            for node in jsonResponse["data"]:
                data = node["node"]
                update_or_create_anime(data)
                self.stdout.write((f"FINISHED PROCESSING {data['title']}"))

            if "next" not in jsonResponse["paging"]:
                url_object.url = "done"
                url_object.save()
                break

            url_object.url = jsonResponse["paging"]["next"]
            url_object.save()

            self.stdout.write("Fetching next page")

        self.stdout.write(self.style.SUCCESS("FINISHED FETCHING DATA, UPDATED TO DB"))