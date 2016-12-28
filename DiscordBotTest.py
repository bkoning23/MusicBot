import discord
import asyncio
from discord.ext import commands
import datetime
from song import song
import youtube_dl
from collections import deque


client = commands.Bot(command_prefix='!', description="")
token = 'MjYxMjcyNDY2NzE3MDE2MDc0.C0GBrw.nTyS9_lZMfOznPKmPOhXmUvtgik'

player_dict = {}
song_list = deque()

play_lock = asyncio.Lock()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')

@client.event
async def on_message(message):
        if message.content.startswith('!test'):
                await client.send_message(message.channel, 'Cookie is awesome')
        elif message.content.startswith('!playasdfasdf'):
                channel = discord.utils.get(message.server.channels, name='General', type=discord.ChannelType.voice)
                voice = await client.join_voice_channel(channel)
                player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=dQw4w9WgXcQ', use_avconv=True)
                player.start()
        await client.process_commands(message)

@client.command()
async def echo(message: str):
        await client.say(message)

@client.command(pass_context=True)
async def play(context, message: str):
        await play_lock
        try:
                user_voice_chan = context.message.author.voice_channel
                bot_voice_chan = client.voice_client_in(context.message.server)
                if user_voice_chan is None:
                        await client.say("You must be in a voice channel to play audio")
                if bot_voice_chan is None:
                        bot_voice_chan = await client.join_voice_channel(user_voice_chan)
                await process_song(message)
                if (bot_voice_chan.server not in player_dict):
                        song = song_list.popleft()
                        player = await bot_voice_chan.create_ytdl_player('https://youtube.com/watch?v={}'.format(song.yt_id), use_avconv=True)
                        await client.say(("{} - {} ({})").format(song.title, song.uploader, str(datetime.timedelta(seconds=song.duration))))
                        player_dict[bot_voice_chan.server] = player
                        player.start()
        finally:
                play_lock.release()
                
@client.command()
async def queue():
        i = 0 
        for p in song_list:
                await client.say(("{}. {} - {} ({})").format(i, p.title, p.uploader, str(datetime.timedelta(seconds=p.duration))))
                i = i + 1

async def process_song(message: str):
        ydl_opts = {}

        if(message.startswith("https://www.youtube.com/")):
                pass
        else:
                ydl_opts = {'default_search': 'ytsearch:'}
        new_song = None
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        with ydl:
                result = ydl.extract_info(message, download=False)
        new_song = song(result['id'])
        new_song.title = result['title']
        new_song.uploader = result['uploader']
        new_song.duration = result['duration']
        song_list.append(new_song)

@client.command(pass_context=True)
async def stop(context):
        voice_client = client.voice_client_in(context.message.server)
        if voice_client is None:
                await client.say("I'm not connected")
        else:
                player = player_dict[voice_client.server]
                player.pause()
                await asyncio.sleep(5)
                await client.say("I'm connected")
                player.resume()
        
@client.command(pass_context=True)
async def volume(context, message: str):
        print(message)
        voice_client = client.voice_client_in(context.message.server)
        if voice_client is None:
                await client.say("I'm not connected")
        elif 0 <= float(message) <= 200:
                player = player_dict[voice_client.server]
                player.volume = float(message) / 100
        else:
                await client.say("Nah man.")

client.run(token)
