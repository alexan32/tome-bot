# This extension is used to associate discord users/guilds with the appropriate
# user data in the back end. 
#

import discord
from discord.ext import commands
import config.config as config
from bot_extensions.util import getRoleStrings, getContextInfo
from services import command_svc
import re
import json
import os
import requests
from config.config import UPDATE_FLAG
logger = config.LOGGER

registrationMessage = """
You have been invited to join a game in a server {guildName}. Log into the tome website and navigate the the "join game" form.

Your user ID: 
```{discordId}```
{guildName} guild ID: 
```{guildId}```
Do not share your user ID with anyone.
"""

class ManagementCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("register extension init")

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


    @commands.command()
    async def me(self, ctx, *args):
        await ctx.message.delete()


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


    @commands.command()
    async def quickplay(self, ctx, *args):
        await ctx.message.delete()

        first = args[0]
        last = args[1]
        
        participant = ctx.author.id
        guildId = ctx.guild.id
        
        responses = command_svc.quickPlay(participant, guildId, first, last)
        
        for response in responses:
            await ctx.send(f"```{response}```")


    @commands.command()
    async def download(self, ctx, *args):
        await ctx.message.delete()
        
        participant = ctx.author.id
        guildId = ctx.guild.id

        characterData = command_svc.getCharacterData(participant, guildId)
        first = characterData["meta"]["first"]
        last = characterData["meta"]["last"]
        fileName = f"{first}-{last}.json"
        f = open(fileName, 'w')
        f.write(json.dumps(characterData))
        f.close()
        f = open(fileName, 'r')
        await ctx.send(file=discord.File(f), delete_after=60.0)
        await ctx.message.delete()
        f.close()
        os.remove(fileName)

    @commands.command()
    async def upload(self, ctx):
        participant = ctx.author.id
        guildId = ctx.guild.id
        try:
            attachment_url = ctx.message.attachments[0].url
            file_request = requests.get(attachment_url)
            contents = json.loads(file_request.content.decode("utf-8"))
            contents["participant"] = str(participant)
            contents[UPDATE_FLAG] = True
        except Exception as e:
            print(e)
            await ctx.send(f"```Failed to process file. Make sure that you attach a valid character JSON file before sending.```", delete_after=60.0)
        else:
            print(contents)
            status, messages = command_svc.updateCharacter(participant, guildId, contents)
            if status != 200:
                for message in messages:
                    await ctx.send(f"```{status}. {messages[0]}```", delete_after=60.0)
                    await ctx.message.delete()
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(ManagementCog(bot))
