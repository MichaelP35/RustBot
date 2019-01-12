import discord
import asyncio
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")


token = open("token.txt", "r").read()  # Reads Token Based on token.txt.
client = discord.Client()  # Starts the discord client.


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

    return online, idle, offline


async def user_metrics_background_task():  # Based on number of users, it prints an graph.
    await client.wait_until_ready()
    global server_guild
    server_guild = client.get_guild(372445121050050560)
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

            await asyncio.sleep(5)

        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)


@client.event  # Event decorator/wrapper.
async def on_ready():  # Method expected by client. This runs once when connected.
    print(f'We have logged in as {client.user}')  # Notification of login.
    await client.change_presence(activity=discord.Game("r.help"))  # Sets "Game" Activity to "r.help".


@client.event
async def on_message(message):  # Event that happens per any message.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")  # Records message.

    if "r.help" in message.content.lower():  # r.help lists all commands.
        await message.author.send("```r.help: DMs the user of all available commands.")  # Sends the message through DM.

    elif "r.test" in message.content.lower():  # r.test tests if bot responds.
        await message.channel.send("**Hello, World!**")  # Sends the message in the channel the user messaged in.

    elif "r.version" in message.content.lower():  # r.version states version of discordpy being used.
        await message.channel.send(f"**Running Discord.py v{discord.__version__}**")

    elif "r.members" == message.content.lower():  # Provides both number of users and user graph.
        online, idle, offline = community_report(server_guild)
        await message.channel.send(f"Total Members: {server_guild.member_count}```Online: {online}.\n"
                                   f"Idle/Busy: {idle}.\nOffline: {offline}```")
        file = discord.File("online.png", filename="online.png")
        await message.channel.send(file=file)


client.loop.create_task(user_metrics_background_task())  # Tasks the Bot to generate an graph of member activity.
client.run(token)  # Activates the RustBot.
