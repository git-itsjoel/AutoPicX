#© 𝙄𝙩𝙨 ⚡ 𝙅𝙤𝙚𝙡 | #𝘼𝙗𝙊𝙪𝙩𝙈𝙚_𝘿𝙆

from .. import client, TIME, CHANNEL_ID
from telethon import events, types
import logging 
import os
import asyncio
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import InputMessagesFilterPhotos

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
lock = asyncio.Lock()

class temp(object):
    CANCEL = False

async def change_profile_pic(client):
    channel_id = CHANNEL_ID
    
    async with lock:
        while True:
            if temp.CANCEL:
                break
            async for message in client.iter_messages(channel_id, reverse=True, filter=InputMessagesFilterPhotos):
                if temp.CANCEL:
                    break
                photo = await client.download_media(message=message.photo)
                try:
                    await client(UploadProfilePhotoRequest(file=await client.upload_file(f'{photo}')))
                    os.remove(photo)
               
                except Exception as e:
                    logger.exception(e)
                    continue
                await asyncio.sleep(TIME)
        

@client.on(events.NewMessage(outgoing=True, pattern='!cancel'))
async def handle_cancel(event):
    if not lock.locked():
        msg = await event.respond('𝙉𝙤 𝙋𝙧𝙤𝙘𝙚𝙨𝙨 𝙍𝙪𝙣𝙣𝙞𝙣𝙜...')
        await asyncio.sleep(30)
        await msg.delete()
        return
    temp.CANCEL = True
    msg = await event.respond('𝘾𝙖𝙣𝙘𝙚𝙡𝙞𝙣𝙜 𝘼𝙪𝙩𝙤𝙋𝙞𝙘𝙓...')
    await asyncio.sleep(30)
    await msg.delete()

@client.on(events.NewMessage(outgoing=True, pattern='!start'))
async def handle_start(event):
    temp.CANCEL = False
    if lock.locked():
        msg = await event.respond("𝘼𝙡𝙧𝙚𝙖𝙙𝙮 𝘼 𝙋𝙧𝙤𝙘𝙚𝙨𝙨 𝙄𝙨 𝙍𝙪𝙣𝙣𝙞𝙣𝙜......")
        await asyncio.sleep(30)
        await msg.delete()  
        return      
    try:
        msg = await event.respond("𝙇𝙖𝙪𝙣𝙘𝙝𝙞𝙣𝙜 𝘼𝙪𝙩𝙤𝙋𝙞𝙘𝙓......")
        await change_profile_pic(client)
        await asyncio.sleep(30)
        await msg.delete()
    except Exception as e:
        logging.exception(e)
        await event.respond(str(e))

