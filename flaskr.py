
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort
from flask import render_template, flash
from contextlib import closing
import bokeh.plotting as p
from model import Entry, User
from database import db_session

DATABASE = r'tmp\flaskr.db'
DEBUG = True
SECRET_KEY = 'dev key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    try:
        g.db.close()
    except AttributeError:
        pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def show_entries():
    from bokeh import embed, plotting, resources
    entries = Entry.query.order_by('date').all()


    all_dia = [i.dia for i in entries]
    all_sys = [i.sys for i in entries]
    all_pulse = [i.pulse for i in entries]
    fig = plotting.figure(toolbar_location='right', width=520, height=350,
                          logo=None, x_axis_type='datetime'
                        )

    x = range(len(all_dia))
    x = [i.date for i in entries]
    fig.line(x, all_dia, color='red')
    fig.line(x, all_sys, color='blue')
    fig.line(x, all_pulse, color='black')
    script, div = embed.components(fig, resources.INLINE)
    return render_template('show_entries.html', entries=entries, script=script,
                           div=div)



@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    form = request.form
    sys, dia, pulse = form['systolic'], form['diatolic'], form['pulse']
    when, side = form['time'], form['side']
    entry = Entry(sys, dia, pulse, side, when)
    db_session.add(entry)
    db_session.commit()
    flash("Succesful posted")
    return redirect(url_for('show_entries'))


@app.route('/delete/<entry_id>')
def delete_entry(entry_id):
    if not session.get('logged_in'):
        abort(401)
    to_del = Entry.query.get(entry_id)
    db_session.delete(to_del)
    db_session.commit()
    return redirect(url_for('show_entries'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid login'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid password'
        else:
            session['logged_in'] = True
            flash('logged in!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    app.run(debug=True)
