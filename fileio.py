#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) oVoIndia | oVo-HxBots

import asyncio, os, requests, time
from requests import post
from multiupload import anjana
from telethon.sync import events, Button
from multiupload.utils import downloader, humanbytes
from config import Config

@anjana.on(events.NewMessage(pattern='^/fileio'))
async def fileio(event):
	user_id = event.sender_id
	if event.reply_to_msg_id:
		pass
	else:
		return await event.edit("Please Reply to File")

	async with anjana.action(event.chat_id, 'typing'):
		await asyncio.sleep(2)
	msg = await event.reply("**Processing...**")
	amjana = await event.get_reply_message()


	## FILEIO LIMITATION CHECKING
	if amjana.file.size > 1048576:
		return await event.edit("Oof.. File size too Large. FileIO Limitation is 100MB")  

	##UPLOADING...
	result = await downloader(
		f"downloads/{amjana.file.name}",
		amjana.media.document,
		msg,
		time.time(),
		f"**š· Downloading...**\nā² **File Name:** {amjana.file.name}",
	)

	async with anjana.action(event.chat_id, 'document'):
		await msg.edit("Now Uploading to FileIO")
		url = f"https://file.io/"
		r = post(url, files={'file': open(f'{result.name}','rb')})
	await anjana.action(event.chat_id, 'cancel')

	hmm = f'''File Uploaded successfully !!
Server: FileIO

**~ File name:** __{amjana.file.name}__
**~ File size:** __{humanbytes(amjana.file.size)}__
NOTE: Once the download is complete, The file will be deleted from our servers.'''
	await msg.edit(hmm, buttons=(
		[Button.url('š¦ Download', r.json()['link'])],
		[Button.url('Support Chat š­', 't.me/hxsupport')]
		))

	os.remove(result.name)
