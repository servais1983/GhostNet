import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ghostnet.db")

class DatabaseManager:
    """Gestionnaire de base de données SQLite pour GhostNet."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Crée les tables si elles n'existent pas."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alertes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    niveau TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def insert_alerte(self, type_, niveau, message):
        """Insère une alerte dans la base."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO alertes (type, niveau, message) VALUES (?, ?, ?)",
                (type_, niveau, message)
            )
            conn.commit()
            return cursor.lastrowid

    def get_alertes(self, limit=100):
        """Récupère les alertes les plus récentes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, type, niveau, message, timestamp FROM alertes ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()