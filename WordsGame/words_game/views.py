from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player, Game
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
import time  # Добавим библиотеку для работы с временем
from .utils import get_all_words, is_valid_word, get_random_starting_player

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
        games_waiting = Game.objects.filter(game_state='waiting').exclude(players=player)

        if games_waiting.exists():
            game = games_waiting.first()
            game.players.add(player)
            game.save()

            return JsonResponse({'success': True, 'waiting': True, 'game_id': game.id})
        else:
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
        # Добавим задержку перед переходом в GamePlay
        time.sleep(5)  # Задержка 5 секунд (ваш таймер)

        # Обновляем статус игры
        game_waiting.game_state = 'playing'
        game_waiting.save()

        # Перенаправляем в GamePlay
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
        all_words_set = get_all_words()

        if game.game_state == 'playing':
            # Если игра в состоянии playing, перенаправляем в GamePlay
            return render(request, 'GamePlay.html', {'game': game, 'players': players, 'all_words': all_words_set})
        else:
            # Иначе, оставляем на странице ожидания
            return render(request, 'GameWaiting.html', {'game_waiting': game, 'players': players, 'game_id': game_id})

    except Game.DoesNotExist:
        return HttpResponseNotFound("Game not found")

def game_play(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        players = game.players.all()

        if not game.current_player:
            game.current_player = get_random_starting_player(players)
            game.save()

        current_player = game.current_player
        used_words = set()
        start_time = time.time()

        winner = None

        if request.method == 'POST':
            word = request.POST.get('word', '').lower()
            last_letter = request.POST.get('last_letter', '').lower()

            if is_valid_word(word, used_words, last_letter) and word not in used_words:
                used_words.add(word)

                current_player = players.filter(id=current_player.id).first()
                next_player = players.exclude(id=current_player.id).first()

                last_letter = word[-1]

                if 'pass_turn' in request.POST:
                    if word:
                        game.current_player = next_player
                    else:
                        winner = current_player
                        game.current_player = None
                    game.save()
                    return JsonResponse({'success': True, 'word': word, 'winner': winner.name if winner else None})

                game.current_player = next_player
                game.save()
                start_time = time.time()

                return JsonResponse({
                    'success': True,
                    'word': word,
                    'last_letter': last_letter,
                    'current_player': next_player.name,
                    'winner': None,
                })

            else:
                return JsonResponse({'success': False, 'error': 'Invalid word'})

        elapsed_time = time.time() - start_time
        remaining_time = max(0, 15 - elapsed_time)
        if elapsed_time > 15:
            winner = current_player
            game.current_player = None
            game.save()
            return JsonResponse({'success': True, 'timeout': True, 'winner': winner.name})

        return render(request, 'GamePlay.html', {'game': game, 'players': players, 'current_player': current_player, 'remaining_time': remaining_time})

    except Game.DoesNotExist:
        return HttpResponseNotFound("Game not found")
