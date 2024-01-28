import config.config as config
import discord
import argparse

from discord.ext import commands


# GET ENVIRONMENT VALUES
parser = argparse.ArgumentParser()
parser.add_argument('--stage', required=False, default="dev")
stage = parser.parse_args().stage
config.init(stage)

token = config.ENVIRONMENT["token"]
logHandler = config.HANDLER
logger = config.LOGGER

# CONFIGURE BOT INTENTS
intents = discord.Intents(
    messages=True,
    guilds=True,
    members=True
)
intents.message_content = True

# CONFIGURE BOT COMMANDS
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    logger.info("loading bot extensions.")
    await bot.load_extension("bot_extensions.register")
    await bot.load_extension("bot_extensions.role")
    await bot.load_extension("bot_extensions.command")
    logger.info("======= BOT IS READY! =======")

# LAUNCH BOT
bot.run(config.ENVIRONMENT["token"], log_handler=logHandler)