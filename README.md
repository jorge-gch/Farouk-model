<p align="center">
  <img src="static/images/icons/icon_farouk.svg" alt="farouk icon" style="max-width: 200px; width: 100%;">
</p>

# FAROUK MODEL

A system designed to process and analyze WhatsApp chats using Python.

---

## How to Run the App

Below are the instructions for **Windows** and **Ubuntu/Linux**. Just follow the steps, set up the data folder, and run the project.

---

# Windows

### 1. Install Python 3.10+

Download it from the official website. Make sure to check **"Add to PATH"** during installation.

### 2. Create the virtual environment

```powershell
python -m venv env
```

### 3. Activate the virtual environment

```powershell
env\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Prepare the data folder

Inside the `data/` folder, create a folder named **whatsapp/**.
Place all your exported WhatsApp chat files there.

### 6. Run the application

```powershell
python main.py
```

---

# Ubuntu / Linux

### 1. Install virtualenv (if needed)

```bash
pip install virtualenv
```

### 2. Create the virtual environment

```bash
python3 -m venv env
```

### 3. Activate the environment

```bash
source env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the data directory

Inside `data/`, create the folder structure:

```
data/
  └── whatsapp/
```

Put all your WhatsApp chat files inside the `whatsapp/` folder.

### 6. Run the app

```bash
python3 main.py
```
