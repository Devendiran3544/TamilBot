from userbot import bot, ALIVE_NAME
from telethon import events
from userbot.utils import command, remove_plugin, load_module
from var import Var
import importlib
from pathlib import Path
from userbot import LOAD_PLUG
import sys
import asyncio
import traceback
import os
from datetime import datetime

tamilthumb = "./resources/TamilBot.jpg"


DELETE_TIMEOUT = 5
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TamilBot"
TAID = bot.uid

@command(pattern="^.install", outgoing=True)
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "userbot/plugins/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! Cannot install this plugin.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@command(pattern="^.send (?P<shortname>\w+)$", outgoing=True)
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match["shortname"]
    start = datetime.now()
    the_plugin_file = "./userbot/plugins/{}.py".format(input_str)
    end = datetime.now()
    ms = (end - start).seconds
    men = f"__**✨ Plugin Name:- {input_str} .**__\n__**✨ Uploaded in {ms} seconds.**__\n__**✨Uploaded by :-**__ [{DEFAULTUSER}](tg://user?id={TAID})")
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        thumb=tamilthumb,
        caption=men,
        force_document=True,
        allow_cache=False,
        reply_to=event.message.reply_to_msg_id
    )
    await asyncio.sleep(5)
    await event.delete()
    

@command(pattern="^.unload (?P<shortname>\w+)$", outgoing=True)
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"Unloaded {shortname} successfully")
    except Exception as e:
        await edit_or_reply(
            event, "Successfully unload {shortname}\n{}".format(shortname, str(e))
        )


@command(pattern="^.load (?P<shortname>\w+)$", outgoing=True)
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_or_reply(event, f"Successfully loaded {shortname}")
    except Exception as e:
        await edit_or_reply(
            event,
            f"Could not load {shortname} because of the following error.\n{str(e)}",
        )
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        thumb=tamilthumb,
        caption=men,
        force_document=True,
        allow_cache=False,
        reply_to=message_id,
    )
    await asyncio.sleep(5)
    await event.delete()
