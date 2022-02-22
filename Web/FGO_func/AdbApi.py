# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:32:19 2021

@author: McLaren
"""

import time
import cv2 as cv
import os
from Web.FGO_func.Notice import send_message
import Web.FGO_func.device as device
from Web.FGO_func.decorator import EnableFgoPause

template_pool = {i[:-4]: cv.imread(f"Web/FGO_func/Template/{i}") for i in os.listdir("Web/FGO_func/Template") if i[-4:] == ".jpg"}


class Fuse:
    def __init__(self):
        self.value = 0
        self.tolerant_time = 50  # 截取50张图片后仍未发现对应目标则报错
        # 防止程序死在死循环里

    def increase(self):
        self.value += 1

    def reset(self):
        self.value = 0

    def alarm(self, template_name: str):
        if self.value == self.tolerant_time:
            send_message(text='【FGO】: Encounter a fuse error. Currently fused at: {}.jpg.'.format(template_name))
            print(" Fuse Error!")


fuse = Fuse()


@EnableFgoPause
def match_template(filename: str, show_switch=False, threshold=0.85):
    """
    Given the file name of the template, attempts to find the portion
    that matchs the template and returns the result
    尝试在截图中匹配目标模板，返回匹配的结果与具体位置


    Parameters
    ----------
    filename : str
        模板的无后缀文件名
        File name of the template, without postfix
    show_switch : bool, optional
        Bool variable for displaying the matching image.
        This variable is used for debugging and shouldn't be changed otherwise.
        The default is False.
        是否显示匹配的图片部分。
        此参数为测试用，正常使用时无需改动。
        默认值为 False。
    threshold : float, optional
        Minimum rate of matching.
        The default is 0.85.
        与模板的最低匹配度。
        默认为 0.85。

    Returns
    -------
    bool
        The final status of matching
        是否有图片部分与模板匹配
    (int, int)
        Coordinates of the center of the matching portion of the picture
        与模板匹配的图片部分的中心坐标

    """

    fuse.increase()

    img = device.dev.snapshot(quality=99)

    player_template = cv.resize(template_pool[filename], None,
                                fx=device.global_zoom_coefficient,
                                fy=device.global_zoom_coefficient,
                                interpolation=cv.INTER_AREA) \
        if device.global_zoom_coefficient != 1 else template_pool[filename]
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    # 当图片中有与模板匹配度超过85%的部分时：
    if max_val > threshold:
        # 框选出目标，并标出中心点
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] + player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1] / 2), max_loc[1] + int(player_template.shape[0] / 2))

        if show_switch:
            cv.circle(img, player_spot, 10, (0, 255, 255), -1)
            cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 3)
            cv.namedWindow("FGO_MatchResult", cv.WINDOW_KEEPRATIO)
            cv.imshow("FGO_MatchResult", img)
            # 显示结果2秒钟
            k = cv.waitKey(5000)
            if k == -1:
                cv.destroyAllWindows()

        fuse.reset()
        return True, player_spot
    else:
        fuse.alarm(filename)
        return False, (-1, -1)


# def mouse_swipe(from_, to, duration=500):
#     pass


@EnableFgoPause
def touch(x_position: int, y_position: int, times=1, interval=0.5, zoom=False):
    for i in range(times):
        if not zoom:
            device.dev.touch((x_position, y_position))
        else:
            device.dev.touch(
                (int(x_position * device.global_zoom_coefficient), int(y_position * device.global_zoom_coefficient)))
        time.sleep(interval)


@EnableFgoPause
def touch_button(position: tuple, times=1, interval=0.5):
    for i in range(times):
        device.dev.touch((int(position[0] * device.global_zoom_coefficient),
                          int(position[1] * device.global_zoom_coefficient)))
        time.sleep(interval)


if __name__ == "__main__":
    match_template("Rainbow_box", True, 0.9)
