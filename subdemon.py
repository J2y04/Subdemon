import argparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import time
from datetime import datetime
from colorama import Fore, init
import os

validate = URLValidator()

rn = datetime.now().strftime("%D %H:%M:%S")
rnt = datetime.now().strftime("%H:%M:%S")

def config_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Specify a URL to attack.")
    parser.add_argument("-w", help="Wordlist for Directory Brute-Force Attack.")

    args = parser.parse_args()
    
    if not args.w:
        print("\n[-] No wordlist specified.")
        print("Quitting....")
        time.sleep(2)
        exit()
    if not args.u:
        print("\n[-] No URL specified.")
        print("Quitting....")
        time.sleep(1)
        exit()

    subfind(args)
    

def main():
    banner()
    shii()

def banner():

    init(autoreset=True)

    # Define ASCII art
    ascii_art = r"""
                   __        __ 
       _______  __/ /_  ____/ /__  ____ ___  ____  ____      
      / ___/ / / / __ \/ __  / _ \/ __ `__ \/ __ \/ __ \     
     (__  ) /_/ / /_/ / /_/ /  __/ / / / / / /_/ / / / /     
    /____/\__,_/_.___/\__,_/\___/_/ /_/ /_/\____/_/ /_/      
    ═══════════════════════════════════════════════════
               SUBDEMON V.1 - Made by J2y04
    """

    def gradient_fade(text, start_color, end_color):
        lines = text.splitlines()
        steps = len(lines)
        r1, g1, b1 = start_color
        r2, g2, b2 = end_color
        for i, line in enumerate(lines):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            print(f"\033[38;2;{r};{g};{b}m{line}")
            time.sleep(0.05)      
    start_color = (0, 255, 255)  
    end_color = (0, 0, 139)      
    gradient_fade(ascii_art, start_color, end_color)

def shii():
    print(Fore.BLUE + '[INFO] ' + Fore.WHITE + 'DEV: J2y04')
    print(Fore.BLUE + '[INFO] ' + Fore.WHITE + 'CREDITS: https://github.com/J2y04')
    print(Fore.GREEN + '[STATUS] ' + Fore.WHITE + f'Started SUBDEMON V.1 at {rn}')
    print(Fore.GREEN + '[STATUS] ' + Fore.WHITE + f'Successfully Initialized.')
    

def subfind(args):
    try:
        validate(args.u)
        print("\nURL is valid <:)>...")
    except ValidationError:
        print("[-] Invalid URL quitting..")
        time.sleep(1)
        quit()
    words = []  
    try:
        with open(args.w, "r") as list:
            words = [word.strip() for word in list if word.strip()]
    except Exception:
        print(f"[-] Error occurred while reading the wordlist file {args.w}.") 
        quit()

    # Subfinding
    subdomain = None
    for word in words:
        subdomain = f"{args.u}/{word}"
        try:
            #request
            req = requests.get(subdomain, timeout=2)
            if req.status_code == 200:
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}")
            elif req.status_code == 204:
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}")
            else:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}")
        except requests.exceptions.RequestException:
            print(f"[-] An Error occurred while forming a request to {subdomain}.")
        except Exception as e:
            print(f"[{rnt}] [-] An Error occurred: {e}")
            input("Press any key to exit...")
            quit()
if __name__ == "__main__":
    main()
    config_args()                                                                                                  