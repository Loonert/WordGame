from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Player, Game
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json

@csrf_exempt
@require_POST
def create_player(request):
    name = request.POST.get('name')  # Получаем имя игрока из POST-запроса
    player = Player.objects.create(name=name)
    return JsonResponse({'playerID': player.id}, status=201)


@csrf_exempt
@require_POST
# def start_game(request):
#     player_id = request.POST.get('playerID')  # Получаем идентификатор игрока из POST-запроса
#     player = get_object_or_404(Player, id=player_id)
#
#     # Проверяем, что игрок еще не участвует в активной игре
#     active_game = Game.objects.filter(players=player, game_state='active').first()
#     if active_game:
#         return JsonResponse({'error': 'Player is already in an active game'}, status=400)
#
#     # Создаем новую игру и добавляем в нее текущего игрока
#     game = Game.objects.create(current_player=player)
#     game.players.add(player)
#
#     return JsonResponse({
#         'gameState': game.game_state,
#         'gameID': game.id,
#         'currentPlayerID': game.current_player.id
#     })

# from django.shortcuts import render

def start_game(request, player_id):
    # Получить имя игрока из базы данных или сессии
    player = Player.objects.get(id=player_id)
    player_name = player.name

    return render(request, 'start_game.html', {'player_name': player_name})



@csrf_exempt
@require_POST
def check_word(request, game_id):
    player_id = request.POST.get('playerID')
    word = request.POST.get('word')

    player = get_object_or_404(Player, id=player_id)
    game = get_object_or_404(Game, id=game_id)

    # Проверяем валидность слова (ваша логика здесь)

    return JsonResponse({'valid': True})  # Или {'valid': False} в зависимости от результата проверки


@csrf_exempt
@require_POST
def pass_turn(request, game_id):
    player_id = request.POST.get('playerID')

    player = get_object_or_404(Player, id=player_id)
    game = get_object_or_404(Game, id=game_id)

    # Обновляем состояние игры (ваша логика здесь)

    return JsonResponse({'currentPlayerID': game.current_player.id})


@csrf_exempt
@require_POST
def time_is_up(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Завершаем игру и определяем победителя (ваша логика здесь)

    return JsonResponse({
        'winnerPlayerID': winner.id,
        'gameStatus': 'finished'
    })

# important // если не post, то рендерим MainPage.html иначе
def MainPage(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        response = requests.post('http://127.0.0.1:8000/api/games/start', data={'name': player_name})

        try:
            player_data = response.json()
        except JSONDecodeError:
            player_data = {}

        if response.status_code == 201:
            # Перенаправление на страницу игры или куда-то еще
            return redirect('game_page', player_data.get('playerID', ''))
        else:
            return JsonResponse({'error': 'Failed to create player'}, status=400)

    return render(request, 'MainPage.html')


from django.shortcuts import render
from django.http import JsonResponse
import requests

def game_page(request, game_id):
    # Получить playerID из сессии или параметров запроса
    player_id = request.session.get('player_id')

    if request.method == 'POST':
        # Отправить запрос на начало игры
        response = requests.post(f'http://127.0.0.1:8000/your-app/api/games/{game_id}/start', json={'playerID': player_id})

        if response.status_code == 200:
            game_data = response.json()
            # Обработать данные игры и передать их в шаблон
            return JsonResponse({'status': 'Game started successfully', 'game_data': game_data})
        else:
            return JsonResponse({'error': 'Failed to start game'}, status=400)

    return render(request, 'game_page.html', {'game_id': game_id})


