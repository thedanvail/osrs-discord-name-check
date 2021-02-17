# name checking
import os

import asyncio
import discord
from discord.ext import commands
from detect_names import exists_player
from datetime import datetime, timedelta



from dotenv import load_dotenv

load_dotenv()
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
    """on_member_update Method

    Detects and messages a user when their nickname changes
    """

    # ignore if not a name change
    if before.nick == after.nick:
        return

    if before.bot:
        return

    print(before.name)

    if exists_player(after.nick):
        await after.send(
            f'Looks good, thanks {after.nick}!'
        )
        return

    elif after.nick is None and not exists_player(after.name):
        await after.send(
            f'Did you just remove your nickname? It looks like your discord name doesn\'t quite match.'
        )
        return

    # If no nickname and normal name doesn't exist
    elif not exists_player(before.name) and not exists_player(after.nick):
            await after.send(
                f'Hmm, it looks like {after.nick} might not be right.'
            )
            return

    elif not exists_player(after.nick):
        await after.send(
            f'Hey {after.nick}, could there be a typo? I can\'t find you in the high scores.'
        )
        return

async def background_check():
    """background_check Method

    Checks all users in the background for whether their name is in the high scores.
    Messages a max of 1x per day
    """
    await client.wait_until_ready()

    member_dict = {member: None for member in client.get_all_members()}

    while not client.is_closed():

        for member, last_messaged in member_dict.items():
            if member.bot:
                continue

            # message once per day
            if last_messaged is not None and last_messaged + timedelta(days=1) > datetime.now():
                continue

            print(member.name)

            if member.nick is None and not exists_player(member.name) and last_messaged is None:
                await member.send(
                    f'Hello {member.name}, please remember to add your username as your nickname in {member.guild.name}!'
                )
                member_dict[member] = datetime.now()

            elif not exists_player(member.nick):
                await member.send(
                    f'Hi {member.nick}, it looks like your username may have changed, please remeber to update your nickname in {member.guild.name} to match!'
                )
                member_dict[member] = datetime.now()

        await asyncio.sleep(10)  # task runs every day 60*60*24

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

# @client.command(name="update")
# async def update(ctx):
#     await ctx.send(f"I can update your nickname here if you want")
#     await ctx.fetch_message()

# @client.command(name="ignore")
# async def ignore(ctx):
#     await ctx.send(f"")

client.loop.create_task(background_check())

client.run(TOKEN)
