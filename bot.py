# name checking
import os

import asyncio
import discord
from discord.ext import commands
from detect_names import exists_player
from datetime import datetime, timedelta

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
# client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_update(before, after):

    # ignore if not a name change
    if before.nick == after.nick:
        return

    if before.bot:
        return

    # If no nickname and normal name doesn't exist
    if before.nick is None and not exists_player(before.name):
        if exists_player(after.nick):
            await after.send(f'Thanks {after.nick}!')

        else:
            await after.send(f'Hmm, it looks like {after.nick} might not be right.')

    ##  for debugging
    # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')
    if not exists_player(after.nick):
        await member.send(
            f'Hey {after.nick}, could there be a typo? It looks like this player might not exist. '
        )

async def background_check():
    await client.wait_until_ready()

    # members = '\n - '.join([f'{member.name} | {member.nick}' for member in guild.members])
    # print(f'Names: \n - {members}')

    member_dict = {member: None for member in client.get_all_members()}

    # player_check = [f'{member.name} | {member.nick} | {exists_player(member.nick)} ' for member in guild.members]

    while not client.is_closed():

        for member, last_messaged in member_dict.items():
            if member.bot:
                continue

            # message once per day
            if last_messaged is not None and last_messaged + timedelta(days=1) > datetime.now():
                continue

            # for debugging
            # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')

            if member.nick is None and not exists_player(member.name) and last_messaged is None:
                await member.send(
                    f'Hello {member.name}, please remember to add your username as your nickname in {member.guild.name}!'
                )
                member_dict[member] = datetime.now()

            if not exists_player(member.nick):
                await member.send(
                    f'Hi {member.nick}, it looks like your username may have changed, please update your nickname in {member.guild.name} to match :)'
                )
                member_dict[member] = datetime.now()

        await asyncio.sleep(10)  # task runs every day 60*60*24

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command(name="ignore")
async def ignore(ctx):
    await ctx.send(f"Got it, no more from me for now")


client.loop.create_task(background_check())

client.run(TOKEN)