import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Clears messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("Invalid argument, must be a number.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")

    @commands.command(brief="Kicks user")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to kick.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find that user.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")

    @commands.command(brief="Bans user")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to ban.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find that user.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")

    @commands.command(brief="Unbans user")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"{user.mention} was unbanned.")
                return
        await ctx.send("Could not find that user.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to unban.")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("Invalid argument, must be a user.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")

    @commands.command(brief="Mutes user")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.message.guild.roles, name='Muted')
        await member.add_roles(role)
        await ctx.send(f"{member.mention} was muted.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to mute.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find that user.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")

    @commands.command(brief="Unmutes user")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.message.guild.roles, name='Muted')
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} was unmuted.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You must specify a user to unmute.")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Could not find that user.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You must be an admin to use that command.")


def setup(client):
    client.add_cog(Admin(client))
