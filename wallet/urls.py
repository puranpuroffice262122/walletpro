from django.urls import path
from . import views
app_name = 'wallet'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transactions/', views.transactions, name='transactions'),
    path('notifications/', views.notifications, name='notifications'),
    path('products/', views.products, name='products'),
    path('buy/<int:pk>/', views.buy_product, name='buy_product'),
    path('api/balance/', views.get_balance, name='get_balance'),
]
