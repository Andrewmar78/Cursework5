from random import uniform
from dataclasses import dataclass
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    # id: int
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage_random(self):
        """Случайный выбор силы удара в заданном диапазоне"""
        return uniform(self.min_damage, self.max_damage)


ArmorSchema = marshmallow_dataclass.class_schema(Armor)
WeaponSchema = marshmallow_dataclass.class_schema(Weapon)


@dataclass
class EquipmentData:
    weapons: list
    armors: list


class Equipment:
    def __init__(self, file_path):
        self.file_path = file_path
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """Возвращаем объект класса оружия по имени"""
        index = self.get_weapons_names().index(weapon_name)
        weapon_dict = list(iter(self.equipment.weapons[i] for i in range(len(self.equipment.weapons))))[index]
        weapon = Weapon(name=weapon_dict["name"], min_damage=weapon_dict["min_damage"],
                        max_damage=weapon_dict["max_damage"], stamina_per_hit=weapon_dict["stamina_per_hit"])
        return weapon

    def get_armor(self, armor_name: str) -> Armor:
        """Возвращаем объект класса брони по имени"""
        index = self.get_armors_names().index(armor_name)
        armor_dict = list(iter(self.equipment.armors[i] for i in range(len(self.equipment.armors))))[index]
        armor = Armor(name=armor_dict["name"], defence=armor_dict["defence"],
                      stamina_per_turn=armor_dict["stamina_per_turn"])
        return armor

    def get_weapons_names(self) -> list:
        """Возвращаем список с оружием"""
        return list(iter(self.equipment.weapons[i]["name"] for i in range(len(self.equipment.weapons))))

    def get_armors_names(self) -> list:
        """Возвращаем список с броней"""
        return list(iter(self.equipment.armors[i]["name"] for i in range(len(self.equipment.armors))))

    # @staticmethod
    def _get_equipment_data(self) -> EquipmentData:
        """Загружаем json в переменную EquipmentData"""
        with open(self.file_path, "r", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)

            except marshmallow.exceptions.ValidationError:
                raise ValueError


EquipmentSchema = marshmallow_dataclass.class_schema(Equipment)
