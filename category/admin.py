
# Register your models here.
from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
   #pre populate field 
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
# pass the class to register function 
admin.site.register(Category,CategoryAdmin)