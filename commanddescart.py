#-----------Comando de roles Inicio--------------

@client.command()
async def roles(ctx): Comando para cargos
    HorseEmoji = client.get_emoji(770751818158047318) emoji :HorseT8:
    msgEvent = await ctx.send(embed=EmbedsObj.get_RolesEventCommand())
    msgHorse = await ctx.send(embed=EmbedsObj.get_RolesHorseCommand())

    await msgEvent.add_reaction("🌲")
    await msgEvent.add_reaction("🐟") 
    await msgEvent.add_reaction("💰")
    await msgEvent.add_reaction("⚔️")
    await msgEvent.add_reaction("🐉")
    await botmsg.add_reaction(HorseEmoji)
    await msgEvent.add_reaction("🆕")
    await msgEvent.add_reaction("🗡️")

@client.event
async def on_raw_reaction_add(payload): Reacao para adicionar os cargos
    guild = client.get_guild(payload.guild_id)                  
    member = payload.member
    HorseEmoji = client.get_emoji(770751818158047318)

    if payload.user_id != 819262080200736840:
        if payload.emoji.name == "🌲":
            role = discord.utils.get(guild.roles, name='Epic Tree')
            await member.add_roles(role)
        elif payload.emoji.name == "🐟":
            role = discord.utils.get(guild.roles, name='Megalodon')
            await member.add_roles(role)
        elif payload.emoji.name == "💰":
            role = discord.utils.get(guild.roles, name='Coin Rain')
            await member.add_roles(role)
        elif payload.emoji.name == "⚔️":
            role = discord.utils.get(guild.roles, name='Arena')
            await member.add_roles(role)
        elif payload.emoji.name == "🐉":
            role = discord.utils.get(guild.roles, name='Miniboss')
            await member.add_roles(role)
        elif payload.emoji.name == HorseEmoji:
            role = discord.utils.get(guild.roles, name='Breedar')
            await member.add_roles(role)
        elif payload.emoji.name == "🆕":
            role = discord.utils.get(guild.roles, name='Updates')
            await member.add_roles(role)
        elif payload.emoji.name == "🗡️":
            role = discord.utils.get(guild.roles, name='Duel')
            await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload): Reacao para retirar os cargos
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    #HorseEmoji = client.get_emoji(770751818158047318)

    if payload.user_id != 819262080200736840:
        if payload.emoji.name == "🌲":
            role = discord.utils.get(guild.roles, name='Epic Tree')
            await member.remove_roles(role)
        elif payload.emoji.name == "🐟":
            role = discord.utils.get(guild.roles, name='Megalodon')
            await member.remove_roles(role)
        elif payload.emoji.name == "💰":
            role = discord.utils.get(guild.roles, name='Coin Rain')
            await member.remove_roles(role)
        elif payload.emoji.name == "⚔️":
            role = discord.utils.get(guild.roles, name='Arena')
            await member.remove_roles(role)
        elif payload.emoji.name == "🐉":
            role = discord.utils.get(guild.roles, name='Miniboss')
            await member.remove_roles(role)
        elif payload.emoji.name == "🆕":
            role = discord.utils.get(guild.roles, name='Updates')
            await member.remove_roles(role)
        elif payload.emoji.name == "🗡️":
            role = discord.utils.get(guild.roles, name='Duel')
            await member.remove_roles(role)

#------------Comando de roles Fim----------------

#------------Embeds--------------------

def get_RolesEventCommand(self): #Embed Command roles

        RolesCommand = discord.Embed(
            title = "Reaja para ganhar os cargos",
            color = 0xFE2EF7, #Roxo
        )

        RolesCommand.description = ":evergreen_tree:-Epic Tree\n:fish:-Megalodon\n:moneybag:-Coin Rain\n⚔️-Arena\n:dragon:-Miniboss\n:new:-Updates\n🗡️-Duel"  #"{}".format(self.HorseEmoji)
        
        return RolesCommand

@client.command()
@commands.is_owner()
async def give_role(ctx, names):
        members = ctx.guild.members
        for x in members:
            for y in x.roles:
                if y.name == 'ㅤㅤㅤﾠ⚔️RPG EPIC⚔️' or y.name == 'Normie' or y.name == 'ㅤㅤ💥Rpg Epic Eventos💥':
                    await x.remove_roles(y)

@client.command()
@commands.is_owner()
async def give_role(ctx, names):
        members = ctx.guild.members
        role = discord.utils.get(ctx.guild.roles, name='ㅤㅤㅤㅤ🕹️Games🕹️')
        for x in members:
            if x.bot:
                await x.remove_roles(role)
        print("finish")