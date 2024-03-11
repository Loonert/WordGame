from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player, Game
from django.http import HttpResponseNotFound

def MainPage(request):
    if request.method == 'POST':
        player_name = request.POST.get('name')
        player = Player.objects.create(name=player_name)
        request.session['player_id'] = player.id  # Сохраняем ID игрока в сессии
        return redirect('start_page')

    return render(request, 'MainPage.html')

from django.http import HttpResponseBadRequest

def start_page(request):
    if request.method == 'POST':
        player_id = request.session.get('player_id')
        if not player_id:
            return HttpResponseBadRequest("Player ID not found in session.")

        player = Player.objects.get(id=player_id)
        games_waiting = Game.objects.filter(game_state='waiting')

        if games_waiting.exists():
            game = games_waiting.first()
            game.players.add(player)
            game.save()
        else:
            game = Game.objects.create(current_player=player)

        return JsonResponse({'success': True, 'game_id': game.id})
    else:
        player_id = request.session.get('player_id')
        if not player_id:
            # Если нет ID игрока в сессии, перенаправляем на главную страницу
            return redirect('main_page')

        player = Player.objects.get(id=player_id)
        return render(request, 'StartPage.html', {'player_name': player.name, 'game_id': None})


def game_page(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        players = game.players.all()
        return render(request, 'GamePlay.html', {'game': game, 'players': players})
    except Game.DoesNotExist:
        # Обработка случая, когда игра с указанным game_id не существует
        return HttpResponseNotFound("Game not found")

