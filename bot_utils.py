import discord
import asyncio

class BotHelper:
	channels = {}
	voice_client = None
	voice_connected = False
	tts_setting = False
	tts_destination_channel = "general"

	def __init__(self, bot):
		self.bot = bot

	def set_channels(self, channels):
		self.channels = channels

	def set_voice_client(self, voice):
		self.voice_client = voice
		self.voice_connected = True

	def set_tts_channel(self, tts_channel):
		self.tts_destination_channel = tts_channel

	def get_tts_channel(self):
		return self.get_channel(self.tts_destination_channel)

	def get_voice_client(self):
		return self.voice_client

	async def join_voice_channel(self, channel_name):
		if self.voice_connected:
			await self.voice_client.move_to(self.get_channel(channel_name))
		else:
			voice = await self.bot.join_voice_channel(self.get_channel(channel_name))
			self.set_voice_client(voice)
			self.voice_connected = True

	async def disconnect_voice_client(self):
		await self.voice_client.disconnect()
		self.voice_client = None
		self.voice_connected = False

	def get_channel(self, channel_name):
		return self.channels[channel_name]

	def get_channels_dict(self):
		return self.channels

	def check_voice_connected(self):
		return self.voice_connected

	def tts_allowed(self):
		return self.tts_setting

	def tts_toggle(self):
		self.tts_setting = not self.tts_setting

	def query_channel(self, channel_name):
		if channel_name in self.channels:
			return True
		else:
			return False