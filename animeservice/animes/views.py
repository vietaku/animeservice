from django.contrib.auth.models import User, Group
from animeservice.animes.models import Anime, Studio
from rest_framework import viewsets
from rest_framework import permissions
from animeservice.animes.serializers import AnimeSerializer, UserSerializer, GroupSerializer, StudioSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [permissions.IsAuthenticated]

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

# Define a dictionary to map seasons to their start dates
season_start_month = {
    'winter': 1,
    'spring': 4,
    'summer': 7,
    'fall': 10
}