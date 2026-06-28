# Ukraine Alert Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org) [![Pyrogram](https://img.shields.io/badge/latest-pyrogram-orange)](https://docs.pyrogram.org/) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A Telegram bot built with Pyrogram. The bot was created around 2023, with the aim of notifying residents of Ukraine about missile attacks in the regions of Ukraine.

---

## ⚠️ Archived / Discontinued

This project is **no longer maintained** and has been **shut down** due to the unavailability of the underlying service it relied on.

The source code remains available for reference and educational purposes only. No further updates, bug fixes, or support will be provided.

---

## 📋 Features

- `/start` — welcome message
- `/bash` — terminal management directly via telegram messages
- Admin-only commands
- Async scheduler
- Auto updating map from alerts.com.ua
- Language exported to JSON

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language |
| Pyrogram | Telegram MTProto framework |
| python-dotenv | Environment config |
| pillow | Images |

---

## 🚀 Quick Start

```bash

git clone https://github.com/ma3rd-nepon/ua-alert-bot.git

cd ua-alert-bot

pip install -r requirements.txt

cp .env_example .env # Fill in API_ID, API_HASH, BOT_TOKEN in .env

python src/main.py

```

## 📁 Project Structure

```
├── assets/       
│   └── map.png                 # Country map, with marked areas under attack
├── src/
│   ├── main.py                 # Entry point
│   └── utils/
│        └── utils.py           # Some Utilities
├── .env_example                # Example of .env file
├── LICENSE
├── README.md
└── requirements.txt            # Project Dependencies
```

📄 License
MIT © mread-bot, 2025

See LICENSE for full text.
