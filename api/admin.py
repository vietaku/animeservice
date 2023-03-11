import json
import logging
from django.contrib import admin
from .models import *
from django.db.models import JSONField 
from django.forms import widgets

logger = logging.getLogger(__name__)

class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


class AnimeAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_date'
    list_display = ('title', 'mal_id', 'start_date', 'popularity', 'mean', 'is_translated')
    list_filter = ('is_translated',)
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_translated')

# class AnimeQueryAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Season information', {'fields': ['year', 'season']}),
#         ('Query information', {'fields': ['sort', 'get_all_available_animes','limit','offset']}),
#         ('Options', {'fields': ['get_all_fields', 'overide_value']}),
#         ('Fields information', {'fields': ['title','main_picture','alternative_titles','start_date','end_date','synopsis','mean','rank','popularity','genres','media_type','status','num_episodes','start_season','broadcast','source','average_episode_duration','studios','nsfw','rating'], 'classes': ['collapse']}),
#     ]

admin.site.register(Anime, AnimeAdmin)
admin.site.register(Studio)
admin.site.register(Tag, TagAdmin)
# admin.site.register(AnimeQuery, AnimeQueryAdmin)