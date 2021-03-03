import discord
from discord.ext import commands
import requests
import json
import os
import time


api_key = os.environ.get("WEATHER_API_KEY")


class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Displays information about the weather.", description="Usage: '.weather <day>'")
    async def weather(self, ctx, target="today"):
        class Reading:
            def __init__(self, time, temp, description):
                self.time = time
                self.temp = int(round(temp - 273))
                self.description = description

            def find_day(timestamp):
                object = time.gmtime(timestamp)
                return time.strftime("%A", object)

        url = f"http://api.openweathermap.org/data/2.5/forecast?q=Edinburgh,GB&appid={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        readings = []

        for i in range(40):
            readings.append(Reading(data["list"][i]["dt"],
                                    data["list"][i]["main"]["temp"],
                                    data["list"][i]["weather"][0]["description"]))

        day_data = []
        if target == "today":
            today_timestamp = time.time()
            target = Reading.find_day(today_timestamp).lower()
        for reading in readings:
            if Reading.find_day(reading.time).lower() == target.lower():
                day_data.append(reading)
        if len(day_data) == 0:
            raise Exception("No weather available for that day")

        message = discord.Embed(
            title=f"Weather data for: {target.upper()}", colour=discord.Colour.red())
        for reading in day_data:
            time_object = time.gmtime(reading.time)
            hour = time.strftime("%I", time_object).lstrip("0")
            half = time.strftime("%p", time_object)
            temp = reading.temp
            description = reading.description
            message.add_field(name=f"{hour}{half}",
                              value=f"Temperature: {temp}°C \nWeather - {description}", inline=True)
        await ctx.send(embed=message)

    @weather.error
    async def weather_error(self, ctx, error):
        await ctx.send("Weather was not found for that day. ")


def setup(client):
    client.add_cog(Weather(client))
