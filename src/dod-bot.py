import os

import discord
import string
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class DodClient(discord.Client):
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

if __name__ == "__main__":
    client = DodClient()   
    client.run(TOKEN)
    