import random
import string

from flask import request, render_template, Blueprint, abort, redirect, url_for
from .db_utils import DBUtils
from CTFd.utils.decorators import admins_only, authed_only

bouncer_bp = Blueprint("bouncer", __name__, template_folder="templates", static_folder="assets")


def load_bp(plugin_route):
    def invite_generator(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    @bouncer_bp.route(plugin_route, methods=["GET"])
    @admins_only
    def get_config():
        return render_template("ctfd_bouncer/config.html", config=DBUtils.get_config(),
                               invites=zip(DBUtils.get_all_invites(), DBUtils.get_all_invite_uses()))

    @bouncer_bp.route(plugin_route, methods=["POST"])
    @admins_only
    def update_config():
        config = request.form.to_dict()
        del config["nonce"]

        DBUtils.save_config(config.items())
        return render_template("ctfd_bouncer/config.html", config=DBUtils.get_config(),
                               invites=zip(DBUtils.get_all_invites(), DBUtils.get_all_invite_uses()))

    @bouncer_bp.route(f"{plugin_route}/<invite_id>", methods=["DELETE"])
    @admins_only
    def delete_invite(invite_id):
        DBUtils.delete_invite(invite_id)
        return {"success": True}

    @bouncer_bp.route(f"{plugin_route}/invite/new", methods=["GET"])
    @admins_only
    def view_new_invite():
        return render_template("ctfd_bouncer/new_invite.html", invite_code=invite_generator())

    @bouncer_bp.route(f"{plugin_route}/invite/new", methods=["POST"])
    @admins_only
    def new_invite():
        form_data = request.form.to_dict()
        DBUtils.insert_invite(form_data["invite_code"], int(form_data["invite_uses"]))

        return redirect(url_for("bouncer.get_config"))

    return bouncer_bp
