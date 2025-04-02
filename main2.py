import requests
import json
import subprocess
from pyrogram import Client,filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import tgcrypto
from p_bar import progress_bar
from details import api_id, api_hash, bot_token, sudo_groups
from urllib.parse import parse_qs, urlparse
from subprocess import getstatusoutput
import helper
import logging
import time
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession
from pyrogram.types import User, Message
import sys ,io
import re
import os
from pyrogram.types import InputMediaDocument
import time
import random 
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors.exceptions import MessageIdInvalid
import os
import yt_dlp
from bs4 import BeautifulSoup
from pyrogram.types import InputMediaDocument





botStartTime = time.time()
batch = []
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)
      
@bot.on_message(filters.command(["start"]) & filters.chat(sudo_groups))
async def start_handler(bot: Client, m: Message):
    menu_text = (
        "Welcome to **TXT** Downloader Bot! \n\n"
        "[Generic Services]\n"
        "1. For All PDF /pdf\n"
        "2. For TXT /txt \n"
    )
    
    await m.reply_text(menu_text)


@bot.on_message(filters.command(["restart"]))
async def restart_handler(bot: Client, m: Message):
 rcredit = "Bot Restarted by " + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
 if (f'{m.from_user.id}' in batch or batch == []) or m.from_user.id == sudo_groups:
    await m.reply_text("Restarted ✅", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
 else:
 	await m.reply_text("You are not started this batch 😶.")

def meFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]
  
def humanbytes(size):
    size = int(size)
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"

@bot.on_message(filters.command(["pdf"]) & filters.chat(sudo_groups))
async def c_pdf(bot: Client, m: Message):
    editable = await m.reply_text("**Hello I am All in one pdf DL Bot\n\nSend TXT file To Download.**")
    input99: Message = await bot.listen(editable.chat.id)
    x = await input99.download()
    await input99.delete(True)
    try:
        with open(x, "r", encoding="utf-8") as f:
            content = f.read().split("\n")
        links = [i.split(":", 1) for i in content if i]
        os.remove(x)
    except Exception as e:
        logging.error(e)
        await m.reply_text("Invalid file input ❌.")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found in given txt {len(links)}\n\nSend From range, you want to download,\n\nInitial is 1")
    input1: Message = await bot.listen(editable.chat.id)
    count = int(input1.text)

    await m.reply_text("**Enter Batch Name**")
    inputy: Message = await bot.listen(editable.chat.id)
    raw_texty = inputy.text

    try:
        for i in range(count - 1, len(links)):
            name = links[i][0].strip()
            url = links[i][1].strip()
            cc = f'{str(count).zfill(3)}. {name}.pdf\n\n**Batch:-** {raw_texty}\n\n'
            
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"{name}.pdf", 'wb') as pdf_file:
                    pdf_file.write(response.content)
                await m.reply_document(f'{name}.pdf', caption=cc)
                os.remove(f'{name}.pdf')
            else:
                await m.reply_text(f"Failed to download {name}.pdf")

            count += 1
            time.sleep(2)
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Completed ✅")

@bot.on_message(filters.command(["stats"]))
async def stats(_,event: Message):
    logging.info('31')
    currentTime = meFormatter((time.time() - botStartTime))
    osUptime = meFormatter((time.time() - boot_time()))
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats = f'Bot Uptime: {currentTime}\n'\
            f'OS Uptime: {osUptime}\n'\
            f'Total Disk Space: {total}\n'\
            f'Used: {used} | Free: {free}\n'\
            f'Upload: {sent}\n'\
            f'Download: {recv}\n'\
            f'CPU: {cpuUsage}%\n'\
            f'RAM: {mem_p}%\n'\
            f'DISK: {disk}%\n'\
            f'Physical Cores: {p_core}\n'\
            f'Total Cores: {t_core}\n'\
            f'SWAP: {swap_t} | Used: {swap_p}%\n'\
            f'Memory Total: {mem_t}\n'\
            f'Memory Free: {mem_a}\n'\
            f'Memory Used: {mem_u}\n'
    
    await event.reply_text(f"{stats}")    


@bot.on_message(filters.command(["txt"]) & filters.chat(sudo_groups))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**Hello DeAr**, I am Txt Downloader Bot.\nI can download videos from **TXT file** one by one.\n\n**Developer: Smile Bhai** \n**Language:** Python\n**Framework:** 🔥Pyrogram\n\nNow Send Your TXT File:-\n") 
    input_msg = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    
    await input_msg.delete(True)

    path = f"./downloads/{m.chat.id}"
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"Downloaded by [{m.from_user.first_name}](tg://user?id={m.from_user.id})" if m.from_user else "Downloaded anonymously"
    
    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split("://", 1) for i in content]
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return
    
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend from where you want to download (initial is **1**)")
    input0 = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send `df` for grabbing it from txt.**")
    input1 = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    b_name = file_name if raw_text0 == 'df' else raw_text0
    
    await editable.edit("**Enter resolution**")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    res = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }.get(raw_text2, "UN")

    await editable.edit("**Enter Caption or send `df` for default or just /skip**")
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    creditx = {
        'df': credit,
        '/skip': ''
    }.get(raw_text3, raw_text3)
    await input3.delete(True)
   
    await editable.edit("Now send the **Thumb url**\nEg » ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6 = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    count = int(raw_text) if len(links) > 1 else 1
    
    try:
        message = await bot.send_message(sudo_groups, f"❇️ {b_name}")
        await message.pin()
        
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'your-access-token'}).json()['url']

            elif '/master.mpd' in url:
                id =  url.split("/")[-2]
                url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                cc = f'** {str(count).zfill(3)}.** {name1} {res}.mkv\n\n**Batch:-** {b_name}\n\n{creditx}'
                cc1 = f'** {str(count).zfill(3)}.** {name1}.pdf \n\n**Batch:-** {b_name}\n\n{creditx}'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        cmd = f'aria2c -o "{name}.pdf" "{url}"'
                        os.system(cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ Downloading »**\n\n**Name:-** `{name}\n\nQuality:- {raw_text2}`\n\n**With ❤️ From Admins.**"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(20)

            except Exception as e:
                await m.reply_text(
                    f"**Downloading Interrupted **\n\n{str(e)}\n**Name:-**  {name}\n\n**Link:-** \n\n `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done ✅")






@bot.on_message(filters.command(["ziptxt"]) & filters.chat(sudo_groups))
async def ziptxt_handler(bot: Client, m: Message):
    try:
        editable = await m.reply_text("Send links listed in a txt file in format **Name:link**")
        input_msg = await bot.listen(editable.chat.id, timeout=300)
        x = await input_msg.download()
        await input_msg.delete(True)

        # Create downloads directory if not exists
        os.makedirs(f"./downloads/{m.chat.id}", exist_ok=True)
        
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"Downloaded by [{m.from_user.first_name}](tg://user?id={m.from_user.id})" if m.from_user else "Downloaded anonymously"
        
        try:
            with open(x, "r") as f:
                content = f.read().splitlines()
            links = [i.split("://", 1) for i in content if i.strip()]
            os.remove(x)
        except Exception as e:
            await m.reply_text(f"Error reading file: {str(e)}")
            if os.path.exists(x):
                os.remove(x)
            return

        if not links:
            await m.reply_text("No valid links found in the file.")
            return

        # Get user inputs
        inputs = await get_user_inputs(bot_links=len(links), editable=editable, file_name=file_name)
        if not inputs:
            return

        b_name, start_from, res, creditx, thumb = inputs

        # Process thumb
        thumb_path = await process_thumbnail(thumb)
        
        # Start processing
        message = await bot.send_message(sudo_groups, f"❇️ {b_name}")
        await message.pin()

        count = start_from
        for i in range(start_from - 1, len(links)):
            try:
                url = await process_url(links[i][1])
                name = await generate_filename(links[i][0], count)
                
                if url.endswith(".pdf"):
                    await handle_pdf(bot, m, url, name, b_name, creditx)
                elif url.endswith(".zip"):
                    await handle_zip(bot, m, url, name, b_name, creditx)
                else:
                    await handle_video(bot, m, url, name, b_name, res, creditx, thumb_path)
                
                count += 1
                time.sleep(5)  # Basic rate limiting
            except FloodWait as e:
                await m.reply_text(f"Flood wait: Sleeping for {e.x} seconds")
                time.sleep(e.x)
                continue
            except Exception as e:
                await m.reply_text(f"Error processing {links[i][0]}: {str(e)}")
                continue

        await m.reply_text("Done ✅")
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception as e:
        await m.reply_text(f"Main Error: {str(e)}")

async def get_user_inputs(tot_links, editable, file_name):
    try:
        await editable.edit(f"Total links found: {tot_links}\nSend starting index (default 1):")
        input0 = await bot.listen(editable.chat.id, timeout=120)
        start_from = int(input0.text) if input0.text.isdigit() else 1
        await input0.delete(True)

        await editable.edit("Enter Batch Name or send 'df' to use filename:")
        input1 = await bot.listen(editable.chat.id, timeout=120)
        b_name = file_name if input1.text.lower() == 'df' else input1.text
        await input1.delete(True)
        
        await editable.edit("Enter resolution (144,240,360,480,720,1080):")
        input2 = await bot.listen(editable.chat.id, timeout=120)
        res = {
            "144": "256x144", "240": "426x240", "360": "640x360",
            "480": "854x480", "720": "1280x720", "1080": "1920x1080"
        }.get(input2.text, "UN")
        await input2.delete(True)

        await editable.edit("Enter caption or 'df' for default or '/skip' for none:")
        input3 = await bot.listen(editable.chat.id, timeout=120)
        creditx = {
            'df': credit, '/skip': ''
        }.get(input3.text, input3.text)
        await input3.delete(True)
       
        await editable.edit("Send thumb URL or 'no' to skip:")
        input6 = await bot.listen(editable.chat.id, timeout=120)
        thumb = input6.text
        await input6.delete(True)
        await editable.delete()

        return b_name, start_from, res, creditx, thumb

    except Exception as e:
        await editable.edit(f"Input error: {str(e)}")
        return None

async def process_url(url_part):
    url = "https://" + url_part.replace("file/d/", "uc?export=download&id=")\
                              .replace("www.youtube-nocookie.com/embed", "youtu.be")\
                              .replace("?modestbranding=1", "")\
                              .replace("/view?usp=sharing", "")
    
    if "visionias" in url:
        async with ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                text = await resp.text()
                url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
    elif 'videos.classplusapp' in url:
        url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                          headers={'x-access-token': 'your-access-token'}).json()['url']
    elif '/master.mpd' in url:
        id = url.split("/")[-2]
        url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"
    
    return url

async def generate_filename(name_part, count):
    name1 = re.sub(r'[^\w\s-]', '', name_part).strip()
    return f'{str(count).zfill(3)}) {name1[:60]}'

async def process_thumbnail(thumb_url):
    if thumb_url.lower() in ['no', '']:
        return None
    
    try:
        thumb_path = "thumb.jpg"
        if thumb_url.startswith(("http://", "https://")):
            getstatusoutput(f"wget '{thumb_url}' -O '{thumb_path}'")
            return thumb_path if os.path.exists(thumb_path) else None
    except:
        return None

async def handle_pdf(bot, m, url, name, b_name, caption):
    try:
        cmd = f'aria2c -x16 -k1M -o "{name}.pdf" "{url}"'
        os.system(cmd)
        
        if os.path.exists(f"{name}.pdf"):
            await bot.send_document(
                chat_id=m.chat.id,
                document=f"{name}.pdf",
                caption=f"* {name}.pdf\n*Batch »* {b_name}\n\n{caption}"
            )
            os.remove(f"{name}.pdf")
    except Exception as e:
        raise Exception(f"PDF Error: {str(e)}")

async def handle_zip(bot, m, url, name, b_name, caption):
    try:
        if "youtu" in url:
            # Handle YouTube links that might have 'zip' in URL but are actually videos
            ytf = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
            os.system(cmd)
            
            if os.path.exists(f"{name}.mp4"):
                await bot.send_video(
                    chat_id=m.chat.id,
                    video=f"{name}.mp4",
                    caption=f"* {name}.mp4\n*Batch »* {b_name}\n\n{caption}"
                )
                os.remove(f"{name}.mp4")
        else:
            # Handle actual ZIP files
            cmd = f'aria2c -x16 -k1M -o "{name}.zip" "{url}"'
            os.system(cmd)
            
            if os.path.exists(f"{name}.zip"):
                await bot.send_document(
                    chat_id=m.chat.id,
                    document=f"{name}.zip",
                    caption=f"* {name}.zip\n*Batch »* {b_name}\n\n{caption}"
                )
                os.remove(f"{name}.zip")
    except Exception as e:
        raise Exception(f"ZIP Error: {str(e)}")

async def handle_video(bot, m, url, name, b_name, res, caption, thumb_path):
    try:
        if "youtu" in url:
            ytf = f"bv*[height<={res.split('x')[1]}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        else:
            ytf = f"bv*[height<={res.split('x')[1]}]+ba/b/bv+ba"
        
        cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
        os.system(cmd)
        
        if os.path.exists(f"{name}.mp4"):
            await bot.send_video(
                chat_id=m.chat.id,
                video=f"{name}.mp4",
                caption=f"* {name} {res}.mp4\n*Batch »* {b_name}\n\n{caption}",
                thumb=thumb_path if thumb_path else None
            )
            os.remove(f"{name}.mp4")
    except Exception as e:
        raise Exception(f"Video Error: {str(e)}")













@bot.on_message(filters.command(["zip"]) & filters.chat(sudo_groups))
async def ziptxt_handler(bot: Client, m: Message):
    try:
        editable = await m.reply_text("Send links listed in a txt file in format **Name:link**")
        input_msg = await bot.listen(editable.chat.id, timeout=300)
        x = await input_msg.download()
        await input_msg.delete(True)

        # Create downloads directory if not exists
        os.makedirs(f"./downloads/{m.chat.id}", exist_ok=True)
        
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"Downloaded by [{m.from_user.first_name}](tg://user?id={m.from_user.id})" if m.from_user else "Downloaded anonymously"
        
        try:
            with open(x, "r") as f:
                content = f.read().splitlines()
            links = [i.split("://", 1) for i in content if i.strip()]
            os.remove(x)
        except Exception as e:
            await m.reply_text(f"Error reading file: {str(e)}")
            if os.path.exists(x):
                os.remove(x)
            return

        if not links:
            await m.reply_text("No valid links found in the file.")
            return

        # Get user inputs
        await editable.edit(f"Total links found: {len(links)}\nSend starting index (default 1):")
        input0 = await bot.listen(editable.chat.id, timeout=120)
        start_from = int(input0.text) if input0.text.isdigit() else 1
        await input0.delete(True)

        await editable.edit("Enter Batch Name or send 'df' to use filename:")
        input1 = await bot.listen(editable.chat.id, timeout=120)
        b_name = file_name if input1.text.lower() == 'df' else input1.text
        await input1.delete(True)
        
        await editable.edit("Enter resolution (144,240,360,480,720,1080):")
        input2 = await bot.listen(editable.chat.id, timeout=120)
        res = {
            "144": "256x144", "240": "426x240", "360": "640x360",
            "480": "854x480", "720": "1280x720", "1080": "1920x1080"
        }.get(input2.text, "UN")
        await input2.delete(True)

        await editable.edit("Enter caption or 'df' for default or '/skip' for none:")
        input3 = await bot.listen(editable.chat.id, timeout=120)
        creditx = {
            'df': credit, '/skip': ''
        }.get(input3.text, input3.text)
        await input3.delete(True)
       
        await editable.edit("Send thumb URL or 'no' to skip:")
        input6 = await bot.listen(editable.chat.id, timeout=120)
        thumb = input6.text
        await input6.delete(True)
        await editable.delete()

        # Process thumb
        thumb_path = None
        if thumb.lower() not in ['no', ''] and thumb.startswith(("http://", "https://")):
            thumb_path = "thumb.jpg"
            getstatusoutput(f"wget '{thumb}' -O '{thumb_path}'")
            if not os.path.exists(thumb_path):
                thumb_path = None

        # Start processing
        message = await bot.send_message(sudo_groups, f"❇️ {b_name}")
        await message.pin()

        count = start_from
        for i in range(start_from - 1, len(links)):
            try:
                # Process URL
                url_part = links[i][1]
                url = "https://" + url_part.replace("file/d/", "uc?export=download&id=")\
                                        .replace("www.youtube-nocookie.com/embed", "youtu.be")\
                                        .replace("?modestbranding=1", "")\
                                        .replace("/view?usp=sharing", "")
                
                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                elif 'videos.classplusapp' in url:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                                    headers={'x-access-token': 'your-access-token'}).json()['url']
                elif '/master.mpd' in url:
                    id = url.split("/")[-2]
                    url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"
                
                # Generate filename
                name_part = links[i][0]
                name1 = re.sub(r'[^\w\s-]', '', name_part).strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'

                # Handle different file types
                if url.endswith(".pdf"):
                    await handle_pdf(bot, m, url, name, b_name, creditx)
                elif url.endswith(".zip"):
                    await handle_zip(bot, m, url, name, b_name, creditx)
                else:
                    await handle_video(bot, m, url, name, b_name, res, creditx, thumb_path)
                
                count += 1
                time.sleep(5)  # Basic rate limiting
            except FloodWait as e:
                await m.reply_text(f"Flood wait: Sleeping for {e.x} seconds")
                time.sleep(e.x)
                continue
            except Exception as e:
                await m.reply_text(f"Error processing {links[i][0]}: {str(e)}")
                continue

        await m.reply_text("Done ✅")
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception as e:
        await m.reply_text(f"Main Error: {str(e)}")

async def handle_pdf(bot, m, url, name, b_name, caption):
    try:
        cmd = f'aria2c -x16 -k1M -o "{name}.pdf" "{url}"'
        os.system(cmd)
        
        if os.path.exists(f"{name}.pdf"):
            await bot.send_document(
                chat_id=m.chat.id,
                document=f"{name}.pdf",
                caption=f"* {name}.pdf\n*Batch »* {b_name}\n\n{caption}"
            )
            os.remove(f"{name}.pdf")
    except Exception as e:
        raise Exception(f"PDF Error: {str(e)}")

async def handle_zip(bot, m, url, name, b_name, caption):
    try:
        if "youtu" in url:
            # Handle YouTube links that might have 'zip' in URL but are actually videos
            ytf = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
            os.system(cmd)
            
            if os.path.exists(f"{name}.mp4"):
                await bot.send_video(
                    chat_id=m.chat.id,
                    video=f"{name}.mp4",
                    caption=f"* {name}.mp4\n*Batch »* {b_name}\n\n{caption}"
                )
                os.remove(f"{name}.mp4")
        else:
            # Handle actual ZIP files
            cmd = f'aria2c -x16 -k1M -o "{name}.zip" "{url}"'
            os.system(cmd)
            
            if os.path.exists(f"{name}.zip"):
                await bot.send_document(
                    chat_id=m.chat.id,
                    document=f"{name}.zip",
                    caption=f"* {name}.zip\n*Batch »* {b_name}\n\n{caption}"
                )
                os.remove(f"{name}.zip")
    except Exception as e:
        raise Exception(f"ZIP Error: {str(e)}")

async def handle_video(bot, m, url, name, b_name, res, caption, thumb_path):
    try:
        if "youtu" in url:
            ytf = f"bv*[height<={res.split('x')[1]}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        else:
            ytf = f"bv*[height<={res.split('x')[1]}]+ba/b/bv+ba"
        
        cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
        os.system(cmd)
        
        if os.path.exists(f"{name}.mp4"):
            await bot.send_video(
                chat_id=m.chat.id,
                video=f"{name}.mp4",
                caption=f"* {name} {res}.mp4\n*Batch »* {b_name}\n\n{caption}",
                thumb=thumb_path if thumb_path else None
            )
            os.remove(f"{name}.mp4")
    except Exception as e:
        raise Exception(f"Video Error: {str(e)}")







bot.run()
