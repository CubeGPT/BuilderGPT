<div align="center">
<img src="https://github.com/Zhou-Shilin/picx-images-hosting/blob/master/buildergpt-logo.jpeg?raw=true"/> 
<img src="https://img.shields.io/badge/Builder-GPT-blue">
<a href="https://github.com/CubeGPT/BuilderGPT/pulls"><img src="https://img.shields.io/badge/PRs-welcome-20BF20"></a>
<img src="https://img.shields.io/badge/License-Apache-red">
<a href="https://crowdin.com/project/bukkitgpt"><img src="https://img.shields.io/badge/i18n-Crowdin-darkblue"></a>
<!-- <p>English | <a href="https://github.com/CubeGPT/BukkitGPT/blob/master/README-zh_cn.md">简体中文</a></p> -->
<br/>
</div>

> [!NOTE]
> Developers and translators are welcome to join the CubeGPT Team!

## Introduction
> Give GPT your idea, AI generates customized Minecraft structures.

BuilderGPT is an open source, free, AI-powered Minecraft structure generator. It was developed for minecraft map makers. It can generate structures in `*.schem` format and users can import them via worldedit, etc.

## Partner
[![](https://www.bisecthosting.com/partners/custom-banners/c37f58c7-c49b-414d-b53c-1a6e1b1cff71.webp)](https://bisecthosting.com/cubegpt)

## Features

- [x] Generate structures
- [x] Export generated structures to `*.schem` files
- [ ] Export generated structures to OOC commands
- [ ] Edit structures

### Other projects of CubeGPT Team
- [x] Bukkit plugin generator. {*.jar} ([BukkitGPT](https://github.com/CubeGPT/BukkitGPT))
- [x] Structure generator. {*.schem} ([BuilderGPT](https://github.com/CubeGPT/BuilderGPT))
- [ ] Serverpack generator. {*.zip} (ServerpackGPT or ServerGPT, or..?)
- [ ] Have ideas or want to join our team? Send [us](mailto:admin@baimoqilin.top) an email!

## How it works

After the user enters a requirement, the program causes `gpt-4-preview` to generate a `json` containing the content of the structure, for example:
```json
{
    "materials": [
            "A": "minecraft:air",
            "S": "minecraft:stone",
            "G": "minecraft:glass"
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
The program then parses this `json` response and generates a `*.schem` file for the user to import the structure into the game.

## Requirements
You can use BukkitGPT on any device with [Python 3+](https://www.python.org/).  

And you need to install this package:
```
pip install openai
```

## Quick Start

*(Make sure you have the [Python](https://www.python.org) environment installed on your computer)*

### Console
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
