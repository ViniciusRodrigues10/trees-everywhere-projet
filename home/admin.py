from django.contrib import admin
from .models import Account, Profile, Tree, PlantedTree


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active")


admin.site.register(Account, AccountAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "joined")


admin.site.register(Profile, ProfileAdmin)


class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name")


admin.site.register(Tree, TreeAdmin)


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = (
        "tree",
        "user",
        "age",
        "planted_at",
        "latitude",
        "longitude",
        "account",
    )


admin.site.register(PlantedTree, PlantedTreeAdmin)
