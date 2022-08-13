from __future__ import annotations

from abc import ABC, abstractmethod
from classes.equipment import Weapon, Armor
from classes.war_classes import UnitClass


class BaseUnit(ABC):
    """ Базовый класс юнита """
    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor):
        """При инициализации класса Unit используем свойства класса UnitClass"""
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.stamina: float = unit_class.max_stamina
        self.hp: float = unit_class.max_health
        self.weapon: Weapon = weapon
        self.armor: Armor = armor
        self._is_skill_used: bool = False

    @property
    def health_points(self):
        """Возвращаем аттрибут hp в красивом виде"""
        return round(self.hp, 1) if self.hp > 0 else 0

    @property
    def stamina_points(self):
        """Возвращаем аттрибут stamina в красивом виде"""
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """Присваиваем нашему герою новое оружие"""
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """Одеваем новую броню"""
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """Логика расчета урона и получение величины урона"""
        damage = self.unit_class.attack * self.weapon.damage_random

        if target.stamina >= target.armor.stamina_per_turn:
            defence = target.armor.defence
        else:
            defence = 0

        if damage > defence:
            hit_damage = damage - defence
        else:
            hit_damage = 0

        return round(hit_damage, 2)

    def get_damage(self, hit_damage: float) -> None:
        """Переопределяем новое значение здоровья"""
        self.hp -= hit_damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """Этот метод будет переопределен ниже"""
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """Метод использования умения, если использовано - обычный удар"""
        if self._is_skill_used:
            self.hit(target=target)
            return f"{self.name} хотел использовать {self.unit_class.skill.name}, но его уже не осталось. " \
                   f"Пришлось применить обычный удар"
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)
