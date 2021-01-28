from django.urls import path
from users_transactions import views

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:pk>/', views.user_detail),
    path('users/<int:pk>/transactions', views.user_transactions_list),
    path('users/<int:pk>/transactions/summary', views.user_transactions_summary_by_account),
    path('transactions/', views.transactions_list),
    path('transactions/<str:pk>/', views.transaction_detail),
]