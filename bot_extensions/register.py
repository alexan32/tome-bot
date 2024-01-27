# This extension is used to associate discord users/guilds with the appropriate
# user data in the back end. 
#

from discord.ext import commands
import config.config as config
from bot_extensions.util import getRoleStrings
import re
logger = config.LOGGER

registrationMessage = """
You have been invited to join a game in a server {guildName}. Log into the tome website and navigate the the "join game" form.

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
        await ctx.message.delete()

        # get user info
        guild = self.bot.get_guild(ctx.guild.id)
        member = guild.get_member(ctx.author.id)
        roles = getRoleStrings(member)

        # confirm member has valid role
        if not("gm" in roles or "player" in roles):
            await ctx.send("You need to have the 'gm' or 'player' role to join the game. Ask the server owner or gm to add you.")
            return
        
        # send invite message
        channel = await member.create_dm()
        await channel.send(registrationMessage.format(guildName=guild.name, guildId=guild.id, discordId=ctx.author.id))


    @commands.command()
    async def invite(self, ctx, *args):
        await ctx.message.delete()

        # check # args
        if len(args) != 1:
            await ctx.send("incorrect number of args recieved. expected !invite @<user display name>.")
            return

        userMention = args[0]

        # get target member
        targetUserId = re.search(r"(\d+)", userMention)
        if not targetUserId:
            await ctx.send("No user mention was detected. Use !help for more info.")
            return 

        targetUserId = targetUserId.group(0)
        guild = self.bot.get_guild(ctx.guild.id)
        targetMember = guild.get_member(int(targetUserId))

        # confirm member has valid role
        roles = getRoleStrings(targetMember)
        if not("gm" in roles or "player" in roles):
            await ctx.send("This member does not have the 'gm' or 'player' role, which are required before they can join the game.")
            return

        # send invite message
        channel = await targetMember.create_dm()
        await channel.send(registrationMessage.format(guildName=guild.name, guildId=guild.id, discordId=ctx.author.id))

async def setup(bot):
    await bot.add_cog(RegisterCog(bot))
