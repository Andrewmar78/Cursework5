from flask import Flask, render_template


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route("/")
    def index():
        """Страница главного меню"""
        return render_template("index.html")

    return app
