import discord  # Main Discord API Wrapper.
from discord.ext import commands  # Discord API Wrapper Extension for Simplified Commands.
import asyncio  # Needed for Background Tasks.
import time  # Needed for Background Tasks.
import pandas as pd  # Needed for Parsing CSV.
import matplotlib.pyplot as plt  # Needed for Graphing.
from matplotlib import style  # Needed for Graph Styling.
style.use("fivethirtyeight")  # Sets Graph Style.


client = commands.Bot(command_prefix='r.', activity=discord.Game('r.help'))  # Refers the bot as 'Client'.
client.remove_command("help")  # Removes integrated 'help' for commands.


def community_report(guild):  # Calculates number of users based on being online, offline, or idle.
    online = 0
    idle = 0
    offline = 0
    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline  # Returns number of users in corresponding section.


async def user_metrics_background_task():  # Based on number of users, it prints an graph.
    await client.wait_until_ready()
    global server_guild
    server_guild = client.get_guild(372445121050050560)  # Sets the guild (Set to OGT).
    while True:
        try:
            online, idle, offline = community_report(server_guild)
            with open("usermetrics.csv", "a") as f:
                f.write(f"{int(time.time())},{online},{idle},{offline}\n")
            plt.clf()
            df = pd.read_csv("usermetrics.csv", names=['time', 'online', 'idle', 'offline'])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            df['total'] = df['online'] + df['offline'] + df['idle']
            df.drop("time", 1,  inplace=True)
            df.set_index("date", inplace=True)
            df['online'].plot()
            plt.legend()
            plt.savefig("online.png")

            await asyncio.sleep(5)  # Waits 5 secs before repeating task.

        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)


@client.event  # Event Decorator/Wrapper.
async def on_ready():  # Method expected by client. This runs once when connected.
    print(f'We have logged in as {client.user}\n')  # Notification of login.


@client.event  # Event Decorator/Wrapper.
async def on_member_join(member):  # Users that join will get the initiating role.
    role = discord.utils.get(member.server.roles, name='Initiating')
    await discord.Member.add_roles(member, role)


@client.event  # Event Decorator/Wrapper.
async def on_message(message):  # Event that happens per any message.
    if message.author != client.user:  # If the message isn't from RustBot.
        print(f"#{message.channel} | {message.author}({message.author.name}): {message.content}")  # Logs message.
    await client.process_commands(message)  # Allows for commands to be registered by @client.command().


@client.command()  # Creates a Command.
async def help(ctx):  # Help: Sends a DM listing all available commands.
    await ctx.author.send("```\n"
                          "r.help: DMs the user of all available commands.\n"
                          "r.ping: States the Ping of the Bot.\n"
                          "r.members: Provides Statistics regarding Server Members Activity.\n"
                          "r.version: States the version of Discord.py that is being used\n"
                          "```")


@client.command()  # Creates a Command.
async def ping(ctx):  # Ping: Sends a channel message stating ping of RustBot.
    ping_ = client.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"My ping is {ping}ms")


@client.command()  # Creates a Command.
async def members(ctx):  # Members: Sends a channel message containing data of member activity.
    online, idle, offline = community_report(server_guild)
    await ctx.channel.send(f"__Total Members:__ **{server_guild.member_count}**\n"
                           f"Online: **{online}**\n"
                           f"Idle/Busy: **{idle}**\n"
                           f"Offline: **{offline}**")
    file = discord.File("online.png", filename="online.png")
    await ctx.channel.send(file=file)


@client.command()  # Creates a Command.
async def version(ctx):  # Version: Sends a channel message containing version of discord.py being run.
    await ctx.channel.send(f"Running Discord.py **v{discord.__version__}**")


client.loop.create_task(user_metrics_background_task())  # Tasks the Bot to generate an graph of member activity.
client.run(open("token.txt", "r").read())  # Activates RustBot and reads token.txt on root directory.
