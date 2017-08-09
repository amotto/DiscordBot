import discord
from discord.ext import commands
import asyncio
from collections import deque
import youtube_player
import bot_utils
import random

description = '''A bot that attempts to meme. 
				Use at your own discretion. 
				Results may vary.'''

bot = commands.Bot(command_prefix='$', description=description)
yt = youtube_player.YouTubePlayer(bot=bot)
bot_helper = bot_utils.BotHelper(bot)

@bot.event
async def on_ready():
	channels = {}
	for channel in list(bot.get_all_channels()):
		channels[channel.name] = channel
	bot_helper.set_channels(channels)

@bot.command()
async def test():
	await bot.say('reading loud and clear')

@bot.command()
async def join(*channel : str):
	channel_name = " ".join(channel)
	if not bot_helper.query_channel(channel_name):
		await bot.say('No such voice channel')
	else:
		await bot_helper.join_voice_channel(channel_name)
		yt.setVoiceElements(voice=bot_helper.get_voice_client(), channels=bot_helper.get_channels_dict())

@bot.command()
async def disconnect():
	if bot_helper.check_voice_connected():
		await bot_helper.disconnect_voice_client()

@bot.command()
async def stop():
	await yt.stop_yt_playing()

@bot.command()
async def pause():
	yt.toggle_pause()

@bot.command()
async def play(youtube_url : str):
	await yt.play(youtube_url)

@bot.command()
async def twitch(streamer : str):
	await bot.say('https://www.twitch.tv/' + streamer)

@bot.command()
async def tts():
	if bot_helper.tts_allowed():
		bot_helper.tts_toggle()
		await bot.say('TTS callouts turned off')
	else:
		bot_helper.tts_toggle()
		await bot.say('TTS callouts turned on')

@bot.command()
async def tts_dest(*destination : str):
	bot_helper.set_tts_channel(" ".join(destination))
	await bot.say('TTS callouts destination is %s' % destination)

@bot.event
async def on_voice_state_update(b_member, a_member):
	if bot_helper.check_voice_connected() and bot_helper.tts_allowed():
		bot_channel = bot_helper.get_voice_client().channel
		destination_channel = bot_helper.get_tts_channel()
		if (b_member.voice_channel != a_member.voice_channel) and (a_member.voice_channel == bot_channel) and (a_member.id != bot.user.id):
			message = ('%s joined %s' % (a_member.name, bot_channel.name))
			await bot.send_message(destination_channel, message, tts=True)

@bot.command()
async def end():
	await bot.say('shutting down...')
	await bot.close()

def __main__():
	bot.run('MzQzODI4NDIzNDUxNDc1OTcw.DGkQXg.Q73M7V7LVWKITtGdOtHDJRnC1KA')

if __name__ == "__main__":
	__main__()
