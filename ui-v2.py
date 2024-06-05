from cube_qgui.__init__ import CreateQGUI
from cube_qgui.banner_tools import *
from cube_qgui.notebook_tools import *
from playwright.sync_api import Playwright, sync_playwright
import os
import shutil
import uuid

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
    progressbar.set(20)

    response = core.askgpt(config.SYS_GEN, config.USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL)
    progressbar.set(80)

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

    print("Rendering...")
    with sync_playwright() as playwright:
        browser.run(playwright, progress_bar)

    print("Rendering finished. Result:")
    root.print_image("temp/screenshot.png")

    progress_bar.set(100)

    return True

def open_config(args: dict):
    """
    Opens the config file.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    os.system("notepad config.py")

    return True

root = CreateQGUI(title="BuilderGPT",
                  tab_names=["Generate", "Render", "Settings"]
                  )

# Initialize Core
core.initialize()

# Banner
root.add_banner_tool(GitHub("https://github.com/CubeGPT/BuilderGPT"))

# Generate Page
root.add_notebook_tool(InputBox(name="Game Version", default="1.20.1", label_info="Game Version", tab_index=0))
root.add_notebook_tool(InputBox(name="Description", default="A simple house", label_info="Description", tab_index=0))

root.add_notebook_tool(Progressbar(name="Generation Progress", title="Progress", tab_index=0))
root.add_notebook_tool(RunButton(generate, "Generate", tab_index=0))

# Render Page
root.add_notebook_tool(ChooseFileTextButton(name="Schematic File Path", label_info="Schematic File", tab_index=1))
root.add_notebook_tool(Progressbar(name="Rendering Progress", title="Progress", tab_index=1))
root.add_notebook_tool(RunButton(render, "Render", tab_index=1))

# Settings Page
root.add_notebook_tool(RunButton(open_config, "Open Config", "Open Config", tab_index=2))

# Sidebar
root.set_navigation_about(author="CubeGPT Team",
                              version=config.VERSION_NUMBER,
                              github_url="https://github.com/CubeGPT/BuilderGPT",
                              other_info=["Morden UI Test"])



# Run
root.run()