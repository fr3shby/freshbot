import discord
from discord.ext import commands
from kahoot import client


class Kahoot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Sends 50 bots to a kahoot", description="Usage: '.kahoot <pin> <name>'")
    async def kahoot(self, ctx, pin, *, name):
        bot = client()
        for i in range(0, 50):
            bot.join(pin, name + str(i))
        await ctx.send("Bots sent")


def setup(client):
    client.add_cog(Kahoot(client))
