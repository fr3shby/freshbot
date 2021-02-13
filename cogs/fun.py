import discord
from discord.ext import commands
import json

secrets = open("secret.json", "r")
data = json.load(secrets)
hairline_image = data["hairline_image"]
french_gaff = data["french_gaff"]


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Shushes another user.", description="Usage: '.shush @user'")
    async def shush(self, ctx, user: discord.Member):
        await ctx.send(user.mention)
        await ctx.send("https://tenor.com/view/shh-shush-shaq-be-quiet-face-warp-gif-17428668")

    @shush.error
    async def shush_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to shush.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find that user.")

    @commands.command(brief="The forbidden image")
    async def hairline(self, ctx):
        await ctx.send(hairline_image)

    @commands.command(brief="Karen alert :flushed:")
    async def ash(self, ctx):
        await ctx.send("https://tenor.com/view/karen-karening-intensifies-done-iam-done-gif-16742218")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "french gaff" in message.content.lower():
            await message.channel.send(french_gaff)


def setup(client):
    client.add_cog(Fun(client))
