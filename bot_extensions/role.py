from discord.ext import commands
import discord
import config.config as config
import re
from bot_extensions.util import getContextInfo

logger = config.LOGGER

class RoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("role extension init")

    @commands.command()
    async def initialize(self, ctx):
        await ctx.message.delete()

        guild = self.bot.get_guild(ctx.guild.id)
        ownerId = guild.owner_id
        author = guild.get_member(ctx.author.id)

        if author.id != ownerId:
            await ctx.send("only the server owner can run the initialize command.")
            return
        
        logger.info(f"running initialize command for guild:{guild.name}. guildId:{guild.id}")
        for role_name in config.ROLES:
            role = discord.utils.get(guild.roles, name=role_name)
            if role is None:
                await guild.create_role(name = role_name)

        await ctx.send("bot roles initialized")


    @commands.command()
    async def assignrole(self, ctx, *args):
        await ctx.message.delete()

        # CHECK NUMBER OF ARGS
        if len(args) != 2:
            await ctx.send("incorrect number of args recieved. expected !assignrole @<user display name> <role name>")
            return

        userMention = args[0]
        roleName = args[1].lower()

        # GET TARGET USER
        targetUserId = re.search(r"(\d+)", userMention)
        if not targetUserId:
            await ctx.send("No user mention was detected. Use !help for more info.")
            return 
        else:
            targetUserId = targetUserId.group(0)

        # GRAB CONTEXT INFO
        contextInfo = getContextInfo(self.bot, ctx)
        authorIsOwner = contextInfo["authorIsOwner"]
        authorRoles = contextInfo["roles"]
        guild = contextInfo["guild"]
        
        # VALIDATE ROLE ARG
        role = discord.utils.get(guild.roles, name=roleName)
        if role is None:
            await ctx.send(f"Role '{roleName}' does not exist. Check that the server owner has run the !initialize command, or that the server owner has created the '{roleName}' role.")
            return
        
        # CHECK THAT AUTHOR HAS PERMISSION TO SET ROLE
        if roleName == "player" and not (authorIsOwner or "gm" in authorRoles or "admin" in authorRoles):
            ctx.send("Only server owners, admins, or gms can assign the 'player' role")
            return
            
        elif roleName == "gm" and not (authorIsOwner or "admin" in authorRoles):
            ctx.send("Only server owners and admins can assingn the 'gm' role")
            return
            
        elif roleName == "admin" and not authorIsOwner:
            ctx.send("Only server owners can assign the 'admin' role")
            return
                
        # ASSIGN ROLE
        logger.info(f"assigning role '{role}' to {targetUserId} {contextInfo['displayName']}")
        targetMember = guild.get_member(int(targetUserId))
        await targetMember.add_roles(role)
        await ctx.send(f"Gave role '{roleName}' to {targetMember.display_name}")


async def setup(bot):
    await bot.add_cog(RoleCog(bot))