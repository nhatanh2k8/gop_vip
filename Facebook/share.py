
import sys 
import os 
os.system('clear') 
import requests 
import threading 
import time 
import json
from time import strftime 
from pystyle import Colorate, Colors, Write, Add, Center 

__Copyright__ = 'Anh Code✔️' '[1;91m[[1;92m●[1;91m][1;97m ➻❥'   

def banner(): 
    print(f'''  
[1;33m╔═══════════════════════════════════════════════╗
[1;33m║[1;35m
███╗░░██╗██╗░░██╗░█████╗░████████╗
████╗░██║██║░░██║██╔══██╗╚══██╔══╝
██╔██╗██║███████║███████║░░░██║░░░
██║╚████║██╔══██║██╔══██║░░░██║░░░
██║░╚███║██║░░██║██║░░██║░░░██║░░░
╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░

[1;33m[1m░█████╗░███╗░░██╗██╗░░██╗
██╔══██╗████╗░██║██║░░██║
███████║██╔██╗██║███████║
██╔══██║██║╚████║██╔══██║
██║░░██║██║░╚███║██║░░██║
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝
[1;31m[1m[1m██████╗░███████╗
██╔══██╗╚════██║
██║░░██║░░███╔═╝
██║░░██║██╔══╝░░
██████╔╝███████╗
╚═════╝░╚══════╝╠═══════════════════════════════════════════════╣
[1;33m║[1;34m▶ Nhóm Tele  : [1;35mhttps://t.me/shareanhcode          [1;33m║
[1;33m║[1;34m▶ Tele : [1;35mhttps://t.me/anhcode.click           [1;33m║
[1;33m║[1;34m▶ Zalo : [1;35mno                            [1;33m║
[1;33m║[1;34m▶ Mua Key Vip Cứ Liên Hệ Tele Nhé              [1;33m║
[1;33m║[1;34m▶ Nếu Có Lỗi Vui Lòng Báo Cho Facebook Nhé     [1;33m║
[1;33m╚═══════════════════════════════════════════════╝
[1;32m-------------------------------------------------''')

    t = Colorate.Horizontal(Colors.white_to_black, "- - - - - - - - - - - - - - - - - - - - - - - - -")
    print(t)

def clear(): 
    if(sys.platform.startswith('win')): 
        os.system('cls') 
    else: 
        os.system('clear') 

gome_token = [] 

def get_token(input_file): 
    for cookie in input_file: 
        header_ = { 
            'authority': 'business.facebook.com', 
            'accept': '*/*',
            'cookie': cookie, 
            'referer': 'https://www.facebook.com/' 
        } 
        try: 
            home_business = requests.get('https://business.facebook.com/content_management', headers=header_).text 
            token = home_business.split('EAAG')[1].split('","')[0] 
            cookie_token = f'{cookie}|EAAG{token}' 
            gome_token.append(cookie_token) 
        except: 
            pass 
    return gome_token 
 
def share(tach, id_share): 
    cookie = tach.split('|')[0] 
    token = tach.split('|')[1] 
    he = { 
        'accept': '*/*', 
        'cookie': cookie, 
        'host': 'graph.facebook.com' 
    } 
    try: 
        requests.post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published=0&access_token={token}', headers=he).json() 
    except: 
        pass 
     
def main_share(): 
    clear() 
    banner() 

    while True:
        file_name = input("[1;31m[[1;37m[1;31m] [1;37m=> [1m[38;5;51mNhập tên file chứa Cookies (.txt) hoặc 'exit' để thoát: [1;35m").strip()
        if file_name.lower() == "exit":
            print("[1;32m[!] Đã thoát tool.")
            sys.exit()
        if not file_name or not file_name.endswith(".txt") or not os.path.isfile(file_name):
            print("[1;31m[!] Tên file không hợp lệ hoặc không tồn tại. Vui lòng thử lại!")
            continue
        with open(file_name, "r") as f:
            input_file = f.read().split('\n')
        break

    id_share = input("[1;31m[[1;37m[1;31m] [1;37m=> [1m[38;5;51mNhập ID Cần Share: [1;35m") 
    delay = int(input("[1;31m[[1;37m[1;31m] [1;37m=> [1m[38;5;51mNhập Delay Share: [1;35m")) 
    total_share = int(input("[1;31m[[1;37m[1;31m] [1;37m=> [1m[38;5;51mBao Nhiêu Share Thì Dừng Tool: [1;35m")) 

    all = get_token(input_file) 
    total_live = len(all) 
    print(f'[1;31m────────────────────────────────────────────────────────────') 
    if total_live == 0: 
        sys.exit() 

    stt = 0 
    while True: 
        for tach in all: 
            stt = stt + 1 
            threa = threading.Thread(target=share, args=(tach, id_share)) 
            threa.start() 
            print(f'[1;91m[[1;33m{stt}[1;91m][1;31m ➤ [1;95mSHARE[1;31m ➤[1;36m THÀNH CÔNG[1;31m ➤ ID ➤[1;31m[1;93m {id_share} [1;31m➤ 
', end='
') 
            time.sleep(delay) 
        if stt == total_share: 
            break 

    gome_token.clear() 
    input('[38;5;245m[[1;32mSUCCESS[38;5;245m] [1;32mĐã Share Thành Công | Nhấn [Enter] Để Chạy Lại [0m[0m') 

while True: 
    try: 
        main_share() 
    except KeyboardInterrupt: 
        print('
[38;5;245m[[38;5;9m![38;5;245m] [38;5;9mThắc Mắc Ibox Fb[0m') 
        sys.exit()
