import os
import re

def getData():
    messages=getWhatsappData()
    return messages

def getWhatsappData():
    pattern = r"^\d{1,2}/\d{1,2}/\d{2,4},.*? - .*?: (.*)$"
    folder = "./data/whatsapp"
    chat = ""

    for file_name in os.listdir(folder):
        path = os.path.join(folder, file_name)
        if os.path.isfile(path) and file_name.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                chat += f.read() + "\n"

    messages = []
    for line in chat.splitlines():
        match = re.match(pattern, line)
        if match:
            text = match.group(1).strip()
            if text and not text.startswith('<Multimedia'):
                messages.append(text)
    return messages