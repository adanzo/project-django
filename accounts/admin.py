from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserProfile
# Register your models here.
## we do this class to make the password in the model accounts read only
#django custome user model
class AccountAdmin(UserAdmin):
    #fields we want to display from model Account
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')

admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
