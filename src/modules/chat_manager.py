# modules/chat_manager.py

import json
import os
import sqlite3
from datetime import datetime
import uuid

class Chat:
    def __init__(self, title, messages=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.creation_time = datetime.now().isoformat()
        self.messages = messages or []

    def add_message(self, message):
        self.messages.append(message)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'creation_time': self.creation_time,
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
                    creation_time TEXT,
                    filename TEXT
                )
            ''')

    def save_chat(self, chat):
        filename = f"{chat.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = os.path.join(self.chats_dir, filename)
        
        with open(file_path, 'w') as f:
            json.dump(chat.to_dict(), f, indent=2)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO chats (id, title, creation_time, filename)
                VALUES (?, ?, ?, ?)
            ''', (chat.id, chat.title, chat.creation_time, filename))

        return chat.id

    def list_chats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, creation_time FROM chats ORDER BY creation_time DESC')
            return cursor.fetchall()

    def load_chat(self, chat_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT filename FROM chats WHERE id = ?', (chat_id,))
            result = cursor.fetchone()
            if result:
                filename = result[0]
                file_path = os.path.join(self.chats_dir, filename)
                with open(file_path, 'r') as f:
                    chat_data = json.load(f)
                chat = Chat(chat_data['title'], chat_data['messages'])
                chat.id = chat_data['id']
                chat.creation_time = chat_data['creation_time']
                return chat
        return None
