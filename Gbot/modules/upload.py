"""
Copyright ( C ) GopiNath  
"""

import asyncio
import datetime
import os
import time
import traceback

import aiohttp
from telethon import events

from Gbot import telethn, TEMP_DOWNLOAD_DIRECTORY, SUPPORT_CHAT, LOGGER
from Gbot.modules.urluploader import download_file
from Gbot.utils.pluginhelpers import humanbytes, progress


def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.now()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


async def send_to_transfersh_async(file):

    size = os.path.getsize(file)
    size_of_file = humanbytes(size)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    LOGGER.debug(f"\nUploading file: {file_name} (size of the file: {size_of_file})")
    url = "https://transfer.sh/"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session, session.post(
                url, data={str(file): f}) as response:
            download_link = await response.text()

    LOGGER.debug(
        f"Link to download file(will be saved till {final_date}):\n{download_link}"
    )

    return download_link, final_date, size_of_file


async def send_to_tmp_async(file):
    url = "https://tmp.ninja/api.php?d=upload-tool"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session, session.post(
                url, data={"file": f}) as response:
            download_link = await response.text()

    return download_link


@telethn.on(events.NewMessage(pattern="/transfersh"))
async def tsh(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(progress(d, t, ilk, start, "Downloading...")))
        except Exception as e:
            traceback.print_exc()
            LOGGER.debug(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("Uploading to TransferSh...")
            download_link, final_date
            await send_to_transfersh_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"File Successfully Uploaded to TransferSh.\n\nLink 👉 {download_link}\nExpired Date 👉 {final_date}\n\nUploaded by *@{SUPPORT_CHAT}*"
            )
        except Exception as e:
            traceback.print_exc()
            LOGGER.debug(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

    raise events.StopPropagation


@telethn.on(events.NewMessage(pattern="/tmpninja"))
async def tmp(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(progress(d, t, ilk, start, "Downloading...")))
        except Exception as e:
            traceback.print_exc()
            LOGGER.debug(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("Uploading to TmpNinja...")
            download_link = await send_to_tmp_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"File Successfully Uploaded to TmpNinja.\n\nLink 👉 {download_link}\n\nUploaded by *@Gbot*"
            )
        except Exception as e:
            traceback.print_exc()
            LOGGER.debug(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

    raise events.StopPropagation


@telethn.on(events.NewMessage(pattern="/up"))
async def up(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")

        try:
            filename = os.path.join(TEMP_DOWNLOAD_DIRECTORY,
                                    os.path.basename(url.text))
            await download_file(url.text, filename, ilk, start, telethn)
        except Exception as e:
            LOGGER.debug(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("Uploading to Telegram...")

            dosya = await telethn.upload_file(
                filename,
                progress_callback=lambda d, t: asyncio.get_event_loop().
                create_task(
                    progress(d, t, orta, start, "Uploading to Telegram...")),
            )

            str(time.time() - start)
            await telethn.send_file(
                event.chat.id,
                dosya,
                force_document=True,
                caption="Uploaded By *@Gbot*",
            )
        except Exception as e:
            traceback.print_exc()

            LOGGER.debug(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

        await orta.delete()

    raise events.StopPropagation


def main():
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.mkdir(TEMP_DOWNLOAD_DIRECTORY)


if __name__ == "__main__":
    main()
