import os
import random
import asyncio
import discord
from discord.ext import commands


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.Jf0NnGpH2AhNM3BtwZufwwHaJ4%3Fpid%3DApi&f=1&ipt=ef3be790512c73f0009f9bca8c588ae38001833fcc351dc47cae3a45b2806b0c&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.kKBf8FoNYCG-9E7hco2DEAHaEo%3Fpid%3DApi&f=1&ipt=706aaa228cc13c589de5aa2370b7060d396ef82abd55212dc8938a22139c808f&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%2Fid%2FOIP.5aKhA8rhSGnJzNnkGJgtLwHaLH%3Fpid%3DApi&f=1&ipt=c5348cc9cf42d1dfc159655ab565738212e97a3eb389bcfa7b38cb61e1084b85&ipo=images",
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
    print(f"Bot is ready. Logged in as {bot.user}")


# The Info Command
@bot.command()
async def info(ctx):
    await ctx.send("Welcome to the CyberFish Discord Bot! This is a simple bot made by BootlegFish. Here are some of the commands you can use ")
    await ctx.send("Also Please Note That This Bot Is Still In Beta Testing")
    await ctx.send("!info")
    await ctx.send("!hello")
    await ctx.send("!bootleg")
    await ctx.send("!fish")
    await ctx.send("!ZY")
    await ctx.send("!rice")
    await ctx.send("!catnuke")
    await ctx.send("!stopcatnuke")
    await ctx.send("!quote")
    await ctx.send("!dog")
    await ctx.send("!joke")
    await ctx.send("!credits")


# The Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send("wsg bro")


# The Bootleg Command
@bot.command()
async def bootleg(ctx):
    await ctx.send("BootlegFish Created Me! He Is Awesome! Go Check Him Out https://thebtlgfish.github.io")


# The ZY command
@bot.command()
async def ZY(ctx):
    await ctx.send("ZY RULES")


# The Rice Command
@bot.command()
async def rice(ctx):
    await ctx.send("AACubing Disses Bootleg Rice....")


# The Credits Command
@bot.command()
async def credits(ctx):
    await ctx.send("Here are all of the people that helped make me!")
    await asyncio.sleep(2)
    await ctx.send("Bootleg Fish: The Person Who Coded The Bot https://thebtlgfish.github.io")
    await asyncio.sleep(2)
    await ctx.send("AAcubing (Aka Bootleg Creator): Emotional Support")
    await asyncio.sleep(2)
    await ctx.send("And Thanks To The ZY Cult, For all of the support")


# Fish Command
@bot.command()
async def fish(ctx):
    await ctx.send("https://bootleginifishinini.codehs.me/images/bootleg.png")


# The Quote Command
@bot.command()
async def quote(ctx):
    quote = random.choice(quotes)
    await ctx.send(quote)


# The Joke Command
@bot.command()
async def joke(ctx):
    joke = random.choice(jokes)
    await ctx.send(joke)


# Dog Command
@bot.command()
async def dog(ctx):
    dog = random.choice(dogs)
    await ctx.send(dog)


# Catnuke Task
bot.catnuke_task = None


# Catnuke Command
@bot.command()
async def catnuke(ctx):
    if bot.catnuke_task and not bot.catnuke_task.done():
        await ctx.send("Cat nuke is already running!")
        return

    async def spam_cat():
        try:
            while True:
                await ctx.send("cat")
                await asyncio.sleep(1.5)
        except asyncio.CancelledError:
            await ctx.send("Cat nuke stopped.")
            raise

    bot.catnuke_task = asyncio.create_task(spam_cat())
    await ctx.send("Started cat nuke!")


# Stop Catnuke Command
@bot.command()
async def stopcatnuke(ctx):
    if bot.catnuke_task and not bot.catnuke_task.done():
        bot.catnuke_task.cancel()
        await ctx.send("Stopping cat nuke...")
    else:
        await ctx.send("No cat nuke is currently running.")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {str(error)}")
    print(f"Command Error: {error}")



bot.run(TOKEN)
