import sqlite3

from typing import List, Optional

from database.base import BaseDB
from models.character import CharactersModel

class SQLiteDB(BaseDB):
    def __init__(self):
        self._initialize_client()
        self._set_schema()

    def _initialize_client(self):
        self.client = sqlite3.connect('data/db.db', check_same_thread=False)
        self.client.row_factory = sqlite3.Row  # Allows dict-like access to rows

    def _set_schema(self):
        try:
            with open('schema.sql', 'r') as schema_file:
                schema_sql = schema_file.read()
            with self.client:  # Auto-commits and handles transactions properly
                self.client.executescript(schema_sql)
        except Exception as e:
            print(f"Error initializing database schema: {e}")

    def add(self, data: CharactersModel) -> int:
        with self.client as conn:  # Ensures commit happens safely
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO characters (name, prompt, profile_image_url) VALUES (?, ?, ?)", 
                (data.name, data.prompt, data.profile_image_url)
            )
            last_id = cursor.lastrowid
        return last_id  # Cursor auto-closes after `with` block

    def get(self, id: int) -> Optional[CharactersModel]:
        with self.client as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE id = ?", (id,))
            result = cursor.fetchone()
        if result:
            return CharactersModel(id=result["id"], name=result["name"], prompt=result["prompt"], profile_image_url=result["profile_image_url"])
        return None

    def get_all_characters(self) -> List[CharactersModel]:
        with self.client as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters")
            result = cursor.fetchall()
        return [CharactersModel(id=row["id"], name=row["name"], prompt=row["prompt"], profile_image_url=row['profile_image_url']) for row in result]
