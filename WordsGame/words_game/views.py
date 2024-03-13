from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player, Game
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
import time  # Добавим библиотеку для работы с временем

def MainPage(request):
    if request.method == 'POST':
        player_name = request.POST.get('name')
        player = Player.objects.create(name=player_name)
        request.session['player_id'] = player.id  # Сохраняем ID игрока в сессии
        return redirect('start_page')

    return render(request, 'MainPage.html')

def start_page(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('main_page')

    player = Player.objects.get(id=player_id)

    if request.method == 'POST':
        # Проверяем, есть ли свободные лобби
        games_waiting = Game.objects.filter(game_state='waiting').exclude(players=player)

        if games_waiting.exists():
            # Если есть свободное лобби, подключаем игрока и переходим в него
            game = games_waiting.first()
            game.players.add(player)
            game.save()

            return JsonResponse({'success': True, 'waiting': True, 'game_id': game.id})
        else:
            # Если свободных лобби нет, создаем новую игру и переходим в нее
            game = Game.objects.create(current_player=player, game_state='waiting')
            game.players.add(player)
            game.save()

            return JsonResponse({'success': True, 'waiting': True, 'game_id': game.id})

    return render(request, 'StartPage.html', {'player_name': player.name})


def game_waiting(request, game_id):
    game_waiting = Game.objects.get(id=game_id, game_state='waiting')
    players = game_waiting.players.all()

    # Если в комнате ожидания достаточно игроков, переходим в игру
    if players.count() >= 2:
        time.sleep(5)  # Задержка 5 секунд (ваш таймер)
        return redirect('game_page', game_id=game_id)

    player_id = request.session.get('player_id')
    if player_id:
        current_player = Player.objects.get(id=player_id)
        return render(request, 'GameWaiting.html', {'game_waiting': game_waiting, 'players': players, 'game_id': game_id, 'player_name': current_player.name})
    else:
        return HttpResponseNotFound("Player not found")



def game_page(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        players = game.players.all()
        return render(request, 'GamePlay.html', {'game': game, 'players': players})
    except Game.DoesNotExist:
        # Обработка случая, когда игра с указанным game_id не существует
        return HttpResponseNotFound("Game not found")
