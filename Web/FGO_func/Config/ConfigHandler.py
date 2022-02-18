# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""

import Web.FGO_func.Config.FgoConfig as gc
import json
import os

basic_path = "Web/FGO_func/Config/"
battle_file_path = basic_path + "battle/"
config_file_name = basic_path + "fgo_config.json"
battle_file_name = battle_file_path + "{}.json"

Config = {}


def init_config():
    global Config
    with open(config_file_name, "r", encoding='utf-8') as f:
        Config = json.loads(f.read())  # load的传入参数为字符串类型
    for key, value in Config.items():
        setattr(gc, key, value)


def save_config():
    with open(config_file_name, "w", encoding='utf-8') as f:
        json.dump(Config, f, indent=2)  # 传入文件描述符，和dumps一样的结果


def update_config(config_data):
    global Config
    for key, value in config_data.items():
        Config[key] = value
        setattr(gc, key, value)


def get_config():
    return Config  # load的传入参数为字符串类型


def save_battle_script(config_data, script_name: str, force_overwrite: bool = False):
    if script_name.endswith(".json"):
        script_name = script_name[0: len(script_name)-5]
    if not force_overwrite:
        if "{}.json".format(script_name) in os.listdir(battle_file_path):
            return False, "Already contains file with the same name. You might check the force overwrite checkbox."
    try:
        with open(battle_file_name.format(script_name), "w", encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)  # 传入文件描述符，和dumps一样的结果
        return True, "Script saved."
    except BaseException as e:
        return False, str(e)


def delete_battle_script(script_name: str):
    if "{}.json".format(script_name) not in os.listdir(battle_file_path):
        return True, "Already deleted."
    try:
        os.remove(battle_file_name.format(script_name))
        return True, "Script deleteded."
    except BaseException as e:
        return False, str(e)


def get_single_battle_script(script_name: str = "default"):
    if "{}.json".format(script_name) not in os.listdir(battle_file_path):
        return False, "Script file {}.json not found.".format(script_name)
    try:
        with open(battle_file_name.format(script_name), "r", encoding='utf-8') as f:
            return True, json.loads(f.read())  # load的传入参数为字符串类型
    except BaseException as e:
        return False, str(e)


def get_all_battle_script(useless):
    try:
        return True, list(filter(lambda x: x.endswith(".json"), os.listdir(battle_file_path)))
    except BaseException as e:
        return False, str(e)


init_config()
