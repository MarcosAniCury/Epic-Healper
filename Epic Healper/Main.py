from discord import embeds
import EmbedsEpicHealper
import TOKEN
import discord
import random
from EmbedsEpicHealper import EpicHealperEmbeds
from discord.ext import commands
from discord.ext.commands import bot

client = commands.Bot(intents = discord.Intents.all(), command_prefix=TOKEN.get_prefix())

EmbedsObj = None

ArenaList = None #Variavel da arena

@client.event
async def on_ready(): #Bot start
    print("BOT ONLINE - Digite help h para ajuda") 
    print(client.user.name)
    print(client.user.id)
    print("----------------------")
    global EmbedsObj 
    EmbedsObj = EmbedsEpicHealper.EpicHealperEmbeds(client)

    await client.change_presence(activity=discord.Game("\"help h\" alias \"h h\"")) #Alterar status do bot


class MyHelp(commands.HelpCommand): #Overwrite help
    def __init__(self):
        super().__init__(command_attrs={
        'aliases': ['h'],
        })

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        HelpEmbed = EmbedsObj.get_HelpCommand()
        await channel.send(embed=HelpEmbed)

client.help_command = MyHelp() #Quando digitar <prefix> help vai chamar a funcao

#-----------Comando de roles Inicio--------------

@client.command()
async def roles(ctx): #Comando para cargos
    HorseEmoji = client.get_emoji(770751818158047318) #emoji :HorseT8:
    botmsg = await ctx.send(embed=EmbedsObj.get_RolesCommand())

    await botmsg.add_reaction("🌲")
    await botmsg.add_reaction("🐟") 
    await botmsg.add_reaction("💰")
    await botmsg.add_reaction("⚔️")
    await botmsg.add_reaction("🐉")
    await botmsg.add_reaction(HorseEmoji)
    await botmsg.add_reaction("🆕")

@client.event
async def on_raw_reaction_add(payload): #Reacao para adicionar os cargos
    guild = client.get_guild(payload.guild_id)                  
    member = payload.member
    HorseEmoji = client.get_emoji(770751818158047318)

    if payload.emoji.name == "🌲" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Epic Tree')
        await member.add_roles(role)
    elif payload.emoji.name == "🐟" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Megalodon')
        await member.add_roles(role)
    elif payload.emoji.name == "💰" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Coin Rain')
        await member.add_roles(role)
    elif payload.emoji.name == "⚔️" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Arena')
        await member.add_roles(role)
    elif payload.emoji.name == "🐉" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Miniboss')
        await member.add_roles(role)
    elif payload.emoji.name == HorseEmoji and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Breedar')
        await member.add_roles(role)
    elif payload.emoji.name == "🆕" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Updates')
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload): #Reacao para retirar os cargos
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    HorseEmoji = client.get_emoji(770751818158047318)

    if payload.emoji.name == "🌲" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Epic Tree')
        await member.remove_roles(role)
    elif payload.emoji.name == "🐟" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Megalodon')
        await member.remove_roles(role)
    elif payload.emoji.name == "💰" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Coin Rain')
        await member.remove_roles(role)
    elif payload.emoji.name == "⚔️" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Arena')
        await member.remove_roles(role)
    elif payload.emoji.name == "🐉" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Miniboss')
        await member.remove_roles(role)
    elif payload.emoji.name == HorseEmoji and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Breedar')
        await member.remove_roles(role)
    elif payload.emoji.name == "🆕" and payload.user_id != 819262080200736840:
        role = discord.utils.get(guild.roles, name='Updates')
        await member.remove_roles(role)

#------------Comando de roles Fim----------------

@client.command()
async def ping(ctx): #Comando para testar a latencia
    await ctx.send("Pong")

#--------------Arena Commands Inicio-------------------

EmbedAnterior = None

@client.event
async def on_message(message):
    #Variaveis importantes
    global ArenaList
    global EmbedAnterior
    guild = message.guild
    member = guild.get_member(message.author.id)

    if message.content.lower().startswith("a start"): #Iniciar a lista
        if ArenaList == None: #Verifica se a lista está Vazia
            ArenaList = [member]
            embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
            EmbedAnterior =  await message.channel.send(embed=embed_A_List)
        else:
            await message.channel.send("Arena já em andamento digite \"a join\" para entrar", delete_after=10)
        await message.delete()

    elif message.content.lower().startswith("a list"): #Verificar a lista
        roles_names = [x.name for x in member.roles]
        if 'Sistema' in roles_names or 'Sub-Sistema' in roles_names : #Verifica se o user possui permissão
            if ArenaList == None: #Verifica se a lista está vazia
                await message.channel.send("Arena Vazia, para criar uma digite \"a start\"", delete_after=10) #comando para verificar ArenaList
            else:
                embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
                await message.channel.send(embed=embed_A_List) 
        else:
            await message.channel.send("Você não tem acesso a esse comando", delete_after=10)  
        await message.delete()

    elif message.content.lower().startswith("a join"): #Entrar na lista
        if ArenaList != None and len(ArenaList) < 10: #Verifica se ela está vazia ou cheia
            ArenaList.append(member)
            embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
            await message.channel.delete_messages([EmbedAnterior])
            EmbedAnterior = await message.channel.send(embed=embed_A_List)
        else:
            await message.channel.send("Arena Vazia, para criar uma digite \"a start\"", delete_after=10)
        await message.delete()

    elif message.content.lower().startswith("a reset"): #Resetar a lista
        roles_names = [x.name for x in member.roles]
        if 'Sistema' in roles_names or 'Sub-Sistema' in roles_names : #Verifica se o user possui permissão
            if ArenaList == None: #Verifica se está vazia
                await message.channel.send("Arena Vazia, para criar uma digite \"a start\"", delete_after=10)
            else:
                ArenaList = None
                await message.channel.delete_messages([EmbedAnterior])
                await message.channel.send("Arena Resetada", delete_after=10)
        else:
            await message.channel.send("Você não tem acesso a esse comando", delete_after=10)
        await message.delete()

    elif message.content.lower().startswith("a leave"): #Sair da lista
        if ArenaList == None:
            await message.channel.send("Arena Vazia, para criar uma digite \"a start\"", delete_after=10)
        elif member in ArenaList:
            ArenaList.remove(member)
            embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
            await message.channel.delete_messages([EmbedAnterior])
            EmbedAnterior = await message.channel.send(embed=embed_A_List)
            if len(ArenaList) <= 0:
                    ArenaList = None
            await message.channel.send("Você saiu da arena", delete_after=10)
        else:
            await message.channel.send("Você não entrou na arena digite \"a join\" para entrar", delete_after=10)

    await client.process_commands(message)

#------------Arena Commands Fim-----------------

client.run(TOKEN.get_token()) #Token do bot
