from django.urls import path
from .views import (
    FoodListView, FoodDetailView, FoodCreateView, FoodUpdateView, FoodDeleteView,
    AdminDashboardView, AdminFoodListView, AdminUserListView, AdminAnalyticsView
)

app_name = 'food'

urlpatterns = [
    path('', FoodListView.as_view(), name='list'),
    path('<int:pk>/', FoodDetailView.as_view(), name='detail'),
    path('create/', FoodCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', FoodUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', FoodDeleteView.as_view(), name='delete'),

    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-foods/', AdminFoodListView.as_view(), name='admin_foods'),
    path('admin-users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin-analytics/', AdminAnalyticsView.as_view(), name='admin_analytics'),
]
