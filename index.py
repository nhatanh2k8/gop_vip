# Các dòng import giữ nguyên như của bạn...
import threading, base64, os, time, re, json, random
from datetime import datetime, timedelta
from time import sleep, strftime
from bs4 import BeautifulSoup
import requests, socket, sys

try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    import requests, random, re
    from random import randint
    import requests, pystyle
    import socks
except:
    os.system("pip install faker")
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system('pip install requests && pip install bs4 && pip install pystyle')
    print('__Vui Lòng Chạy Lại Tool__')

from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
whiteb = "\033[1;39m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'
dev = "\033[1;39m[\033[1;31m×\033[1;39m]\033[1;39m"

def banner():
    banner = f"""
\033[1;34m╔═══════════╗
\033[1;36m║▇◤▔▔▔▔▔▔▔◥▇║
\033[1;36m║▇▏◥▇◣┊◢▇◤▕▇║
\033[1;36m║▇▏▃▆▅▎▅▆▃▕▇║
\033[1;36m║▇▏╱▔▕▎▔▔╲▕▇║
\033[1;36m║▇◣◣▃▅▎▅▃◢◢▇║
\033[1;36m║▇▇◣◥▅▅▅◤◢▇▇║
\033[1;36m║▇▇◣╲▇╱◢▇▇▇║
\033[1;36m║▇▇▇▇◣▇◢▇▇▇▇║
\033[1;34m╚═══════════╝
\033[1;97mTool By: \033[1;32mAnhhCode            \033[1;97mPhiên Bản: \033[1;32m4.0     
\033[97m════════════════════════════════════════════════  
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Youtube\033[1;31m  : \033[1;97m☞ \033[1;36mAnhCode\033[1;31m♔ \033[1;97m☜
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Facebook\033[1;31m : \033[1;97mhttps://www.facebook.com/profile.php?id=61570408533569
\033[1;97m[\033[1;91m❣\033[1;97m]\033[1;97m Telegram\033[1;31m : \033[1;97m☞\033[1;32mhttps://t.me/shareanhcode🔫\033[1;97m☜
\033[97m════════════════════════════════════════════════
"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush() 
        sleep(0.000001)

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    print("\033[1;37m╔══════════════════════╗         ")
    print("\033[1;37m║  \033[1;32mTool TikTok \033[1;37m║          ")
    print("\033[1;37m╚══════════════════════╝           ")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m1.1 \033[1;97m: \033[1;34mTool Gộp TikTok \033[1;32m[Online]")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m1.2 \033[1;97m: \033[1;34mTool Gộp TikTok (Zefoy)  \033[1;32m[Online]")
    print("\033[1;37m╔══════════════════════╗         ")
    print("\033[1;37m║  \033[1;32mTool Facebook \033[1;37m║          ")
    print("\033[1;37m╚══════════════════════╝           ")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m2.1 \033[1;97m: \033[1;34mTool Share Ảo Facebook \033[1;32m[Online]")
    print(f"\033[97m════════════════════════════════════════════════════════")
    print("\033[1;37m╔══════════════════════╗         ")
    print("\033[1;37m║  \033[1;32mTiện ích \033[1;37m║          ")
    print("\033[1;37m╚══════════════════════╝           ")
    print(f"\033[1;97m[\033[1;32m*\033[1;97m] \033[1;33m3.1 \033[1;97m: \033[1;34mTool Dec \033[1;32m[Online]")
    print(f"\033[97m════════════════════════════════════════════════════════")
    
    chon = input('\033[1;91m┌─╼\033[1;97m[\033[1;91m<\033[1;97m/\033[1;91m>\033[1;97m]--\033[1;91m>\033[1;97m Nhập lựa chọn \033[1;97m \n\033[1;91m└─╼\033[1;91m✈ \033[1;33m : ')
    print('\033[1;39m─────────────────────────────────────────────────────────── ')

    if chon == '1.1':
        exec(requests.get('https://raw.githubusercontent.com/nhatanh2k8/gop_vip/refs/heads/main/Tiktok/goptt.py').text)
    elif chon == '1.2':
        exec(requests.get('https://raw.githubusercontent.com/nhatanh2k8/gop_vip/refs/heads/main/Tiktok/he_enc.py').text)
    elif chon == '2.1':
        exec(requests.get('https://raw.githubusercontent.com/Anhcode2008/AnhhCode/refs/heads/main/TienIchFaceBook/share.py').text)
    elif chon == '3.1':
        exec(requests.get('https://raw.githubusercontent.com/nhatanh2k8/gop_vip/refs/heads/main/Tienich/xuatdec_enc.py').text)
    else:
        sys.exit("")
