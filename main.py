import os

from flask import Flask, url_for, redirect, make_response, session
from flask import render_template
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from data.jobs import Jobs
from db import db_session
from data.users import User  # импорт модели пользователя
from data.login import LoginForm
from flask_login import LoginManager, login_user
from api import jobs_api, jobs_resourse

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'My_secret_key'


@app.route('/')
def main():
    return render_template('base.html', title='Главная')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    pictures = os.listdir('static/img/galery')
    if request.method == 'GET':
        return render_template('galery.html',
                               pictures=pictures,
                               title='Галерея',
                               lnp=len(pictures))


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Контакты')


if __name__ == '__main__':
    app.run()
    #db_session.global_init("db/blogs.db")
    # request1('db/blogs.db')

