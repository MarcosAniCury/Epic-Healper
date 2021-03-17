#Meus arquivos .py
from Scripts import TOKENs
from Scripts import EmbedsEpicHealper
from Scripts import CRUD

#Bibliotecas python
import discord
import random
from discord import embeds
from discord.ext import commands
from discord.ext.commands import bot
from pymongo import MongoClient

client = commands.Bot(intents = discord.Intents.all(), command_prefix=TOKENs.get_prefix())

EmbedsObj = None
banco = None

ArenaList = None #Variavel da arena

#Arr = [("Server_id",ctx.guild.id),("Channel_Arena_Commands", "None"),("Channel_Arena_Execute", canal),("Channel_Miniboss", "None"),("Channel_Not_Allower", "None")] #Dict in array form

#----------Bot Status Inicio------------

@client.event
async def on_ready():
    print("BOT ONLINE - Digite help h para ajuda") 
    print(client.user.name)
    print(client.user.id)
    print("----------------------")
    global EmbedsObj 
    global banco
    EmbedsObj = EmbedsEpicHealper.EpicHealperEmbeds(client)
    banco = CRUD.Crud()

    await client.change_presence(activity=discord.Game("\"help h\" alias \"h h\"")) #Alterar status do bot

@client.event
async def on_disconnect():
    print("Bot desconectado verifique sua conexão")

@client.event
async def on_resumed():
    print("BOT ONLINE - Digite help h para ajuda") 
    print(client.user.name)
    print(client.user.id)
    print("----------------------")
    global EmbedsObj 
    global banco
    EmbedsObj = EmbedsEpicHealper.EpicHealperEmbeds(client)
    banco = CRUD.Crud()

    await client.change_presence(activity=discord.Game("\"help h\" alias \"h h\"")) #Alterar status do bot

@client.event
async def on_guild_join(guild):
    Ex = tuple(banco.read_ServidoresById(711375776351649875).items())
    Arr = {"Server_id":"None"}
    for x in Ex:
        if x[0] != "_id": 
            Arr[x[0]] = "None"
    Arr["Server_id"] = guild.id
    banco.ServidoresCheck(Arr,"Server_id")

#----------Bot Status Fim------------

#-------------Comandos Help Inicio-----------

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

@client.command(aliases = ["hadm"])
async def helpadm(ctx):
    if compareAdms_withRoles(ctx.guild, ctx.author.roles): #Verifica se o user possui permissão
        HelpAdmEmbed = EmbedsObj.get_HelpAdmCommand()
        await ctx.send(embed=HelpAdmEmbed)
    else:
        await ctx.send("Você não tem acesso a esse comando", delete_after=10)

#-------------Comandos Help Fim-----------

#------------Comandos Importantes Inicio-----------

@client.command()
async def ping(ctx): #Comando para testar a latencia
    await ctx.send("Pong")

@client.command()
async def set_adm(ctx, role): #Adiciona um cargo como adm
    guild = ctx.guild
    if(ctx.author.id == guild.owner.id):
        role = role.split(",")
        role_mentions = [x.mention for x in ctx.guild.roles] 
        if set(role).intersection(role_mentions): #Verifica se o cargo existe
            Obj = banco.read_ServidoresById(guild.id)
            retorno = None
            if len(role) > 1:
                retorno = "Os seguintes cargos foram adicionados como adms:"
                for x in role:
                    retorno += " \u200b"+x
                Obj["Roles_Adms"] = role
            else:
                retorno = "O seguinte cargo foi adicionado como adms: "+role[0]
                Obj["Roles_Adms"] = role[0]
            banco.ServidoresCheck(Obj,"Roles_Adms")
            await ctx.send(retorno)
        else:
            await ctx.send("Esse cargo não existe", delete_after=10)
    else:
        await ctx.send("Apenas o dono do server tem acesso a essa permissão", delete_after=10)

#------------Comandos Importantes Fim-----------

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


#--------------Arena Commands Inicio-------------------

EmbedAnterior = None

@client.event
async def on_message(message):
    #Variaveis importantes
    global ArenaList
    global EmbedAnterior
    guild = message.guild
    member = guild.get_member(message.author.id)

    channel = banco.read_ServidoresById(guild.id)
    if channel["Channel_Arena_Commands"] == message.channel.mention: #Verificar se os comandos estão habilitados nesse chat
        if message.content.lower().startswith("a join"): #Entrar na lista
            if ArenaList != None and len(ArenaList) < 10: #Verifica se ela está vazia ou cheia
                ArenaList.append(member)
                embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
                await message.channel.delete_messages([EmbedAnterior])
                EmbedAnterior = await message.channel.send(embed=embed_A_List, delete_after=20)
                if len(ArenaList) == 10:
                    await message.channel.send("Arena enviada para"+channel["Channel_Arena_Execute"], delete_after=20)
                    Arena = EmbedsObj.get_ArenaExecute(ArenaList)
                    await enviarArena(guild).send(embed=Arena)
            else:
                ArenaList = [member]
                embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
                EmbedAnterior =  await message.channel.send(embed=embed_A_List)
            await message.delete()

        elif message.content.lower().startswith("a leave"): #Sair da lista
            if ArenaList == None:
                await message.channel.send("Arena Vazia, para criar uma digite \"a join\"", delete_after=10)
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

        elif message.content.lower().startswith("a reset"): #Resetar a lista
            if compareAdms_withRoles(guild,member.roles): #Verifica se o user possui permissão
                if ArenaList == None: #Verifica se está vazia
                    await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10)
                else:
                    ArenaList = None
                    await message.channel.delete_messages([EmbedAnterior])
                    await message.channel.send("Arena Resetada", delete_after=10)
            else:
                await message.channel.send("Você não tem acesso a esse comando", delete_after=10)
            await message.delete()

        elif message.content.lower().startswith("a list"): #Verificar a lista
            if compareAdms_withRoles(guild,member.roles): #Verifica se o user possui permissão
                if ArenaList == None: #Verifica se a lista está vazia
                    await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10) #comando para verificar ArenaList
                else:
                    embed_A_List = EmbedsObj.get_ArenaCommand(ArenaList)
                    await message.channel.send(embed=embed_A_List) 
            else:
                await message.channel.send("Você não tem acesso a esse comando", delete_after=10)  
            await message.delete()
    await client.process_commands(message)

def enviarArena(guild): #Funcao para enviar a arena para outro chat
    obj = banco.read_ServidoresById(guild.id) #Pegar do bd o canal para executar a arena
    retorno = None

    for x in guild.channels:
        if obj["Channel_Arena_Execute"] == x.mention:
            retorno = x

    return retorno

@client.command()
async def set_arena_commands(ctx, canal):
    if compareAdms_withRoles(ctx.guild,ctx.author.roles): #Verifica se o user possui permissão
        if channel_Exist(ctx.guild, canal): #Verifica se o canal existe
            Obj = banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Arena_Commands"] = canal
            banco.ServidoresCheck(Obj,"Channel_Arena_Commands") #Armazenamento
            await ctx.send("Comandos da arena setada para o canal "+canal, delete_after=10)
        else:
            await ctx.send("Esse canal não existe", delete_after=10)
    else:
        await ctx.send("Você não tem acesso a esse comando", delete_after=10)  

@client.command()
async def set_arena_execute(ctx , canal):
    if compareAdms_withRoles(ctx.guild,ctx.author.roles): #Verifica se o user possui permissão
        if channel_Exist(ctx.guild, canal): #Verifica se o canal existe
            Obj = banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Arena_Execute"] = canal
            banco.ServidoresCheck(Obj,"Channel_Arena_Execute") #Armazenamento
            await ctx.send("Execução da arena setada para o canal "+canal, delete_after=10)
        else:
            await ctx.send("Esse canal não existe", delete_after=10)
    else:
        await ctx.send("Você não tem acesso a esse comando", delete_after=10)

#------------Arena Commands Fim-----------------

#-----------Funcoes do Server Inicio-----------

def compareAdms_withRoles(guild,roles): #Verifica se os cargos tem permissão de ADM
    Obj = banco.read_ServidoresById(guild.id)
    adms = list(Obj["Roles_Adms"])
    roles_name = [x.mention for x in roles]
    retorno = False
    for x in roles_name:
        if x in adms:
            retorno = True
    return retorno

def channel_Exist(guild, canal): #Verifica se o canal existe
    channel_mentions = [x.mention for x in guild.channels]
    return canal in channel_mentions

#-----------Funcoes do Server Fim-----------

client.run(TOKENs.get_token()) #Token do bot
