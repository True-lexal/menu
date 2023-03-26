from django.contrib import admin
from .models import *


class MenuElementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'main_menu')
    list_filter = ('main_menu', 'parent')
    prepopulated_fields = {'url': ('title', )}


admin.site.register(Menu)
admin.site.register(MenuElements, MenuElementsAdmin)
