from django.contrib.auth.models import User, Group
from animeservice.animes.models import Studio, Anime, Tag
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class StudioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Studio
        fields = ['url', 'id', 'name']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name_translated']

class AnimeSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    studios = serializers.StringRelatedField(many=True)

    class Meta:
        model = Anime
        fields = '__all__'