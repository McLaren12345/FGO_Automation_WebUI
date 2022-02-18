# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""

import time
from tqdm import tqdm
import random
from Web.FGO_func.AdbApi import *
import Web.FGO_func.MysticCodes as MysticCodes
import Web.FGO_func.Config.FgoConfig as gc
from Web.FGO_func.Notice import send_message
import json


def wait_for_battle_start(need_press=False, pre_delay: int = 1):
    time.sleep(pre_delay)
    Flag, Position = match_template("Attack_button")
    while bool(1 - Flag):
        time.sleep(0.25)
        if need_press:
            touch_button(gc.button["SkipAnimation"])
        Flag, Position = match_template("Attack_button")


def wait_for_friend_show_ready():
    Flag, Position = match_template("friend_sign")
    while bool(1 - Flag):
        time.sleep(0.25)
        Flag, Position = match_template("friend_sign")
        if Flag:
            break
        Flag, Position = match_template("no_friend")
        if Flag:
            break


def enter_battle():
    menuFlag, Position1 = match_template("Menu_button")
    reenterFlag, Position2 = match_template("reenter_battle")

    while not (menuFlag or reenterFlag):
        time.sleep(1)  # Original value is 1
        menuFlag, Position1 = match_template("Menu_button")
        reenterFlag, Position2 = match_template("reenter_battle")

    if menuFlag:
        LastOrderFlag, Position3 = match_template("LastOrder_sign")
        if LastOrderFlag:
            touch(Position3[0] + 300, Position3[1] + 65)
            print(" Entered last order success")
            return "LastOrder"
        else:
            touch_button(gc.button["DefaultBattlePosition"])
            print(" Entered default success")
            return "Default"
    elif reenterFlag:
        touch_button(gc.button["ReenterBattleButton"])
        print(" Reentered battle success")
        return "Reenter"
    else:
        print(" ReadyToBattle Error")
        raise RuntimeError("Enter battle error.")


def apple_feed():
    def try_feed(item_: str):
        itemFlag, itemPosition = match_template(item_)
        if getattr(gc, "use_{}".format(item_)) and itemFlag:
            touch(itemPosition[0] + 100, itemPosition[1])
            time.sleep(1)
            touch_button(gc.button["FeedAppleDecideButton"])  # 决定
            setattr(gc, "num_{}_used".format(item_), getattr(gc, "num_{}_used".format(item_)) + 1)
            print(" Feed {} success".format(item_.lower()).replace("_", " "))
            return True
        return False

    time.sleep(1)
    recoverFlag, Position = match_template("AP_recover")
    if not recoverFlag:
        print(" No need to feed apple")
        return

    for item in ["Silver_apple", "Gold_apple", "Crystal_stone"]:
        if try_feed(item):
            return

    print(" No apple remain")
    raise RuntimeError("No apple remain.")


def find_friend(servant):
    wait_for_friend_show_ready()

    Flag, Position = match_template(servant + "_skill_level")
    time_limit_flag = 1
    # 找310CBA直到找到为止
    while bool(1 - Flag):
        print(" Didn't find {}, retry. Attempt{}".format(servant, time_limit_flag))
        if time_limit_flag > 1:
            time.sleep(15)
            # Flag,Position = Base_func.match_template('Refresh_friend')
        touch_button(gc.button["RefreshFriendButton"])  # refresh
        time.sleep(1.5)
        touch_button(gc.button["RefreshFriendDecideButton"])
        touch(Position[0], Position[1])

        wait_for_friend_show_ready()

        Flag, Position = match_template(servant + "_skill_level")
        time_limit_flag += 1

    if Flag:
        print(" Success find", servant)
        touch(Position[0], Position[1] - 60)
        time.sleep(1.5)


def budao():
    while True:
        while True:
            time.sleep(1)
            Flag, Position = match_template("Battlefinish_sign")
            if Flag:
                break
            Flag, Position = match_template("Attack_button")
            if Flag:
                break
        Flag, Position = match_template("Attack_button")
        if Flag:
            touch_button(gc.button["AttackButton"])  # 点击attack按钮
            time.sleep(1)
            Card_index = random.sample(range(0, 4), 3)  # 随机三张牌
            touch(gc.position["CardLeftBias"] + (Card_index[0]) * gc.position["CardGap"],
                  gc.position["CardVerticalPosition"], zoom=True)
            touch(gc.position["CardLeftBias"] + (Card_index[1]) * gc.position["CardGap"],
                  gc.position["CardVerticalPosition"], zoom=True)
            touch(gc.position["CardLeftBias"] + (Card_index[2]) * gc.position["CardGap"],
                  gc.position["CardVerticalPosition"], zoom=True)
            print(" Card has pressed")
        else:
            break


def quit_battle():
    time.sleep(10)
    finFlag, Position = match_template("Battlefinish_sign")
    attackFlag, Position = match_template("Attack_button")
    while not (finFlag or attackFlag):
        time.sleep(1)
        finFlag, Position = match_template("Battlefinish_sign")
        attackFlag, Position = match_template("Attack_button")
    if finFlag:
        pass
    elif attackFlag:
        print(" 翻车，进入补刀程序")  # 翻车检测
        budao()
    print(" Battle finished")
    time.sleep(1)
    rainbowFlag, Position = match_template("Rainbow_box")  # 检测是否掉礼装，若掉落则短信提醒
    if rainbowFlag:
        gc.num_Craft += 1
        send_message(extra_text="Currently {} crafts have dropped.".format(gc.num_Craft))
    touch_button(gc.button["NextStep"], 6)
    touch_button(gc.button["RefuseFriendRequest"], 2)  # 拒绝好友申请
    print(" Quit success")
    time.sleep(1)


def master_skill(func, parameter_list: list):
    touch_button(gc.button["MasterSkillButton"])  # 御主技能按键
    func(parameter_list)
    wait_for_battle_start()
    print(" Master skill{} has pressed".format(parameter_list[0]))
    time.sleep(1)


def character_skill(parameter_list: list):  # 角色编号，技能编号，选人（可选）
    if len(parameter_list) == 2:
        character_no, skill_no, para = parameter_list[0], parameter_list[1], None
    elif len(parameter_list) == 3:
        character_no, skill_no, para = parameter_list[0], parameter_list[1], parameter_list[2]
    else:
        return
    charPos = (gc.position["CharacterSkillLeftBias"] +
               (character_no - 1) * gc.position["ServantGap"] +
               (skill_no - 1) * gc.position["CharacterSkillGap"], gc.position["CharacterSkillVerticalPosition"])
    touch(charPos[0], charPos[1], zoom=True)
    if para is not None:
        targetPos = (gc.position["SelectCharacterLeftBias"] +
                     (para - 1) * gc.position["SelectCharacterGap"],
                     gc.position["SelectCharacterVerticalPosition"])  # 技能选人
        touch(targetPos[0], targetPos[1], zoom=True)
    wait_for_battle_start()
    print(" Character{}'s skill{} has pressed".format(character_no, skill_no))


def card(treasure_device_no=1):
    touch_button(gc.button["AttackButton"])  # 点击attack按钮
    time.sleep(1.5)
    touch(gc.position["NoblePhantasmLeftBias"] + (treasure_device_no - 1) * gc.position["NoblePhantasmGap"],
          gc.position["NoblePhantasmVerticalPosition"], zoom=True)  # 打手宝具,参数可选1-3号宝具位
    Card_index = random.sample(range(0, 4), 2)  # 随机两张牌
    touch(gc.position["CardLeftBias"] + (Card_index[0]) * gc.position["CardGap"],
          gc.position["CardVerticalPosition"], zoom=True)
    touch(gc.position["CardLeftBias"] + (Card_index[1]) * gc.position["CardGap"],
          gc.position["CardVerticalPosition"], zoom=True)
    print(" Card has pressed")


def phrase_battle_script(script_name: str):
    with open("Web/FGO_func/Config/battle/" + script_name + ".json", "r", encoding='utf-8') as f:
        battle_script = json.loads(f.read())  # load的传入参数为字符串类型

    mystic_codes = getattr(MysticCodes, battle_script.get("MysticCodes", "chaldea_combat_uniform"))
    battle_turns = battle_script.get("Turns", [])
    for turn in battle_turns:
        character_skill_list = turn.get("character_skill", [])
        master_skill_list = turn.get("master_skill", [])
        card_num = turn.get("card", 1)
        # 等待战斗开始
        wait_for_battle_start(need_press=True, pre_delay=8)
        [character_skill(para) for para in character_skill_list]
        [master_skill(mystic_codes, para) for para in master_skill_list]
        card(card_num)


def battle(script_name: str):
    touch_button(gc.button["StartBattleButton"])
    print(" Start battle button pressed")
    phrase_battle_script(script_name)


def fgo_process(times=1, servant="CBA", script_name="default"):
    gc.estimated_finished_time = 180 * gc.remaining_battle_times
    for _ in range(times):
        start = time.clock()
        enter_battle()
        apple_feed()
        find_friend(servant)
        battle(script_name)
        quit_battle()
        end = time.clock()
        gc.remaining_battle_times -= 1
        gc.last_battle_time_usage = (end - start) // 1
        gc.estimated_finished_time = (end - start) * gc.remaining_battle_times // 1
        print(" ")
        print(" {} times of battles remain.".format(gc.remaining_battle_times))
        print(" Currently {} Gold Apples, {} Silver Apples used, {} Crafts droped.".format(gc.num_Gold_apple_used,
                                                                                           gc.num_Silver_apple_used,
                                                                                           gc.num_Craft))


def main():
    fgo_process(5, "Caster_Altria")
    print(" All done!")


if __name__ == "__main__":
    main()
