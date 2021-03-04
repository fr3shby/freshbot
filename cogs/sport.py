import discord
from discord.ext import commands
import requests
import json
from os import environ

api_key = environ.get("X_RAPIDAPI_KEY")


class Team:
    def __init__(self, rank, name, points):
        self.rank = rank
        self.name = name
        self.points = points


class Sport(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Displays the premier league table")
    async def pl(self, ctx):
        url = "https://v3.football.api-sports.io/standings?league=39&season=2020"
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        table = []

        for i in range(0, 20):
            table.append(Team(data["response"][0]["league"]["standings"][0][i]["rank"],
                              data["response"][0]["league"]["standings"][0][i]["team"]["name"],
                              data["response"][0]["league"]["standings"][0][i]["points"]))

        ranks = "\n".join([str(team.rank) for team in table])
        teams = "\n".join([str(team.name) for team in table])
        points = "\n".join([str(team.points) for team in table])

        message = discord.Embed(
            title="Current Premier League Table", colour=discord.Colour.green())
        message.add_field(name="Rank", value=ranks, inline=True)
        message.add_field(name="Team", value=teams, inline=True)
        message.add_field(name="Points", value=points, inline=True)
        await ctx.send(embed=message)


def setup(client):
    client.add_cog(Sport(client))
