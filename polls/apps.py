from django.apps import AppConfig
from django.contrib import admin


class PollsConfig(AppConfig):
    # Configure default settings for the app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        from django.conf import settings

        # Configure admin site appearance
        admin.site.site_header = settings.ADMIN_SITE_HEADER
        admin.site.site_title = settings.ADMIN_SITE_TITLE
        admin.site.index_title = settings.ADMIN_INDEX_TITLE
        admin.site.site_url = '/admin/'
