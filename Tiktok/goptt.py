import requests
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import random
import threading
from colorama import init, Fore, Back, Style

# Khởi tạo colorama
init()

# Constants
CURRENT_TIME = "2025-04-12 06:49:06"
CURRENT_USER = "anhcode"

class TikTokStats:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
        }
    
    def get_user_info(self, username):
        try:
            url = f'https://www.tiktok.com/api/user/detail/?uniqueId={username}&secUid=&lang=en'
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                user = data.get('userInfo', {})
                stats = user.get('stats', {})
                return {
                    'nickname': user.get('user', {}).get('nickname', ''),
                    'followers': stats.get('followerCount', 0),
                    'following': stats.get('followingCount', 0),
                    'likes': stats.get('heartCount', 0),
                    'videos': stats.get('videoCount', 0)
                }
            return None
        except:
            return None

    def get_video_info(self, video_id):
        try:
            url = f'https://www.tiktok.com/api/video/detail/?itemId={video_id}'
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                stats = data.get('itemInfo', {}).get('itemStruct', {}).get('stats', {})
                return {
                    'likes': stats.get('diggCount', 0),
                    'comments': stats.get('commentCount', 0),
                    'shares': stats.get('shareCount', 0),
                    'views': stats.get('playCount', 0)
                }
            return None
        except:
            return None

class Statistics:
    def __init__(self):
        self.follow_stats = {}
        self.like_stats = {}
        self.start_time = datetime.now()
        self.last_update = datetime.now()
        self.total_follows = 0
        self.total_likes = 0
        self.tiktok_stats = TikTokStats()
        self.lock = threading.Lock()

    def get_duration(self):
        duration = datetime.now() - self.start_time
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60
        return hours, minutes, seconds

    def update_follow(self, username):
        with self.lock:
            self.follow_stats[username] = self.follow_stats.get(username, 0) + 1
            self.total_follows += 1
            self.last_update = datetime.now()
            self.display_realtime_stats(username=username)
    def display_realtime_stats(self, username=None, video_url=None):
        """Hiển thị thống kê realtime với thông báo thành công"""
        clear_screen()
        print(f"Current Date and Time (UTC): {format_time()}")
        
        width = 70
        print(f"\n{Fore.CYAN}╔{'═' * (width-2)}╗")
        print(f"║{' ' * ((width-20)//2)}TIẾN TRÌNH XỬ LÝ{' ' * ((width-20)//2)}║")
        print(f"╠{'═' * (width-2)}╣")
        
        # Thông tin chung
        hours, minutes, seconds = self.get_duration()
        print(f"║  ⏱️ Thời gian chạy: {hours:02d}:{minutes:02d}:{seconds:02d}{' ' * (width-30)}║")
        print(f"║  👥 Tổng Follow: {self.total_follows} lần {' ' * (width-20)}║")
        print(f"║  💖 Tổng Like: {self.total_likes} lần{' ' * (width-18)}║")
        
        # Hiển thị thành công nếu có
        if username:
            print(f"║  ✨ Đã tăng follow thành công cho @{username}{' ' * (width-len(username)-35)}║")
        if video_url:
            short_url = video_url[:30] + "..." if len(video_url) > 30 else video_url
            print(f"║  ✨ Đã tăng like thành công cho video{' ' * (width-35)}║")
            print(f"║     {short_url}{' ' * (width-len(short_url)-5)}║")
        
        print(f"╠{'═' * (width-2)}╣")
        
        # Chi tiết Follow
        if self.follow_stats:
            for username, count in self.follow_stats.items():
                print(f"║  @{username}: {count} lần{' ' * (width-len(username)-15)}║")
        
        # Chi tiết Like
        if self.like_stats:
            for url, count in self.like_stats.items():
                short_url = url[:30] + "..." if len(url) > 30 else url
                print(f"║  {short_url}: {count} lần{' ' * (width-len(short_url)-10)}║")
        
        print(f"╚{'═' * (width-2)}╝{Style.RESET_ALL}")
    def update_like(self, video_url):
        with self.lock:
            self.like_stats[video_url] = self.like_stats.get(video_url, 0) + 1
            self.total_likes += 1
            self.last_update = datetime.now()
            username = video_url.split('@')[1].split('/')[0] if '@' in video_url else None
            self.display_realtime_stats(username=username, video_url=video_url)
    def display_stats(self):
        """Hiển thị thống kê tổng quan"""
        width = 70
        print(f"\n{Fore.CYAN}╔{'═' * (width-2)}╗")
        print(f"║{' ' * ((width-20)//2)}THỐNG KÊ TỔNG QUAN{' ' * ((width-20)//2)}║")
        print(f"╠{'═' * (width-2)}╣")
        
        # Thông tin chung
        hours, minutes, seconds = self.get_duration()
        print(f"║  ⏱️ Thời gian chạy: {hours:02d}:{minutes:02d}:{seconds:02d}{' ' * (width-30)}║")
        print(f"║  👥 Follow đã tăng cho : {self.total_follows}lần{' ' * (width-30)}")
        print(f"║  💖 Like đã tăng cho : {self.total_likes}lần{' ' * (width-28)}║")
        print(f"║  ⌛ Cập nhật cuối: {self.last_update.strftime('%H:%M:%S')}{' ' * (width-35)}║")
        
        print(f"╠{'═' * (width-2)}╣")
        
        # Chi tiết Follow
        if self.follow_stats:
            print("║  📊 CHI TIẾT FOLLOW:                                    ║")
            for username, count in self.follow_stats.items():
                print(f"║    @{username}: {count} lần{' ' * (width-len(username)-20)}║")
        
        # Chi tiết Like
        if self.like_stats:
            print("║  💝 CHI TIẾT LIKE:                                      ║")
            for url, count in self.like_stats.items():
                short_url = url[:30] + "..." if len(url) > 30 else url
                print(f"║    {short_url}: {count} lần{' ' * (width-len(short_url)-15)}║")
        
        print(f"╚{'═' * (width-2)}╝{Style.RESET_ALL}")
            
            
            
            
            
            
            
            
            
            
            
            
def get_session():
    """Khởi tạo session với animation loading"""
    headers = {
        'authority': 'tikfollowers.com',
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    
    try:
        clear_screen()
        print_banner()
        animate_loading("Đang kết nối đến server...", 2)
        
        session = requests.Session()
        response = session.get('https://tikfollowers.com', headers=headers, timeout=30)
        
        if response.status_code == 200:
            session.headers.update(headers)
            animate_success_message("✅ Kết nối thành công!")
            time.sleep(1)
            clear_screen()
            print_banner()
            return session
    except:
        pass
    return None
def show_processing_status(message, success=True):
    """Hiển thị trạng thái xử lý với hiệu ứng"""
    if success:
        print(f"\n{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[⌛] {message}{Style.RESET_ALL}")
def format_time():
    """Format thời gian hiện tại theo UTC"""
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
def show_real_time_stats(stats, current_task):
    """Hiển thị bảng thống kê realtime"""
    clear_screen()
    
    
    width = 70
    print(f"\n{Fore.CYAN}╔{'═' * (width-2)}╗")
    print(f"║{' ' * ((width-20)//2)}TIẾN TRÌNH XỬ LÝ{' ' * ((width-20)//2)}║")
    print(f"╠{'═' * (width-2)}╣")
    
    # Thông tin chi tiết
    hours, minutes, seconds = stats.get_duration()
    print(f"║  ⏱️ Thời gian chạy: {hours:02d}:{minutes:02d}:{seconds:02d}{' ' * (width-30)}║")
    print(f"║  👥 Tổng Follow đã tăng: {stats.total_follows} lần{' ' * (width-30)}║")
    print(f"║  💖 Tổng Like đã tăng: {stats.total_likes} lần{' ' * (width-28)}║")
    print(f"║  🔄 Trạng thái: {current_task}{' ' * (width-len(current_task)-15)}║")
    
    # Chi tiết Follow và Like nếu có
    if stats.follow_stats or stats.like_stats:
        print(f"╠{'═' * (width-2)}╣")
        if stats.follow_stats:
            for username, count in stats.follow_stats.items():
                print(f"║  @{username}: {count} lần{' ' * (width-len(username)-15)}║")
        if stats.like_stats:
            for url, count in stats.like_stats.items():
                short_url = url[:30] + "..." if len(url) > 30 else url
                print(f"║  {short_url}: {count} lần{' ' * (width-len(short_url)-10)}║")
    
    print(f"╚{'═' * (width-2)}╝{Style.RESET_ALL}")
def process_tasks(session, usernames, video_urls, stats):
    """Xử lý tasks theo trình tự"""
    # Xử lý Follow trước
    if usernames:
        animate_text("⚡ ĐANG XỬ LÝ FOLLOW...", Fore.CYAN)
        for username in usernames:
            show_real_time_stats(stats, f"Đang xử lý Follow: @{username}")
            try:
                result = buff_follow(session, username, stats)
                if result:
                    animate_success_message(f"✨ Đã tăng follow thành công cho @{username}")
                time.sleep(1)
            except Exception:
                continue

    # Sau đó xử lý Like
    if video_urls:
        animate_text("\n⚡ ĐANG XỬ LÝ LIKE...", Fore.MAGENTA)
        for url in video_urls:
            show_real_time_stats(stats, f"Đang xử lý Like: {url[:30]}...")
            try:
                result = buff_like(session, url, stats)
                if result:
                    animate_success_message(f"✨ Đã tăng like thành công cho video")
                time.sleep(1)
            except Exception:
                continue

    return True

def get_csrf_token(session, url):
    """Lấy CSRF token với loading animation"""
    try:
        sys.stdout.write(f"\r{Fore.CYAN}⌛ Đang lấy token...{Style.RESET_ALL}")
        sys.stdout.flush()
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        for line in response.text.split('\n'):
            if 'csrf_token' in line:
                csrf_token = line.split("csrf_token = '")[1].split("'")[0]
                print(f"\r{' ' * 50}\r", end="")
                return csrf_token
    except:
        print(f"\r{' ' * 50}\r", end="")
    return None

def buff_follow(session, username, stats):
    """Xử lý tăng follow với hiệu ứng và thông báo"""
    try:
        # Hiển thị đang lấy token
        sys.stdout.write(f"\r{Fore.CYAN}⌛ Đang lấy token...{Style.RESET_ALL}")
        sys.stdout.flush()
        
        csrf_token = get_csrf_token(session, 'https://tikfollowers.com/free-tiktok-followers')
        if not csrf_token:
            return False

        # Xóa dòng "Đang lấy token"
        print(f"\r{' ' * 50}\r", end="")

        data = {
            'type': 'follow',
            'q': f'@{username}' if not username.startswith('@') else username,
            'google_token': 't',
            'token': csrf_token
        }
        
        response = session.post(
            'https://tikfollowers.com/api/free',
            json=data,
            timeout=30
        )
        result = response.json()

        if result.get('success'):
            data_follow = result['data']
            send_data = {
                'google_token': 't',
                'token': csrf_token,
                'data': data_follow,
                'type': 'follow'
            }
            
            send_response = session.post(
                'https://tikfollowers.com/api/free/send',
                json=send_data,
                timeout=30
            )
            send_result = send_response.json()

            if send_result.get('success'):
                stats.update_follow(username)
                # Hiển thị thành công
                animate_success_message(f"✨ Đã tăng follow thành công cho @{username}")
                # Hiển thị thống kê realtime
                show_real_time_stats(stats, f"Follow thành công: @{username}")
                return True
            else:
                if 'wait' in send_result.get('message', '').lower():
                    wait_time = get_wait_time(send_result['message'])
                    print(f"\n{Fore.YELLOW}⏳ Cần đợi trước khi tiếp tục...{Style.RESET_ALL}")
                    for i in range(wait_time, 0, -1):
                        sys.stdout.write(f"\r{Fore.YELLOW}⌛ Đang chờ {i} giây...{Style.RESET_ALL}")
                        sys.stdout.flush()
                        time.sleep(1)
                    print(f"\r{' ' * 50}\r", end="")
                    return False
        return False
        
    except Exception as e:
        print(f"\r{' ' * 50}\r", end="")
        return False

def buff_like(session, video_url, stats):
    """Xử lý tăng like với hiệu ứng và thông báo"""
    try:
        # Hiển thị đang lấy token
        sys.stdout.write(f"\r{Fore.CYAN}⌛ Đang lấy token...{Style.RESET_ALL}")
        sys.stdout.flush()
        
        csrf_token = get_csrf_token(session, 'https://tikfollowers.com/free-tiktok-likes')
        if not csrf_token:
            return False

        # Xóa dòng "Đang lấy token"
        print(f"\r{' ' * 50}\r", end="")

        data = {
            'type': 'like',
            'q': video_url,
            'google_token': 't',
            'token': csrf_token
        }
        
        response = session.post(
            'https://tikfollowers.com/api/free',
            json=data,
            timeout=30
        )
        result = response.json()

        if result.get('success'):
            data_like = result['data']
            send_data = {
                'google_token': 't',
                'token': csrf_token,
                'data': data_like,
                'type': 'like'
            }
            
            send_response = session.post(
                'https://tikfollowers.com/api/free/send',
                json=send_data,
                timeout=30
            )
            send_result = send_response.json()

            if send_result.get('success'):
                stats.update_like(video_url)
                # Hiển thị thành công
                short_url = video_url[:40] + "..." if len(video_url) > 40 else video_url
                animate_success_message(f"✨ Đã tăng like thành công cho video: {short_url}")
                # Hiển thị thống kê realtime
                show_real_time_stats(stats, f"Like thành công: {short_url}")
                return True
            else:
                if 'wait' in send_result.get('message', '').lower():
                    wait_time = get_wait_time(send_result['message'])
                    print(f"\n{Fore.YELLOW}⏳ Cần đợi trước khi tiếp tục...{Style.RESET_ALL}")
                    for i in range(wait_time, 0, -1):
                        sys.stdout.write(f"\r{Fore.YELLOW}⌛ Đang chờ {i} giây...{Style.RESET_ALL}")
                        sys.stdout.flush()
                        time.sleep(1)
                    print(f"\r{' ' * 50}\r", end="")
                    return False
        return False
        
    except Exception as e:
        print(f"\r{' ' * 50}\r", end="")
        return False
def get_wait_time(message):
    """Lấy thời gian chờ từ message"""
    wait_time = 300  # Mặc định 5 phút
    try:
        if 'Minutes' in message:
            minutes = int(message.split(':')[1].split('Minutes')[0].strip())
            wait_time = minutes * 60
        elif 'Seconds' in message:
            wait_time = int(message.split(':')[1].split('Seconds')[0].strip())
    except:
        pass
    return wait_time

def get_usernames():
    """Nhập username với giao diện đẹp"""
    usernames = []
    count = 1
    
    box_width = 60
    print(f"\n{Fore.YELLOW}╔{'═' * (box_width-2)}╗")
    print(f"║{' ' * ((box_width-20)//2)}NHẬP USERNAME{' ' * ((box_width-20)//2)}║")
    print(f"╠{'═' * (box_width-2)}╣")
    print("║  • Nhập username TikTok (có thể có @ hoặc không)       ║")
    print("║  • Để trống và ấn Enter để kết thúc                    ║")
    print(f"╚{'═' * (box_width-2)}╝\n{Style.RESET_ALL}")
    
    while True:
        username = input(f"{Fore.CYAN}[{count}] ⪼ {Style.RESET_ALL}").strip()
        
        if username == "":
            if len(usernames) == 0:
                print(f"\n{Fore.RED}❌ Vui lòng nhập ít nhất một username!{Style.RESET_ALL}\n")
                continue
            break
            
        username = username.strip('@') if username.startswith('@') else username
        
        if username in usernames:
            print(f"\n{Fore.YELLOW}⚠️ Username này đã được thêm trước đó!{Style.RESET_ALL}\n")
            continue
            
        if len(username) < 2:
            print(f"\n{Fore.YELLOW}⚠️ Username quá ngắn!{Style.RESET_ALL}\n")
            continue
            
        usernames.append(username)
        print(f"\n{Fore.GREEN}✅ Đã thêm: @{username}{Style.RESET_ALL}\n")
        count += 1
    
    if usernames:
        show_input_summary("DANH SÁCH USERNAME ĐÃ NHẬP", usernames, "username")
    
    return usernames
def get_video_urls():
    """Nhập URL video với giao diện đẹp"""
    video_urls = []
    count = 1
    
    box_width = 60
    print(f"\n{Fore.YELLOW}╔{'═' * (box_width-2)}╗")
    print(f"║{' ' * ((box_width-20)//2)}NHẬP LINK VIDEO{' ' * ((box_width-20)//2)}║")
    print(f"╠{'═' * (box_width-2)}╣")
    print("║  • Nhập link video TikTok (https://www.tiktok.com/...) ║")
    print("║  • Để trống và ấn Enter để kết thúc                    ║")
    print(f"╚{'═' * (box_width-2)}╝\n{Style.RESET_ALL}")
    
    while True:
        url = input(f"{Fore.CYAN}[{count}] ⪼ {Style.RESET_ALL}").strip()
        
        if url == "":
            if len(video_urls) == 0:
                print(f"\n{Fore.RED}❌ Vui lòng nhập ít nhất một link video!{Style.RESET_ALL}\n")
                continue
            break
            
        if not url.startswith(('http://www.tiktok.com/', 'https://www.tiktok.com/', 'http://vt.tiktok.com/', 'https://vt.tiktok.com/')):
            print(f"\n{Fore.YELLOW}⚠️ Link video không hợp lệ! Vui lòng nhập link từ tiktok.com{Style.RESET_ALL}\n")
            continue
            
        if url in video_urls:
            print(f"\n{Fore.YELLOW}⚠️ Link video này đã được thêm trước đó!{Style.RESET_ALL}\n")
            continue
            
        video_urls.append(url)
        print(f"\n{Fore.GREEN}✅ Đã thêm video #{count}{Style.RESET_ALL}\n")
        count += 1
    
    if video_urls:
        show_input_summary("DANH SÁCH VIDEO ĐÃ NHẬP", video_urls, "video")
    
    return video_urls
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, color=Fore.MAGENTA, delay=0.03):
    """Hiệu ứng chữ chạy mượt mà"""
    print()
    for char in text:
        sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def animate_loading(text, duration=1):
    """Hiệu ứng loading với spinner"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f'\r{Fore.CYAN}{char} {text}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * 50 + "\r", end="")

def animate_success_message(text):
    """Hiệu ứng thông báo thành công"""
    print()
    for char in text:
        sys.stdout.write(f"{Fore.GREEN}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")


def show_input_summary(title, items, type="username"):
    """Hiển thị bảng tổng kết sau khi nhập"""
    clear_screen()
    print_banner()  # Hiển thị lại banner
    
    width = 70
    print(f"\n{Fore.CYAN}╔{'═' * (width-2)}╗")
    print(f"║{' ' * ((width-len(title))//2)}{title}{' ' * ((width-len(title))//2)}║")
    print(f"╠{'═' * (width-2)}╣")
    
    if type == "username":
        for i, item in enumerate(items, 1):
            print(f"║  {i}. @{item:<{width-7}}║")
    else:
        for i, item in enumerate(items, 1):
            short_url = item[:45] + "..." if len(item) > 45 else item
            print(f"║  {i}. {short_url:<{width-7}}║")
    
    print(f"╠{'═' * (width-2)}╣")
    print(f"║  📊 Tổng số: {len(items):<{width-13}}║")
    print(f"╚{'═' * (width-2)}╝{Style.RESET_ALL}")
    
    animate_success_message("✨ Đã nhập thành công! Bắt đầu tiến hành xử lý...")
    time.sleep(1)
def print_banner():
    """Banner đẹp với hiệu ứng màu sắc"""
    banner = f"""
\033[38;2;255;20;147m┏━━━❨❨★ ❩❩━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❨❨★ ❩❩━━━┓

\033[1;35m
███╗░░██╗██╗░░██╗░█████╗░████████╗
\033[1;31m\033[1m\033[1m████╗░██║██║░░██║██╔══██╗╚══██╔══╝
██╔██╗██║███████║███████║░░░██║░░░
\033[1;33m\033[1m██║╚████║██╔══██║██╔══██║░░░██║░░░
\033[1;31m\033[1m\033[1m██║░╚███║██║░░██║██║░░██║░░░██║░░░
╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░

\033[1;33m\033[1m░█████╗░███╗░░██╗██╗░░██╗
\033[1;31m\033[1m\033[1m██╔══██╗████╗░██║██║░░██║
\033[1;33m\033[1m███████║██╔██╗██║███████║
\033[1;33m\033[1m██╔══██║██║╚████║██╔══██║
\033[1;31m\033[1m\033[1m██║░░██║██║░╚███║██║░░██║
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝
\033[1;31m\033[1m\033[1m██████╗░███████╗
██╔══██╗╚════██║
\033[1;33m\033[1m██║░░██║░░███╔═╝
\033[1;31m\033[1m\033[1m██║░░██║██╔══╝░░
\033[1;33m\033[1m██████╔╝███████╗
╚═════╝░╚══════╝
\033[1;36m⭐️ DEVELOPED BY: \033[1;97mANHCODE
\033[1;36m⭐️ TELE   : \033[1;97mhttps://t.me/anhcodeclick
\033[1;36m⭐️ NHÓM       : \033[1;97mhttps://t.me/shareanhcode
\033[1;36m⭐️ WEBSITE    : \033[1;97mhttps://anhcode.click
\033[1;36m⭐️ VERSION    : \033[1;97m2.0.3 (Premium)
\033[1;36m⭐️ TIME       : \033[1;97m{CURRENT_TIME}
\033[1;36m⭐️ ADMIN      : \033[1;97m{CURRENT_USER}
\033[1;95m                  ╭─━━━━━━━━━━━━━━━━━━━━─╮
                  │   TOOL SIÊU VIP PRO  │
                  ╰─━━━━━━━━━━━━━━━━━━━━─╯
\033[38;2;255;20;147m┗━━━❨❨★ ❩❩━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❨❨★ ❩❩━━━┛
"""
    for line in banner.split('\n'):
        print(f"{Fore.MAGENTA}{line}{Style.RESET_ALL}")

def print_menu():
    """Menu với màu sắc và biểu tượng"""
    menu = """
\033[38;2;255;20;147m┏━━━❨❨★ ❩❩━━━━━━━━━━━ MENU CHÍNH ━━━━━━━━━━❨❨★ ❩❩━━━┓
\033[1;36m            ╭─━━━━━━━━━━━━━━━━━━━━─╮
            │    THÔNG TIN TOOL    │
            ╰─━━━━━━━━━━━━━━━━━━━━─╯
\033[1;36m     ╭─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
     │  \033[1;97m[1] 🚀 Tăng Follow TikTok             \033[1;36m│
     │  \033[1;97m[2] 💖 Tăng Like Video TikTok         \033[1;36m│
     │  \033[1;97m[3] 🌟 Chạy Cả Hai Chức Năng          \033[1;36m│
     │  \033[1;97m[4] ℹ️  Thông Tin Tool                 \033[1;36m│
     │  \033[1;97m[5] 📝 Hướng Dẫn Sử Dụng              \033[1;36m│
     │  \033[1;97m[6] 📊 Xem Thống Kê Hiện Tại          \033[1;36m│
     │  \033[1;97m[0] ❌ Thoát                          \033[1;36m│
     ╰─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

\033[38;2;255;20;147m┗━━━❨❨★ ❩❩━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❨❨★ ❩❩━━━┛\033[0m
"""
    print(f"{Fore.CYAN}{menu}{Style.RESET_ALL}")

def print_split_stats(stats):
    """Hiển thị thống kê chia đôi màn hình đẹp"""
    width = 100
    half_width = width // 2 - 2
    
    # Header
    print(f"\n{Fore.CYAN}╔" + "═" * (width-2) + "╗")
    print(f"║" + " " * ((width-20)//2) + f"{Fore.MAGENTA}✨ THỐNG KÊ HIỆN TẠI ✨{Fore.CYAN}" + " " * ((width-20)//2) + "║")
    print(f"╠" + "═" * (half_width) + "╦" + "═" * (half_width) + "╣")
    
    # Title
    print(f"║{Fore.WHITE} {'THEO DÕI FOLLOW':^{half_width}} {Fore.CYAN}║{Fore.WHITE} {'THEO DÕI LIKE':^{half_width}} {Fore.CYAN}║")
    print(f"╠" + "─" * (half_width) + "╬" + "─" * (half_width) + "╣")
    
    # Thông tin chung
    hours, minutes, seconds = stats.get_duration()
    print(f"║{Fore.WHITE} ⏱️ Thời gian: {hours:02d}:{minutes:02d}:{seconds:02d} {Fore.CYAN}║{Fore.WHITE} 📊 Tổng like: {stats.total_likes:>5} {Fore.CYAN}║".center(width))
    print(f"║{Fore.WHITE} 👥 Tổng follow: {stats.total_follows:>5} {Fore.CYAN}║{Fore.WHITE} ⌛ Cập nhật: {stats.last_update.strftime('%H:%M:%S')} {Fore.CYAN}║".center(width))
    
    # Separator
    print(f"╠" + "═" * (half_width) + "╬" + "═" * (half_width) + "╣")
    
    # Content
    follow_lines = [f"@{user}: {count} lần" for user, count in stats.follow_stats.items()]
    like_lines = [f"{url[:25]}....: {count} lần" for url, count in stats.like_stats.items()]
    
    max_lines = max(len(follow_lines), len(like_lines), 1)
    follow_lines.extend([''] * (max_lines - len(follow_lines)))
    like_lines.extend([''] * (max_lines - len(like_lines)))
    
    for f_line, l_line in zip(follow_lines, like_lines):
        print(f"║{Fore.WHITE} {f_line:<{half_width}} {Fore.CYAN}║{Fore.WHITE} {l_line:<{half_width}} {Fore.CYAN}║")
    
    # Footer
    print(f"╚" + "═" * (half_width) + "╩" + "═" * (half_width) + "╝{Style.RESET_ALL}")

def animate_success(message):
    """Hiệu ứng thông báo thành công"""
    colors = [Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    print("\n")
    for i, char in enumerate(message):
        color = colors[i % len(colors)]
        sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")

def show_info():
    """Hiển thị thông tin tool"""
    info = """
🔰 Tên Tool: TikTok Tool Premium
👨‍💻 Author: AnhCode
📅 Phát hành: xx/04/2025
🔄 Phiên bản: 2.0.3
💎 Loại: Premium
📊 Hỗ trợ: Theo dõi realtime
    """
    print_fancy_box(info, color=Fore.MAGENTA)
    input(f"{Fore.CYAN}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")

def show_tutorial():
    """Hiển thị hướng dẫn sử dụng"""
    tutorial = """
1. Chọn chức năng từ menu chính
2. Với tăng Follow:
   - Nhập username TikTok (không cần @)
   - Có thể nhập nhiều username
3. Với tăng Like:
   - Nhập link video TikTok
   - Có thể nhập nhiều video
4. Theo dõi thông tin realtime:
   - Số follow/like tăng
   - Thông tin tài khoản
   - Thông tin video
    """
    print_fancy_box(tutorial, color=Fore.CYAN)
    input(f"{Fore.MAGENTA}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")
def print_fancy_box(text, padding=1, color=Fore.CYAN):
    """In text trong khung viền đẹp"""
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 2 * padding
    
    print(f"{color}╔{'═' * width}╗{Style.RESET_ALL}")
    for line in lines:
        print(f"{color}║{' ' * padding}{line:<{width-2*padding}}{' ' * padding}║{Style.RESET_ALL}")
    print(f"{color}╚{'═' * width}╝{Style.RESET_ALL}")

def loading_animation():
    """Animation loading ban đầu"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(3):  # Lặp 3 lần
        for char in chars:
            sys.stdout.write(f'\r{Fore.CYAN}{char} Đang khởi động...{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * 50 + "\r", end="")

def print_progress(current, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """Thanh tiến trình đẹp"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{Fore.CYAN}{prefix} |{bar}| {percent}% {suffix}{Style.RESET_ALL}', end='\r')
    if current == total:
        print()
def start_animation():
    """Animation khởi động chương trình"""
    clear_screen()
    print("\n\n")
    animate_text("🌟 ĐANG KHỞI ĐỘNG TIKTOK TOOL SIÊU VIP CỦA ANHCODE 🌟", Fore.MAGENTA)
    print("\n")
    
    # Loading bar
    for i in range(101):
        print_progress(i, 100, prefix='Khởi động:', suffix='Hoàn tất', length=50)
        time.sleep(0.05)
    time.sleep(0.2)
    clear_screen()

def main():
    try:
        # Khởi tạo statistics
        stats = Statistics()
        
        # Animation khởi động
        start_animation()
        
        while True:
            clear_screen()
            print_banner()
            print_menu()
            
            choice = input(f"\n{Fore.MAGENTA}[?] Nhập lựa chọn của bạn: {Style.RESET_ALL}")
            
            if choice == '1':
                clear_screen()
                print_banner()
                animate_text("🚀 CHỨC NĂNG TĂNG FOLLOW TIKTOK", Fore.CYAN)
                
                session = get_session()
                if session:
                    usernames = get_usernames()
                    clear_screen()
                    # In thông tin thời gian và người dùng
                    print(f"Admin: {CURRENT_USER}{Style.RESET_ALL}")
                    # Chạy vô hạn
                    while True:
                        for username in usernames:
                            try:
                                buff_follow(session, username, stats)
                                # Đợi 3-5 giây giữa mỗi lần buff
                                time.sleep(random.uniform(3, 5))
                            except Exception as e:
                                print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
                                continue
            
            elif choice == '2':
                clear_screen()
                print_banner()
                animate_text("💖 CHỨC NĂNG TĂNG LIKE VIDEO TIKTOK", Fore.MAGENTA)
                
                session = get_session()
                if session:
                    video_urls = get_video_urls()
                    clear_screen()
                    # In thông tin thời gian và người dùng
                    print(f"Admin: {CURRENT_USER}{Style.RESET_ALL}")
                    # Chạy vô hạn
                    while True:
                        for url in video_urls:
                            try:
                                buff_like(session, url, stats)
                                # Đợi 3-5 giây giữa mỗi lần buff
                                time.sleep(random.uniform(3, 5))
                            except Exception as e:
                                print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
                                continue
            
            elif choice == '3':
                clear_screen()
                print_banner()
                animate_text("🌟 CHẠY CẢ HAI CHỨC NĂNG", Fore.YELLOW)
                
                session = get_session()
                if session:
                    usernames = get_usernames()
                    video_urls = get_video_urls()
                    clear_screen()
                    # In thông tin thời gian và người dùng
                    print(f"Admin: {CURRENT_USER}{Style.RESET_ALL}")
                    # Chạy vô hạn
                    while True:
                        # Xử lý Follow
                        for username in usernames:
                            try:
                                buff_follow(session, username, stats)
                                time.sleep(random.uniform(2, 4))
                            except Exception:
                                continue
                        
                        # Xử lý Like
                        for url in video_urls:
                            try:
                                buff_like(session, url, stats)
                                time.sleep(random.uniform(2, 4))
                            except Exception:
                                continue
            
            elif choice == '4':
                clear_screen()
                print_banner()
                show_info()
                continue
            
            elif choice == '5':
                clear_screen()
                print_banner()
                show_tutorial()
                continue
            
            elif choice == '6':
                clear_screen()
                print_banner()
                # In thông tin thời gian và người dùng
                print(f"Admin: {CURRENT_USER}{Style.RESET_ALL}")
                stats.display_stats()
                input(f"\n{Fore.CYAN}Nhấn Enter để quay lại menu chính...{Style.RESET_ALL}")
                continue
            
            elif choice == '0':
                clear_screen()
                print_banner()
                # In thông tin thời gian và người dùng
                print(f"Admin: {CURRENT_USER}{Style.RESET_ALL}")
                stats.display_stats()
                animate_text("🌟 Cảm ơn bạn đã sử dụng tool! Hẹn gặp lại 👋", Fore.MAGENTA)
                break
            
            else:
                animate_text("❌ Lựa chọn không hợp lệ!", Fore.RED)
                time.sleep(2)
                continue
                
    except KeyboardInterrupt:
        print("\n")
        animate_text("⚠️ Đã dừng chương trình theo yêu cầu.", Fore.YELLOW)
        stats.display_stats()
    except Exception as e:
        print("\n")
        animate_text(f"❌ Lỗi không mong muốn: {str(e)}", Fore.RED)
    finally:
        if 'session' in locals() and session:
            session.close()

if __name__ == '__main__':
    # Cập nhật thời gian và user hiện tại
    CURRENT_TIME = format_time()  # Sử dụng thời gian thực
    CURRENT_USER = "AnhCode"
    
    # Khởi chạy chương trình
    main()