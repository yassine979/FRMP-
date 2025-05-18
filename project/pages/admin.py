from django.contrib import admin
from .models import Ligue, Actualite, concours, Club , ContactMessage, CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("🧑‍💼  Informations Personnelles", {
            "fields": ("username", "email", "first_name", "last_name"),
        }),
        ("🎭 Permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser"),
        }),
         ("📅 Dates Importantes", {
            "fields": ("last_login", "date_joined"),
        }),
    )
    
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" />'
        return 'Aucune image'
    display_profile_picture.short_description = 'Photo de profil'
    display_profile_picture.allow_tags = True   


@admin.register(Ligue)
class LigueAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_pub', 'ligue')
    list_filter = ('date_pub', 'ligue')
    search_fields = ('titre', 'contenu')

@admin.register(concours)
class ConcoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', 'ligue', 'club')
    list_filter = ('date_debut', 'date_fin', 'ligue', 'club')
    search_fields = ('nom', 'description')
    
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'ligue')
    list_filter = ('ville', 'ligue')
    search_fields = ('nom', 'description')
    
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'message')
    search_fields = ('full_name', 'email', 'phone')
