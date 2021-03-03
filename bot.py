import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents, help_command=None)
token = os.environ.get("BOT_TOKEN")


@client.event
async def on_ready():
    print("Freshbot started")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Checking for gimps..."))


@client.event
async def on_member_join(member):
    print("Member joined")
    channel = client.get_channel(623959523450814487)
    await channel.send(f"{member.mention} has joined the server. :smile:")


@client.event
async def on_member_remove(member):
    print("Member left")
    channel = client.get_channel(623959523450814487)
    await channel.send(f"{member.mention} has left the server. :pensive:")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

client.load_extension("cogs.useful")
client.load_extension("cogs.fun")
client.load_extension("cogs.kahoot")
client.load_extension("cogs.reddit")
client.load_extension("cogs.covid")
client.load_extension("cogs.sport")
client.load_extension("cogs.weather")
client.load_extension("cogs.admin")

client.run(token)
