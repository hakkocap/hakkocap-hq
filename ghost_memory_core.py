import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

class SovereignMemory:
    def __init__(self, db_path="/tmp/swp_comms/ghost_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        print("🏴‍☠️ [시스템] 한국어 벡터 임베딩 모델 로드 중 (jhgan/ko-sroberta-multitask)...")
        self.model = SentenceTransformer('jhgan/ko-sroberta-multitask')
        print("✅ [완료] 모델 로드 및 두뇌 활성화 완료.")
        self._set_up_db()

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

    def store(self, text, category="general"):
        emb = self.model.encode(text).astype(np.float32).tobytes()
        self.cursor.execute("INSERT INTO long_term_memory (content, embedding, category) VALUES (?, ?, ?)",
                            (text, emb, category))
        self.conn.commit()

    def update_profile(self, key, value):
        self.cursor.execute("""
            INSERT INTO user_profile (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
        """, (key, value))
        self.conn.commit()

    def recall(self, query, top_k=3):
        query_vec = self.model.encode(query).astype(np.float32)
        self.cursor.execute("SELECT id, content, embedding, category FROM long_term_memory WHERE embedding IS NOT NULL")
        rows = self.cursor.fetchall()
        if not rows: return []
        
        results = []
        for row in rows:
            mem_id, content, emb_blob, cat = row
            mem_vec = np.frombuffer(emb_blob, dtype=np.float32)
            norm_q = np.linalg.norm(query_vec)
            norm_m = np.linalg.norm(mem_vec)
            if norm_q == 0 or norm_m == 0:
                score = 0
            else:
                score = np.dot(query_vec, mem_vec) / (norm_q * norm_m)
            results.append((score, content, cat))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
