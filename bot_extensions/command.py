from discord.ext import commands
import config.config as config
import services.command_svc as command_svc


logger = config.LOGGER

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("Command extention init")


    @commands.command()
    async def counter(self, ctx, *args):
        # await ctx.message.delete()

        participant = ctx.author.id
        guildId = ctx.guild.id
        _input = "counter " + " ".join(args)
        
        responses = command_svc.counter(participant, guildId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")


    @commands.command()
    async def composite(self, ctx, *args):
        # await ctx.message.delete()

        participant = ctx.author.id
        guildId = ctx.guild.id
        _input = "composite " + " ".join(args)
        
        responses = command_svc.composite(participant, guildId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")


    @commands.command()
    async def func(self, ctx, *args):
        # await ctx.message.delete()

        participant = ctx.author.id
        guildId = ctx.guild.id
        _input = "func " + " ".join(args)
        
        responses = command_svc.func(participant, guildId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")


    @commands.command()
    async def roll(self, ctx, *args):
        # await ctx.message.delete()

        participant = ctx.author.id
        guildId = ctx.guild.id
        _input = "roll " + " ".join(args)
        
        responses = command_svc.roll(participant, guildId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")
        

async def setup(bot):
    await bot.add_cog(CommandCog(bot))