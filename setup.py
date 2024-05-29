from cx_Freeze import setup, Executable

import config

files = [
    "browser.py",
    "config.py",
    "config.yaml",
    "console.py",
    "core.py",
    "LICENSE",
    "log_writer.py",
    "logo.png",
    "README.md",
    "requirements.txt",
    "ui.py"
]

setup(name='BuilderGPT',
      version=config.VERSION_NUMBER,
      maintainer="CubeGPT Team",
      maintainer_email="admin@cubegpt.org",
      url="https://github.com/CubeGPT/BuilderGPT",
      license="Apache License 2.0",
      description='An open source, free, AI-powered Minecraft structure generator developed by CubeGPT.',
      executables=[Executable('ui.py', base="gui")],
      options={
          "build_exe": {
              "include_files": files,
          }
      })