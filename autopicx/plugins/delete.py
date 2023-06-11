import random
import asyncio
from pyrogram import Client, filters
from .. import API_ID, API_HASH, PYRO_SESSION
from .autopic import del_lock, lock, temp

if PYRO_SESSION is not None:
    autopicx = Client(
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
            deleted = 0
            remaining = await client.get_chat_photos_count("me")
            async for photo in client.get_chat_photos("me"):  
                if temp.CANCEL:
                    break 
                await client.delete_profile_photos([photo.file_id])
                remaining-=1
                deleted+=1
                
                if deleted % 50 == 0:
                    await message.edit(f"🗑️ Dᴇʟᴇᴛᴇᴅ: `{delete}`\n🎗️ Rᴇᴍᴀɪɴɪɴɢ: `{remaining}`\n😴 Sʟᴇᴇᴘɪɴɢ: `120 sec`")
                    await asyncio.sleep(120)
                else:
                    sleep = random.randint(1, 60)
                    await message.edit(f"🗑️ Dᴇʟᴇᴛᴇᴅ: `{delete}`\n🎗️ Rᴇᴍᴀɪɴɪɴɢ: `{remaining}`\n😴 Sʟᴇᴇᴘɪɴɢ: `{sleep}`")
                    await asyncio.sleep(sleep)
          
    autopicx.run()