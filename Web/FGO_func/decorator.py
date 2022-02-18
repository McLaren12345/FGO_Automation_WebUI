# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:32:19 2021

@author: McLaren
"""

import time
import Web.FGO_func.Config.FgoConfig as gc
from functools import wraps


def EnableFgoPause(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        while gc.global_pause:
            time.sleep(1)
        return func(*args, **kwargs)

    return decorated
