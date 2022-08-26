"""
Copyright ( C ) GopiNath  
"""

import os
import shutil

from PIL import Image, ImageOps
from Gbot import LOGGER


async def black_border(client: Client, message: Message):
    try:
        userid = str(chat_id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True)
            a = await client.download_media(message=message.reply_to_message,
                                            file_name=download_location)
            await msg.edit("Processing Image...")
            img = Image.open(a)
            img_with_border = ImageOps.expand(img, border=100, fill="black")
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "imaged-black-border.png"
            img_with_border.save(edit_img_loc)
            await message.reply_chat_action("upload_photo")
            await message.reply_to_message.reply_photo(edit_img_loc,
                                                       quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        LOGGER.debug("black_border-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        try:
            await message.reply_to_message.reply_text("Something went wrong!",
                                                      quote=True)
        except Exception:
            return


async def green_border(client: Client, message: Message):
    try:
        userid = str(chat_id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True)
            a = await client.download_media(message=message.reply_to_message,
                                            file_name=download_location)
            await msg.edit("Processing Image...")
            img = Image.open(a)
            img_with_border = ImageOps.expand(img, border=100, fill="green")
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "imaged-green-border.png"
            img_with_border.save(edit_img_loc)
            await message.reply_chat_action("upload_photo")
            await message.reply_to_message.reply_photo(edit_img_loc,
                                                       quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        LOGGER.debug("green_border-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        try:
            await message.reply_to_message.reply_text("Something went wrong!",
                                                      quote=True)
        except Exception:
            return


async def blue_border(client: Client, message: Message):
    try:
        userid = str(chat_id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True)
            a = await client.download_media(message=message.reply_to_message,
                                            file_name=download_location)
            await msg.edit("Processing Image...")
            img = Image.open(a)
            img_with_border = ImageOps.expand(img, border=100, fill="blue")
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "imaged-blue-border.png"
            img_with_border.save(edit_img_loc)
            await message.reply_chat_action("upload_photo")
            await message.reply_to_message.reply_photo(edit_img_loc,
                                                       quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        LOGGER.debug("blue_border-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        try:
            await message.reply_to_message.reply_text("Something went wrong!",
                                                      quote=True)
        except Exception:
            return


async def red_border(client: Client, message: Message):
    try:
        userid = str(chat_id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True)
            a = await client.download_media(message=message.reply_to_message,
                                            file_name=download_location)
            await msg.edit("Processing Image...")
            img = Image.open(a)
            img_with_border = ImageOps.expand(img, border=100, fill="red")
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "imaged-red-border.png"
            img_with_border.save(edit_img_loc)
            await message.reply_chat_action("upload_photo")
            await message.reply_to_message.reply_photo(edit_img_loc,
                                                       quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        LOGGER.debug("red_border-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        try:
            await message.reply_to_message.reply_text("Something went wrong!",
                                                      quote=True)
        except Exception:
            return
