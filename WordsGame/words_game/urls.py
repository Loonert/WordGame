from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name='main_page'),
    path('start/<int:player_id>/', views.start_page, name='start_page'),
]
