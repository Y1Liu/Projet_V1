
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
class TrajectForm(FlaskForm):
	depart = StringField('Adresse de depart', validators=[DataRequired()])
	arrivee = StringField('Adresse d arrivee', validators=[DataRequired()])
	mode = SelectField('Moyen de transport', choices=[('Voiture', 'Voiture'), ('Train', 'Train')])
	pause_voyage = SelectField('Duree maximale d un trajet avant une pause', choices=[('1h', '1h'),('2h', '2h'),('3h', '3h'),('4h', '4h'),('5h', '5h'),('6h', '6h'),])
	tps_repas = SelectField('Duree maximale du repas', choices=[('30min', '30min'),('1h', '1h'),('2h', '2h')])
	submit = SubmitField('Valider')