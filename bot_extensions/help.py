from discord.ext import commands
import config.config as config

logger = config.LOGGER

class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("Hello extention init")

    @commands.command()
    async def help(self, ctx, *args):
        logger.info(f"args: {args}")
        await ctx.send("hello!")
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(HelpCog(bot))