import discord
import asyncio
from discord.ext import commands
import datetime
import song

client = commands.Bot(command_prefix='!', description="")
token = 'MjYxMjcyNDY2NzE3MDE2MDc0.C0GBrw.nTyS9_lZMfOznPKmPOhXmUvtgik'

player_dict = dict()
song_list = list()

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
        voice_chan = context.message.author.voice_channel
        active_player = player_dict[context.message.server]
        if voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
        elif active_play is not None:
                await client.say("adding to queue")
                song_list.append(message)
        elif(message.startswith("https://www.youtube.com/")):
                voice = await client.join_voice_channel(voice_chan)
                player = await voice.create_ytdl_player(message, use_avconv=True)
                await client.say(("{} - {} ({})").format(player.title, player.uploader, str(datetime.timedelta(seconds=player.duration))))
                player_dict[voice.server] = player 
                player.start()
                
@client.command(pass_context=True)
async def queue(context):
        

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
