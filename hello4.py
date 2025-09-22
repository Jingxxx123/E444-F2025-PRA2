from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NameEmailForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootrap = Bootstrap(app)
moment = Moment(app)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST']) 
@app.route('/index', methods=['GET', 'POST']) 
def index(): 
    form = NameEmailForm() 
    email = None         
    is_uoft = None
    name = None
    
    if form.validate_on_submit():

        name = form.name.data.strip()
        email = form.email.data.strip()
        is_uoft = 'utoronto' in email.lower()

        old_name = session.get('name')
        old_emial = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_emial is not None and old_emial != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['is_uoft'] = is_uoft


    return render_template('index.html', form=form, name=name, email=email, is_uoft=is_uoft, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)