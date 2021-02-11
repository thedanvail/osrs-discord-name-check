# name checking
import os

import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from detect_names import exists_player


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')

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


async def background_check():
    await client.wait_until_ready()

    # for guild in client.guilds:
    #     if guild.name == GUILD:
    #         break

    # print(f'{client.user} has connected to following guilds:')
    # print(f'{guild.name} (id: {guild.id})')
    # print(f'{guild.name} has: {len(guild.members)} members')


    # members = '\n - '.join([f'{member.name} | {member.nick}' for member in guild.members])
    # print(f'Names: \n - {members}')

    # player_check = [f'{member.name} | {member.nick} | {exists_player(member.nick)} ' for member in guild.members]

    while not client.is_closed():

        for member in client.get_all_members():
            if member.bot:
                continue

            player_exists = exists_player(member.nick)
            ##  for debugging
            # print(f'{member.name} | {member.nick} | {exists_player(member.nick)}')

            if member.nick is None:
                await member.send(
                    f'Hello {member.name}, please remember to add your username as your nickname!'
                )

            elif not player_exists:
                await member.send(
                    f'Hi {member.nick}, it looks like your username may have changed, please update your nickname in {member.guild.name} to match :)'
                )

        await asyncio.sleep(60)  # task runs every day

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

# @client.command()
# async def clear(ctx, amount=3) :
#     await ctx.channel.purge(limit=amount)

client.loop.create_task(background_check())

client.run(TOKEN)