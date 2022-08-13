from flask import render_template, request, url_for
from werkzeug.utils import redirect
from classes import equipment
from classes.base import Arena
from classes.war_classes import unit_classes, equipment
from classes.unit import PlayerUnit, EnemyUnit
from config import BaseConfig
from server import create_app

# import logging
# logging.basicConfig(filename="basic.log", level=logging.INFO)

# Загрузка конфигурации из config.py
app = create_app(BaseConfig)

# Не могу сообразить, как использовать в таком виде:
# heroes = {
#     "player": PlayerUnit,
#     "enemy": EnemyUnit
# }

# А так не очень корректно все:
heroes = {
    "player": None,
    "enemy": None
}

arena = Arena()


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    """Нанесение удара"""
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    """Использование умения"""
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    """Пропуск хода"""
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    """Завершение игры по кнопке"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """Выбор героя"""
    """Получаем форму героя"""
    if request.method == "GET":
        hero = {"head": "Выбираем своего героя", "classes": unit_classes, "weapons": equipment.get_weapons_names(),
                "armors": equipment.get_armors_names()}
        return render_template("hero_choosing.html", result=hero)

    """Отправляем форму и переходим на выбор противника"""
    if request.method == "POST":
        username = request.form.get("name")
        unit_class = unit_classes[request.form.get("unit_class")]
        weapon = equipment.get_weapon(request.form.get("weapon"))
        armor = equipment.get_armor(request.form.get("armor"))

        # heroes["player"](username, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes["player"] = PlayerUnit(name=username, unit_class=unit_class, weapon=weapon, armor=armor)

        # Не уверен, что правильно, подсмотрел в интернете:
        return redirect(url_for("choose_enemy"), 302, Response=None)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """Выбор противника"""
    """Получаем форму противника"""
    if request.method == "GET":
        enemy = {"head": "Выбираем противника", "classes": unit_classes, "weapons": equipment.get_weapons_names(),
                 "armors": equipment.get_armors_names()}
        return render_template("hero_choosing.html", result=enemy)

    """Отправляем форму и переходим в бой"""
    if request.method == "POST":
        username = request.form.get("name")
        unit_class = unit_classes[request.form.get("unit_class")]
        weapon = equipment.get_weapon(request.form.get("weapon"))
        armor = equipment.get_armor(request.form.get("armor"))

        # heroes["enemy"](name=username, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes["enemy"] = EnemyUnit(name=username, unit_class=unit_class, weapon=weapon, armor=armor)

        return redirect(url_for("start_fight"), 302, Response=None)
