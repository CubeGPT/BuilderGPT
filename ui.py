from cube_qgui.__init__ import CreateQGUI
from cube_qgui.banner_tools import *
from cube_qgui.notebook_tools import *
from playwright.sync_api import Playwright, sync_playwright
from tkinter import filedialog
import os
import shutil
import uuid
import time
import threading

from log_writer import logger, get_log_filename
import config
import core
import browser

def get_schematic(description, progressbar):
    """
    Generate a schematic based on the given description.

    Args:
        description (str): The description of the schematic.

    Returns:
        mcschematic.MCSchematic: The generated schematic.
    """
    # Start the progress bar update in a separate thread
    progress_thread = threading.Thread(target=update_progress_bar, args=(progressbar, 0, 95, 0.75))
    progress_thread.start()

    if config.GIVE_GPT_BLOCK_ID_LIST:
        with open("block_id_list.txt", "r") as f:
            block_id_list = f.read()
        sys_gen = config.SYS_GEN + f"\n\nUsable Block ID List:\n{block_id_list}"
    else:
        sys_gen = config.SYS_GEN

    response = core.askgpt(sys_gen, config.USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL)

    # Wait for the progress thread to finish
    progress_thread.join()

    # Ensure progress reaches 80% once askgpt completes
    progressbar.set(95)

    # Wait for the progress thread to finish
    progress_thread.join()

    schem = core.text_to_schem(response)
    progressbar.set(100)

    return schem

def get_schematic_advanced(description, progressbar):
    """
    Generates a schematic using advanced mode.

    Args:
        description (str): The description of the schematic.

    Returns:
        mcschematic.MCSchematic: The generated schematic.
    """
    progressbar.set(10)
    print("(Advanced Mode) Generating programme...")
    programme = core.askgpt(config.BTR_DESC_SYS_GEN, config.BTR_DESC_USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL, disable_json_mode=True)
    progressbar.set(30)

    print("(Advanced Mode) Generating image tag...")
    image_tag = core.askgpt(config.IMG_TAG_SYS_GEN, config.IMG_TAG_USR_GEN.replace("%PROGRAMME%", programme), config.GENERATE_MODEL, disable_json_mode=True)
    progressbar.set(50)

    print("(Advanced Mode) Generating image...")
    tag = image_tag + ", minecraft)"
    image_url = core.ask_dall_e(tag)
    progressbar.set(60)

    print("(Advanced Mode) Generating schematic...")
    response = core.askgpt(config.SYS_GEN_ADV, config.USR_GEN_ADV.replace("%DESCRIPTION%", description), config.VISION_MODEL, image_url=image_url)
    progressbar.set(90)

    schem = core.text_to_schem(response)
    progressbar.set(100)

    return schem

def generate(args: dict):
    """
    Generate a schematic based on the provided arguments.

    Args:
        args (dict): A dictionary containing the arguments for generating the schematic.
            - "Description": The description of the schematic.
            - "Game Version": The version of the game.

    Returns:
        bool: True
    """
    description = args["Description"].get()
    game_version = args["Game Version"].get()

    progressbar = args["Generation Progress"]

    if config.ADVANCED_MODE:
        schem = get_schematic_advanced(description, progressbar)
    else:
        schem = get_schematic(description, progressbar)

    raw_name = core.askgpt(config.SYS_GEN_NAME, config.USR_GEN_NAME.replace("%DESCRIPTION%", description), config.NAMING_MODEL, disable_json_mode=True)

    name = raw_name + "-" + str(uuid.uuid4())

    version_tag = core.input_version_to_mcs_tag(game_version)

    schem.save("generated", name, version_tag)

    print("Schematic saved as " + name + ".schem")

    return True

def render(args: dict):
    """
    Renders a schematic file using the provided arguments.

    Args:
        args (dict): A dictionary containing the necessary arguments for rendering.

    Returns:
        bool: True
    """
    progress_bar = args["Rendering Progress"]

    progress_bar.set(0)
    print("Start rendering...")

    schematic_path = args["Schematic File Path"].get()

    print(f"Set schematic path to {schematic_path}.")

    try:
        os.remove("temp/waiting_for_upload.schem")
        os.remove("temp/screenshot.png")
    except FileNotFoundError:
        pass

    progress_bar.set(10)

    print("Copying schematic file...")
    shutil.copy(schematic_path, "temp/waiting_for_upload.schem")
    progress_bar.set(20)

    if args["Headless-Enable"].get() == 1:
        print("Headless mode enabled.")
        is_headless = True
    else:
        print("Headless mode disabled.")
        is_headless = False

    print("Rendering...")
    with sync_playwright() as playwright:
        browser.run(playwright, progress_bar, is_headless=is_headless)

    print("Rendering finished. Result:")
    root.print_image("temp/screenshot.png")

    progress_bar.set(100)

    return True

def export_log(args: dict):
    """
    Exports the log file.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    log_filename = get_log_filename() + ".log"

    filepath = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])

    shutil.copy(log_filename, filepath)

    MessageBox.info(f"Log file exported to {filepath}")

    return True

def update_progress_bar(progressbar, start, end, interval):
    current = start
    while current < end:
        time.sleep(interval)
        current += 1
        progressbar.set(current)
        if current >= end:
            break

def open_config(args: dict):
    """
    Opens the config file.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    os.system("notepad config.yaml")

    return True

def save_apply_config(args: dict):
    """
    Saves and applies the configuration.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    keys = ["API_KEY", "BASE_URL"]

    for key in keys:
        value = args[key].get()

        if key == "ADVANCED_MODE":
            value = True if value == 1 else False
        else:
            pass

        config.edit_config(key, value)

    config.load_config()

    args["DevTool_CONFIG_API_KEY_DISPLAY"].set(f"CONFIG.API_KEY = {config.API_KEY}")
    args["DevTools_CONFIG_BASE_URL_DISPLAY"].set(f"CONFIG.BASE_URL = {config.BASE_URL}")

    return True

def load_config(args: dict):
    """
    Loads the configuration.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    config.load_config()

    args["API_KEY"].set(config.API_KEY)
    args["BASE_URL"].set(config.BASE_URL)

    return True

def print_args(args: dict):
    """
    Prints the arguments.

    Args:
        args (dict): A dictionary containing the arguments.

    Returns:
        bool: Always True.
    """
    for arg, v_fun in args.items():
        print(f"Name: {arg}, Value: {v_fun.get()}")

    return True

def raise_error(args: dict):
    """
    Raises an error.

    Args:
        args (dict): A dictionary containing the arguments.
    """
    raise Exception("This is a test error.")

root = CreateQGUI(title="BuilderGPT",
                  tab_names=["Generate", "Render", "Settings", "DevTools"]
                  )

logger("Starting program.")

# Initialize Core
core.initialize()

# Banner
root.add_banner_tool(GitHub("https://github.com/CubeGPT/BuilderGPT"))
root.add_banner_tool(BaseBarTool(bind_func=export_log, name="Export Log"))

# Generate Page
root.add_notebook_tool(InputBox(name="Game Version", default="1.20.1", label_info="Game Version", tab_index=0))
root.add_notebook_tool(InputBox(name="Description", default="A simple house", label_info="Description", tab_index=0))

root.add_notebook_tool(Progressbar(name="Generation Progress", title="Progress", tab_index=0))
root.add_notebook_tool(RunButton(bind_func=generate, name="Generate", text="Generate", tab_index=0))

# Render Page
root.add_notebook_tool(ChooseFileTextButton(name="Schematic File Path", label_info="Schematic File", tab_index=1))
root.add_notebook_tool(Progressbar(name="Rendering Progress", title="Progress", tab_index=1))
render_button = HorizontalToolsCombine([
    ToggleButton(options=("Enable", 1), name="Headless", title="Headless",tab_index=1),
    RunButton(bind_func=render, name="Render", text="Render", tab_index=1)
])
root.add_notebook_tool(render_button)

# Settings Page
root.add_notebook_tool(InputBox(name="API_KEY", default=config.API_KEY, label_info="API Key", tab_index=2))
root.add_notebook_tool(InputBox(name="BASE_URL", default=config.BASE_URL, label_info="BASE URL", tab_index=2))

config_buttons = HorizontalToolsCombine([
     BaseButton(bind_func=save_apply_config, name="Save & Apply Config", text="Save & Apply", tab_index=2),
     BaseButton(bind_func=load_config, name="Load Config", text="Load Config", tab_index=2),
     BaseButton(bind_func=open_config, name="Open Config", text="Open Full Config", tab_index=2)
])
root.add_notebook_tool(config_buttons)

# DevTools Page
root.add_notebook_tool(Label(name="DevTool_DESCRIPTION", text="This is a testing page for developers. Ignore it if you are a normal user.", tab_index=3))
root.add_notebook_tool(Label(name="DevTool_CONFIG_API_KEY_DISPLAY", text=f"CONFIG.API_KEY = {config.API_KEY}", tab_index=3))
root.add_notebook_tool(Label(name="DevTools_CONFIG_BASE_URL_DISPLAY", text=f"CONFIG.BASE_URL = {config.BASE_URL}", tab_index=3))
root.add_notebook_tool(RunButton(bind_func=print_args, name="Print Args", text="Print Args", tab_index=3))
root.add_notebook_tool(RunButton(bind_func=raise_error, name="Raise Error", text="Raise Error", tab_index=3))

# Sidebar
root.set_navigation_about(author="CubeGPT Team",
                              version=config.VERSION_NUMBER,
                              github_url="https://github.com/CubeGPT/BuilderGPT",
                              other_info=["Morden UI Test"])



# Run
root.run()