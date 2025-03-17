import os
import random
import string
import customtkinter as ctk
import time
from datetime import datetime

LOG_FILE = "hwid_spoofer.log"

# script by .krns on discord 
def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def log_action(action):
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}\n")


def animate_status(text, emoji, color):
    for i in range(3):
        status_label.configure(text=f"{text}{'.' * i} {emoji}", text_color=color)
        root.update()
        time.sleep(0.3)
    status_label.configure(text=f"{text} {emoji}")


def spoof_hwid():
    new_hwid = generate_random_id()
    os.system(f'reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid /t REG_SZ /d "{new_hwid}" /f')
    log_action(f"HWID changé en {new_hwid}")
    animate_status("HWID modifié ! Redémarrage recommandé", "✅", "#00FF00")


def reset_hwid():
    os.system(r'reg delete HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid /f')
    log_action("HWID réinitialisé !")
    animate_status("HWID réinitialisé ! Redémarrage nécessaire", "⚠️", "#FFA500")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("HWID Spoofer")
root.geometry("400x300")

label = ctk.CTkLabel(root, text="💻 HWID Spoofer", font=("Arial", 18))
label.pack(pady=15)

spoof_button = ctk.CTkButton(root, text="🚀 Spoof HWID", fg_color="#1E90FF", command=spoof_hwid)
spoof_button.pack(pady=10)

reset_button = ctk.CTkButton(root, text="🔄 Reset HWID", fg_color="#FF4500", command=reset_hwid)
reset_button.pack(pady=10)

status_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
status_label.pack(pady=20)

root.mainloop()
