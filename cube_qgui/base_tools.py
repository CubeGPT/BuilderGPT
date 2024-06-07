# Author: Acer Zhang
# Datetime:2021/9/21 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import threading
import traceback
import sys
from typing import Dict

import tkinter

from cube_qgui.manager import *

from log_writer import logger


def check_callable(bind_func):
    if bind_func and not hasattr(bind_func, "__call__"):
        if hasattr(bind_func, "__name__"):
            name = bind_func.__name__
        else:
            name = bind_func
        raise Exception(f"{name}的bind_func不能被调用，其至少需要具备__call__方法，建议在此传入函数/方法或自行构建具备__call__方法的对象。\n"
                        f"Example:\n"
                        f"    def xxx():\n"
                        f"        Do sth\n"
                        f"    MakeThisTool(bind_func=xxx)\n"
                        f"Error example:\n"
                        f"    def xxx():\n"
                        f"        Do sth\n"
                        f"    MakeThisTool(bind_func=xxx())")


def make_anchor(anchor):
    if anchor:
        r_anchor = str()
        if TOP in anchor:
            r_anchor = "n"
        if BOTTOM in anchor:
            r_anchor = "s"
        if LEFT in anchor:
            r_anchor += "w"
        if RIGHT in anchor:
            r_anchor += "e"
        return r_anchor
    else:
        return None


def make_side(side):
    if side:
        if side == TOP:
            side = "top"
        elif side == BOTTOM:
            side = "bottom"
        elif side == LEFT:
            side = "left"
        else:
            side = "right"
        return side
    else:
        return None


class ArgInfo:
    def __init__(self, name=None, set_func=None, get_func=None):
        if not name and (set_func or get_func):
            raise Exception(f"请设置{self.__class__.__name__}的name")
        if name:
            self.all_info = {name: self}
        else:
            self.all_info = dict()

        check_callable(set_func)
        check_callable(get_func)
        self.set_func = set_func
        self.get_func = get_func

    def set(self, *args, **kwargs):
        return self.set_func(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_func(*args, **kwargs)

    def get_info(self):
        return self.all_info

    def __add__(self, other):
        other_info = other.all_info
        if other_info:
            for info_name in other_info:
                if info_name in self.all_info:
                    self.all_info[f"{info_name}-QGUI-Conflict-Field-{len(self.all_info)}"] = other_info[info_name]
                else:
                    self.all_info[info_name] = other_info[info_name]
        return self

    def __getitem__(self, item):
        return self.all_info[item]


def select_var_dtype(dtype):
    if issubclass(dtype, int):
        return tkinter.IntVar
    elif issubclass(dtype, float):
        return tkinter.DoubleVar
    elif issubclass(dtype, str):
        return tkinter.StringVar
    elif issubclass(dtype, bool):
        return tkinter.BooleanVar


class BaseTool:
    """
    基础工具集，提供基础异步Callback
    1. 写Build，记得继承才会有self.master，继承时候传**kwargs
    2. 若需返回信息，请重写get_info方法->ArgInfo
    3. 如绑定func，需要封装Callback
    """

    def __init__(self,
                 bind_func=None,
                 name: str = None,
                 style: str = "primary",
                 async_run: bool = False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        check_callable(bind_func)
        self.bind_func = bind_func
        self.name = name
        self.style = style + "." if style else ""
        self.async_run = async_run
        # 控制并发模式
        self.concurrency_mode = concurrency_mode

        # 占位符
        self.global_info = None
        self.master = None

        # 重复点击的Flag
        self.async_run_event = threading.Event()
        self.thread_pool = list()

    def _callback(self, func, start_func=None, end_func=None):
        """
        支持同步和异步的Callback
        :param func: 函数对象
        :param start_func: 开始前的函数对象
        :param end_func: 结束后的函数对象
        """
        if func:
            if not self.async_run:
                def render():
                    if start_func:
                        start_func()
                    func(self.global_info.get_info())
                    if end_func:
                        end_func()
            else:
                def render():
                    # 若不允许并发则在启动时加Flag
                    if self.async_run_event.is_set():
                        if self.concurrency_mode == ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG:
                            return lambda: print("当前设置为禁止并发，请勿重复点击，因为点了也没用")
                    else:
                        self.async_run_event.set()

                    if start_func:
                        start_func()

                    def new_func(obj):
                        try:
                            func(obj)
                        except Exception as e:
                            print("-----ERROR MSG START-----")
                            print(traceback.print_exc())
                            print("-----ERROR MSG END-----")

                            # Record the error message to the log
                            logger(f"Error: {e}")
                        if end_func:
                            end_func()
                        # 清除Flag，此时按钮可以再次点击
                        self.async_run_event.clear()

                    t = threading.Thread(target=new_func, args=(self.global_info.get_info(),))
                    t.setDaemon(True)
                    t.start()

                    self.thread_pool.append(t)
            return render
        else:
            def none():
                pass

            return none

    def build(self, *args, **kwargs) -> tkinter.Frame:
        self.global_info = kwargs.get("global_info")
        self.master = kwargs.get("master")

    def get_arg_info(self) -> ArgInfo:
        return ArgInfo()


if __name__ == '__main__':
    n = ArgInfo(set_func=lambda: print("a"))
    a = ArgInfo("A", None, lambda: print("a"))
    b = ArgInfo("B", None, lambda: print("b"))
    c = ArgInfo("A", None, lambda: print("a"))
    n += a + b + c
    a.get()
    pass
