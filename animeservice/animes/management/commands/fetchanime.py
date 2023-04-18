import pytz
import requests
from animeservice.animes.models import Anime, Studio, Tag
from animeservice.animes.utils import AnimeSeason, update_or_create_anime
from django.core.management.base import BaseCommand
from datetime import datetime

# prepare url to fetch animes from MAL
def prepare_url(year, season):
    url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season}"

    headers = {
        "X-MAL-CLIENT-ID": "4a17101ff85b13ca8baaa4c6ede7d567",
    }

    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,nsfw\
    ,genres,media_type,status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,studios"

    MAX_LIMIT_NUMBER_OF_ANIME = 500

    payload = {
        "sort": "anime_num_list_users",
        "limit": MAX_LIMIT_NUMBER_OF_ANIME,
        "offset": "0",
        "fields": fields,
    }

    return url, headers, payload

# Fetch seasonal animes from MAL if it's the first day of the month
class Command(BaseCommand):
    help = "Fetch seasonal animes from MAL if it's the first day of the month"

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='Force to fetch animes regardless of the date',
        )
        parser.add_argument('-y', '--year', type=int, help='The year')
        parser.add_argument('-s', '--season', type=str, help='The season (e.g. winter, spring, summer, fall)')
        
        
    def handle(self, *args, **options):
        if not self.can_fetch_anime(options):
            return
        
        self.stdout.write("Fetching animes")

        currentAnimeSeason = AnimeSeason()
        year = options['year'] if options['year'] != None else currentAnimeSeason.year
        season = options['season'] if options['season'] != None else currentAnimeSeason.season

        url, headers, payload = prepare_url(year, season)
        print(url)

        response = requests.get(url, headers=headers, params=payload)
        jsonResponse = response.json()

        while True:
            for node in jsonResponse["data"]:
                data = node["node"]
                update_or_create_anime(data)
                self.stdout.write((f"FINISHED PROCESSING {data['title']}"))

            if "next" not in jsonResponse["paging"]:
                break

            url = jsonResponse["paging"]["next"]
            self.stdout.write("Fetching next page")
            response = requests.get(url, headers=headers)
            jsonResponse = response.json()
        self.stdout.write(self.style.SUCCESS("FINISHED FETCHING DATA, UPDATED TO DB"))

    # Check from options if we can fetch anime from MAL
    def can_fetch_anime(self, options):
        isForcing = bool(options['force'])
        if isForcing:
            return True

        hasSeasonalOptions = options['year'] != None and options['season'] != None
        isTheFirstDayOfTheMonth = datetime.now().day == 1

        if not (isTheFirstDayOfTheMonth or hasSeasonalOptions):
            self.stdout.write(self.style.WARNING("Not fetching today"))
            return False
        
        isSeasonValid = options ['season'] in ['winter', 'spring', 'summer', 'fall']
        if not isSeasonValid:
            self.stdout.write(self.style.ERROR("Invalid season"))
            return False
        
        return True