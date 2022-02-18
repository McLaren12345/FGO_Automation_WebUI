# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:32:19 2021

@author: McLaren
"""

from airtest.core.android.android import *

try:
    dev = Android()
    global_zoom_coefficient = dev.display_info["height"] / 1080
except IndexError as e:
    dev = None
    global_zoom_coefficient = 0
    print("No android device found.")


def re_init_device(serial_no: str):
    global dev, global_zoom_coefficient
    if device_is_ready() and (serial_no == dev.serialno):
        return True, ""
    try:
        dev = Android(serialno=serial_no)
        global_zoom_coefficient = dev.display_info["height"] / 1080
        return True, ""
    except BaseException as e_:
        return False, str(e_)


def list_available_devices():
    if not ADB().devices(state="device"):
        return {"current_device": 0, "device_list": []}
    device_list = [device[0] for device in ADB().devices(state="device")]
    try:
        current_device = device_list.index(dev.serialno)
    except BaseException as _:
        current_device = 0
    return {"current_device": current_device, "device_list": device_list}


def device_is_ready():
    try:
        return not dev.is_locked()
    except BaseException as _:
        return False


def get_current_device():
    try:
        return dev.serialno
    except BaseException as _:
        return ""