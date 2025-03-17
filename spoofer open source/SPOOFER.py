import ctypes
import os
import sys
import time
import winreg
import subprocess
import msvcrt  


def run_as_admin():
    if not is_admin():
        script = sys.argv[0]  
        params = " ".join(sys.argv[1:])  
        command = f'runas /user:Administrator "python {script} {params}"' 
        os.system(command)  
        sys.exit()  


def is_admin():
    try:
        return os.geteuid() == 0  
    except AttributeError:
        return os.name == 'nt' and ctypes.windll.shell32.IsUserAnAdmin() != 0


def print_green(text):
    print(f"\033[92m{text}\033[0m")


ascii_art = r"""
.../||   .|'''''| .|''''|, '||\   ||` '\\  //`               
 // ||   || .     ||    ||  ||\\  ||    \\//                  
//..||.. || |''|| ||    ||  || \\ ||     ||                   
    ||   ||    || ||    ||  ||  \\||     ||                   
    ||   `|....|' `|....|' .||   \||.   .||.                  
                                                             
.|'''|  '||'''|, .|''''|, .|''''|, '||''''| '||''''| '||'''|,
||       ||   || ||    || ||    ||  ||  .    ||   .   ||   ||
`|'''|,  ||...|' ||    || ||    ||  ||''|    ||'''|   ||...|'
 .   ||  ||      ||    || ||    ||  ||       ||       || \\  
 |...|' .||      `|....|' `|....|' .||.     .||....| .||  \\.
                                                             
'||  ||` '||      ||` |''||''| '||'''|.                      
 ||  ||   ||      ||     ||     ||   ||                      
 ||''||   ||  /\  ||     ||     ||   ||                      
 ||  ||    \\//\\//      ||     ||   ||                      
.||  ||.    \/  \/    |..||..| .||...|'                      
"""


def print_fading_text(text, delay=0.02):
    lines = text.split("\n")
    for line in lines:
        print_green(line)
        time.sleep(delay)  


def wait_for_keypress():
    print("\n🔹 Appuyez sur une touche pour continuer...")
    msvcrt.getch()  


print_fading_text(ascii_art, delay=0.02)
wait_for_keypress()


print("\n🔐 Entrez le mot de passe pour utiliser le Spoofer: ", end="", flush=True)
password = ""
correct_password = "HWIDSPOOF"

while True:
    char = msvcrt.getch()
    
    if char == b"\r":  
        break
    elif char == b"\b":  
        password = password[:-1]
        print("\b \b", end="", flush=True)  
    else:
        password += char.decode("ascii")  
        print("*", end="", flush=True)  

if password != correct_password:
    print("\n❌ Mot de passe incorrect. Fermeture du programme.")
    exit()

print("\n✅ Mot de passe correct ! Lancement du spoofer...")
wait_for_keypress()


def spoof_machine_guid():
    key = r"SOFTWARE\\Microsoft\\Cryptography"
    try:
        reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg, "MachineGuid", 0, winreg.REG_SZ, "1337-GUID-7364-ZKFJA")
        winreg.CloseKey(reg)
        print_green("[+] Machine GUID spoofed avec succès !")
    except Exception as e:
        print(f"[-] Erreur : {e}")


def spoof_mac_address(interface="Ethernet"):
    new_mac = "00:13:25:36:48:50"
    try:
        subprocess.run(f'netsh interface set interface "{interface}" admin=disable', shell=True)
        subprocess.run(f'reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\"4D36E972-E325-11CE-BFC1-08002BE10318"\\0001 /v NetworkAddress /t REG_SZ /d {new_mac} /f', shell=True)
        subprocess.run(f'netsh interface set interface "{interface}" admin=enable', shell=True)
        print_green("[+] Adresse MAC spoofed avec succès !")
    except Exception as e:
        print(f"[-] Erreur : {e}")


print_green("🔄 Spoofing en cours...")

spoof_machine_guid()


spoof_mac_address()


print_green("✅ Spoofing terminé ! Redémarrez votre PC pour appliquer les changements.")
wait_for_keypress()


run_as_admin()
