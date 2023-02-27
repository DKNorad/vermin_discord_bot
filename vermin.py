import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
import config


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")


bot = MyBot()
bot.run(config.DISCORD_TOKEN)

tree = app_commands.CommandTree(bot)
@tree.command(name="help", description="Displays all the available commands.")
@tree.command(name="play", description="Play a song.")
