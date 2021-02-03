# bot.py
import os

import asyncio
import discord
from dotenv import load_dotenv
from detect_names import exists_player


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# client = discord.Client()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        # channel = self.get_channel(1234567) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60) # task runs every 60 seconds



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def background_check():
    await client.wait_until_ready()

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to following guilds:')
    print(f'{guild.name} (id: {guild.id})')
    #
    print(f'{guild.name} has: {len(guild.members)} members')
    # members = '\n - '.join([f'{member.name} | {member.nick}' for member in guild.members])
    # print(f'Names: \n - {members}')

    # player_check = [f'{member.name} | {member.nick} | {exists_player(member.nick)} ' for member in guild.members]

    # print(player_check)

    while not client.is_closed():
        for member in guild.members:
            if member.name == 'Test Bot - OSRS':
                continue

            player_exists = exists_player(member.nick)

            if member.nick is None:
                # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')
                await member.send(
                    f'Hello {member.name}, please remember to add your username as your nickname!'
                )

            elif not player_exists:
                # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')
                await member.send(
                    f'Hi {member.name}, please update your user name! (is it still {member.nick}?)'
                )

        await asyncio.sleep(60*60*24)  # task runs every day

client.loop.create_task(background_check())

@client.event
async def member_join(member):
    await member.send(
        f'Welcome to the clan, {member.name}!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(TOKEN)