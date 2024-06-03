# Author: Acer Zhang
# Datetime: 2021/8/31 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
from typing import List

import tkinter
import tkinter.font
from ttkbootstrap import Style

from cube_qgui.manager import QStyle, FONT
from cube_qgui.base_frame import BaseNoteBook, BaseBanner, BaseNavigation
from cube_qgui.banner_tools import BaseBarTool
from cube_qgui.notebook_tools import BaseNotebookTool
from cube_qgui.base_tools import check_callable


class CreateQGUI:
    """
    创建最基础的QGUI程序

    :param title: 主程序标题
    :param style: 皮肤，需通过QStyle来确定
    :param stout: 标准输出流
    :param tab_names: List[str] 功能区Tab页面，默认为“主程序控制台”
    :param banner: QGUI的Banner对象
    :param navigation: QGUI的navigation对象
    :param notebook: QGUI的notebook对象
    :param bind_func: 全局事件绑定
    """

    def __init__(self,
                 title="Unnamed",
                 style: dict = None,
                 stout=None,
                 tab_names: List[str] = None,
                 banner: BaseBanner = None,
                 navigation: BaseNavigation = None,
                 notebook: BaseNoteBook = None,
                 bind_func=None):
        super().__init__()
        self.title = title
        self.style = style

        self.root = tkinter.Tk()
        if bind_func:
            check_callable(bind_func=bind_func)
            self.root.bind_all("<1>", bind_func)
        if self.style:
            self.root.style = Style(**self.style)
        else:
            self.root.style = Style(**QStyle.default)
        self.root.style.configure('bg.TFrame', background=self.root.style.colors.inputbg)
        self.root.style.configure('bg.TLabel', background=self.root.style.colors.inputbg)
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(family=FONT, size=10)
        self.root.option_add("*Font", "TkDefaultFont")
        self.root.geometry("940x520")
        self.root.wm_resizable(False, False)
        self.root.title(self.title)

        # 初始化组件
        self.banner = banner if banner else BaseBanner(title=self.title)
        self.navigation = navigation if navigation else BaseNavigation()
        self.notebook = notebook if notebook else BaseNoteBook(tab_names=tab_names, stdout=stout)

        self.banner.build(self.root, self.get_global_info)
        self.navigation.build(self.root, self.get_global_info)
        self.notebook.build(self.root, self.get_global_info)

    @property
    def get_global_info(self):
        # ToDo 做个 global_info管理器，目前信息只从Notebook中流出
        return self.notebook.global_info

    def add_banner_tool(self, tool: BaseBarTool):
        """
        在程序最上方添加小组件
        :param tool: 继承于BaseBarTool的组件对象

        Example
            from qgui.banner_tools import GitHub
            q_gui = CreateQGUI()
            q_gui.add_banner_tool(GitHub())
        """
        self.banner.add_tool(tool)

    abt = add_banner_tool

    def add_notebook_tool(self, tool: BaseNotebookTool):
        """
        在程序中央功能区添加小组件
        :param tool: 继承于BaseNotebookTool的组件对象

        Example
            from qgui.notebook_tools import RunButton
            q_gui.add_notebook_tool(RunButton())
        """
        self.notebook.add_tool(tool)

    ant = add_notebook_tool

    def set_navigation_about(self,
                             author: str = "Unknow Author",
                             version: str = "N/A",
                             github_url: str = None,
                             bilibili_url: str = None,
                             blog_url: str = None,
                             other_info: List[str] = None):
        """
        设置左侧导航栏的程序基本信息
        :param author: 作者
        :param version: 版本号
        :param github_url: GitHub链接
        :param bilibili_url: bilibili链接
        :param blog_url: blog链接
        """
        self.navigation.add_about(author=author,
                                  version=version,
                                  github_url=github_url,
                                  bilibili_url=bilibili_url,
                                  blog_url=blog_url,
                                  other_info=other_info)

    sna = set_navigation_about

    def set_navigation_info(self,
                            title: str,
                            info: str):
        """
        设置左侧导航栏其他信息
        :param title: 标题
        :param info: 信息
        """
        self.navigation.add_info(title=title, info=info)

    sni = set_navigation_info

    def print_tool(self, tool: BaseNotebookTool):
        """
        在终端中打印组件
        :param tool: 继承于BaseNotebookTool的组件对象
        """
        self.notebook.print_tool(tool)

    def print_image(self, image):
        """
        在终端中打印图像
        :param image: 图像所在路径 or pillow图片对象
        """
        self.notebook.print_image(image)

    def run(self):
        """
        展示GUI界面
        """
        self.root.mainloop()


if __name__ == '__main__':
    from qgui.banner_tools import BaseBarTool
    from qgui.notebook_tools import BaseChooseFileTextButton

    _tmp = CreateQGUI()
    _tmp.add_banner_tool(BaseBarTool(lambda: print(0)))
    _tmp.add_notebook_tool(BaseChooseFileTextButton(lambda: print(1)))
    _tmp.set_navigation_about()
    _tmp.run()