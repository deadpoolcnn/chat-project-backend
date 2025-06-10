# Flask Encrypted Chat System

This project is a Flask-based encrypted chat system supporting user registration, login, friend management, and secure message transmission using RSA and AES encryption algorithms.

## Features
- User registration/login (RSA key pair generated automatically, public key uploaded to server)
- Friend management (add, delete, query friends)
- Encrypted message transmission (frontend uses AES to encrypt message content, encrypts AES key with friend's public key, signs message)
- Message storage and query (backend only stores ciphertext, does not decrypt)

## Project Structure
```
app.py                # Flask application entry point
models.py             # Database models (User, Message, Friend)
database.py           # Database initialization
routes/               # Routes (auth, friends, messages)
utils/                # Utility functions (crypto, decorators, etc.)
requirements.txt      # Dependency list
instance/chat.db      # SQLite database file
```

## Quick Start
1. Install dependencies:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start the service:
   ```sh
   python app.py
   ```
3. Access the API documentation or frontend page.

## Main Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- PyCryptodome

## Notes
- All encryption, decryption, and signature operations are recommended to be performed on the frontend. The backend only stores and forwards ciphertext.
- The database file chat.db is located in the instance directory by default.
- For detailed design, see `Flask加密聊天系统设计文档.md`.

---
If you have any questions, feel free to open an issue or contact the author.
