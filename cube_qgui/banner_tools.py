# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import webbrowser

import tkinter
from tkinter import ttk
from cube_qgui.manager import ICON_PATH, ConcurrencyModeFlag
from cube_qgui.base_tools import ArgInfo, BaseTool

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")
GITHUB_ICON = os.path.join(ICON_PATH, "github.png")
AI_STUDIO_ICON =  os.path.join(ICON_PATH, "up_cloud.png")


class BaseBarTool(BaseTool):
    """
    基础Banner工具集
    需注意的是，如需增加异步等操作，请为函数添加_callback
    """

    def __init__(self,
                 bind_func,
                 name="Unnamed Tool",
                 icon=None,
                 style=None,
                 async_run: bool = True,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(bind_func=bind_func,
                         name=name,
                         style=style,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)

        if icon and not os.path.exists(icon):
            raise f"Please check if {os.path.abspath(icon)} exists."
        if not icon:
            icon = RUN_ICON
        self.icon = icon

    def build(self, *args, **kwargs):
        super().build(*args, **kwargs)
        self.img = tkinter.PhotoImage(file=self.icon)

        btn = ttk.Button(self.master,
                         text=self.name,
                         image=self.img,
                         compound="left",
                         command=self._callback(self.bind_func) if self.async_run else self.bind_func,
                         style=self.style + "TButton")

        btn.pack(side="left", ipadx=5, ipady=5, padx=0, pady=1)


class RunTool(BaseBarTool):
    def __init__(self,
                 bind_func,
                 name="Start Processing",
                 icon=None,
                 style="success",
                 async_run: bool = True,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        if not icon:
            icon = RUN_ICON
        super(RunTool, self).__init__(bind_func,
                                      name=name,
                                      icon=icon,
                                      style=style,
                                      async_run=async_run,
                                      concurrency_mode=concurrency_mode)


class GitHub(BaseBarTool):
    def __init__(self,
                 url,
                 name="View on GitHub",
                 style="primary"):
        icon = GITHUB_ICON
        bind_func = self.github_callback
        super().__init__(bind_func,
                         name=name,
                         icon=icon,
                         style=style)
        self.github_url = url

    def github_callback(self, args):
        webbrowser.open_new(self.github_url)


class AIStudio(BaseBarTool):
    def __init__(self,
                 url,
                 name="Use on AI Studio",
                 style="primary"):
        icon = AI_STUDIO_ICON
        bind_func = self.ai_studio_callback
        super().__init__(bind_func,
                         name=name,
                         icon=icon,
                         style=style)
        self.ai_studio_url = url

    def ai_studio_callback(self, args):
        webbrowser.open_new(self.ai_studio_url)
