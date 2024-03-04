from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name='MainPage'),
    path('api/games/start', views.start_game, name='start_game'),
    path('game/<int:game_id>/', views.game_page, name='game_page'),
    path('api/games/start/', views.create_player, name='create_player'),  # Add a trailing slash
    path('api/games/<int:game_id>/check-word', views.check_word, name='check_word'),
    path('api/games/<int:game_id>/pass-turn', views.pass_turn, name='pass_turn'),
    path('api/games/<int:game_id>/time-is-up', views.time_is_up, name='time_is_up'),
]
