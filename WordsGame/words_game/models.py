from django.db import models

# Create your models here.
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)
    # Другие поля, которые могут быть полезными для вашего приложения

    def __str__(self):
        return self.name

class Game(models.Model):
    players = models.ManyToManyField(Player)
    current_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='current_game_player')
    game_state = models.CharField(max_length=20, default='waiting')  # 'waiting', 'active', 'finished'

    def __str__(self):
        return f"Game {self.id}"
