# RustBot
A Discord Bot written in Python utilizing discord.py.

This bot is a work in progress and lacks many features. The goal of this project is to learn the discord.py module and
write a discord bot from the ground up.

# Current Features:

1. **r.help**

Sends a DM to the user __which__ will include the list of available commands.
   
2. **r.test**

Makes the bot state "**Hello, World!**".

3. **r.version**

Makes the bot state what version of discordpy is being used. This may later change
into stating the version of the bot.

4. **r.members**

Makes the bot state: Total User Population of Guild/Server (Based on Guild ID) and
Number of Users Online&Offline&Idle. Along with this, the bot posts a graph which shows
the total numbers of users online throughout a timeline (Starting from When the Bot Joined the Server).
This graph is generated in the background.

# Setting it Up

As of writting this, the bot is very early in development and setting it up requires some programming knowledge. If you want to set it up, just follow Sent's guide on https://pythonprogramming.net/discordpy-basic-bot-tutorial-introduction/ . You just need to follow it until the first code block is shown. Ensure that the token.txt file contains the token of your bot, and the guild id
is the id of the server the bot is in.
