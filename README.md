# RustBot
A Discord Bot written in Python utilizing the [discord.py module](https://discordpy.readthedocs.io/en/latest/).

This bot is a work in progress and lacks many features. The goal of this project is to learn the discord.py module and
write a discord bot from the ground up. I want to thank Sentdex for the guide he has published which can be [found here](https://pythonprogramming.net/discordpy-basic-bot-tutorial-introduction/).

## Current Features:

1. **r.help**

   Sends a DM listing all available commands.
   
2. **r.ping**

   Sends a channel message stating ping of RustBot.

3. **r.members**

   Sends a channel message containing data of member activity.

4. **r.version**

   Sends a channel message containing version of discord.py being run.
   
5. **r.weather**

   r.weather: Sends a channel message containing weather data based on zip-code (US Only).

## Setting it Up

As of writing this, the bot is very early in development and setting it up requires some programming knowledge. If you want to set it up, just follow [Sent's guide](https://pythonprogramming.net/discordpy-basic-bot-tutorial-introduction/). You just need to follow it until the first code block is shown. Ensure that the token.txt file contains the token of your bot, and the guild id
is the id of the server the bot is in.
