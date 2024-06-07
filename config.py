import yaml
from log_writer import logger

with open("config.yaml", "r") as conf:
    config_content = yaml.safe_load(conf)
    for key, value in config_content.items():
        if key == "CODING_MODEL" and value == "gpt-4":
            globals()[key] = "gpt-4-turbo-preview" # Force using gpt-4-turbo-preview if the user set the CODING_MODEL to gpt-4. Because gpt-4 is not longer supports json modes.
        globals()[key] = value
        logger(f"config: {key} -> {value}")

def edit_config(key, value):
    """
    Edits the config file.

    Args:
        key (str): The key to edit.
        value (str): The value to set.

    Returns:
        bool: True
    """

    with open("config.yaml", "r") as conf:
        config_content = conf.readlines()
    
    with open("config.yaml", "w") as conf:
        for line in config_content:
            if line.startswith(key):
                if value == True:
                    write_value = "True"
                elif value == False:
                    write_value = "False"
                else:
                    write_value = f"\"{value}\""
                if "#" in line:
                    conf.write(f"{key}: {write_value} # {line.split('#')[1]}\n")
                else:
                    conf.write(f"{key}: {write_value}\n")
            else:
                conf.write(line)

    return True