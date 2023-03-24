from django.contrib.auth.models import User, Group
from animeservice.animes.models import Anime, Studio
from rest_framework import viewsets
from rest_framework import permissions
from animeservice.animes.serializers import AnimeSerializer, UserSerializer, GroupSerializer, StudioSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]