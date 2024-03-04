from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player  # Подключаем модель Player

def MainPage(request):
    if request.method == 'POST':
        player_name = request.POST.get('name')

        # Создаем игрока в базе данных
        player = Player.objects.create(name=player_name)

        # Перенаправляем на страницу StartPage с данными игрока
        return redirect('start_page', player_id=player.id)

    return render(request, 'MainPage.html')

def start_page(request, player_id):
    # Выводим приветствие на странице StartPage
    player = Player.objects.get(id=player_id)
    return render(request, 'StartPage.html', {'player_name': player.name})
