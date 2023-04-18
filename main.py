import os

from flask import Flask, url_for, redirect, make_response, session
from flask import render_template
from flask import request
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'My_secret_key'


@app.route('/')
def main():
    return render_template('base.html', title='Главная')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/galery', methods=['GET'])
def galery():
    if request.method == 'GET':
        return render_template('galery.html',
                               title='Галерея')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Контакты')


if __name__ == '__main__':
    app.run()


