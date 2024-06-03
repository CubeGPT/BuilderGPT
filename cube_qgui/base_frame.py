# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import sys
import webbrowser
import time
from typing import List

import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from cube_qgui.manager import BLACK, FONT
from cube_qgui.banner_tools import BaseBarTool
from cube_qgui.third_party.collapsing_frame import CollapsingFrame
from cube_qgui.notebook_tools import BaseNotebookTool
from cube_qgui.os_tools import StdOutWrapper, DataCache
from cube_qgui.base_tools import ArgInfo

TITLE_BG_COLOR = BLACK


# ToDo 主题部分可考虑通过增加warmup来解决

class _Backbone:
    """
    整个界面的基础，存放共有的变量
    """

    def __init__(self, f_style="primary"):
        """
        请务必检查self.frame是否做了pack等定位操作，无操作将不会被显示
        :param f_style:
        """
        # 统一用place
        self.style = f_style

        # 全局变量
        self.global_info = ArgInfo()

    def build(self, master, global_info):
        self.frame = ttk.Frame(master, style=self.style + ".TFrame")
        self.global_info = global_info


class BaseNavigation(_Backbone):
    """
    左侧导航栏基本框架
    """

    def __init__(self, style="primary"):
        super(BaseNavigation, self).__init__(f_style=style)
        self.tabs = dict()

    def add_about(self,
                  author: str = "未知作者",
                  version: str = "0.0.1",
                  github_url: str = None,
                  bilibili_url: str = None,
                  blog_url: str = None,
                  other_info: List[str] = None):
        bus_cf = CollapsingFrame(self.frame)
        bus_cf.pack(fill='x', pady=0)

        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title="Info", style='secondary.TButton')

        ttk.Label(bus_frm, text=f"Author:\t{author}", style="TLabel", justify="left", wraplength=160).pack(anchor="nw")
        ttk.Label(bus_frm, text=f"Version:\t{version}", style="TLabel", justify="left", wraplength=160).pack(anchor="nw")

        if other_info:
            for line in other_info:
                ttk.Label(bus_frm, text=line, style="TLabel").pack(anchor="nw")

        if github_url:
            def github_callback(event):
                webbrowser.open_new(github_url)

            github_label = ttk.Label(bus_frm, text=f"> View on GitHub", style="info.TLabel", justify="left")
            github_label.pack(anchor="nw")
            github_label.bind("<Button-1>", github_callback)

        if bilibili_url:
            def bilibili_callback(event):
                webbrowser.open_new(bilibili_url)

            bilibili_label = ttk.Label(bus_frm, text=f"> View on bilibili", style="info.TLabel", justify="left")
            bilibili_label.pack(anchor="nw")
            bilibili_label.bind("<Button-1>", bilibili_callback)

        if blog_url:
            def blog_callback(event):
                webbrowser.open_new(blog_url)

            blog_label = ttk.Label(bus_frm, text=f"> View on blog", style="info.TLabel", justify="left")
            blog_label.pack(anchor="nw")
            blog_label.bind("<Button-1>", blog_callback)

    def add_info(self,
                 title: str,
                 info: str):
        bus_cf = CollapsingFrame(self.frame)
        bus_cf.pack(fill='x', pady=0)

        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title=title, style='secondary.TButton', justify="left")

        ttk.Label(bus_frm, text=info, style="TLabel", wraplength=160).pack(anchor="nw")

    # def add_homepage(self, tool):
    #     btn = ttk.Button(self.frame,
    #                      text=tool.name,
    #                      image=tool.name,
    #                      compound='left',
    #                      command=tool.bind_func)
    #     btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)
    def build(self, master, global_info):
        super(BaseNavigation, self).build(master, global_info)
        self.frame.place(x=0, y=50, width=180, height=470)


class BaseNoteBook(_Backbone):
    """
    中间Notebook部分框架
    """

    def __init__(self,
                 style="primary",
                 tab_names: List[str] = None,
                 stdout=None):
        super(BaseNoteBook, self).__init__(f_style=style)
        self.tab_names = tab_names
        self.nb_frames = list()

        # 初始化总输出行数
        self.line_len = 2
        if not stdout:
            stdout = sys.stdout
        self.stdout = stdout

        sys.stdout = StdOutWrapper(self.stdout, callback=self._write_log_callback)
        sys.stderr = StdOutWrapper(self.stdout, callback=self._write_log_callback)

        self.image_cache = DataCache()

    def add_tool(self, tool: BaseNotebookTool, to_notebook=True):

        if tool.tab_index >= len(self.nb_frames):
            raise ValueError(f"设置的index大小越界，当前页面数量为{len(self.nb_frames)}，分别为：{self.nb_frames}，而"
                             f"您设置的index为{tool.tab_index}，超过了当前页面数量。")
        if to_notebook:
            frame = self.nb_frames[tool.tab_index]
            tool_frame = tool.build(master=frame, global_info=self.global_info)
        else:
            tool_frame = tool.build(global_info=self.global_info)
        tool_info = tool.get_arg_info()
        self.global_info += tool_info
        return tool_frame

    def build(self, master, global_info):
        super(BaseNoteBook, self).build(master, global_info)
        self.frame.place(x=182, y=55, width=750, height=460)
        self.nb = ttk.Notebook(self.frame)
        self.nb.pack(side="top", fill="both")

        if self.tab_names:
            for tab_name in self.tab_names:
                sub_frame = ttk.Frame(self.nb)
                sub_frame.pack(anchor="nw", expand="yes")
                self.nb_frames.append(sub_frame)
                self.nb.add(sub_frame, text=tab_name)
        else:
            sub_frame = ttk.Frame(self.nb)
            sub_frame.pack(anchor="nw", expand="yes")
            self.nb_frames.append(sub_frame)
            self.nb.add(sub_frame, text="Generate")
        self.global_info += ArgInfo(name="QGUI-BaseNoteBook",
                                    set_func=self._select_notebook_callback,
                                    get_func=lambda: print("BaseNoteBook不支持get"))

        # 增加OutPut
        self.console_frame = ttk.Frame(self.frame,
                                       style=self.style + ".TFrame")
        self.console_frame.pack(side="top", fill='both', expand="yes")

        # 标题
        self.title = ttk.Label(self.console_frame,
                               font=(FONT, 15),
                               style=self.style + ".Inverse.TLabel",
                               text="Console Log",
                               justify="left")
        self.title.pack(side="top", fill="x", padx=10, pady=5)

        # 文本
        self.text_area = ScrolledText(self.console_frame,
                                      highlightcolor=master.style.colors.primary,
                                      highlightbackground=master.style.colors.border,
                                      highlightthickness=1)

        self.text_area.pack(fill="both", expand="yes")

        self.text_area.insert("end", "Console Connected\n")
        self.text_area.configure(state="disable")

    def print_tool(self, tool: BaseNotebookTool):
        self.text_area.configure(state="normal")
        self.text_area.window_create("end", window=self.add_tool(tool, to_notebook=False))
        self.text_area.configure(state="disable")
        print("")

    def print_image(self, image):
        from PIL import Image, ImageTk
        if isinstance(image, str):
            image = Image.open(image)
        w, h = image.size
        scale = 128 / max(w, h)
        w *= scale
        h *= scale
        image = image.resize((int(w), int(h)))
        image = ImageTk.PhotoImage(image)
        self.image_cache += image
        self.text_area.configure(state="normal")
        self.text_area.image_create("end", image=image)
        self.text_area.configure(state="disable")
        print("")

    def _select_notebook_callback(self, index):
        self.nb.select(index)

    def _write_log_callback(self, text):
        self.text_area.configure(state="normal")

        # 对print形式的进度条进行适配
        if "\r" in text:
            self.text_area.delete(str(self.line_len) + ".0", str(self.line_len) + ".end")
            self.line_len -= 1
            text = text[text.index("\r") + 1:] + " "

        if len(text) > 0 and text != "\n":
            text = time.strftime("%H:%M:%S", time.localtime()) + "\t" + text

        self.text_area.insert("end", text)
        self.line_len += 1
        self.text_area.configure(state="disable")
        self.text_area.see("end")


class BaseBanner(_Backbone):
    def __init__(self,
                 title: str = "QGUI Tesing Program",
                 style="primary"):
        super(BaseBanner, self).__init__(f_style=style)
        self.img_info = dict()
        self.title = title

    def add_tool(self, tool: BaseBarTool):
        """
        添加小工具组件
        :param
        """
        tool.build(master=self.frame, global_info=self.global_info)
        tool_info = tool.get_arg_info()
        self.global_info += tool_info

    def build(self, master, global_info):
        super(BaseBanner, self).build(master, global_info)
        self.frame.place(x=0, y=0, width=940, height=50)
        # 占位标题
        black = tkinter.Frame(self.frame,
                              height=10,
                              bg=TITLE_BG_COLOR)
        black.pack(side="right", anchor="se")
        # 主标题
        title = ttk.Label(self.frame,
                          font=(FONT, 22),
                          text=self.title,
                          style=self.style + ".Inverse.TLabel")
        title.pack(side="right", anchor="se", padx=5, pady=3)


if __name__ == '__main__':
    pass
