import discord
import asyncio
from discord.ext import commands
import datetime
from song import song
import youtube_dl
from collections import deque
from discordserver import discordserver
import random
import os

client = commands.Bot(command_prefix='!', description="")
token = 'MjYxMjcyNDY2NzE3MDE2MDc0.C0GBrw.nTyS9_lZMfOznPKmPOhXmUvtgik'

server_dict = {}

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')

@client.command(pass_context=True)
async def genji(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/progenji.webm', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Genji"
        player.uploader = "Genji"
        player.duration = 0
        submit_audio_to_queue(context, player)
        print("Submit Genji")

@client.command(pass_context=True)
async def nosey(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/nosey'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/nosey/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Nosey"
        player.uploader = "Nosey"
        player.duration = 0
        submit_audio_to_queue(context, player)
        print("Submit Nosey")

@client.command(pass_context=True)
async def tidus(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/tidus.m4a', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Tidus"
        player.uploader = "Tidus"
        player.duration = 0
        submit_audio_to_queue(context, player)
        print("Submit Tidus")

def after_audio_completed(server):
        coro = audio_complete(server)
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
                fut.result()
        except:
                print (sys.exc_info()[0])
                print('we fucked')

async def test_audio_complete(server):
        print ("Test")

async def audio_complete(server):
        print("audio complete")
        queue_complete = server_dict[server.id].queue_complete()
        if queue_complete:
                await server.voice_client.disconnect()

def submit_audio_to_queue(context, player):
        if context.message.server.id not in server_dict:
                server_dict[context.message.server.id] = discordserver(client)
        server_dict[context.message.server.id].play(player)
        print(server_dict[context.message.server.id].queue)

@client.command(pass_context=True)
async def play(context, message: str):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        if(message.startswith("https://www.youtube.com/")):
                ydl_opts = {}
        else:
                ydl_opts = {'default_search': 'ytsearch:'}
        player = await bot_voice_chan.create_ytdl_player(message, use_avconv=True, ytdl_options=ydl_opts, after=lambda: after_audio_completed(context.message.server))
        submit_audio_to_queue(context, player)
        await client.say(("{} - {} ({})").format(player.title, player.uploader, str(datetime.timedelta(seconds=player.duration))))
                
@client.command(pass_context=True)
async def queue(context):
        i = 1 
        for p in server_dict[context.message.server.id].queue:
                await client.say(("{}. {} - {} ({})").format(i, p.title, p.uploader, str(datetime.timedelta(seconds=p.duration))))
                i = i + 1

async def get_voice_client(context):
        bot_voice_chan = client.voice_client_in(context.message.server)
        user_voice_chan = context.message.author.voice_channel
        if user_voice_chan is None:
                return None
        if bot_voice_chan is None:
                bot_voice_chan = await client.join_voice_channel(user_voice_chan)
        return bot_voice_chan

@client.command(pass_context=True)
async def skip(context):                                                        
        await client.say("Skip doesn't work good luck")
        server_dict[context.message.server.id].skip_song()
        
        
@client.command(pass_context=True)
async def volume(context, message: str):
        voice_client = client.voice_client_in(context.message.server)
        if voice_client is None:
                await client.say("I'm not connected")
        elif 0 <= float(message) <= 200:
                server_dict[context.message.server.id].current_player.volume = float(message) / 100
                await client.say(("Volume is {}").format(message))
        
        else:
                await client.say("Nah man.")

client.run(token)
