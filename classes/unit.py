from __future__ import annotations
from classes.baseunit import BaseUnit
from random import randint


class PlayerUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        """
        Расчет повреждения от удара,
        изменения выносливости после удара,
        проверка силы брони при ударе
        """
        if self.stamina_points >= self.weapon.stamina_per_hit:

            target.get_damage(self._count_damage(target))

            self.stamina -= self.weapon.stamina_per_hit
            target.stamina -= target.armor.stamina_per_turn

            if target.stamina < 0:
                target.stamina = 0

            if self._count_damage(target) > 0:
                return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} соперника " \
                       f"и наносит {round(self._count_damage(target),1)} урона."
            return f"{self.name}, используя {self.weapon.name}, наносит удар," \
                   f" но {target.armor.name} соперника его останавливает."

        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило силенок."

    def enemy_hit(self, target: BaseUnit) -> str:
        pass


class EnemyUnit(PlayerUnit):
    def enemy_hit(self, target: BaseUnit) -> str:
        """Функция ответного удара соперника"""

        """Случайное использование умения, шанс 20%"""
        if not self._is_skill_used:
            hit_skill = randint(0, 4)
            if hit_skill == 4:
                return self.use_skill(target)

        """Если умение уже использовано, то обычный удар"""
        # Не работает ((()))
        return self.hit(target)

