from django.urls import path
from . import views

urlpatterns = [
    path('my-households/', views.MyHouseholdsListCreateAPIView.as_view()),
    path('my-households/create/', views.MyHouseholdCreateAPIView.as_view()), # TODO deprecated
    path('households/<int:pk>/', views.HouseholdDetailAPIView.as_view()),
    path('memberships/', views.MembershipView.as_view()),  # POST (invite)
    path('memberships/<int:household_id>/', views.MembershipView.as_view()),  # DELETE (leave)
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path("tasks/", views.TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view()),
    path("tasks/<int:task_id>/responsibility/", views.TaskResponsibilityView.as_view()),
    path("shopping-items/", views.ShoppingItemListCreateView.as_view()),
    path("shopping-items/<int:pk>/", views.ShoppingItemDetailView.as_view()),
    path("auth/me/", views.MeView.as_view(), name="auth_me"),

    # TODO DELETE OR RESTRICT TO ADMIN
    path('users/', views.UsersListAPIView.as_view()),
    path('households/', views.HouseholdListAPIView.as_view()),
]