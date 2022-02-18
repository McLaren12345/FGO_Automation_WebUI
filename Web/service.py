# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""

from flask import Flask, url_for, request, render_template, redirect, session, make_response
from Web.FGO_func.FgoThreadController import FgoThread
import Web.FGO_func.device as FgoDevice
from Web.FGO_func.Notice import send_message
import Web.FGO_func.Config.ConfigHandler as ConfigHandler
import sys

task = FgoThread()


def task_action(action: str) -> dict:
    if action not in ["create", "start", "pause", "resume", "stop"]:
        return {"success": False, "msg": "Bad syntax, no '{}' method for task object.".format(action)}
    if not FgoDevice.device_is_ready():
        return {"success": False, "msg": "Android device is not connected or activated."}
    return getattr(sys.modules[__name__], "_{}_task".format(action))()


def _create_task() -> dict:
    global task
    type_ = request.form.get("type", "")
    times = int(request.form.get("times", 1))
    servant = request.form.get("servant", "Caster_Altria")
    script_name = request.form.get("script_name", "default")
    if task.is_alive():
        return {"success": False,
                "msg": "Fail to create task. Another thread is running now. Terminate it before creating a new task."}
    else:
        if type_ not in ["battle", "summon"]:
            return {"success": False, "msg": "task type: '{}' not defined or supported.".format(type_)}
        task = FgoThread(type_, times, servant, script_name)
        return {"success": True, "msg": "Task created."}


def _start_task() -> dict:
    if task.has_started:
        return _resume_task()
    try:
        task.start()
        return {"success": True, "msg": "Task started."}
    except RuntimeError as e:
        return {"success": False, "msg": str(e)}


def _resume_task() -> dict:
    success, msg = task.resume()
    return {"success": success, "msg": msg}


def _pause_task() -> dict:
    success, msg = task.pause()
    return {"success": success, "msg": msg}


def _stop_task() -> dict:
    task.stop()
    return {"success": True, "msg": "Task stopped."}


def update_fgo_config() -> dict:
    try:
        config = request.get_json()
        ConfigHandler.update_config(config)
        ConfigHandler.save_config()
        return {"success": True, "msg": "Configuration updated."}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def get_fgo_config() -> dict:
    return {"success": True, "conf_map": ConfigHandler.get_config()}


def manage_battle_script(action: str) -> dict:
    return getattr(sys.modules[__name__], "_{}_battle_script".format(action))()


def _delete_battle_script() -> dict:
    try:
        script_name = request.form.get("script_name", "")
        success, msg = ConfigHandler.delete_battle_script(script_name)
        return {"success": success, "msg": msg}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def _save_battle_script() -> dict:
    try:
        data = request.get_json()
        script = data.get("script", {})
        script_name = data.get("script_name", "default")
        force_overwrite = bool(data.get("force_overwrite", False))
        success, msg = ConfigHandler.save_battle_script(script, script_name, force_overwrite)
        return {"success": success, "msg": msg}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def get_battle_script(type_: str) -> dict:
    try:
        script_name = request.values.get("script_name", "")
        success, result = getattr(ConfigHandler, "get_{}_battle_script".format(type_))(script_name)
        return {"success": success, "result": result}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def get_current_status() -> dict:
    return task.current_status()


def init_device():
    try:
        serial_no = request.form.get("serial_no", None)
        success, result = FgoDevice.re_init_device(serial_no)
        return {"success": success, "msg": result}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def list_device():
    try:
        return {"success": True, "result": FgoDevice.list_available_devices()}
    except BaseException as e:
        return {"success": False, "msg": str(e)}


def test_email():
    try:
        success, result = task.test_email()
        return {"success": success, "msg": result}
    except BaseException as e:
        return {"success": False, "msg": str(e)}
