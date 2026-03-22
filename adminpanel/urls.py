from django.urls import path
from . import views
app_name = 'adminpanel'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('users/<int:pk>/action/', views.user_action, name='user_action'),
    path('deposits/', views.deposits, name='deposits'),
    path('deposits/<int:pk>/action/', views.deposit_action, name='deposit_action'),
    path('withdrawals/', views.withdrawals, name='withdrawals'),
    path('withdrawals/<int:pk>/action/', views.withdrawal_action, name='withdrawal_action'),
    path('transactions/', views.all_transactions, name='transactions'),
    path('products/', views.products_view, name='products'),
    path('products/<int:pk>/toggle/', views.toggle_product, name='toggle_product'),
    path('orders/', views.orders_view, name='orders'),
]
