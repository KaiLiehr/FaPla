import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from api.models import Household, Membership, List, Task, Recipe

# TODO Add tasks, lists, and recipies

class Command(BaseCommand):
    help = 'Creates application data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset the DB before re-populating')

    def handle(self, *args, **kwargs):
        # get or create superuser

        # in case prior data is not wanted, clears out all models' objects
        if kwargs['reset']:
            print("Since reset-flag is set, DB will be cleared(including Users)!")
            User.objects.all().delete()
            Household.objects.all().delete()
            Membership.objects.all().delete()
            List.objects.all().delete()
            Task.objects.all().delete()
            Membership.objects.all().delete()
            Recipe.objects.all().delete()

        # CREATE SUPERUSER
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')
            print("!!! Added SUPERUSER 'admin' with pw 'test' !!!")

        # CREATE USER OBJECTS all with display_name=username
        added = 0
        duplicates = 0
        user_names = ["Test&User1", "JOHN DOE", "Jane Täü-öst&", "DAVE", "Tim", "John@Carlos", "Generic_Username",]
        test_pwd = "test"
        for user_name in user_names:
            user, created = User.objects.get_or_create(username= user_name, defaults={})
            if created:
                print(f"Added User: {user.username}!")
                user.set_password(test_pwd)
                user.save()
                added +=1
            else:
                duplicates +=1
        all_users = User.objects.all()
        print(f"New Users added: {added}, Duplicates discarded: {duplicates}, Total number of users: {len(all_users)}!")

        
        # CREATE HOUSEHOLD OBJECTS
        added = 0
        duplicates = 0
        household_names = ["Test&H1", "Home", "Haus von Täü-öst%", "Shopping circle", "Our Shopping- & Todolists", "Einkauf@Weihnachten", "Generic_Household",]
        
        for household_name in household_names:
            new_household, created = Household.objects.get_or_create(
                name= household_name, 
                defaults={
                    'creator': User.objects.filter(username='admin').first(),
                }
                )
            if created:
                print(f"Added Household: {new_household}!")
                added +=1
            else:
                duplicates +=1
        all_households = Household.objects.all()
        print(f"New Households added: {added}, Duplicates discarded: {duplicates}, Total number of households: {len(all_households)}!")


        # CREATE MEMBERSHIP OBJECTS, intermediary for the ManyToMany Relation between Households and Users
        added = 0
        duplicates = 0

        # go through all households
        for given_household in all_households:

            round_added = 0

            # take a random number of random users to be members of the given household
            member_number = random.randrange(len(all_users))
            chosen_members = random.sample(list(all_users), member_number)

            # create actual membership objects for all chosen members
            for member in chosen_members:
                membership, created = Membership.objects.get_or_create(
                    household= given_household,
                    member= member,
                    defaults={
                        'inviter': User.objects.filter(username='admin').first(),
                    }
                )
                if created:
                    print(f"Added Membership with {membership}!")
                    round_added +=1
                else:
                    duplicates +=1
            print(f"{round_added} new members assigned to Household: {given_household}")
            added = added + round_added
        all_memberships = Membership.objects.all()
        print(f"Memberships added: {added}, Duplicates discarded: {duplicates}, Total number of memberships(for all households): {len(all_memberships)}!")

        