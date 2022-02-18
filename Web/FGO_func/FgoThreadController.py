# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:32:19 2021

@author: McLaren
"""
import ctypes
import threading
import time
import Web.FGO_func.Config.FgoConfig as gc
import Web.FGO_func.FgoFunc as FgoFunc
import Web.FGO_func.FgoOptionalFunc as FgoOptionalFunc
import Web.FGO_func.device as FgoDevice
from Web.FGO_func.Notice import send_message


class StoppableThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._has_started = False
        self._is_alive = False
        self.status = "Not started."

    def pause(self):
        if self.status == "Terminated." or self.status == "SystemExit.":
            return False, "Task terminated or exited."
        self.status = "Paused."
        gc.global_pause = True
        return True, "Task paused."

    def resume(self):
        if self.status == "Terminated." or self.status == "SystemExit.":
            return False, "Task terminated or exited."
        self.status = "Running."
        gc.global_pause = False
        return True, "Task resumed."

    def _get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id_, thread in threading._active.items():
            if thread is self:
                return id_

    def stop(self):
        self._is_alive = False
        gc.global_pause = False
        thread_id = self._get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print(' Exception raise failed.')
        self.status = "Terminated."

    def is_alive(self) -> bool:
        return self._is_alive and self._has_started

    @property
    def has_started(self):
        return self._has_started


class FgoThread(StoppableThread):

    def __init__(self, type_: str = "battle", times: int = 0, servant: str = "Caster_Altria",
                 script_name: str = "", *args, **kwargs):
        super(FgoThread, self).__init__(*args, **kwargs)
        self._type = type_
        self._battle_times = 0
        gc.remaining_battle_times = 0
        if self._type == "battle":
            self._battle_times = times
            gc.remaining_battle_times = times
        self._servant = servant
        self._script_name = script_name
        gc.global_error_flag = False
        gc.global_error_msg = ""
        gc.last_battle_time_usage = 0

    def run(self):
        self._has_started = True
        self._is_alive = True
        self.status = "Running."
        try:
            if self._type.lower() == "battle":
                FgoFunc.fgo_process(self._battle_times, self._servant, self._script_name)
            elif self._type.lower() == "summon":
                FgoOptionalFunc.friend_point_summon()
        except BaseException as e:
            self.status = "SystemExit."
            gc.global_error_flag = True
            gc.global_error_msg = str(e)
        finally:
            if self.status != "SystemExit.":
                self.status = "Finished."

    def get_running_status(self):
        return self.status

    @staticmethod
    def test_email():
        return send_message("【FGO】: This is a test email.")

    def current_status(self):
        return {"taskType": self._type, "errMsg": gc.global_error_msg, "taskStatus": self.get_running_status(),
                "totalTimes": self._battle_times, "servant": self._servant, "timeLeft": gc.estimated_finished_time,
                "itemUsage": {"GoldApple": gc.num_Gold_apple_used, "SilverApple": gc.num_Silver_apple_used,
                              "BronzeApple": gc.num_Bronze_apple_used, "CrystalStone": gc.num_Crystal_stone_used},
                "craftDropped": gc.num_Craft, "scriptName": self._script_name + ".json",
                "remainingTime": gc.remaining_battle_times, "lastBattleTimeUsage": gc.last_battle_time_usage,
                "device_status": FgoDevice.device_is_ready(), "errFlag": gc.global_error_flag,
                "dev_serial_no": FgoDevice.get_current_device()}


if __name__ == "__main__":
    a = FgoThread("", times=1, servant="Caster_Altria")
