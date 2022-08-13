from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from unit import BaseUnit


# Лучше бы переместить базовый класс в отдельный файл
class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    # @abstractmethod
    # def skill_effect(self) -> str:
    #     pass

    def skill_effect(self):
        """Уменьшение выносливости нападающего и здоровья цели"""
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f"{self.user.name} использует {self.name} и наносит {round(self.damage,1)} урона сопернику."

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """Проверка, достаточно ли выносливости у игрока для применения умения"""
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но силенок не хватило."


"""Отдельные классы умений"""
class FuryPunch(Skill):
    name: str = "Свирепый пинок"
    stamina: float = 6.0
    damage: float = 12.0

    # def skill_effect(self):
    #     """Уменьшение выносливости нападающего и здоровья цели"""
    #     self.user.stamina -= self.stamina
    #     self.target.hp -= self.damage
    #     return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."


class HardShot(Skill):
    name: str = "Мощный укол"
    stamina: float = 5.0
    damage: float = 15.0

    # def skill_effect(self):
    #     """Уменьшение выносливости нападающего и здоровья цели"""
    #     self.user.stamina -= self.stamina
    #     self.target.hp -= self.damage
    #     return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."


class MagicFire(Skill):
    name: str = "Волшебное пламя"
    stamina: float = 5.0
    damage: float = 20.0
