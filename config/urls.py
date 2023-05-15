from django.urls import include, path
from rest_framework import routers
from animeservice.animes import views
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'animes', views.AnimeViewSet)
router.register(r'animes/season/(?P<year>[0-9]{4})/(?P<season>\w+)', views.SeasonalAnimeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'studios', views.StudioViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', RedirectView.as_view(url='dich/', permanent=False)),
    path('export-animes/', views.export_animes, name='export_animes'),
    path('export-anime-initial-recommendations/', views.export_anime_initial_recommendations, name='export_anime_initial_recommendations'),
    path('export-anime-statistics/', views.export_anime_statistics, name='export_anime_statistics'),
    path('export-anime-relations/', views.export_anime_relations, name='export_anime_relations'),
    path('dich/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/animes/season/<int:year>/<str:season>/', views.SeasonalAnimeViewSet.as_view({'get': 'list'}), name='season-animes'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tinymce/', include('tinymce.urls')),
]