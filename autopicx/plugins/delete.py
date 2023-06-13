import pytz
import math
import random
import asyncio
import datetime
from pyrogram import Client, filters
from .. import API_ID, API_HASH, PYRO_SESSION
from .autopic import del_lock, lock, temp

if PYRO_SESSION is not None:
    autopicx = Client(
        name = "AutoPicX",
        api_id = API_ID,
        api_hash = API_HASH,
        session_string = PYRO_SESSION
        )
        
    @autopicx.on_message(filters.regex("!delete"))
    async def pyro_del_dp(client, message):
        temp.CANCEL = False
        if del_lock.locked():
            return await message.edit("**Pʀᴏᴄᴇss Aʟʀᴇᴀᴅʏ Iɴᴛɪᴀᴛᴇᴅ !**") 

        if lock.locked(): 
            return await message.edit("**Sᴛᴏᴘ Tʜᴇ Oɴɢᴏɪɴɢ DP Cʜᴀɴɢɪɴɢ Fɪʀsᴛ !**") 
    
        async with del_lock:
            await message.edit("**Sᴛᴀʀᴛɪɴɢ Tᴏ Dᴇʟᴇᴛᴇ...**") 
            tz = pytz.timezone('Asia/Kolkata')
            start_time = datetime.datetime.now(tz)
            deleted = 0
            remaining = await client.get_chat_photos_count("me")
            async for photo in client.get_chat_photos("me"):  
                if temp.CANCEL:
                    break 
                await client.delete_profile_photos([photo.file_id])
                remaining-=1
                deleted+=1 
                tz = pytz.timezone('Asia/Kolkata')               
                current_time = datetime.datetime.now(tz)
                ttime = current_time.strftime("%I:%M:%S %p - %d %b, %Y")
                elapsed_time = current_time - start_time
                time_remaining = elapsed_time / deleted * remaining
                elapsed_time_str = get_readable_time(elapsed_time)
                time_remaining_str = get_readable_time(time_remaining)
                if deleted % 50 == 0:
                    await message.edit(f"**🗑️ Dᴇʟᴇᴛᴇᴅ: `{deleted}`\n🎗️ Rᴇᴍᴀɪɴɪɴɢ: `{remaining}`\n😴 Sʟᴇᴇᴘɪɴɢ: `120 sec`\n\n⏳ Tɪᴍᴇ Tᴀᴋᴇɴ: {elapsed_time_str}\n⏰ ETC: {time_remaining_str}\n🎈 Lᴀsᴛ Uᴘᴅᴀᴛᴇᴅ: {ttime}**")
                    await asyncio.sleep(120)
                else:
                    sleep = random.randint(1, 60)
                    await message.edit(f"**🗑️ Dᴇʟᴇᴛᴇᴅ: `{deleted}`\n🎗️ Rᴇᴍᴀɪɴɪɴɢ: `{remaining}`\n😴 Sʟᴇᴇᴘɪɴɢ: `{sleep}`\n\n⏳ Tɪᴍᴇ Tᴀᴋᴇɴ: {elapsed_time_str}\n⏰ ETC: {time_remaining_str}\n🎈 Lᴀsᴛ Uᴘᴅᴀᴛᴇᴅ: {ttime}**")
                    await asyncio.sleep(sleep)
          
    autopicx.run()

def get_readable_time(seconds) -> str:
    """
    Return a human-readable time format
    """

    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)

    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)

    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)

    if minutes != 0:
        result += f"{minutes}m"

    seconds = int(seconds)
    result += f"{seconds}s"
    return result
