from CTFd.models import (
    db,
)


class BouncerConfig(db.Model):
    key = db.Column(db.String(length=128), primary_key=True)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<BouncerConfig (0) {1}>".format(self.key, self.value)


class BouncerInvites(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invite_code = db.Column(db.String(8), unique=True)
    uses = db.Column(db.Integer)

    def __init__(self, invite_code, uses):
        self.invite_code = invite_code
        self.uses = uses

    def __repr__(self):
        return "<BouncerInvites (0) {1} {2}>".format(self.id, self.invite, self.uses)


class BouncerUses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invite_id = db.Column(None, db.ForeignKey("bouncer_invites.id"))
    user_id = db.Column(None, db.ForeignKey("users.id"))

    # Relationships
    user = db.relationship("Users", foreign_keys="BouncerUses.user_id", lazy="select")
    invite = db.relationship("BouncerInvites", foreign_keys="BouncerUses.invite_id", lazy="select")

    def __init__(self, invite_id, user_id):
        self.invite_id = invite_id
        self.user_id = user_id

    def __repr__(self):
        return "<BouncerUses (0) {1} {2}>".format(self.id, self.invite_id, self.user_id)
