# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 22:16:33 2021

@author: McLaren
"""

# 邮件提醒功能，若启用必须设置为True，并配置后续内容
# 配置QQ邮箱的SMTP服务即可实现邮件发送
# 详见：https://www.cnblogs.com/Alear/p/11594932.html
email_notice = True
email = ""  # 邮箱
passwd = ""  # 填入发送方邮箱的授权码

# 体力恢复配置
use_Crystal_stone = False
use_Gold_apple = True
use_Silver_apple = True
use_Bronze_apple = False

# 按键与位置全局配置区（目前软件可以自适应1080p与720p分辨率，其余分辨率需要自行修改配置）
# 可以通过Base_func中window_capture开启debug参数查看游戏界面的截图
# 像素测量可以采用Photoshop等专业软件，也可使用win10下的图片软件，裁剪功能里可以设置单位为像素进行测量

position = {
    "CardLeftBias": 205,  # 第一张卡牌与界面左侧距离
    "CardVerticalPosition": 765,  # 卡牌距顶端垂直距离
    "CardGap": 383,  # 卡牌间距
    "NoblePhantasmLeftBias": 623,  # 第一张宝具与界面左侧距离
    "NoblePhantasmVerticalPosition": 356,  # 宝具距顶端垂直距离
    "NoblePhantasmGap": 356,  # 宝具卡牌间距
    "CharacterSkillLeftBias": 115,  # 战斗界面中英灵第一张技能按键与界面左侧距离
    "CharacterSkillVerticalPosition": 868,  # 技能按键距顶端垂直距离
    "ServantGap": 480,  # 战斗界面中英灵间距
    "CharacterSkillGap": 142,  # 技能按键间距间距
    "SelectCharacterLeftBias": 498,  # 选人界面第一个英灵与界面左侧距离
    "SelectCharacterVerticalPosition": 623,  # 选人界面英灵中心距顶端垂直距离
    "SelectCharacterGap": 445,  # 选人界面英灵间距
    "MasterSkillVerticalPosition": 473,  # 御主技能按键距顶端垂直距离
    "MasterSkillLeftBias": 1352,  # 第一个御主技能按键距与界面左侧距离
    "MasterSkillGap": 142,  # 御主技能按键间距
    "ChangeOrderServantLeftBias": 213,  # 换人界面第一个英灵与界面左侧距离
    "ChangeOrderServantGap": 302,  # 换人界面英灵间距
    "ChangeOrderServantVerticalPosition": 534  # 换人界面英灵中心距顶端垂直距离
}

button = {
    "DefaultBattlePosition": (1407, 276),  # 默认的关卡位置（右上角）
    "ReenterBattleButton": (1254, 845),  # “连续出击“按键
    "FeedAppleDecideButton": (1263, 836),  # 吃苹果决定按键
    "RefreshFriendButton": (1281, 196),  # 刷新好友按键
    "RefreshFriendDecideButton": (1254, 845),  # 刷新好友决定按键
    "AttackButton": (1708, 907),  # 攻击按键
    "NextStep": (1754, 990),  # 下一步按键（关卡结束后确认战利品时右下角的按键）
    "RefuseFriendRequest": (418, 934),  # 拒绝好友申请按键
    "MasterSkillButton": (1797, position["MasterSkillVerticalPosition"]),  # 御主技能按键
    "StartBattleButton": (1780, 1014),  # 开始战斗按键
    "ChangeOrderDecideButton": (943, 943),  # 御主换人技能决定按键
    "SkipAnimation": (960, 355),  # 跳过动画时点击
    "FriendPointSummonButton": (960, 840),  # 友情点召唤
    "FriendPointResummon": (1150, 1014),  # 继续友情点召唤
    "FriendPointSummonConfirm": (1245, 855)  # 友情点召唤确认
}

# 战斗中金银苹果使用数量、礼装掉落数量
num_Gold_apple_used = 0
num_Silver_apple_used = 0
num_Bronze_apple_used = 0
num_Crystal_stone_used = 0
num_Craft = 0

global_pause = False

remaining_battle_times = 0
estimated_finished_time = 0
last_battle_time_usage = 0
global_error_flag = False
global_error_msg = ""
