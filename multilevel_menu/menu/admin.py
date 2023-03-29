from django.contrib import admin

from menu.models import Item, Menu


class ItemsInline(admin.TabularInline):
    model = Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'slug')
    list_filter = ('menu',)
    fieldsets = (
        (
            'Добавить новый пункт меню', {
                'fields': ('menu', 'parent', 'title', 'slug')
            }
        ),
    )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = (ItemsInline,)
