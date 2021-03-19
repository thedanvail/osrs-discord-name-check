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


# LoA
# guild = client.get_guild(319781102950547457)


role_name = "Nickname Approved!"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    # print(client.user.id)
    for guild in client.guilds:
        print(guild)
        print(guild.id)
        print(guild.roles)
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
        member_dict[after] = datetime.now()
        await grant_approval(after)
        return

    elif after.nick is None and not exists_player(after.name):
        await after.send(
            f'Did you just remove your nickname? It looks like your discord name doesn\'t quite match.'
        )
        await remove_approval(after)
        return

    # If no nickname and normal name doesn't exist
    elif not exists_player(before.name) and not exists_player(after.nick):
        await after.send(
            f'Hmm, it looks like {after.nick} might not be right.'
        )
        await remove_approval(after)
        return

    elif not exists_player(after.nick):
        await after.send(
            f'Hey {after.nick}, could there be a typo? I can\'t find you in the high scores.'
        )
        await remove_approval(after)
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


# @bot.command(pass_context=True)
@commands.bot_has_permissions(manage_roles=True)
@commands.has_role(role_name)
async def remove_approval(user):
    try:
        role = discord.utils.get(guild.roles, name=role_name)
        await user.remove_roles(role)

    except discord.errors.Forbidden:
        print("Whoops, maybe you're trying to edit server admin?")

    else:
        await user.send("Sorry, gonna need you to update your name to your in-game name to approve you again!")



# @bot.command(pass_context=True)
@commands.bot_has_permissions(manage_roles=True)
@commands.has_role(role_name)
async def grant_approval(user):
    try:
        role = discord.utils.get(guild.roles, name=role_name)
        if role not in user.roles:
            await user.add_roles(role)
            await user.send(f"You're awesome, and you can now speak in {user.guild.name}")
            print(f"Role granted to {user.name} in {user.guild.name}")

    except discord.errors.Forbidden:
        print("Whoops, maybe you're trying to edit server admin?")

    else:
        print(f"Finished granting")
        # await user.send("You've been granted the speaking stick!")



# check name
#  if name exists, allow speaking

# if name no longer matches, give 5 days to change
# if not, then revoke role

# @client.command(pass_context=True)
@commands.bot_has_permissions(manage_roles=True)
@commands.has_role(role_name)
async def consider_approval(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name=role_name)
    # await ctx.send(role)
    if exists_player(member.nick):
        try:
            await member.add_roles(role)
        except discord.ext.commands.errors.BotMissingPermissions:
            await ctx.send("Ah, I don't have permission to save you, please contact your guild leader!")
        else:
            await ctx.send(f"hey {ctx.author.name}, {member.nick} has been giving a role called: {role.name}")

    else:
        await name_check(member)


async def background_check():
    """background_check Method

    Checks all users in the background for whether their name is in the high scores.
    Messages a max of 1x per day
    """
    await client.wait_until_ready()

    global member_dict
    global member_last_failed

    member_dict = {member: None for member in client.get_all_members()}

    member_last_failed = {member: None for member in client.get_all_members()}

    global guild

    # hwuh
    # guild = client.get_guild(797237739748851713)

    # bot testing
    guild = client.get_guild(699647540340981790)


    while not client.is_closed():

        for member in member_dict:

            # skip bots
            if member.bot:
                continue

            last_checked = member_dict[member]

            print(f'{member.name}, {member.nick} | {last_checked}')

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
                await grant_approval(member)
                continue

            # 2. player exists but no nickname, maybe couldn't set nickname to exact name
            elif member.nick is None and exists_player(member.name):

                try:
                    await member.edit(nick=member.name, reason='update nickname to name for consistency')
                except discord.errors.Forbidden:
                    print(f"Can't edit names in {member.guild.name}")

                member_dict[member] = datetime.now()

                await grant_approval(member)
                continue
                # await member.send(
                #     f'If your in-game name is {member.name}, I\'m impressed with your identity consistency!'
                #     f'If not, please update your nickname in {member.guild.name} so we know who you are.'
                # )
                # await member.edit(nick=member.name)
                # member_dict[member] = datetime.now()

            # 3. if no nickname and regular name doesn't match
            elif member.nick is None and not exists_player(member.name):

                member_dict[member] = datetime.now()
                await member.send(
                    f'Hello {member.name}, please remember to add your in-game name as your nickname in {member.guild.name}!'
                )
                await remove_approval(member)
                continue

            # if no nickname and regular name doesn't match

            elif not exists_player(member.nick):
                await member.send(
                    f'Hey {member.nick}, friendly reminder to update your nickname in {member.guild.name} to your in-game name!'
                )
                member_dict[member] = datetime.now()
                await remove_approval(member)

        # seconds between loop
        await asyncio.sleep(60)



@client.command(
    name='ping',
    brief="Returns bot latency"
)
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="update")
async def update(ctx, *args):

    member = ctx.message.author
    # ign = ' '.join(args)
    await name_check(member)


async def name_check(member):

    await member.send(f"""I can update your nickname for {guild} here - \n Please enter as it appears in game, I'll ignore anything after a | sign."""
    )

    try:
        msg = await client.wait_for("message", check=check, timeout=120)  # 60 seconds to reply

        ign = msg.content
        print(ign)

        await name_edit(member, ign)

    except asyncio.TimeoutError:
        await member.send("Please go ahead to manually edit your nickname, or try me again")


async def name_edit(member, name):
    # member = ctx.message.author

    if exists_player(name):
        try:
            await member.edit(nick=name)

        except discord.errors.Forbidden:
            await member.send(f"Ah, looks like I'm lacking permissions to edit in {guild.name}")

        except AttributeError:
            await member.send("Gotta invoke me from a guild channel! Sorry I don't make the rules.")

        except discord.ext.commands.errors.CommandInvokeError:
            await member.send("Something weird happened, sorry try again")

        else:
            # await member.send(f"Looks great, thanks {name}!")
            print('successful name add')

    else:
        await member.send(f"Hmm I'm not finding a match for {name}. Try again?")
        await name_check(member)

@client.command(
    name="timer",
    brief='Returns time until next check'
)
async def timer(ctx):
    last_checked = member_dict[ctx.message.author]

    if last_checked is None:
        next_message = datetime.now() + timedelta(days=1)
    else:
        next_message = last_checked + timedelta(days=1)

    await ctx.send(f'Next check will be at: {next_message.strftime("%m/%d/%Y, %H:%M:%S")}.')


@client.command(
    name="time",
    brief='Returns bot time'
)
async def time(ctx):
    current_time = datetime.now()
    await ctx.send(f'{current_time.strftime("%m/%d/%Y, %H:%M:%S")}')


@client.command(
    name="ignore",
    brief='Turn off notifications for a pretty long time'
)
async def ignore(ctx):
    member_dict[ctx.message.author] = datetime.now() + timedelta(days=365*2)
    await ctx.send(f"You got it, no more from me.")


client.loop.create_task(background_check())

client.run(TOKEN)
