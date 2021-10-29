import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import discord
from discord.ext import commands
import asyncio
import traceback
import aiohttp
counter = 0


CLIENT_SECRET_FILE = 'PATH TO YOUR CLIENT SECRET JSON'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
client = commands.Bot(command_prefix="?")
session = aiohttp.ClientSession()


@client.command()
async def upload(ctx):
    try:
        counter = +1
        await ctx.send("Please provide a video file/attachment you wish to upload")
        def check(message):
            return message.author == ctx.author
        video_message = await client.wait_for("message", check=check, timeout=20)
        video = video_message.attachments[0]
        if video == None:
            await ctx.send("Please provide a video file/attachment, start over")
        else:
            await ctx.send("Great! Now please provide a title for the video")
            title = await client.wait_for("message", check=check, timeout=20)
            await ctx.send("Sweet! Description?")
            description = await client.wait_for("message", check=check, timeout=20)
            await ctx.send("Alright, uploading video now :gear:")
            request_body = {
                'snippet': {
                    'title': title.content,
                    'description': description.content,
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False, 
                },
                'notifySubscribers': False
            }
            video_file = await video.save(f"videotest[{counter}].mp4")
            try:
                response_upload = service.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=f"videotest[{counter}].mp4"
                ).execute()
                await ctx.send(f"Success! :smile: Find the video here: https://youtube.com/watch?v={response_upload['id']}")
            except Exception as e:
                traceback.print_exc()
                await ctx.send("Something went wrong")
    except asyncio.TimeoutError:
        await ctx.send("You failed to respond in time!")
    
        
client.run("BOT TOKEN HERE")
