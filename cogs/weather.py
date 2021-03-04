import discord
from discord.ext import commands
import requests
import json
import time
from os import environ

api_key = environ.get("WEATHER_API_KEY")


class Reading:
    def __init__(self, time, temp, description):
        self.time = time
        self.temp = int(round(temp - 273))
        self.description = description

    def find_day(timestamp):
        object = time.gmtime(timestamp)
        day = time.strftime("%A", object)
        return day

    def find_time(timestamp):
        object = time.gmtime(timestamp)
        hour = time.strftime("%I", object).lstrip("0")
        half = time.strftime("%p", object)
        return hour, half


class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Displays information about the weather.", description="Usage: '.weather <day>'")
    async def weather(self, ctx, target="today"):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q=Edinburgh,GB&appid={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        readings = []

        for i in range(40):
            readings.append(Reading(data["list"][i]["dt"],
                                    data["list"][i]["main"]["temp"],
                                    data["list"][i]["weather"][0]["description"]))

        day_data = []
        if target.lower() == "today":
            today_timestamp = time.time()
            target = Reading.find_day(today_timestamp)
        elif target.lower() == "chewsday":
            target = "Tuesday"
        for reading in readings:
            if Reading.find_day(reading.time).lower() == target.lower():
                day_data.append(reading)
        if len(day_data) == 0:
            raise Exception("No weather available for that day")

        message = discord.Embed(
            title=f"Weather data for: {target.upper()}", colour=discord.Colour.red())
        for reading in day_data:
            hour, half = Reading.find_time(reading.time)
            message.add_field(name=hour + half,
                              value=f"Temperature: {reading.temp}°C \nWeather - {reading.description}", inline=True)
        await ctx.send(embed=message)

    @weather.error
    async def weather_error(self, ctx, error):
        await ctx.send("Weather was not found for that day. ")


def setup(client):
    client.add_cog(Weather(client))
