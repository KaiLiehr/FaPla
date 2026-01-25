#from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from .serializers import HouseholdSerializer, UserSerializer, RegisterSerializer, TaskSerializer
from django.contrib.auth.models import User

from .models import Household, Membership, Task, Responsibility
from .filters import HouseholdFilter


# View for registering as a new user
class RegisterView(generics.CreateAPIView):
    model = User
    serializer_class = RegisterSerializer
    permission_classes = []


# Returns a user's households
class MyHouseholdsListCreateAPIView(generics.ListCreateAPIView):
    #queryset = Household.objects.prefetch_related('memberships__member')
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = HouseholdFilter

    def get_queryset(self):
        return Household.objects.filter(memberships__member=self.request.user).prefetch_related('memberships__member').distinct()
    
# Allow a logged in user to create a new household with itself as member and creator TODO DEPRECATED BY LISTCREATE!!!!!!!!
class MyHouseholdCreateAPIView(generics.CreateAPIView):
    #queryset = Household.objects.prefetch_related('memberships__member')
    model = Household
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super.create(request, *args, **kwargs)



# Allows a specific household to be displayed in detail, updated, or deleted given its key TODO restrict member only, restrict deletion to last member only
class HouseholdDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]
    

# GET/POST of tasks. GET returns all tasks a logged in user is related to(both personal and household tasks)
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return related_tasks_for_user(self.request.user)
    
    #def perform_create(self, serializer):
    #    serializer.save(created_by=self.request.user)

# View for UPDATE/DELETE of a specific task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return related_tasks_for_user(self.request.user)


# POST/DELETE of own responsibility for a given task. Allows a user to take/give up his own responisbility for a task (personal or household).
class TaskResponsibilityView(APIView):
    permission_classes = [IsAuthenticated]

    # returns the task for a given task id iff it's a task of the user
    def get_task(self, user, task_id):
        return related_tasks_for_user(user).filter(id=task_id).first()

    # creates a responsibility object for the user and the given task
    def post(self, request, task_id):
        task = self.get_task(request.user, task_id)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)

        responsibility, created = Responsibility.objects.get_or_create(
            task=task,
            executor=request.user
        )

        if not created:
            return Response(
                {"detail": "You already accepted this task."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_201_CREATED)

    # deletes the responsibility object for the given user and task
    def delete(self, request, task_id):
        task = self.get_task(request.user, task_id)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)

        deleted, _ = Responsibility.objects.filter(
            task=task,
            executor=request.user
        ).delete()

        if not deleted:
            return Response(
                {"detail": "You are not responsible for this task."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)



# --------------------UNFINISHED/NOT FOR PROD VIEWS----------------------

# TODO Recipe listview with queryset = Recipe.objects.filter(public=True) to show all public recipes



# Returns all users TODO DELETE PRIOR TO PRODUCTION!!!!!!!!!!!!
class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('username')

# Returns all households TODO  DELETE PRIOR TO PRODUCTION!!!!!!!!!!!!
class HouseholdListAPIView(generics.ListAPIView):
    queryset = Household.objects.prefetch_related('memberships__member')
    serializer_class = HouseholdSerializer
    filterset_class = HouseholdFilter



# ------------------------------------------------------------- Helper functions -------------------------------------------------------------

# Returns all tasks related to the given user. A task is related if it belongs to a household(household task), 
# where the user is member, or if scope is blank AND the user is the task's creator(personal task).
def related_tasks_for_user(user):
    household_ids = Household.objects.filter(
        members=user
    ).values_list("id", flat=True)

    return Task.objects.filter(
        Q(scope__in=household_ids) |
        Q(scope__isnull=True, created_by=user)
    ).distinct()