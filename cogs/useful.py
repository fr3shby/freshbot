import discord
from discord.ext import commands, tasks


class Useful(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Displays this message!")
    async def help(self, ctx):
        cogs = self.client.cogs
        helpMessage = discord.Embed(
            title="Help", colour=discord.Colour.red())
        for cog in cogs:
            if cog != "Admin":
                commands = self.client.get_cog(cog).get_commands()
                text = "\n".join(
                    [f"`{c.name}`: {c.brief} {c.description}" for c in commands]
                )
                helpMessage.add_field(name=f"{cog}", value=text, inline=False)
        await ctx.send(embed=helpMessage)

    @commands.command(brief="The link to the source.")
    async def repo(self, ctx):
        await ctx.send("https://github.com/0xfinlay/freshbot")


def setup(client):
    client.add_cog(Useful(client))
