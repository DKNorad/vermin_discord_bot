import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
import config


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None)
        self.guild = None
        self.command_tree = None

    async def setup_hook(self):
        for folder in os.listdir("modules"):
            if os.path.exists(os.path.join("modules", folder, "cog.py")):
                await self.load_extension(f"modules.{folder}.cog")


if __name__ == '__main__':
    bot = MyBot()
    bot.run(config.DISCORD_TOKEN)
    bot.command_tree = app_commands.CommandTree(bot)
