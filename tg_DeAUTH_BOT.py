from aiogram import Bot, Dispatcher, types, html, Router, F
import asyncio
from requests import get
import datetime
from aiogram.methods.ban_chat_member import BanChatMember
from datetime import timedelta
import asyncpg
from bs4 import BeautifulSoup
from datetime import datetime
import datetime

bot = Bot(token="6835687685:AAEwpG2EfekgBHLQjqxexgX7sB1tDr0mdtM") #InformationCollectorBOT

router = Router()
now = datetime.datetime.now()
now = now.strftime("%Y%m%d")
channel_id= int(-1001925191431)

url = f'http://phoca/zup_corp3_hs/hs/namiServices/GetFiredEmployees/2/{now}'

uvolen = get(url)
uvolen = uvolen.text

soup = BeautifulSoup(uvolen, 'lxml')
table = soup.find_all('tr')


async def ban_chat_member(tg_id):
    u_id = tg_id
    await bot.ban_chat_member( chat_id = channel_id, user_id = u_id,until_date=datetime.datetime.now() + timedelta(seconds=40))

async def get_user_id_from_database():
 while True:
    for i in table:

        cells = i.find_all('td')
        if len(cells) == 3 and cells[2].text != 'НомерТелефона':
            phone_number = cells[2].text
            phone = phone_number
            conn = await asyncpg.connect(database='db_skynet', user='skynet', password='N@m!db_t1000', host='192.168.8.68')
            query = f"SELECT tg_id FROM skynet_status WHERE phone = {phone}"
            result_1 = await conn.fetchrow(query)
            if result_1 is not None:
                tg_id=result_1['tg_id']
                await conn.execute(f'''
                UPDATE skynet_status set active_status=False WHERE tg_id={tg_id}
                ''')
                await conn.execute("UPDATE skynet_status SET removed = true WHERE tg_id = $1", tg_id)
                await conn.close()
                await ban_chat_member(tg_id)
            else:
                await conn.close()
asyncio.run(get_user_id_from_database())

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == "__main__":
   asyncio.run(main())

   
   
    
