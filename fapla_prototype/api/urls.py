from django.urls import path
from . import views

urlpatterns = [
    path('my-households/', views.MyHouseholdsListCreateAPIView.as_view()),
    path('my-households/create/', views.MyHouseholdCreateAPIView.as_view()),
    path('households/<int:pk>/', views.HouseholdDetailAPIView.as_view()),
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path("tasks/", views.TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view()),
    path("tasks/<int:task_id>/responsibility/", views.TaskResponsibilityView.as_view()),

    # TODO DELETE OR RESTRICT TO ADMIN
    path('users/', views.UsersListAPIView.as_view()),
    path('households/', views.HouseholdListAPIView.as_view()),
]