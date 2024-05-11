import sys
import uuid

from log_writer import logger
import core
import config

def generate_plugin(description):
    response = core.askgpt(config.SYS_GEN, config.USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL)

    schem = core.text_to_schem(response)

    retry_times = 0

    while schem is None and retry_times < 3:
        logger("Json synax error. Regenerating...")
        print("There's something wrong with the AI's reponse. Regenerating...")
        schem = generate_plugin(description)
        retry_times += 1
    
    if retry_times == 3:
        # If the AI generate the json response failed for 3 times, we will stop the program.
        logger("Too much errors. Failed to regenerate.")
        print("Failed to generate the schematic. We recommend you to change the generating model to gpt-4-turbo-preview or other smarter models.")
        
        print("""Options:
              1. Change the generating model to gpt-4-turbo-preview
              2. Exit the program""")
        option = input("Please choose an option: ")

        if option == "1":
            response = core.askgpt(config.SYS_GEN, config.USR_GEN.replace("%DESCRIPTION%", description), "gpt-4-turbo-preview")
            schem = core.text_to_schem(response)
            if schem is None:
                print("Failed to generate the schematic again. This may be caused by a bug in the program or the AI model. Please report this issue to github.com/CubeGPT/BuilderGPT/issues ")
        else:
            sys.exit(1)
    
    return schem

def get_schematic_advanced(description):
    print("(Advanced Mode) Generating programme...")
    programme = core.askgpt(config.BTR_DESC_SYS_GEN, config.BTR_DESC_USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL, disable_json_mode=True)

    print("(Advanced Mode) Generating image tag...")
    image_tag = core.askgpt(config.IMG_TAG_SYS_GEN, config.IMG_TAG_USR_GEN.replace("%PROGRAMME%", programme), config.GENERATE_MODEL, disable_json_mode=True)

    print("(Advanced Mode) Generating image...")
    tag = image_tag + ", minecraft)"
    image_url = core.ask_dall_e(tag)

    print("(Advanced Mode) Generating schematic...")
    response = core.askgpt(config.SYS_GEN_ADV, config.USR_GEN_ADV.replace("%DESCRIPTION%", description), config.VISION_MODEL, image_url=image_url)

    schem = core.text_to_schem(response)

    return schem

if __name__ == "__main__":
    core.initialize()

    print("Welcome to BuilderGPT, an open source, free, AI-powered Minecraft structure generator developed by BaimoQilin (@Zhou-Shilin). Don't forget to check out the config.yaml configuration file, you need to fill in the OpenAI API key.\n")

    # Get user inputs
    version = input("[0/3] What's your minecraft version? (eg. 1.20.1): ")
    description = input("[1/3] What kind of structure would you like to generate? Describe as clear as possible: ")
    render = input("[2/3] Do you want to render the structure? (y/n): ")

    # Log user inputs
    logger(f"console: input version {version}")
    logger(f"console: input description {description}")

    print("Generating...")

    if config.ADVANCED_MODE:
        print("Advanced mode is enabled. Generating a schematic with advanced features.")
        schem = get_schematic_advanced(description)
    else:
        schem = generate_plugin(description)
    
    print("Schematic generated. Generating schematic name...")
    raw_name = core.askgpt(config.SYS_GEN_NAME, config.USR_GEN_NAME.replace("%DESCRIPTION%", description), config.NAMING_MODEL, disable_json_mode=True)

    name = raw_name + "-" + str(uuid.uuid4())

    logger(f"console: Saving {name}.schem to generated/ folder.")
    version_tag = core.input_version_to_mcs_tag(version)

    # Check if the version is valid. If not, ask the user to retype the version number.
    while version_tag is None:
        print("Error: Invalid version number. Please retype the version number.")
        version = input("[re-0/0] What's your minecraft version? (eg. 1.20.1): ")
        version_tag = core.input_version_to_mcs_tag(version)

    schem.save("generated", name, version_tag)

    print(f"Generated with file name \"{name}.schem\". Get your schem file in folder generated.")

else:
    print("Error: Please run console.py as the main program instead of importing it from another program.")