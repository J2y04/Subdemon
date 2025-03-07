import argparse
import os
import requests
import time
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from colorama import Fore, init
rn = datetime.now().strftime("%D %H:%M:%S")
rnt = datetime.now().strftime("%H:%M:%S")

validate = URLValidator()

def config_args():
    parser = argparse.ArgumentParser(description="Subdemon - Subfindig Tool.")
    parser.add_argument("-d", help="Specify a URL to attack.")
    parser.add_argument("-w", help="Wordlist for Directory Brute-Force Attack.")
    parser.add_argument("--timeout", type=int, help="Specify a timeout of response Time from the Server(Default 2).")

    args = parser.parse_args()
    
    if not args.w:
        print("\n[-] No wordlist specified.")
        print("Quitting....")
        time.sleep(2)
        exit()
    if not args.d:
        print("\n[-] No URL specified.")
        print("Quitting....")
        time.sleep(1)
        exit()
    if not "https://" or "http://" in args.d:
        print(f"{Fore.YELLOW}[!]{Fore.RESET}")
        print("Quitting....")
        time.sleep(2)
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
        validate(args.d)
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
        print(f"{Fore.RED}[-]{Fore.RESET} Error occurred while reading the wordlist file {args.w}.") 
        quit()

    # Subfinding
    subdomain = None
    count = 0
    found = False
    print(f"[+] Enumaritng subdomains for {args.d}")
    for word in words:
        subdomain = f"{args.d}/{word}"
        
        try:
            #make the request and compare the status codes
            r = requests.get(subdomain, timeout=args.timeout if args.timeout else 2)
            if r.status_code in [200, 204, 202]:   
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}. Status Code: {r.status_code}. Note: Server replied with requested Content.")
                count += 1
                found = True
                if found == True:
                    with open(f"results.txt", "a") as file:
                        file.write(subdomain + "\n")
            elif r.status_code == 206:
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}. Status Code: {r.status_code}. Note: Server replied with parts of requested Content.")
                count += 1
                found = True
                if found == True:
                    with open(f"results.txt", "a") as file:
                        file.write(subdomain + "\n")
            elif r.status_code == 205:
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}. Status Code: {r.status_code}. Note: Server requested a Reset.")
                count += 1
                found = True
                if found == True:
                    with open(f"results.txt", "a") as file:
                        file.write(subdomain + "\n")
            elif r.status_code in [301, 308]:
                print(f"[{rnt}] {Fore.YELLOW}[!]{Fore.RESET} Subdomain moved permanently: {subdomain}. Status Code: {r.status_code}.")
            elif r.status_code == 302:
                print(f"[{rnt}] {Fore.GREEN}[+]{Fore.RESET} Subdomain Found: {subdomain}. Status Code: {r.status_code}. Note: URL was temporarily moved.")
                count += 1
                found = True
                if found == True:
                    with open(f"results.txt", "a") as file:
                        file.write(subdomain + "\n")
            elif r.status_code in [400, 404, 405, 406, 407, 409]:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Bad Request or URL not found.")
            elif r.status_code == 408:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Request Timed out.")
            elif r.status_code == 413:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Too large payload.")
            elif r.status_code == 410:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Deleted Ressource.")
            elif r.status_code == 414:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Too long URL.")
            elif r.status_code == 451:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code} Cause: Unavailable due to ilegal content.")
            else:
                print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}. Status Code: {r.status_code}")
        except requests.exceptions.RequestException as f:
            print(f"[{rnt}] {Fore.RED}[-]{Fore.RESET} Subdomain Not Found: {subdomain}")
        except Exception as e:
            print(f"[{rnt}] [-] An Error occurred: {e}")
            input("Press any key to exit...")
            quit()
    endmsg(args, count)

def endmsg(args, count):
    print(f"\n[+] Succesfully enumarated subdomains for {args.d}. Results saved in results.txt .")
    print(f"[+] Found {count} Subdomains.")
    print(f"[+] Successfully ended scan at {rn}")
    input("\nPress any key to exit...")
    quit()

if __name__ == "__main__":
    main()
    config_args()                                                                                                  