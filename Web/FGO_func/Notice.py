# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:08:29 2020

@author: McLaren
"""

import Web.FGO_func.Config.FgoConfig as gc
import smtplib
from typing import Tuple
from email.mime.text import MIMEText

subject = "FGO脚本提示信息"  # 主题


def config_check() -> Tuple[bool, str]:
    if not gc.email_notice:
        return False, "Email notice functionality is not enabled."
    elif gc.email == "" or gc.passwd == "":
        print(" Need to correctly complete email config before using email notice!")
        return False, "Email notice is not enabled or email config not correctly completed."
    else:
        return True, ""


def send_message(text: str = "【FGO】: Detect a special drop item. ", extra_text: str = ""):
    valid, msg = config_check()
    if not valid:
        return False, msg
        # 正文
    msg = MIMEText(text + extra_text, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = gc.email
    msg["To"] = gc.email
    host = gc.email.split("@")[-1]

    try:
        s = smtplib.SMTP_SSL("smtp." + host, 465)
        s.login(gc.email, gc.passwd)
        s.sendmail(gc.email, gc.email, msg.as_string())
        return True, ""
    except BaseException as e:
        return False, str(e)
