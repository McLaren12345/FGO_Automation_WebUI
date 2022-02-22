# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""

from flask import Flask, redirect, render_template
from Web import service

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/index')


@app.route('/<page_name>', methods=['GET'])
def home(page_name: str):
    return render_template("{}.html".format(page_name))


@app.route('/task/<action>', methods=['POST'])
def task_action(action: str):
    return service.task_action(action.lower())


@app.route('/config', methods=['GET'])
def get_configuration():
    return service.get_fgo_config()


@app.route('/config', methods=['POST'])
def update_configuration():
    return service.update_fgo_config()


@app.route('/script/<type_>', methods=['GET'])
def get_battle_script(type_: str):
    return service.get_battle_script(type_)


@app.route('/script/<action>', methods=['POST'])
def manage_battle_script(action: str):
    return service.manage_battle_script(action)


@app.route('/status', methods=['GET'])
def get_status():
    return service.get_current_status()


@app.route('/device', methods=['POST'])
def init_device():
    return service.init_device()


@app.route('/device', methods=['GET'])
def list_device():
    return service.list_device()


@app.route('/test_email', methods=['GET'])
def test_email():
    return service.test_email()
