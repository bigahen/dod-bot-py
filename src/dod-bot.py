import os

import discord
from discord import Message
from discord import VoiceChannel
import string
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class DodClient(discord.Client):

    localAudioCommands = {
        'radio': 'src/audio/radio.mp3',
        'cool': 'src/audio/cool.m4a',
        'no!': 'src/audio/no.mp3',
        'you\'re fired': 'src/audio/fired.mp3'
    }

    async def _join_and_play(self, message: Message):
        
        author = message.author

        if author == None:
            return

        voice_channel = author.voice

        if voice_channel == None:
            await message.channel.send('You need to be in a channel to send a message 🙂')
            return 
 
        to_play = self.localAudioCommands[message.content.lower()]

        joined_channel = await voice_channel.channel.connect()
        joined_channel.play(discord.FFmpegPCMAudio(source=to_play))
        #player = joined_channel.create_ffmpeg_player(to_play, after=lambda : print("Finished Playing Audio"))
        #joined_channel.start()
        while joined_channel.is_playing():
            await asyncio.sleep(.1)
        await joined_channel.disconnect()

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f'Yo {member.name}, don\'t be a Dod in my server!')

    async def on_message(self, message):
        # Ignore message sent by the bot 
        if message.author == self.user:
            return 

        m = message.content

        # Strip puncutiation and then split into words 
        words = m.translate(str.maketrans('', '', string.punctuation)).lower().split()

        #Add reaction to messages containing the word 'sir' 
        if 'sir' in words:
            await message.add_reaction('🎩')

        #Check is message is in audio commands
        if m.lower() in self.localAudioCommands.keys():
            await self._join_and_play(message)
    

if __name__ == "__main__":
    client = DodClient()   
    client.run(TOKEN)
    