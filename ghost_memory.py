import sqlite3

class SovereignMemoryTest:
    def __init__(self, db_path="ghost_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._set_up_db()
        print("✅ [완료] long_term_memory 및 user_profile 테이블 준비 완료.")

    def _set_up_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                embedding BLOB,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                category TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

if __name__ == "__main__":
    mem = SovereignMemoryTest("ghost_memory.db")
