from animeservice.animes.models import Anime
from django.core.management.base import BaseCommand
from .firebase import *
import requests
from animeservice.animes.management.commands.fetchanime import update_or_create_anime
from django.contrib.auth.models import User

# get all animes id from firebase
def get_animes():
    snapshots = db.collection(u'animes').where(u'is_translated', u'==', True).stream()

    ids = []
    animes = []

    for snapshot in snapshots:
        anime = snapshot.to_dict()
        ids.append(snapshot.id)
        animes.append(anime)

    return animes, ids

# fetch anime details from MyAnimeList API by id
def get_anime_details(id):
    url = f"https://api.myanimelist.net/v2/anime/{id}"
    headers = {
        "X-MAL-CLIENT-ID": "4a17101ff85b13ca8baaa4c6ede7d567",
    }
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw\
        ,genres,media_type,status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,studios"
    payload = {
        "fields": fields,
    }
    
    response = requests.get(url, headers=headers, params=payload)
    jsonResponse = response.json()
    update_or_create_anime(jsonResponse)
    return jsonResponse



class Command(BaseCommand):
    help = "Syncs animes from Firebase to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='Force to fetch animes regardless of the date',
        )

    def handle(self, *args, **options):
        # get all animes from firebase
        animes, ids = get_animes()

        # loop through all animes and fetch details from MyAnimeList API
        for id in ids:
            self.stdout.write(f"Fetching anime with id {id}")
            get_anime_details(id)
            self.stdout.write(f"Finished fetching anime with id {id}")

            self.stdout.write(f"Updating anime with id {id}")
            anime = Anime.objects.get(mal_id=id)
            anime.synopsis = animes[ids.index(id)]['translated_synopsis']
            self.stdout.write(f"{anime.synopsis}")
            anime.is_translated = True
            anime.translated_by = User.objects.get(username='baotong')
            anime.save()
            self.stdout.write(f"Finished updating anime with id {id}")