import discord

def hasRole(user: discord.Member, role_id: int) -> bool:
    for role in user.roles:
        if role.id == role_id:
            return True
    return False