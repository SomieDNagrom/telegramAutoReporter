import asyncio
import random
import uuid
import os
import sys

from constants_eng import Constants
from pathlib import Path
from environs import Env
from pyrogram import Client, filters
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputPeerChannel, InputReportReasonOther
from __version__ import __version__

env = Env()
env.read_env()

scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
api_id = env.int(Constants.API_ID)
api_hash = env.str(Constants.API_HASH)
session_path = Path(scriptDir + "\\" + Constants.SESSION)
banChannelsPath = Path(scriptDir + "\\" + Constants.BAN_CHANNELS_TXT)

banReasonArray = [Constants.BAN_REASON_1, Constants.BAN_REASON_2,
                  Constants.BAN_REASON_3, Constants.BAN_REASON_4]

timeSleepSeconds = random.randint(Constants.TIMESLEEP_MIN, Constants.TIMESLEEP_MAX)
MAX_REPORT_AMOUNT = random.randint(Constants.REPORT_COUNT_MIN, Constants.REPORT_COUNT_MAX)

print(f"{Constants.VERSION}: {__version__}")


def on_start():
    if session_path.exists():
        if(len(sys.argv) < 1):
            os.remove(session_path)
            print(Constants.ERROR_WRONG_ARGS)
            print(Constants.EXIT_PROGRAM)
            exit()
        elif(len(sys.argv) == 1):
            with open(session_path) as file:
                session_string = file.read()
        else:
            session_string = sys.argv[1]

        if not session_string or session_string == "":
            os.remove(session_path)
            print(Constants.OLD_CONF_REMOVED)
            print(Constants.RESTART_APP)
            exit()
        return Client(session_string, api_id, api_hash)
    else:
        while True:
            with Client(uuid.uuid4().hex, api_id, api_hash) as tmp_app:
                with open(session_path, 'a') as file:
                    session_string = tmp_app.export_session_string()
                    if(session_string != None and session_string != ""):
                        file.write(session_string + " ")
                        print(Constants.USER_ADDED_SESSION)
            if(input(Constants.STOP_ADD_NUMS).lower() == Constants.STOP_ADD_NUMS):
                break

        print(Constants.APP_CONFIGURED)
        print(Constants.RESTART_APP)
        exit()


app = on_start()


@app.on_message(filters.command(commands=Constants.COMMAND_REPORT) & filters.private)
async def cmd_report(client, message):
    print(Constants.EXPORT_FILES)
    await client.send_message("me", Constants.EXPORT_FILES)

    print(Constants.RECOMMENDATION)
    await client.send_message("me", Constants.RECOMMENDATION)

    with open(banChannelsPath) as file:
        ids = list(map(str.strip, file.readlines()))

    random.shuffle(ids)
    limited_ids = ids[:MAX_REPORT_AMOUNT]
    length = len(limited_ids)

    for _, i in enumerate(limited_ids, start=1):
        try:
            peer: InputPeerChannel = await client.resolve_peer(i)
            banReason = random.choice(banReasonArray)
            response = await client.send(data=ReportPeer(peer=peer, reason=InputReportReasonOther(), message=banReason))
            print(f"[{_}/{length}]\n"
                  f"[{i}: {Constants.CHANNEL_REPORTED}]\n"
                  f"[{Constants.REASON}: {banReason}]\n"
                  f"[{Constants.SERVER_RESPONSE}: {response}]")
            await client.send_message("me", f"[{_}/{length}]\n"
                                      f"[{i}: {Constants.CHANNEL_REPORTED}]\n"
                                      f"[{Constants.REASON}: {banReason}]\n"
                                      f"[{Constants.SERVER_RESPONSE}: {response}]")
        except Exception as exc:
            print(exc)
        finally:
            await asyncio.sleep(timeSleepSeconds)

app.connect()
app.send_message("me", Constants.ENTER_COMMAND)
app.send_message("me", f"/{Constants.COMMAND_REPORT}")
app.send_message(
    "me", Constants.START_REPORT)
print(f"{Constants.INFO_DEV}")
app.disconnect()
app.run()