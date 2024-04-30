import sys
import tkinter as tk
import tkinter.messagebox as msgbox

from log_writer import logger
import core
import config

def generate_plugin(description):
    response = core.askgpt(config.SYS_GEN, config.USR_GEN.replace("%DESCRIPTION%", description), config.GENERATE_MODEL)

    schem = core.text_to_schem(response)

    if schem is None:
        msgbox.showerror("Error", "Failed to generate the schematic. We recommend you to change the generating model to gpt-4-turbo-preview or other smarter models.")
        sys.exit(1)
    
    return schem

def generate_schematic():
    version = version_entry.get()
    name = name_entry.get()
    description = description_entry.get()

    core.initialize()

    logger(f"console: input version {version}")
    logger(f"console: input name {name}")
    logger(f"console: input description {description}")

    schem = generate_plugin(description)

    logger(f"console: Saving {name}.schem to generated/ folder.")
    version_tag = core.input_version_to_mcs_tag(version)

    while version_tag is None:
        msgbox.showerror("Error", "Invalid version number. Please retype the version number.")
        version = version_entry.get()
        version_tag = core.input_version_to_mcs_tag(version)

    schem.save("generated", name, version_tag)

    msgbox.showinfo("Success", "Generated. Get your schem file in folder generated.")

def Application():
    global version_entry, name_entry, description_entry

    window = tk.Tk()
    window.title("BuilderGPT")
    
    logo = tk.PhotoImage(file="logo.png")
    logo = logo.subsample(4)
    logo_label = tk.Label(window, image=logo)
    logo_label.pack()

    version_label = tk.Label(window, text="What's your minecraft version? (eg. 1.20.1):")
    version_label.pack()
    version_entry = tk.Entry(window)
    version_entry.pack()

    name_label = tk.Label(window, text="What's the name of your structure? It will be the name of the generated *.schem file:")
    name_label.pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    description_label = tk.Label(window, text="What kind of structure would you like to generate? Describe as clear as possible:")
    description_label.pack()
    description_entry = tk.Entry(window)
    description_entry.pack()

    generate_button = tk.Button(window, text="Generate", command=generate_schematic)
    generate_button.pack()

    window.mainloop()

if __name__ == "__main__":
    Application()
else:
    print("Error: Please run ui.py as the main program instead of importing it from another program.")