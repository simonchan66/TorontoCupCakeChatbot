import aiosqlite

DATABASE_NAME = "chat_history.db"

async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_input TEXT,
                bot_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        
async def clear_chat_history(session_id: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        await db.commit()


async def add_chat_entry(session_id: str, user_input: str, bot_response: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("""
            INSERT INTO chat_history (session_id, user_input, bot_response)
            VALUES (?, ?, ?)
        """, (session_id, user_input, bot_response))
        await db.commit()

async def get_chat_history(session_id: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("""
            SELECT user_input, bot_response FROM chat_history
            WHERE session_id = ? ORDER BY timestamp
        """, (session_id,)) as cursor:
            return await cursor.fetchall()