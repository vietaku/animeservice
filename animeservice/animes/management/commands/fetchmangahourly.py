import pytz
import requests
from animeservice.animes.models import Manga, Url
from django.core.management.base import BaseCommand
from datetime import datetime
import urllib.parse

# initial url to fetch animes from MAL
def initial_url():
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw\
    ,genres,media_type,status,num_volumes,num_chapters,authors"

    MAX_LIMIT_NUMBER_OF_MANGA = 500

    params  = {
        "ranking_type": "all",
        "limit": MAX_LIMIT_NUMBER_OF_MANGA,
        "offset": "0",
        "fields": fields,
    }

    url = "https://api.myanimelist.net/v2/manga/ranking?"+urllib.parse.urlencode(params)
    
    return url

def get_or_create_url_object():
    url_object, created = Url.objects.get_or_create(id=3)

    if created:
        url = initial_url() 
        url_object.url = url
        url_object.save()

    return url_object

def is_all_mangas_fetched():
    url_object = get_or_create_url_object()
    return url_object.url == "done"



# Fetch mangas from MAL if it's the first day of the month
class Command(BaseCommand):
    def handle(self, *args, **options):
        if is_all_mangas_fetched():
            self.stdout.write(self.style.WARNING("All mangas fetched"))
            return

        self.stdout.write("Fetching mangas ranking")

        url_object = get_or_create_url_object()

        headers = {
            "X-MAL-CLIENT-ID": "4a17101ff85b13ca8baaa4c6ede7d567",
        }

        for i in range(10):
            url = url_object.url
            self.stdout.write(f"Fetching {url}")

            response = requests.get(url, headers=headers)
            jsonResponse = response.json()

            for node in jsonResponse["data"]:
                data = node["node"]
                manga_id = data["id"]
                manga, created = Manga.objects.get_or_create(
                    pk=manga_id, 
                    defaults={"mal_data": data})
                if (created):
                    self.stdout.write(self.style.SUCCESS(f"Created {data['title']} ({manga.id})"))

            
            if "next" not in jsonResponse["paging"]:
                url_object.url = "done"
                url_object.save()
                self.stdout.write(self.style.SUCCESS("Reached the end of the list"))
                break

            url_object.url = jsonResponse["paging"]["next"]
            url_object.save()
            self.stdout.write(self.style.WARNING("Saved next url"))

        self.stdout.write(self.style.SUCCESS("FINISHED FETCHING DATA, UPDATED TO DB"))