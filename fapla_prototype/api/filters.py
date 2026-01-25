import django_filters
from .models import Household, User, Membership

class HouseholdFilter(django_filters.FilterSet):
    class Meta:
        model = Household
        fields = {
            'name': ['exact', 'contains'],
            }