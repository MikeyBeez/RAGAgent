# modules/chat_manager.py

import json
import os
import sqlite3
import uuid
from datetime import datetime

class Chat:
    def __init__(self, title, messages=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.messages = messages or []

    def add_message(self, message):
        self.messages.append(message)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'messages': self.messages
        }

class ChatManager:
    def __init__(self, db_path='chats.db', chats_dir='chats'):
        self.db_path = db_path
        self.chats_dir = chats_dir
        os.makedirs(self.chats_dir, exist_ok=True)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TEXT
                )
            ''')

    def save_chat(self, chat):
        filename = f"{chat.id}.json"  # Use chat ID as filename
        file_path = os.path.join(self.chats_dir, filename)
        
        with open(file_path, 'w') as f:
            json.dump(chat.to_dict(), f, indent=2)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO chats (id, title, created_at)
                VALUES (?, ?, ?)
            ''', (chat.id, chat.title, datetime.now().isoformat()))

    def list_chats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, created_at FROM chats ORDER BY created_at DESC')
            return cursor.fetchall()

    def load_chat(self, chat_id):
        file_path = os.path.join(self.chats_dir, f"{chat_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                chat_data = json.load(f)
            chat = Chat(chat_data['title'], chat_data['messages'])
            chat.id = chat_data['id']
            return chat
        return None
