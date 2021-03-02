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

    if before.name == after.nick:
        return

    print(before.name)

    # if before.name.lower() == after.nick.lower() and exists_player(after.nick):
    #     await after.send(
    #         f'Appreciate your effort, {after.nick}!'
    #     )

    if exists_player(after.nick):
        await after.send(
            f'Looks great, thanks {after.nick}!'
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


def check(m):
    return m.content != '' and m.author != client.user


@client.event
async def on_member_join(member: discord.Member):
    await member.send(
        f'Hi {member.name}, welcome to {member.guild.name}, we\'re glad to have you here!'
    )

    await member.send(
        f"Please feel free to edit your nickname manually if your name doesn't match your in-game name - or I can take your username here (as it looks in-game):"
    )

    try:
        msg = await client.wait_for("message", check=check)

        ign = msg.content
        # print(ign)
        # member = ctx.message.author
        if exists_player(ign):
            await member.edit(nick=ign)

        else:
            await member.send(f"Hmm I'm not finding a match for {ign}. Please try changing your name manually")
            # await name(member)
    except discord.errors.Forbidden:
        print(member.guild.name)
        await member.send(
            f"Ah dang, I don't have the permissions to edit nicknames in {member.guild.name}, please change it manually"
        )

    except asyncio.TimeoutError:
        await member.send(
            f"Or please change it manually"
        )


async def background_check():
    """background_check Method

    Checks all users in the background for whether their name is in the high scores.
    Messages a max of 1x per day
    """
    await client.wait_until_ready()

    global member_dict

    member_dict = {member: None for member in client.get_all_members()}

    while not client.is_closed():

        for member in member_dict:

            # skip bots
            if member.bot:
                continue

            last_checked = member_dict[member]

            # debug: print(f'{member.name}, {member.nick} | {last_checked}')

            # message once per day
            if last_checked is not None and last_checked + timedelta(days=1) > datetime.now():
                continue

            # cases:
            # 1. exists nick: great
            # 2. no nickname and exists name: ask once
            # 3. no nick and not exists name: ask daily until fixed
            # 4. no hs nick and exists name: ask daily until fixed
            # 5. no hs nick and not exists name: ask daily until fixed

            # 1. if player exists, set check time and we're good for the day
            if exists_player(member.nick):
                member_dict[member] = datetime.now()
                continue

            # 2. player exists but no nickname, maybe couldn't set nickname to exact name
            elif member.nick is None and exists_player(member.name):

                # try:
                #     await member.edit(nick=member.name, reason='update nickname to name for consistency')
                # except discord.errors.Forbidden:
                #     print(f"Can't edit names in {member.guild.name}")

                # member_dict[member] = datetime.now()
                member_dict[member] = datetime.now()
                continue
                # await member.send(
                #     f'If your in-game name is {member.name}, I\'m impressed with your identity consistency!'
                #     f'If not, please update your nickname in {member.guild.name} so we know who you are.'
                # )
                # await member.edit(nick=member.name)
                # member_dict[member] = datetime.now()

            # 3. if no nickname and regular name doesn't match
            elif member.nick is None and not exists_player(member.name):
                await member.send(
                    f'Hello {member.name}, please remember to add your in-game name as your nickname in {member.guild.name}!'
                )
                member_dict[member] = datetime.now()

            # if member.nick is None:
            #     await member.send(
            #         f'Hello {member.name}, please remember to add your username as your nickname in {member.guild.name}!'
            #     )

                # await member.send(
                #     f"Could you please add a nickname? Please enter as it appears in game."
                # )
                #
                # try:
                #     msg = await client.wait_for("message", check=check, timeout=60)  # 60 seconds to reply
                #
                #     ign = msg.content
                #     print(ign)
                #     # member = ctx.message.author
                #     if exists_player(ign):
                #         await member.send(f"Looks great, thanks {ign}!")
                #         await member.edit(nick=ign)
                #
                #     else:
                #         await member.send(f"Hmm I'm not finding a match for {ign}. Try again?")
                #         # await name(member)
                #
                # except asyncio.TimeoutError:
                #     print('time out')

            # if no nickname and regular name doesn't match

            elif not exists_player(member.nick):
                await member.send(
                    f'Hey {member.nick}, friendly reminder to update your nickname in {member.guild.name} to your in-game name!'
                )
                member_dict[member] = datetime.now()

        # seconds between loop
        await asyncio.sleep(60)

@client.command(
    name='ping',
    brief="Returns bot latency"
)
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

# @client.command(name="update")
# async def update(ctx, *args):
#
#     member = ctx.message.author
#     guild = ctx.guild
#
#     # ign = ' '.join(args)
#
#     await member.send(f"I can update your nickname for {guild} here - ")
#
#     await name(member)


@client.command(
    name="timer",
    brief='Returns time until next message'
)
async def timer(ctx):
    last_checked = member_dict[ctx.message.author]

    if last_checked is None:
        next_message = datetime.now() + timedelta(days=1)
    else:
        next_message = last_checked + timedelta(days=1)
    await ctx.send(f'Next reminder will be at: {next_message.strftime("%m/%d/%Y, %H:%M:%S")}.')


@client.command(
    name="ignore",
    brief='Allows you to turn off notifications from the bot for a pretty long time'
)
async def ignore(ctx):
    member_dict[ctx.message.author] = datetime.now() + timedelta(days=365*2)
    await ctx.send(f"You got it, no more from me.")


client.loop.create_task(background_check())

client.run(TOKEN)
