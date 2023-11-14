import asyncio
from telegram import Bot
import aiohttp
import time
from utils.constants import TELEGRAM_BOT_TOKEN, CHAT_ID , USER_ID

class DcStatus:
    def __init__(self):
        self.isOnline = False

    async def getdata(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.lanyard.rest/v1/users/{USER_ID}') as rawdata:
                data = await rawdata.json()
                return data

    async def send_message_bot(self, bot, chat_id, message):
        await bot.send_message(chat_id, message)

    async def notify(self, bot):
        data = await self.getdata()
        CURRENT_STATUS = data['data']['discord_status']
        USERNAME = data['data']['discord_user']['username']

        if (CURRENT_STATUS in ['online', 'dnd', 'idle']) and not self.isOnline:
            message = f'{USERNAME} is online in Discord'
            await self.send_message_bot(bot, chat_id=CHAT_ID, message=message)
            self.isOnline = True
        elif CURRENT_STATUS == 'offline' and self.isOnline:
            message = f'{USERNAME} went offline in Discord'
            await self.send_message_bot(bot, chat_id=CHAT_ID, message=message)
            self.isOnline = False

myStatus = DcStatus()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
loop = asyncio.get_event_loop()

async def main():
    await myStatus.notify(bot)

if __name__ == '__main__':
    while True:
        
        loop.run_until_complete(main())
        time.sleep(10)









