import json
import logging
from django.contrib import admin
from .models import *
from django.db.models import JSONField 
from django.forms import widgets
from rest_framework.authtoken.admin import TokenAdmin

logger = logging.getLogger(__name__)

TokenAdmin.raw_id_fields = ['user']

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

admin.site.register(Anime, AnimeAdmin)
admin.site.register(Studio)
admin.site.register(Tag, TagAdmin)