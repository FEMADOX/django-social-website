from django.contrib import admin

from account.models import Contact, Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]
    raw_id_fields = ["user"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["user_form", "user_form", "created"]
    list_filter = ["created",]