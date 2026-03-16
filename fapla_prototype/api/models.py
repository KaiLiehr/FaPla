from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
#class User(AbstractUser):
#    display_name = models.CharField(max_length=200)

class Household(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="creator",)
    members = models.ManyToManyField(User, through="Membership", through_fields=("household", "member"),)

    def __str__(self):
        return self.name
    
class Membership(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE,  related_name="memberships")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    inviter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="membership_invites",)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.household.name} X {self.member.username}"
    
    class Meta:
        unique_together = ("household", "member")

# TODO DEPRECATE??? or replace by grouping? 
class List(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

# Task model TODO Recurring TASKS?
class Task(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="task_creator",)
    description = models.TextField(blank=True, null=True)
    finished = models.BooleanField(default=False) # false = task not done yet
    due_by = models.DateTimeField(blank=True, null=True) # optional due date
    scope = models.ForeignKey(Household, on_delete=models.SET_NULL, blank=True, null=True)# denotes the household it belongs to. If none -> personal task
    type = models.CharField(max_length=200, default="") # Still needed now that I have Shopping Item? Maybe Delete later??
    executors = models.ManyToManyField(User, through="Responsibility", through_fields=("task", "executor"),) # users that have accepted this task as their responsibility

    def __str__(self):
        return self.name

# Model for representing the many to many rel between accepted Tasks and Users
class Responsibility(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,  related_name="responsibilities")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responsibilities")
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.name} X {self.executor.username}"

# Separate from "normal" Tasks for their unique fields(amount,unit,brand,store) and removing type, dueby and executors
class ShoppingItem(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="item_creator",)
    description = models.TextField(blank=True, null=True)
    bought = models.BooleanField(default=False) # false = task not done yet
    scope = models.ForeignKey(Household, on_delete=models.SET_NULL, blank=True, null=True)# denotes the household it belongs to. If none -> personal task

    amount = models.CharField(max_length=150, blank=True, null=True)
    # amount = models.FloatField(null=True, blank=True)
    # unit = models.CharField(max_length=50, blank=True) # TODO maybe do an enum with fixed options instead? ml, gram, pack, bottle,... ?
    preferred_brand = models.CharField(max_length=200, blank=True, null=True)
    store = models.CharField(max_length=200, blank=True, null=True)

# TODO Unfinished placeholder, do not implement in frontend yet!!!
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    due_by = models.DateTimeField(blank=True, null=True)    # optional due date for time sensitive tasks
    description = models.TextField() # of the dish
    instructions = models.TextField() # cooking instructions
    public = models.BooleanField(default=False)  # whether it is displayed for other users TODO Replace with more complicated permission scheme like household or friendlist or explicit perm
    image = models.ImageField(upload_to='recipies/', blank=True, null=True)
    #TODO Ingredient and Ingredient-Recipe relational Models

    def __str__(self):
        return self.name





