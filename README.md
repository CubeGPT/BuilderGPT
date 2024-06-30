<div align="center">
<img src="https://github.com/Zhou-Shilin/picx-images-hosting/blob/master/buildergpt-logo.jpeg?raw=true"/> 
<img src="https://img.shields.io/badge/Builder-GPT-blue">
<a href="https://github.com/CubeGPT/BuilderGPT/pulls"><img src="https://img.shields.io/badge/PRs-welcome-20BF20"></a>
<img src="https://img.shields.io/badge/License-Apache-red">
<a href="https://discord.gg/kTZtXw8s7r"><img src="https://img.shields.io/discord/1212765516532289587
"></a>
<!-- <a href="https://crowdin.com/project/bukkitgpt"><img src="https://img.shields.io/badge/i18n-Crowdin-darkblue"></a> -->
<!-- <p>English | <a href="https://github.com/CubeGPT/BukkitGPT/blob/master/README-zh_cn.md">简体中文</a></p> -->
<br>
<a href="https://discord.gg/kTZtXw8s7r">Join our discord</a>
<br/>
</div>

> [!NOTE]
> Developers and translators are welcome to join the CubeGPT Team!

## Introduction
> Give GPT your idea, AI generates customized Minecraft structures.

BuilderGPT is an open source, free, AI-powered Minecraft structure generator. It was developed for minecraft map makers. It can generate structures in `*.schem` format and users can import them via worldedit, etc.

# Showcase
![](https://github.com/Zhou-Shilin/picx-images-hosting/blob/master/img-mUATep311QjghtgbcihXCJwZ.png?raw=true)
![](https://github.com/Zhou-Shilin/picx-images-hosting/blob/master/Snipaste_2024-05-12_21-11-55.png?raw=true)

## GET YOUR FREE API KEY WITH GPT-4 ACCESS
We are pleased to announce that SEC-API is offering a free apikey for users of programs developed by CubeGPT!
This key has access to gpt-4-1106-preview and gpt-3.5-turbo-1106.

**Note that this key does not have access to models such as gpt-4-vision and expires at any time.**

Get the key from [here](https://github.com/orgs/CubeGPT/discussions/1). You can use it in BuilderGPT.

## Partner
[![](https://www.bisecthosting.com/partners/custom-banners/c37f58c7-c49b-414d-b53c-1a6e1b1cff71.webp)](https://bisecthosting.com/cubegpt)

## Features

- [x] Generate structures
- [x] Preview rendered schematic in-program
- [x] Export generated structures to `*.schem` files
- [ ] Export generated structures to `*.mcfunction` files
- [x] **Advanced Mode** (Use Stable Diffusion/DALL-E to generate the design image and let `gpt-4-vision` generate the struture base on it.)
- [ ] Edit structures

### Other projects of CubeGPT Team
- [x] Bukkit plugin generator. {*.jar} ([BukkitGPT](https://github.com/CubeGPT/BukkitGPT))
- [x] Structure generator. {*.schem} ([BuilderGPT](https://github.com/CubeGPT/BuilderGPT))
- [ ] Serverpack generator. {*.zip} (ServerpackGPT or ServerGPT, or..?)
- [ ] Have ideas or want to join our team? Send [us](mailto:admin@baimoqilin.top) an email!

## How it works

After the user enters a requirement, the program uses `gpt-4-preview` to expand the details of the requirement and generate a specific solution. The program then uses the generated solution to generate a drawing tag using `gpt-4-preview`, and then calls Stable Diffusion WebUI or DALL-E to generate a design using the generated tag. The generated schematic is then given to `gpt-4-vision-preview` along with the optimized requirements to generate a `json` containing the content of the structure, for example:

```json
{
    "materials": [
        "A: \"minecraft:air\"",
        "S: \"minecraft:stone\""
    ],
    "structures": [
        {
            "floor": 0,
            "structure": "SSSSSSSS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSSSSSSSS"
        },
        {
            "floor": 1,
            "structure": "SSGGGGSS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSSSSSSSS"
        },
        {
            "floor": 2,
            "structure": "SSGGGGSS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSSSSSSSS"
        },
        {
            "floor": 3,
            "structure": "SSSSSSSS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSAAAAAAS\nSSSSSSSS"
        },
        {
            "floor": 4,
            "structure": "SSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\nSSSSSSSS\n"
        }
    ]
}
```
The program then parses this `json` response. Then it uploads the image (headless) to cubical.xyz and downloads the rendered image from the site using `playwright`.

## Requirements

### Plan A. Windows/Linux (executable edition)

> [!WARNING]
> The version of the executable is still in the testing process. Plan B is recommended if possible.

Nothing. Just download the executable file and run it.

### Plan B. Python (Any operating systems; Recommend if possible)

You can use BukkitGPT on any device with [Python 3+](https://www.python.org/).  

And you need to install the depencies with this command:
```
pip install -r requirements.txt
```

## Quick Start

*(Make sure you have the [Python](https://www.python.org) environment installed on your computer)*

<!--
### Executable/UI
1. Download `windows-build.zip` or `linux-build.zip` from [the release page](https://https://github.com/CubeGPT/BuilderGPT/releases) and unzip it.
2. Edit `config.yaml`, fill in your OpenAI Apikey. If you don't know how, remember that [Google](https://www.google.com/) and [Bing](https://www.bing.com/) are always your best friends.
3. Run `ui.exe` (Windows) or `ui` (Linux), enter the description and let GPT generate the structure.
4. Find your structure in `/generated/<name>.schem`.
5. Import the file into the game via worldedit or other tools. (Google is your best friend~~)
-->

### Python/UI (RECOMMEND)
1. Download `Source Code.zip` from [the release page](https://https://github.com/CubeGPT/BuilderGPT/releases) and unzip it.
2. Edit `config.yaml`, fill in your OpenAI Apikey. If you don't know how, remember that [Google](https://www.google.com/) and [Bing](https://www.bing.com/) are always your best friends.
3. Run `ui.py` (bash `python ui.py`), enter the description and let GPT generate the structure.
4. Find your structure in `/generated/<name>.schem`.
5. Import the file into the game via worldedit or other tools. (Google is your best friend~~)

### Python/Console
1. Download `Source Code.zip` from [the release page]([https:///](https://github.com/CubeGPT/BuilderGPT/releases)) and unzip it.
2. Edit `config.yaml`, fill in your OpenAI Apikey. If you don't know how, remember that [Google](https://www.google.com/) and [Bing](https://www.bing.com/) are always your best friends.
3. Run `console.py` (bash `python console.py`), enter the description and let GPT generate the structure.
4. Find your structure in `/generated/<name>.schem`.
5. Import the file into the game via worldedit or other tools. (Google is your best friend~~)

## Contributing
If you like the project, you can give the project a star, or [submit an issue](https://github.com/CubeGPT/BuilderGPT/issues) or [pull request](https://github.com/CubeGPT/BuilderGPT/pulls) to help make it better.

## License
```
Copyright [2024] [CubeGPT Team]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
