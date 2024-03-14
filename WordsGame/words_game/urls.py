from django.urls import path
from . import views
from .views import MainPage, start_page, game_waiting, game_play

urlpatterns = [
    path('', views.MainPage, name='main_page'),
    path('start/', views.start_page, name='start_page'),
    path('game/<int:game_id>/', views.game_page, name='game_page'),  # Обновленный URL-шаблон
    path('game_waiting/<int:game_id>/', views.game_waiting, name='game_waiting'),
    path('game_play/<int:game_id>/', game_play, name='game_play'),
]
