# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:46:30 2020

@author: McLaren
"""

from Web.FGO_func.AdbApi import *
import Web.FGO_func.Config.FgoConfig as gc
import time


def _all_allies_skill(parameter_list_: list):
    time.sleep(0.4)
    touch(gc.position["MasterSkillLeftBias"] + gc.position["MasterSkillGap"] * (parameter_list_[0] - 1),
          gc.position["MasterSkillVerticalPosition"])


def _one_ally_skill(parameter_list_: list):
    time.sleep(0.4)
    touch(gc.position["MasterSkillLeftBias"] + gc.position["MasterSkillGap"] * (parameter_list_[0] - 1),
          gc.position["MasterSkillVerticalPosition"])
    time.sleep(0.4)
    Position = (
        gc.position["SelectCharacterLeftBias"] + (parameter_list_[1] - 1) * gc.position["SelectCharacterGap"],
        gc.position["SelectCharacterVerticalPosition"])  # 蓝魔放与宝具威力提升，技能选人
    touch(Position[0], Position[1], zoom=True)


# 魔术礼装·迦勒底
def chaldea(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 魔术礼装·魔术协会制服
def mages_association_uniform(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _all_allies_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _all_allies_skill(parameter_list)

    handler(parameter_list)


# 魔术礼装·阿特拉斯院制服
def atlas_institute_uniform(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _all_allies_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _all_allies_skill(parameter_list)

    handler(parameter_list)


# 换人服
def chaldea_combat_uniform(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:  # 加攻
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:  # 眩晕
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:  # 换人
            touch(gc.position["MasterSkillLeftBias"] + gc.position["MasterSkillGap"] * 2,
                  gc.position["MasterSkillVerticalPosition"], zoom=True)
            touch(
                gc.position["ChangeOrderServantLeftBias"] + (parameter_list_[2] + 2) * gc.position[
                    "ChangeOrderServantGap"],
                gc.position["ChangeOrderServantVerticalPosition"], zoom=True)
            touch(
                gc.position["ChangeOrderServantLeftBias"] + (parameter_list_[1] - 1) * gc.position[
                    "ChangeOrderServantGap"],
                gc.position["ChangeOrderServantVerticalPosition"], zoom=True)
            touch_button(gc.button["ChangeOrderDecideButton"])

    handler(parameter_list)


# 金色庆典
def anniversary_blonde(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _all_allies_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 王室品牌
def royal_brand(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 明亮夏日
def brilliant_summer(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _all_allies_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 月之海的记忆
def memories_of_a_lunar_sea(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _all_allies_skill(parameter_list)

    handler(parameter_list)


# 月之背面的记忆
def memories_of_the_far_side_of_the_moon(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _all_allies_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _all_allies_skill(parameter_list)

    handler(parameter_list)


# 2004年的碎片
def fragments_of_year_2004(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 魔术礼装·极地用迦勒底制服
def chaldea_uniform_arctic(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list)

    handler(parameter_list)


# 热带夏日
def tropical_summer(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)


# 华美的新年
def splendid_new_year(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _all_allies_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)


# 第五真说要素环境用迦勒底制服
def chaldea_uniform_true_ether(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)


# 迦勒底船长
def captain_chaldea(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)


# 迦勒底探险者
def chaldea_pathfinder(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _all_allies_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)


# 万圣夜王室装
def halloween_royalty(parameter_list: list):
    def handler(parameter_list_: list):
        if parameter_list_[0] == 1:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 2:
            _one_ally_skill(parameter_list_)
        elif parameter_list_[0] == 3:
            _one_ally_skill(parameter_list_)

    handler(parameter_list)
