from discord.ext import commands
import config.config as config

logger = config.LOGGER

class HelloCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("Hello extention init")

    @commands.command()
    async def hello(self, ctx, *args):
        logger.info(f"args: {args}")
        await ctx.send("hello!")
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(HelloCog(bot))