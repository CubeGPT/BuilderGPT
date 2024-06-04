import time

# 导入CreateQGUI模块
from qgui import CreateQGUI, MessageBox
# 【可选】导入自定义导航栏按钮模块、GitHub导航栏模块
from qgui.banner_tools import BaseBarTool, GitHub, AIStudio
# 【可选】一次性导入所有的主界面工具模块
from qgui.notebook_tools import *
# 【可选】导入占位符
from qgui.manager import QStyle, HORIZONTAL


def click(args: dict):
    MessageBox.info("要开始啦~")
    # 证明一下自己被点到了
    print("你点到我啦~")
    # 通过ChooseFileTextButton(name="文件选择")中预先设置的name参数，使用get方法即可获取对应的输入框信息
    print("你选择的文件是：", args["文件选择"].get())
    # 当然也可以通过name参数来设置对应的内容，使用set方法即可完成设置
    print("保存位置修改为“快看，我被修改啦”", args["保存位置"].set("快看，我被修改啦"))
    # 即使没有指定name，我们照样可以拿到所有的小工具情况
    for arg, v_fun in args.items():
        print("自定义组件Name：", arg, "状态：", v_fun.get())

    # 若我们绑定了进度条，那么每当需要设置进度的时候，通过args["进度条"].set(当前进度)来进行设置吧，倒吸进度条也是可以哒
    for i in range(1, 101):
        time.sleep(0.01)
        args["进度条"].set(i)
        # 增加打印间隔
        if i % 20 == 0:
            print("当前进度", i)
    MessageBox.warning(text="给个评价吧亲~")
    # 也可以在终端中打印组件，顺便绑定用户调研函数
    q_gui.print_tool(RadioButton(["满意", "一般", "你好垃圾啊"], title="体验如何？", name="feedback", bind_func=feedback))
    # 甚至打印图片
    from qgui import RESOURCES_PATH
    q_gui.print_image(os.path.join(RESOURCES_PATH, "demo/panda.jpg"))


def feedback(args: dict):
    # 用户调研Callback
    info = args["feedback"].get()
    if info == "满意":
        print("么么哒")
    elif info == "一般":
        print("啊啊啊，告诉GT哪里没做好吧")
    else:
        print("以后漂流瓶见吧，拜拜！")


def bind_dir(args: dict):
    # 获取所选择文件所在的文件夹路径
    path = os.path.dirname(args["文件选择"].get())
    # 可以通过name参数来设置对应的内容，使用set方法即可完成设置
    args["保存位置"].set(path)
    print("保存位置已自动修改为：", path)


def go_to_first_page(args: dict):
    args["QGUI-BaseNoteBook"].set(0)


# 创建主界面
q_gui = CreateQGUI(title="一个新应用",  # 界面标题
                   tab_names=["主控制台", "选择按钮", "其他小工具"],  # 界面中心部分的分页标题 - 可不填
                   style=QStyle.default)  # 皮肤

# 在界面最上方添加一个按钮，链接到GitHub主页
q_gui.add_banner_tool(GitHub(url="https://github.com/QPT-Family/QGUI"))
# 也可以是AI Studio
q_gui.add_banner_tool(AIStudio(url="https://aistudio.baidu.com/aistudio/personalcenter/thirdview/29724"))
# 要不试试自定义Banner按钮，在大家点击它时触发刚刚定义的click函数，并向它传递其他组件的情况
q_gui.add_banner_tool(BaseBarTool(bind_func=click, name="一个新组件"))

# 在主界面部分添加一个文件选择工具吧，并在选择文件后自动变为文件所在的路径
q_gui.add_notebook_tool(ChooseFileTextButton(name="文件选择", bind_func=bind_dir))
# 再加个文件夹选择工具
q_gui.add_notebook_tool(ChooseDirTextButton(name="保存位置"))
# 当然也可以来个输入框
q_gui.add_notebook_tool(InputBox(name="我是个木有感情的输入框"))
# 想要加一个 进度条 和 运行按钮 而且俩要水平方向排列该如何做？
# 试试HorizontalToolsCombine，它可以接受一组工具并将其进行水平排列
# 这里我们也为RunButton绑定click函数
run_menu = HorizontalToolsCombine([Progressbar(name="进度条"),
                                   RunButton(bind_func=click)],
                                  text="试试HorizontalToolsCombine，它可以接受一组工具并将其进行水平排列")
q_gui.add_notebook_tool(run_menu)

# 第二页 - 复选框和单选框
# 使用VerticalFrameCombine可以将他们在垂直方向快速组合，它们会从左到右按顺序排列
combine_left = VerticalFrameCombine([CheckButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                     CheckToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                     CheckObviousToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                     ToggleButton(options=("开", 1))],
                                    tab_index=1,
                                    text="使用VerticalFrameCombine可以将他们在垂直方向快速组合，它们会从左到右按顺序排列")
q_gui.add_notebook_tool(combine_left)
# 设置title参数后会为其增加标题
combine_right = VerticalFrameCombine([RadioButton(["选择1", "选择2", "选择3"], tab_index=1),
                                      RadioToolButton(["选择1", "选择2", "选择3"], tab_index=1),
                                      RadioObviousToolButton(["选择1", "选择2", "选择3"], tab_index=1)],
                                     title="右侧的复选框")
q_gui.add_notebook_tool(combine_right)

# 第三页
q_gui.add_notebook_tool(Label(text="这只是个简单的Label组件", alignment=RIGHT + TOP, tab_index=2))
q_gui.add_notebook_tool(Slider(default=4, tab_index=2))
q_gui.add_notebook_tool(Combobox(options=["选择1", "选择2", "选择3"], tab_index=2))
q_gui.add_notebook_tool(BaseButton(bind_func=go_to_first_page, text="回到首页", tab_index=2))

# 左侧信息栏
# 简单加个简介
q_gui.set_navigation_about(author="GT",
                           version="0.0.1",
                           github_url="https://github.com/QPT-Family/QGUI",
                           other_info=["欢迎加入QPT！"])
# 也可以加一下其他信息
q_gui.set_navigation_info(title="随便写段话", info="除了QGUI，你还可以试试例如AgentQGUI这样同样简单的GUI框架")
print("小Tips：占位符可以被Print，不信你看HORIZONTAL的描述被打印了出来->", HORIZONTAL)

# 跑起来~切记！一定要放在程序末尾
q_gui.run()
