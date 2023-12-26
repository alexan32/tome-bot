# This extension is used to associate discord users/guilds with the appropriate
# user data in the back end. 
#

from discord.ext import commands
import config.config as config

logger = config.LOGGER

message = """
Are you trying to register your tome account with a server called {guildName}? Log into the tome website and navigate the the "join game" form.

Your user ID: 
```{discordId}```
{guildName} guild ID: 
```{guildId}```
Do not share your user ID with anyone.
"""

class RegisterCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("register extension init")

    @commands.command()
    async def joingame(self, ctx, *args):
        guild = self.bot.get_guild(ctx.guild.id)
        member = guild.get_member(ctx.author.id)
        roles = member.roles
        await ctx.message.delete()
        channel = await member.create_dm()
        await channel.send(message.format(guildName=guild.name, guildId=guild.id, discordId=ctx.author.id))


async def setup(bot):
    await bot.add_cog(RegisterCog(bot))
