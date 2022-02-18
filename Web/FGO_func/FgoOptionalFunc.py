# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 20:17:33 2020

@author: McLaren
"""

from Web.FGO_func.AdbApi import *
import time
import Web.FGO_func.Config.FgoConfig as gc


# 友情池抽取函数
def friend_point_summon():
    touch_button(gc.button["FriendPointSummonButton"])

    touch_button(gc.button["FriendPointSummonConfirm"], 2)
    time.sleep(1)
    touch_button(gc.button["FriendPointResummon"], 9)

    while True:
        touch_button(gc.button["FriendPointSummonConfirm"], 1)
        time.sleep(1)
        touch_button(gc.button["FriendPointResummon"], 9)


if __name__ == '__main__':
    friend_point_summon()
