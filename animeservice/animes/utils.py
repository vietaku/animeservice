from datetime import datetime


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