# bot.py
import os

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

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to following guilds:')
    print(f'{guild.name} (id: {guild.id})')

    print(f'Guild members: {len(guild.members)}')
    members = '\n - '.join([f'{member.name} | {member.nick}' for member in guild.members])
    print(f'Names: \n - {members}')

    for member in guild.members:
        if member.name == 'Test Bot - OSRS':
            continue

        player_exists = exists_player(member.nick)
        if member.nick is None:
            # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')
            await member.send(
                f'Hello {member.name}, please remember to add your username!'
            )

        elif not player_exists:
            # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')
            await member.send(
                f'Hi {member.name}, please update your user name! (is it still {member.nick}?)'
            )

    # player_check = [f'{member.name} | {member.nick} | {exists_player(member.nick)} ' for member in guild.members]

    # print(player_check)

async def my_background_task(member):
    await client.wait_until_ready()
    while not client.is_closed:
        await asyncio.sleep(60*60*24)  # task runs every 60 seconds


@client.event
async def member_join(member):
    pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(TOKEN)