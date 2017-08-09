import discord
from discord.ext import commands
import asyncio
from collections import deque

class YouTubePlayer:

	channels = {}
	voice = None
	players = deque()
	current_player = None
	playing = False
	paused = False
	command_processing = False

	def __init__(self, bot):
		self.bot = bot

	def setVoiceElements(self, voice, channels):
		self.voice = voice
		self.channels = channels

	def check_if_playing(self):
		return self.playing

	async def wait_on_player(self):
		self.command_processing = False
		while self.current_player.is_playing() or self.paused:
			await asyncio.sleep(5)
		if self.playing and (self.current_player.is_playing() != True):
			self.playing = False

	async def play(self, youtube_url):
		if self.command_processing:
			await self.bot.say('Don\'t spam!')
		else:
			if (self.playing or self.paused):
				self.paused = False
				self.command_processing = True
				self.current_player.stop()
				self.current_player = await self.voice.create_ytdl_player(youtube_url)
				self.current_player.start()
				self.playing = True
				await self.wait_on_player()
				
			else:
				self.command_processing = True
				self.current_player = await self.voice.create_ytdl_player(youtube_url)
				self.current_player.start()
				self.playing = True
				await self.wait_on_player()

	def play_yt_links(self):
		self.current_player.volume = 0.2
		self.current_player.start()
		self.playing = True

	def toggle_pause(self):
		if self.playing:
			if self.paused:
				self.current_player.resume()
				self.paused = False
			else:
				self.current_player.pause()
				self.paused = True

	async def stop_yt_playing(self):
		if self.playing:
			self.current_player.stop()
			self.playing = False
			self.paused = False
		else:
			await self.bot.say('Nothing\'s playing')