from django.urls import include, path
from rest_framework import routers
from animeservice.animes import views
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'animes', views.AnimeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'studios', views.StudioViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', RedirectView.as_view(url='dich/', permanent=False)),
    path('dich/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tinymce/', include('tinymce.urls')),
]