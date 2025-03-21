import requests
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import logging
import time

# Import your configuration from details.py
from details import api_id, api_hash, bot_token, sudo_groups

# Initialize the bot
bot = Client(
    "zip_downloader_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@bot.on_message(filters.command(["start"]) & filters.chat(sudo_groups))
async def start_handler(bot: Client, m: Message):
    await m.reply_text("Hello! I'm a bot to download and upload ZIP files from a list. Send me a TXT file with Name:URL(ZIP-URL) format.")

@bot.on_message(filters.command(["zip"]) & filters.chat(sudo_groups))
async def zip_downloader(bot: Client, m: Message):
    editable = await m.reply_text("Please send the TXT file containing the ZIP links (Name:URL(ZIP-URL)).")
    input_message: Message = await bot.listen(editable.chat.id)

    try:
        file_path = await input_message.download()
        await input_message.delete(True)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().splitlines()

        links = [line.split(":", 1) for line in content if line]
        os.remove(file_path)

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        await m.reply_text(f"Error processing the file: {e}")
        return

    if not links:
        await m.reply_text("No valid links found in the file.")
        return

    await editable.edit(f"Found {len(links)} links. Starting download and upload...")

    for i, (name, url) in enumerate(links):
        name = name.strip()
        url = url.strip()
        # Extract the zip URL from the string
        zip_url = url.split("(")[1].split(")")[0]
        if not zip_url.endswith(".zip"):
            await m.reply_text(f"Skipping invalid URL: {zip_url}")
            continue
        
        caption = f"{name}\n\nDownloaded by [{m.from_user.first_name}](tg://user?id={m.from_user.id})" if m.from_user else f"{name}\n\nDownloaded by Anonymous"
        file_name = f"{name}.zip"

        try:
            await download_and_upload(bot, m, zip_url, file_name, caption)
            await editable.edit(f"Downloaded and uploaded: {file_name} ({i+1}/{len(links)})")
        except Exception as e:
            logging.error(f"Error downloading/uploading {file_name}: {e}")
            await m.reply_text(f"Failed to download/upload {file_name}: {e}")

    await m.reply_text("Finished processing all links.")

async def download_and_upload(bot: Client, m: Message, url: str, file_name: str, caption: str):
    try:
        logging.info(f"Downloading {file_name} from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info(f"Uploading {file_name}")
        try:
            await bot.send_document(chat_id=m.chat.id, document=file_name, caption=caption)
        except FloodWait as e:
            logging.warning(f"FloodWait encountered. Sleeping for {e.x} seconds.")
            await asyncio.sleep(e.x)
            await bot.send_document(chat_id=m.chat.id, document=file_name, caption=caption)

        logging.info(f"Successfully uploaded {file_name}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Download failed: {e}")
    except Exception as e:
        raise Exception(f"Upload failed: {e}")
    finally:
        try:
            os.remove(file_name)  # Clean up the downloaded file
            logging.info(f"Removed {file_name}")
        except Exception as e:
            logging.warning(f"Failed to remove {file_name}: {e}")

# Run the bot
bot.run()
