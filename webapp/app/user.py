from flask_login import UserMixin
from db import db
###############################################################################
#CLASSE User
###############################################################################
class User(UserMixin, db.Document):
    # CONSTRUCTEUR DE User
    def __init__(self, email, password, nom, prenom, rue, cp, ville, tags):
        self.email = db.EmailField(max_length=30)
        self.password = db.StringField(max_length=100)
        self.nom = db.StringField(max_length=30)
        self.prenom = db.StringField(max_length=30)
        self.rue = db.StringField(max_length=30)
        self.cp = db.StringField(max_length=30)
        self.ville = db.StringField(max_length=30)
        self.tags = db.ListField(max_length=30)

    def get_email(self):
        return self.email  # String

    def get_password(self):
        return self.password  # String

    def get_nom(self):
        return self.nom  # String

    def get_prenom(self):
        return self.prenom  # String

    def get_rue(self):
        return self.rue  # String

    def get_cp(self):
        return self.cp  # String

    def get_ville(self):
        return self.ville  # String

    def get_tags(self):
        return self.tags  # [String]
###############################################################################