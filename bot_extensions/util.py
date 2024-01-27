from config.config import LOGGER
import discord

logger = LOGGER

def getContextInfo(bot, ctx):
    guild = bot.get_guild(ctx.guild.id)
    ownerId = guild.owner_id
    author = guild.get_member(ctx.author.id)
    roles = list(map(lambda x : x.name, author.roles))
    isOwner = author.id == ownerId
    logger.info(f"author: {author.id}. isOwner: {isOwner}. roles: {roles}")
    return {
        "guild": guild,
        "displayName": author.display_name,
        "discordId": author.id,
        "roles": roles,
        "authorIsOwner": isOwner
    }

def getRoleStrings(member: discord.member):
    return list(map(lambda x : x.name, member.roles))
