import os
import time
import random
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL = int(os.getenv("WELCOME_CHANNEL"))
OWNER_ID = int(os.getenv("OWNER_ID"))


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
    "I have not failed. I've just found 10,000 ways that won't work. – Thomas Edison",
    "If you want to lift yourself up, lift up someone else. – Booker T. Washington",
    "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
    "The best way to get started is to quit talking and begin doing. – Walt Disney",
    "Whether you think you can or you think you can’t, you’re right. – Henry Ford",
    "Opportunities don't happen. You create them. – Chris Grosser",
    "Don’t wait. The time will never be just right. – Napoleon Hill",
    "Perseverance is not a long race; it is many short races one after the other. – Walter Elliot",
    "Hustle in silence and let your success make the noise. – Unknown",
    "Strive not to be a success, but rather to be of value. – Albert Einstein"
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
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "What do you call a bear with no teeth? A gummy bear.",
    "Why can’t your nose be 12 inches long? Because then it would be a foot.",
    "What do you call a snowman with a six-pack? An abdominal snowman."
]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="use !info"))
    print(f"✅ Bot is ready. Logged in as {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {str(error)}")
    print(f"Command Error: {error}")


@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL)
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! Hope you like ice cream.")

@bot.event
async def on_command(ctx):
    with open("command_log.txt", "a") as f:
        f.write(f"{ctx.author} used command: {ctx.message.content}\n")

@bot.event
async def on_command_error(ctx, error):
    with open("command_log.txt", "a") as f:
        f.write(f"{ctx.author} tried command: {ctx.message.content} [ERROR: {error}]\n")
    await ctx.send(f"Error: {error}")

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
        await owner.send(f"🚨 Spam detected from {message.author} in #{message.channel}")
        user_times[uid] = []

    await bot.process_commands(message)



@bot.command()
async def info(ctx):
    await ctx.send("Welcome to the CyberFish Discord Bot! This is a simple bot made by BootlegFish. Here are some of the commands you can use:")
    await ctx.send("Also Please Note That This Bot Is Still In Beta Testing")
    for command in ["!info", "!hello", "!bootleg", "!fish", "!ZY", "!rice", "!catnuke", "!stopcatnuke", "!quote", "!dog", "!joke", "!credits"]:
        await ctx.send(command)

@bot.command()
async def latest(ctx):
    await ctx.send("Latest Features: Added The latest Command and Welcoming Feature. Removed Cat Nuke (Due To Spamming). Updated Commands. Bug Fixes.")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Wsg, {ctx.author.mention}!")

@bot.command()
async def ZY(ctx):
    await ctx.send("ZY RULES")

@bot.command()
async def rice(ctx):
    await ctx.send("AACubing Disses Bootleg Rice....")

@bot.command()
async def credits(ctx):
    await ctx.send("Here are all of the people that helped make me!")
    await asyncio.sleep(2)
    await ctx.send("Bootleg Fish: The Person Who Coded The Bot https://thebtlgfish.github.io")
    await asyncio.sleep(2)
    await ctx.send("AAcubing (Aka Bootleg Creator): Emotional Support")
    await asyncio.sleep(2)
    await ctx.send("And Thanks To The ZY Cult, For all of the support")

@bot.command()
async def quote(ctx):
    await ctx.send(random.choice(quotes))

@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command()
async def dog(ctx):
    await ctx.send(random.choice(dogs))


bot.run(TOKEN)
