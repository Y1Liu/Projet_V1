from flask_login import UserMixin
from routes import db
###############################################################################
#CLASSE User
###############################################################################
class User(UserMixin):
    # CONSTRUCTEUR DE User
    """
    def __init__(self, email, password, nom, prenom, rue, cp, ville, tags):
    """
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)
    nom = db.StringField(max_length=30)
    prenom = db.StringField(max_length=30)
    rue = db.StringField(max_length=30)
    cp = db.StringField(max_length=30)
    ville = db.StringField(max_length=30)
    tags = db.StringField(max_length=30)

    """
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
    """
###############################################################################