from .models import BouncerConfig, BouncerInvites, BouncerUses

from CTFd.models import (
    db
)


class DBUtils:
    DEFAULT_CONFIG = [
        {"key": "bouncer_enabled", "value": "false"},
    ]

    @staticmethod
    def get(key):
        return BouncerConfig.query.filter_by(key=key).first()

    @staticmethod
    def get_config():
        configs = BouncerConfig.query.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def save_config(config):
        for c in config:
            q = db.session.query(BouncerConfig)
            q = q.filter(BouncerConfig.key == c[0])
            record = q.one_or_none()

            if record:
                record.value = c[1]
                db.session.commit()
            else:
                config = BouncerConfig(key=c[0], value=c[1])
                db.session.add(config)
                db.session.commit()
        db.session.close()

    @staticmethod
    def load_default():
        for cv in DBUtils.DEFAULT_CONFIG:
            # Query for the config setting
            k = DBUtils.get(cv["key"])
            # If its not created, create it with its default value
            if not k:
                c = BouncerConfig(key=cv["key"], value=cv["value"])
                db.session.add(c)
        db.session.commit()

    @staticmethod
    def insert_invite(invite_code, uses):
        invite = BouncerInvites(invite_code, uses)
        db.session.add(invite)
        db.session.commit()

    @staticmethod
    def get_all_invites():
        return BouncerInvites.query.all()

    @staticmethod
    def delete_invite(id):
        invite_uses = db.session.query(BouncerUses).filter_by(invite_id=id)

        for invite_use in invite_uses:
            db.session.delete(invite_use)

        db.session.commit()

        invite = db.session.query(BouncerInvites).filter_by(id=id).first()
        db.session.delete(invite)
        db.session.commit()

    @staticmethod
    def get_invite_uses(invite):
        return BouncerUses.query.filter_by(invite_id=invite.id).count()

    @staticmethod
    def get_all_invite_uses():
        invites = DBUtils.get_all_invites()
        invite_uses = list()

        for invite in invites:
            invite_uses.append(DBUtils.get_invite_uses(invite))

        return invite_uses
