import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wocanimei'
#如果这里不加一个secret key， 那么就会被500，服务出错，需要使用csrf
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#这里之前连接mysql出问题了，一直没有解决，我猜想是没有设置远程登录的问题，等下次再试。这次先用sqlite进行学习
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

moment = Moment(app)

bootstrap = Bootstrap(app)
# @app.route('/')
# def index():
# 	return render_template('index.html')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username



# 这下面是之前写网页的时候用的，不知道后面要不要用
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# @app.route('/user/<name>')
# def user(name):
# 	return render_template('user.html',name=name)
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'),404
#
# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template('500.html'),500
#
#
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known']=False
        else:
            session['known']=True
        session['name']=form.name.data
        return redirect(url_for('index'))   #因为函数名字叫index，所以传给URL函数的名字也是index#
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form, name=session.get('name'),
                           known=session.get('known', False))





