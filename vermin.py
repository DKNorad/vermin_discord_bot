import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
from config import config
from config.token import DISCORD_TOKEN


# class MyBot(commands.Bot):
#     def __init__(self):
#         super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None)
#         self.guild = None
#         self.command_tree = None
#
#     async def setup_hook(self):
#         for folder in os.listdir("modules"):
#             if os.path.exists(os.path.join("modules", folder, "music_controller.py")):
#                 await self.load_extension(f"modules.{folder}.cog")
#
#
# if __name__ == '__main__':
#     bot = MyBot()
#     bot.run(config.DISCORD_TOKEN)
#     bot.command_tree = app_commands.CommandTree(bot)
#
#
from modules.music.music_controller import MusicCog

initial_extensions = ['modules.music.commands.music', 'modules.commands.general', 'modules.plugins.button', 'modules.help.cog']
bot = commands.Bot(command_prefix=config.PREFIX, pm_help=True, case_insensitive=True, intents=discord.Intents.all(),
                   help_command=None)


async def load_ext():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if DISCORD_TOKEN == "":
        print("Error: No bot token!")
        exit()


@bot.event
async def on_ready():
    # print(config.STARTUP_MESSAGE)
    await load_ext()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Music, type {config.PREFIX}help"))



    # for guild in bot.guilds:
    #     await register(guild)
    #     print("Joined {}".format(guild.name))
    #
    # print(config.STARTUP_COMPLETE_MESSAGE)


# @bot.event
# async def on_guild_join(guild):
#     print(guild.name)
#     await register(guild)


# async def register(guild):
#
#     guild_to_settings[guild] = Settings(guild)
#     guild_to_audiocontroller[guild] = MusicCog(bot, guild)
#
#     sett = guild_to_settings[guild]
#
#     try:
#         await guild.me.edit(nick=sett.get('default_nickname'))
#     except:
#         pass
#
#     if config.GLOBAL_DISABLE_AUTOJOIN_VC:
#         return
#
#     vc_channels = guild.voice_channels
#
#     if not sett.get('vc_timeout'):
#         if sett.get('start_voice_channel') is None:
#             try:
#                 await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
#             except Exception as e:
#                 print(e)
#
#         else:
#             for vc in vc_channels:
#                 if vc.id == sett.get('start_voice_channel'):
#                     try:
#                         await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
#                     except Exception as e:
#                         print(e)


bot.run(DISCORD_TOKEN, reconnect=True, )
