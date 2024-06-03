# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import platform

from tkinter import messagebox
from ttkbootstrap import Style

import cube_qgui as cqgui

# 资源部分
QGUI_BASE_PATH = os.path.dirname(cqgui.__file__)
RESOURCES_PATH = os.path.join(QGUI_BASE_PATH, "resources")
ICON_PATH = os.path.join(RESOURCES_PATH, "icon")
THEME_PATH = os.path.join(QGUI_BASE_PATH, "theme/ttkbootstrap_themes.json")

HORIZONTAL = "Horizontal水平方向"
VERTICAL = "Vertical垂直方向"
LEFT = "左侧"
RIGHT = "右侧"
TOP = "顶端"
BOTTOM = "底部"


# Tools部分
class ConcurrencyModeFlag:
    # QUEUE_ = "触发后相关事件会以队列的形式执行"
    SAFE_CONCURRENCY_MODE_FLAG = "不允许并发，禁止触发下一个事件"
    # FORCE_CONCURRENCY_MODE_FLAG = "不允许并发，下一个事件被触发时结束上一个事件"


class QStyle:
    default = {"theme": "qgui", "themes_file": THEME_PATH}

    lumen = {"theme": "lumen"}

    paddle = {"theme": "paddlelight", "themes_file": THEME_PATH}

    paddle_dark = {"theme": "paddledark", "themes_file": THEME_PATH}

    pytorch = {"theme": "pytorch", "themes_file": THEME_PATH}

    tensorflow = {"theme": "tensorflow", "themes_file": THEME_PATH}


class MessageBox:
    @staticmethod
    def info(text: str, title: str = "Info - QGUI"):
        messagebox.showinfo(title, text)

    @staticmethod
    def warning(text: str, title: str = "Warning - QGUI"):
        messagebox.showwarning(title, text)

    @staticmethod
    def error(text: str, title: str = "Error - QGUI"):
        messagebox.showerror(title, text)


def show_file_or_path(path, return_func=True):
    def render(*args, **kwargs):
        if platform.system().lower() == "darwin":
            import subprocess
            subprocess.call(["open", path])
        else:
            os.startfile(path)

    if return_func:
        return render
    else:
        return render()


BLACK = "#24262d"
GRAY = "#e3e3e3"
GREEN = "#76b67e"
FONT = "黑体"
