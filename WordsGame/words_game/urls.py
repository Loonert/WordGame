from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name='main_page'),
    path('start/', views.start_page, name='start_page'),
    path('game/<int:game_id>/', views.game_page, name='game_page'),  # Обновленный URL-шаблон
]
