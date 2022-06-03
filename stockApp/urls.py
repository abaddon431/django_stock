from django.urls import path
from . import views

app_name = "stockApp"

urlpatterns = [
    path('', views.home, name='home'),
    path('update-stock', views.update_stock, name='update-stock')
]