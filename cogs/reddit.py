import discord
from discord.ext import commands
import asyncpraw as praw
import random
import json

secrets = open("secret.json", "r")
data = json.load(secrets)
client_id = data["client_id"]
client_secret = data["client_secret"]
username = data["username"]
password = data["password"]


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent="Freshbot",
        )

    @commands.command(brief="Displays okbr post")
    async def okbr(self, ctx):
        subreddit = await self.reddit.subreddit("okbuddyretard")
        submissions = []

        async for submission in subreddit.hot(limit=100):
            if not "v.redd.it" in submission.url:
                submissions.append(
                    {
                        "title": submission.title,
                        "link": submission.url,
                        "text": submission.selftext,
                    }
                )

        submission = random.choice(submissions)
        message = discord.Embed(
            title=submission["title"], description=submission["text"], colour=0xFF4500
        )
        message.set_image(url=submission["link"])
        await ctx.send(embed=message)


def setup(client):
    client.add_cog(Reddit(client))
