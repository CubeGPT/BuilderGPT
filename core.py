from openai import OpenAI
import mcschematic
import sys
import json
import locale

from log_writer import logger
import config

def initialize():
    """
    Initializes the software.

    This function logs the software launch, including the version number and platform.

    Args:
        None

    Returns:
        None
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    logger(f"Launch. Software version {config.VERSION_NUMBER}, platform {sys.platform}")

def askgpt(system_prompt: str, user_prompt: str, model_name: str, disable_json_mode: bool = False, image_url: str = None):
    """
    Interacts with ChatGPT using the specified prompts.

    Args:
        system_prompt (str): The system prompt.
        user_prompt (str): The user prompt.
        model_name (str): The model name to use.
        disable_json_mode (bool): Whether to disable JSON mode.

    Returns:
        str: The response from ChatGPT.
    """
    if image_url is not None and config.USE_DIFFERENT_APIKEY_FOR_VISION_MODEL:
        logger("Using different API key for vision model.")
        client = OpenAI(api_key=config.VISION_API_KEY, base_url=config.VISION_BASE_URL)
    else:
        client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

    logger("Initialized the OpenAI client.")

    # Define the messages for the conversation
    if image_url is not None:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]


    logger(f"askgpt: system {system_prompt}")
    logger(f"askgpt: user {user_prompt}")

    # Create a chat completion
    if disable_json_mode or config.FORCE_DISABLE_JSON_MODE:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            timeout=120
        )
    else:
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=messages,
            timeout=120
        )

    logger(f"askgpt: response {response}")

    # Extract the assistant's reply
    assistant_reply = response.choices[0].message.content
    logger(f"askgpt: extracted reply {assistant_reply}")
    return assistant_reply

def ask_dall_e(description: str):
    """
    Generates a design image using the DALL-E API.

    Args:
        description (str): The prompt or description for generating the image.

    Returns:
        str: The URL of the generated image.
    """
    if config.USE_DIFFERENT_APIKEY_FOR_DALLE_MODEL:
        client = OpenAI(api_key=config.DALLE_API_KEY, base_url=config.DALLE_BASE_URL)
    else:
        client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

    logger("ask_dall_e: Generating design image using DALL-E API.")

    response = client.images.generate(
        model=config.IMAGE_GENERATION_MODEL,
        prompt=description,
        size=config.IMAGE_SIZE,
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    logger(f"ask_dall_e: Generated image URL {image_url}")

    return image_url

def text_to_schem(text: str):
    """
    Converts a JSON string to a Minecraft schematic.

    Args:
        text (str): The JSON string to convert.
        
    Returns:
        mcschematic.MCSchematic: The Minecraft schematic.
    
    """
    try:
        data = json.loads(text)
        logger(f"text_to_command: loaded JSON data {data}")
        schematic = mcschematic.MCSchematic()

        for structure in data["structures"]:
            block_id = structure["block"]
            x = structure["x"]
            y = structure["y"]
            z = structure["z"]

            if structure["type"] == "fill":
                to_x = structure["toX"]
                to_y = structure["toY"]
                to_z = structure["toZ"]

                for x in range(x, to_x + 1):
                    for y in range(y, to_y + 1):
                        for z in range(z, to_z + 1):
                            schematic.setBlock((x, y, z), block_id)

            else:
                schematic.setBlock((x, y, z), block_id)

        return schematic
    
    except (json.decoder.JSONDecodeError, KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
        logger(f"text_to_command: failed to load JSON data. Error message: {e}")

        if config.DEBUG_MODE:
            raise e
        
        return None

def input_version_to_mcs_tag(input_version):
    """
    Converts an input version string to the corresponding MCSchematic tag.

    Args:
        input_version (str): The input version string in the format "X.Y.Z".

    Returns:
        str: The MCSchematic tag corresponding to the input version.

    Example:
        >>> input_version_to_mcs_tag("1.20.1")
        'JE_1_20_1'
    """
    try:
        version = input_version.split(".")
        result = getattr(mcschematic.Version, f"JE_{version[0]}_{version[1]}_{version[2]}")
    except (AttributeError, IndexError) as e:
        logger(f"input_version_to_mcs_tag: failed to convert version {input_version}; {e}")
        return None
    return result

if __name__ == "__main__":
    print("This script is not meant to be run directly. Please run console.py instead.")