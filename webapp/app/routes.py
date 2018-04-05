from flask import render_template, flash, redirect, Markup
from app import app
from app.forms import TrajectForm
from app.cache import cache

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Arnaud'}
	return render_template('index.html', title='Home', user=user)

@app.route('/form', methods=['GET', 'POST'])
@cache.cached(timeout=150)
#@cache.cached(300, key_prefix='form', unless='only_cache_get')
def form():
	form = TrajectForm()
	if form.validate_on_submit():
		flash(Markup('Ville de départ : <b>{}</b>'.format(form.depart.data)))
		flash(Markup('Ville d arrivee : <b>{}</b>'.format(form.arrivee.data)))
		flash(Markup('Moyen de transport : <b>{}</b>'.format(form.mode.data)))
		flash(Markup('Temps maximal de trajet : <b>{}</b>'.format(form.pause_voyage.data)))
		flash(Markup('Durée maximale du repas : <b>{}</b>'.format(form.tps_repas.data)))
		return redirect('/form')
	return render_template('forms.html', title='Formulaire', form=form)



