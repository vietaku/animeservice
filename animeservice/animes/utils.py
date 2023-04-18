from animeservice.animes.models import Anime, Studio, Tag
from datetime import datetime
from dateutil import parser
import pytz

class AnimeSeason:
    def currentSeason(self):
        currentMonth = datetime.now().month
        MONTH_TO_SEASON = [
            "winter",
            "winter",  
            "winter",
            "spring",
            "spring",
            "spring",
            "summer",
            "summer",
            "summer",
            "fall",
            "fall",
            "fall",
        ]
        return MONTH_TO_SEASON[currentMonth]

    def __init__(self, season=None, year=None):
        self.season = season if season is not None else self.currentSeason()
        self.year = year if year is not None else datetime.now().year
        if datetime.now().month == 12:
            self.year += 1


# update or create an Anime from dict
def update_or_create_anime(data):
    # print(data["title"])
    # Anime(**data).save()
    # print(f"PROCESSING {data['title']}")
    # print(f"DJANGO DATABASE: adding {data['title']} ({data['id']})")

    data_studios = []
    if "studios" in data:
        data_studios = [s for s in data["studios"]]
        data.pop("studios")

    data_tags = []
    if "genres" in data:
        data_tags = [t for t in data["genres"]]
        data.pop("genres")

    anime_id = data["id"]
    data.pop("id")

    if "start_date" in data:
        date_time = parser.parse(data.get("start_date"))
        data["start_date"] = date_time.astimezone(
            pytz.timezone("Australia/Sydney")
        )

    if "end_date" in data:
        date_time = parser.parse(data.get("end_date"))
        data["end_date"] = date_time.astimezone(
            pytz.timezone("Australia/Sydney")
        )

    if (
        Anime.objects.filter(pk=anime_id).exists()
        and Anime.objects.get(pk=anime_id).is_translated
    ):
        anime, created = Anime.objects.get_or_create(
            pk=anime_id, defaults={**data}
        )
    else:
        anime, created = Anime.objects.update_or_create(
            pk=anime_id, defaults={**data}
        )

    for s in data_studios:
        studio, created = Studio.objects.get_or_create(
            pk=s["id"], defaults={"name": s["name"]}
        )
        anime.studios.add(studio)

    for t in data_tags:
        tag, created = Tag.objects.get_or_create(
            pk=t["id"], defaults={"name": t["name"]}
        )
        anime.tags.add(tag)