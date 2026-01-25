from django.contrib import admin
from django.contrib.auth.models import User
from .models import Household, Membership


# Register your models here.
class MembershipInline(admin.TabularInline):
    model = Membership

class HouseholdAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline
    ]
    
admin.site.register(Household, HouseholdAdmin)
#admin.site.register(User)
