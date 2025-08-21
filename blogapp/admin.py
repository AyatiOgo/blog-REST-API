from django.contrib import admin
from .models import CustomUSer, Blog
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUSerAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')


admin.site.register(CustomUSer, CustomUSerAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display= ("title", "is_draft", "category", "created_at")

admin.site.register(Blog, BlogAdmin)