from django.contrib.auth.models import User, Group
from animeservice.animes.models import Anime, Studio
from rest_framework import viewsets
from animeservice.animes.serializers import AnimeSerializer, UserSerializer, GroupSerializer, StudioSerializer
import csv
from django.http import HttpResponse
from django.db.models.functions import TruncDate

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class StudioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

class SeasonalAnimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        season = self.kwargs['season']

        if season not in ['winter', 'spring', 'summer', 'fall']:
            return Anime.objects.none()
        
        start_month = f'{season_start_month[season]}'
        end_month = f'{season_start_month[season]+3}'

        print(f'year: {year}, season: {season}, start_month: {start_month}, end_month: {end_month}')
        
        queryset = Anime.objects.filter(
            start_date__year=year, 
            start_date__month__range=(start_month, end_month),
        )
        return queryset

def export_animes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="animes.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'average_episode_duration', 'mean', 'media_type', 'nsfw', 'num_episodes', 'popularity', 'rank', 'rating', 'source', 'start_date', 'status', 'studios', 'tags'])

    for anime in Anime.objects.annotate(start_date_trunced=TruncDate('start_date')).all().values_list('mal_id', 'title', 'average_episode_duration', 'mean', 'media_type', 'nsfw', 'num_episodes', 'popularity', 'rank', 'rating', 'source', 'start_date_trunced', 'status', 'studios__name', 'tags__name'):
        writer.writerow(anime)

    return response

def export_anime_initial_recommendations(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anime_recommendations.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'recommendation_id', 'recommendation_title', 'num_recommendations'])

    for anime in Anime.objects.all():
        recommendations = anime.recommendations
        if recommendations is not None:
            for recommendation in recommendations:
                data = recommendation['node']
                writer.writerow([anime.mal_id, anime.title, data['id'], data['title'], recommendation['num_recommendations']])

    return response

def export_anime_statistics(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anime_statistics.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'status_dropped', 'status_on_hold', 'status_watching', 'status_completed', 'status_plan_to_watch', 'num_list_users'])

    for anime in Anime.objects.all():
        data = anime.statistics
        if data is not None:
            writer.writerow([anime.mal_id, data['status']['dropped'], data['status']['on_hold'], data['status']['watching'], data['status']['completed'], data['status']['plan_to_watch'], data['num_list_users']])

    return response

def export_anime_relations(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anime_relations.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'relation_id', 'relation_title', 'relation_type'])

    for anime in Anime.objects.all():
        relations = anime.related_anime
        if relations is not None:
            for relation in relations:
                data = relation['node']
                writer.writerow([anime.mal_id, anime.title, data['id'], data['title'], relation['relation_type']])

    return response

# Define a dictionary to map seasons to their start dates
season_start_month = {
    'winter': 1,
    'spring': 4,
    'summer': 7,
    'fall': 10
}