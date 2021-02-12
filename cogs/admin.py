import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Clears messages")
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command(brief="Kicks user")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command(brief="Bans user")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(brief="Unbans user")
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"Unbanned: {user.mention}")
                return

    @commands.command(brief="Mutes user")
    async def mute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.message.server.roles, name='Muted')
        await user.add_roles(role)

    @commands.command(brief="Unmutes user")
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.message.server.roles, name='Muted')
        await user.remove_roles(role)


def setup(client):
    client.add_cog(Admin(client))
