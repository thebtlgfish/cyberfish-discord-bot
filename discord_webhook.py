import os
import requests
import time
import threading
import dotenv
from dotenv import load_dotenv

load_dotenv()

CHECK_URL = "https://thebtlgfish.github.io"        
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
INTERVAL = 60

_running = False
_thread = None


def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def send_discord_webhook(webhook_url, message):
    data = {
        "content": message,
        "username": "Fish Blog Security Guard", #Username Of The Webhook Bot
        "avatar_url": "https://thebtlgfish.github.io/images/cat.jpeg" #Avatar of the Webhook Bot
    }
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print(f"Webhook sent: {message}")
    except requests.RequestException as e:
        print(f"Failed to send webhook: {e}")


def _monitor_loop():
    global _running
    print("[Monitor] Starting monitoring loop...")
    while _running:
        is_up = check_website(CHECK_URL)
        status_msg = f"Website {CHECK_URL} is {'UP' if is_up else 'DOWN'}"
        print(status_msg)
        send_discord_webhook(WEBHOOK_URL, status_msg)
        time.sleep(INTERVAL)
    print("[Monitor] Monitoring loop stopped.")


def start_monitor():
    global _running, _thread
    if _running:
        print("[Monitor] Already running.")
        return False
    _running = True
    _thread = threading.Thread(target=_monitor_loop, daemon=True)
    _thread.start()
    return True


def stop_monitor():
    """Stops the monitoring loop."""
    global _running
    if not _running:
        print("[Monitor] Not running.")
        return False
    _running = False
    return True


def main():
    start_monitor()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_monitor()
        print("Stopped by user.")


if __name__ == "__main__":
    main()
