from django.contrib import admin # type: ignore
from django.contrib.auth.admin import UserAdmin# type: ignore
from django.contrib.auth.models import User# type: ignore
from .models import ClientData, UserSubmits# type: ignore
from .models import UserClientInteraction


# Customize the UserAdmin display
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ClientData)
admin.site.register(UserSubmits)
admin.site.register(UserClientInteraction)
