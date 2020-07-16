import json
import os
from .blueprint import load_bp
from .models import BouncerConfig
from .db_utils import DBUtils
from .auth import register

from CTFd.plugins import register_plugin_assets_directory, register_plugin_script

PLUGIN_PATH = os.path.dirname(__file__)
CONFIG = json.load(open(f"{PLUGIN_PATH}/config.json"))


def load(app):
    app.db.create_all()  # Create all DB entities
    register_plugin_assets_directory(
        app, base_path="/plugins/ctfd-bouncer/assets/"
    )  # Register static assets
    DBUtils.load_default()
    bp = load_bp(CONFIG["route"])  # Load blueprint
    app.register_blueprint(bp)  # Register blueprint to the Flask app
    app.view_functions["auth.register"] = register