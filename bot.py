import os
import time
import random
import asyncio
import discord_webhook
import dotenv
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL = int(os.getenv("WELCOME_CHANNEL"))
OWNER_ID = int(os.getenv("OWNER_ID"))

# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_times = {}

quotes = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "Do what you can, with what you have, where you are. – Theodore Roosevelt",
    "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "It always seems impossible until it’s done. – Nelson Mandela",
    "Everything you’ve ever wanted is on the other side of fear. – George Addair",
    "Act as if what you do makes a difference. It does. – William James",
]

dogs = [
    "https://tse1.mm.bing.net/th/id/OIP.Jf0NnGpH2AhNM3BtwZufwwHaJ4",
    "https://tse2.mm.bing.net/th/id/OIP.kKBf8FoNYCG-9E7hco2DEAHaEo",
    "https://tse4.mm.bing.net/th/id/OIP.5aKhA8rhSGnJzNnkGJgtLwHaLH",
]

jokes = [
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "How do you organize a space party? You planet.",
    "Why did the bicycle fall over? Because it was two-tired.",
    "What do you call cheese that isn't yours? Nacho cheese.",
]

welcome_messages = [
    "Welcome to the server, {member.mention}! Hope you like ice cream!",
    "Welcome to the server, {member.mention}! Hope you play video games!",
    "Welcome to the server, {member.mention}! We’ve been expecting you!",
    "Welcome to the server, {member.mention}! How’s your day been?",
    "Welcome to the server, {member.mention}! hope you like the basement to the basement!",
]

dumb_quotes = [
    "Why Overthink Or Underthink, When You Dont Have To Think",
    "If You Are Dumb You Are Dumb",
    "Bob",
    "Bootleg",
]

def owner_only():
    async def predicate(ctx):
        if ctx.author.id != OWNER_ID:
            await ctx.send("Only the bot owner can use this command.")
            raise commands.CheckFailure("User is not the bot owner.")
        return True
    return commands.check(predicate)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=" The Matrix "))
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL)
    if channel:
        await channel.send(random.choice(welcome_messages).format(member=member))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    now = time.time()
    uid = message.author.id
    user_times.setdefault(uid, []).append(now)
    user_times[uid] = [t for t in user_times[uid] if now - t < 10]

    if len(user_times[uid]) > 5:
        await message.channel.send(f"{message.author.mention}, please stop spamming!")
        owner = await bot.fetch_user(OWNER_ID)
        await owner.send(f"Spam detected from {message.author} in #{message.channel}")
        user_times[uid] = []

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return  
    with open("command_log.txt", "a") as f:
        f.write(f"{ctx.author} tried command: {ctx.message.content} [ERROR: {error}]\n")
    await ctx.send(f"Error: {error}")

async def get_or_create_muted_role(guild):
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if not muted_role:
        muted_role = await guild.create_role(name="Muted", reason="Create Muted role for muting users")
        for channel in guild.channels:
            try:
                await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
            except Exception:
                pass
    return muted_role


@bot.command()
@owner_only()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked. {'Reason: ' + reason if reason else ''}")

@bot.command()
@owner_only()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned. {'Reason: ' + reason if reason else ''}")

@bot.command()
@owner_only()
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = await get_or_create_muted_role(ctx.guild)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted indefinitely. {'Reason: ' + reason if reason else ''}")

@bot.command()
@owner_only()
async def timemute(ctx, member: discord.Member, duration: int = 10, *, reason=None):
    if duration <= 0:
        await ctx.send("Duration must be a positive integer!")
        return

    muted_role = await get_or_create_muted_role(ctx.guild)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {duration} minutes. {'Reason: ' + reason if reason else ''}")

    await asyncio.sleep(duration * 60)

    if muted_role in member.roles:
        await member.remove_roles(muted_role, reason="Timed mute expired")
        await ctx.send(f"{member.mention} has been unmuted after {duration} minutes.")

@bot.command()
@owner_only()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role and muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted.")

@bot.command(name="start_monitor")
@owner_only
async def startmonitor(ctx):
    if discord_webhook.start_monitor():
        await ctx.send("Website monitor started!")
    else:
        await ctx.send("Monitor is already running.")


@bot.command(name="stop_monitor")
@owner_only
async def stopmonitor(ctx):
    if discord_webhook.stop_monitor():
        await ctx.send("Website monitor stopped.")
    else:
        await ctx.send("Monitor is not running.")

    
# --- Public Commands ---
@bot.command()
async def info(ctx):
    await ctx.send("**CyberFish Discord Bot** – Made by BootlegFish!\nHere are some available commands:")
    commands_list = [
        "!info", "!hello", "!ZY", "!rice", "!quote", "!dog", "!joke", "!credits", "!latest",
        "!mute", "!timemute", "!unmute", "!kick", "!ban"
    ]
    await ctx.send(", ".join(commands_list))
    await ctx.send("Note: This bot is still in **beta testing!**")

@bot.command()
async def latest(ctx):
    await ctx.send("Latest Features: Added !dumbquote and bugfixes")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Wsg, {ctx.author.mention}!")

@bot.command()
async def ZY(ctx):
    await ctx.send("ZY RULES")

@bot.command()
async def rice(ctx):
    await ctx.send("AACubing disses Bootleg Rice...")

@bot.command()
async def credits(ctx):
    await ctx.send("**Credits:**")
    await asyncio.sleep(1)
    await ctx.send("• Bootleg Fish: Developer → https://thebtlgfish.github.io")
    await asyncio.sleep(1)
    await ctx.send("• AAcubing (Bootleg Creator): Emotional Support")
    await asyncio.sleep(1)
    await ctx.send("• Thanks to the ZY Cult for all the support!")

@bot.command()
async def quote(ctx):
    await ctx.send(random.choice(quotes))

@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command()
async def dog(ctx):
    await ctx.send(random.choice(dogs))

@bot.command()
async def dumbquote(ctx):
    await ctx.send(random.choice(dumb_quotes))


bot.run(TOKEN)
