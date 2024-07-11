import asyncio
from app.cupcake_data import fetch_all_data

class ChatbotManager:
    def __init__(self):
        self.store_info = {}
        self.last_update = None

    async def update_store_info(self):
        self.store_info = await fetch_all_data()
        self.last_update = asyncio.get_event_loop().time()
        print(self.store_info)

    async def get_store_info(self):
        current_time = asyncio.get_event_loop().time()
        if not self.last_update or (current_time - self.last_update) > 36000:  # Update every hour
            await self.update_store_info()
        return self.store_info

chatbot_manager = ChatbotManager()