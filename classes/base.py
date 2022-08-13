from typing import Optional
from classes.unit import BaseUnit, PlayerUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: float = 1.0
    player: BaseUnit = None
    enemy: PlayerUnit = None
    game_is_running: bool = False
    battle_result: str = None

    def start_game(self, player: BaseUnit, enemy: PlayerUnit) -> None:
        """Начало игры, определение игрока и противника"""
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def _check_players_hp(self) -> Optional[bool]:
        """Проверка здоровья для окончания игры"""

        if self.player.hp > 0 and self.enemy.hp > 0:
            return True

        if self.player.hp <= 0 and self.enemy.hp >= 0:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}! '

        if self.player.hp >= 0 and self.enemy.hp <= 0:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}! '

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}! '

        self._end_game()

    def _stamina_regeneration(self) -> None:
        """Расчет регенерации выносливости"""
        player_stamina_regeneration = self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        self.player.stamina += round(player_stamina_regeneration, 1)
        enemy_stamina_regeneration = self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina
        self.enemy.stamina += round(enemy_stamina_regeneration, 1)

        """ Проверка на максимум"""
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self) -> str:
        """Следующий ход: восстановление выносливости, ответный удар противника"""
        if self._check_players_hp():
            self._stamina_regeneration()
            enemy_result = self.enemy.enemy_hit(target=self.player)
            self._stamina_regeneration()
            return enemy_result
        return self.battle_result

    def _end_game(self):
        """Завершение игры, очистка синглтона"""
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """Результат после удара, переход хода"""
        player_hit_result = str(self.player.hit(target=self.enemy))
        return str(self.next_turn()) + player_hit_result

    def player_use_skill(self) -> str:
        """Результат после умения, переход хода"""
        player_skill_result = self.player.use_skill(target=self.enemy)
        return str(self.next_turn()) + player_skill_result
