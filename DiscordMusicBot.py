import discord
import asyncio
from discord.ext import commands
import datetime
import youtube_dl
from collections import deque
from discordserver import discordserver
import random
import os
from dateutil import parser
import math
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


client = commands.Bot(command_prefix='!', description="")
token = config['DEFAULT']['token']

server_dict = {}
numbers = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':1,'j':2,'k':3,'l':4,'m':5,'n':6,'o':7,'p':8}



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')
	#Creates file if it doesn't exist
	f = open("accident.txt", "w+")
	f.close()

@client.command(pass_context=True)
async def accident(context, message:str):
        strtime = str(datetime.datetime.now())
        f = open("accident.txt", "r+")
        if(os.stat("accident.txt").st_size == 0):
                f.write(strtime)
        last_accident = f.readline()
        if(message == "last"):
                await client.say("The last time Cookie fucked us in a car was " + parser.parse(last_accident))
                print(delta)
        elif(message == "new"):
                print("value was new")
        else:
                print("value was wrong")


def is_command(m):
        return (m.content == "!genji") or (m.content == "!nosey") or (m.content == "!tidus") or (m.content == "!cleanup") or (m.author == client.user)
            
@client.command(pass_context=True)
async def cleanup(context):
        await client.purge_from(context.message.channel, limit=100, check=is_command)

@client.command(pass_context=True)
async def wadu(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/wadu'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/wadu/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Wadu"
        player.uploader = "Wadu"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Wadu")

@client.command(pass_context=True)
async def trump(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/trump'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/trump/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Trump"
        player.uploader = "WTrumpadu"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit WaTrumpdu")


@client.command(pass_context=True)
async def wednesday(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        if (datetime.datetime.today().weekday() == 2):
                player = bot_voice_chan.create_ffmpeg_player('sound_bites/wednesday.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        else:
                player = bot_voice_chan.create_ffmpeg_player('sound_bites/notwednesday.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Wednesday"
        player.uploader = "Wednesday"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Data")


@client.command(pass_context=True)
async def data(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/data.wav', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Data"
        player.uploader = "Data"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Data")

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
        await client.delete_message(context.message)
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
        await client.delete_message(context.message)
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
        await client.delete_message(context.message)
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
        player.volume = 0.15
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
        voice_client = client.voice_client_in(context.message.server)
        if voice_client is None:
                await client.say("I'm not connected")
        else:
                server_dict[context.message.server.id].current_player.stop()
                await client.say("Skipping.")       
        
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

@client.command(pass_context=True)
async def e(context, start: str, end: str):

        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        
        start_x = numbers[start[0]]
        start_y = numbers[start[1]]
        end_x = numbers[end[0]]
        end_y = numbers[end[1]]

        dx = math.fabs(start_x - end_x)
        dy = math.fabs(start_y - end_y)
        x = start_x
        y = start_y
        n = 1 + dx + dy
        x_inc = 1 if (end_x > start_x) else -1
        y_inc = 1 if (end_y > start_y) else -1
        error = dx-dy
        dx = dx * 2
        dy = dy * 2

        valid_points = []
        
        while(n>0):
                valid_points.append(tuple((x,y)))
                if(error > 0):
                        x = x + x_inc
                        error = error - dy
                else:
                        y = y + y_inc
                        error = error + dx
                n = n - 1
        valid_drop = False
        file = ''
        while(not valid_drop):
                file = random.choice(os.listdir('sound_bites/Erangel'))
                code = file[-6:-4]
                codeTuple = tuple((numbers[code[0]],numbers[code[1]]))
                if(codeTuple in valid_points):
                        valid_drop = True
        
        if(valid_drop):
                player = bot_voice_chan.create_ffmpeg_player('sound_bites/Erangel/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
                player.title = "Erangel"
                player.uploader = "Erangel"
                player.duration = 0
                submit_audio_to_queue(context, player)
                await client.delete_message(context.message)
                print("Submit Erangel")      

@client.command(pass_context=True)
async def m(context, start: str, end: str):

        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        
        start_x = numbers[start[0]]
        start_y = numbers[start[1]]
        end_x = numbers[end[0]]
        end_y = numbers[end[1]]

        dx = math.fabs(start_x - end_x)
        dy = math.fabs(start_y - end_y)
        x = start_x
        y = start_y
        n = 1 + dx + dy
        x_inc = 1 if (end_x > start_x) else -1
        y_inc = 1 if (end_y > start_y) else -1
        error = dx-dy
        dx = dx * 2
        dy = dy * 2

        valid_points = []
        
        while(n>0):
                valid_points.append(tuple((x,y)))
                if(error > 0):
                        x = x + x_inc
                        error = error - dy
                else:
                        y = y + y_inc
                        error = error + dx
                n = n - 1
        valid_drop = False
        file = ''
        while(not valid_drop):
                file = random.choice(os.listdir('sound_bites/Miramar'))
                code = file[-6:-4]
                codeTuple = tuple((numbers[code[0]],numbers[code[1]]))
                if(codeTuple in valid_points):
                        valid_drop = True
        
        if(valid_drop):
                player = bot_voice_chan.create_ffmpeg_player('sound_bites/Miramar/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
                player.title = "Miramar"
                player.uploader = "Miramar"
                player.duration = 0
                submit_audio_to_queue(context, player)
                await client.delete_message(context.message)
                print("Submit Miramar")

@client.command(pass_context=True)
async def mr(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/Miramar'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Miramar/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Miramar"
        player.uploader = "Miramar"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Miramar")

@client.command(pass_context=True)
async def er(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/Erangel'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Erangel/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "MiErangelramar"
        player.uploader = "MirErangelamar"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit MirErangelamar")


@client.command(pass_context=True)
async def best(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!BEST.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Best"
        player.uploader = "Best"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Best")

@client.command(pass_context=True)
async def boom(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!BOOM.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Boom"
        player.uploader = "Boom"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Boom")

@client.command(pass_context=True)
async def noob(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/NOOB.m4a', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Noob"
        player.uploader = "Noob"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Noob")

@client.command(pass_context=True)
async def dying(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!DYING.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "Dyring"
        player.uploader = "Dying"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit Dying")

@client.command(pass_context=True)
async def espn(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!ESPN.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "ESPN"
        player.uploader = "ESPN"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit ESPN")

@client.command(pass_context=True)
async def fury(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!FURY.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit FURY")

@client.command(pass_context=True)
async def gay(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!GAY.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit GAY")

@client.command(pass_context=True)
async def gaybois(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!GAYBOIS.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit GAYBOIS")

@client.command(pass_context=True)
async def hero(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!HERO.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit HERO")

@client.command(pass_context=True)
async def idiot(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!IDIOT.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit IDIOT")

@client.command(pass_context=True)
async def kills(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!KILLS.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit KILLS")

@client.command(pass_context=True)
async def kobe(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!KOBE.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit KOBE")

@client.command(pass_context=True)
async def mistake(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!MISTAKE.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit MISTAKE")

@client.command(pass_context=True)
async def nooo(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!NOOO.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit NOOO")

@client.command(pass_context=True)
async def organization(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!ORGANIZATION.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit ORGANIZATION")

@client.command(pass_context=True)
async def perfection(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!PERFECTION.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit PERFECTION")

@client.command(pass_context=True)
async def puerto(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!PUERTO.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit PUERTO")

@client.command(pass_context=True)
async def rip(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!RIP.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit RIP")

@client.command(pass_context=True)
async def sadness(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!SADNESS.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit SADNESS")

@client.command(pass_context=True)
async def school(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!SCHOOL.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit SCHOOL")

@client.command(pass_context=True)
async def shit(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!SHIT.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit SHIT")

@client.command(pass_context=True)
async def sogood(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!SOGOOD.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit SOGOOD")

@client.command(pass_context=True)
async def walls(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!WALLS.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit WALLS")

@client.command(pass_context=True)
async def wall(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!WALL.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit WALL")

@client.command(pass_context=True)
async def yank(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!YANK.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit YANK")

@client.command(pass_context=True)
async def yayaya(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!YAYAYA.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit YAYAYA")

@client.command(pass_context=True)
async def hacienda(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!HACIENDA.mp3', use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit HACIENDA")

@client.command(pass_context=True)
async def fuck(context):
        bot_voice_chan = await get_voice_client(context)
        if bot_voice_chan is None:
                await client.say("You must be in a voice channel to play audio")
                return None
        file = random.choice(os.listdir('sound_bites/Commands/!FUCK'))
        player = bot_voice_chan.create_ffmpeg_player('sound_bites/Commands/!FUCK/' + file, use_avconv=True, after=lambda: after_audio_completed(context.message.server))
        player.title = "FUCK"
        player.uploader = "FUCK"
        player.duration = 0
        submit_audio_to_queue(context, player)
        await client.delete_message(context.message)
        print("Submit FUCK")



client.run(token)
