import discord
from discord.ext import commands
from uk_covid19 import Cov19API
import json


class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Shows covid data.", description="Usage: '.covid <country>'")
    async def covid(self, ctx, country="uk"):
        all_nations = [
            "areaType=overview"
        ]

        scotland_only = [
            "areaType=nation",
            "areaName=Scotland"
        ]

        if country == "uk":
            filter = all_nations
        elif country == "scotland":
            filter = scotland_only

        structure = {
            "date": "date",
            "newCases": "newCasesByPublishDate",
            "newDeaths": "newDeaths28DaysByPublishDate",
            "firstDose": "cumPeopleVaccinatedFirstDoseByPublishDate",
            "secondDose": "cumPeopleVaccinatedSecondDoseByPublishDate"
        }

        api = Cov19API(
            filters=filter,
            structure=structure,
            latest_by="cumPeopleVaccinatedSecondDoseByPublishDate"
        )

        data = api.get_json(as_string=True)
        data = json.loads(data)["data"][0]

        message = discord.Embed(
            title=f"{country.upper()} Covid Data as of {data['date']}", colour=discord.Colour.red())
        message.add_field(name="New cases",
                          value=f"{data['newCases']: ,}", inline=True)
        message.add_field(name="New deaths",
                          value=f"{data['newDeaths']: ,}", inline=True)
        message.add_field(name="First dose",
                          value=f"{data['firstDose']: ,}", inline=True)
        message.add_field(name="Second dose",
                          value=f"{data['secondDose']: ,}", inline=True)
        await ctx.send(embed=message)

    @covid.error
    async def covid_error(self, ctx, error):
        await ctx.send("Invalid argument, must be either uk or scotland.")


def setup(client):
    client.add_cog(Covid(client))
