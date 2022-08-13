from dataclasses import dataclass
from classes.equipment import Equipment
from classes.skills import Skill, FuryPunch, HardShot, MagicFire
from config import BaseConfig


@dataclass
class UnitClass:
    """Класс юнита"""
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


equipment = Equipment(BaseConfig.PATH_TO_EQUIPMENT)

"""Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения атрибутов"""
WarriorClass = UnitClass(name="воин", max_health=60.0, max_stamina=30.0, attack=1.0, stamina=0.9,
                         armor=1.2, skill=FuryPunch())
ThiefClass = UnitClass(name="вор", max_health=50.0, max_stamina=25.0, attack=1.5, stamina=1.2,
                       armor=1.0, skill=HardShot())
MagClass = UnitClass(name="маг", max_health=40.0, max_stamina=20.0, attack=0.8, stamina=0.7,
                     armor=0.9, skill=MagicFire())

unit_classes = {ThiefClass.name: ThiefClass, WarriorClass.name: WarriorClass, MagClass.name: MagClass}
