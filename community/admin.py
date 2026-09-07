from django.contrib import admin

from .models import Community, Block, Home, HomeMembership


admin.site.register(Community)
admin.site.register(Block)
admin.site.register(Home)
admin.site.register(HomeMembership)
