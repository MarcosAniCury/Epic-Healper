#Meus arquivos .py
from Armazenamento import TOKENs
from Armazenamento import EmbedsEpicHealper
from Armazenamento import CRUD

#Bibliotecas python
import discord
import random
import os
from asyncio.events import Handle
from discord import embeds
from discord.ext import commands
from discord.ext.commands import bot
from pymongo import MongoClient
from discord.ext.commands.errors import CommandNotFound

client = commands.Bot(intents = discord.Intents.all(), command_prefix=TOKENs.get_prefix())

EmbedsObj = None
banco = None

#----------Bot Status Inicio------------

@client.event
async def on_ready():
    print("BOT ONLINE") 
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
    print("BOT ONLINE - Bot foi reconectado") 
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

#-----------Funcoes do Server Inicio-----------

async def checkRoles(ctx): #Verifica se os cargos tem permissão de ADM
    guild = ctx.guild
    roles = ctx.author.roles
    Obj = banco.read_ServidoresById(guild.id)
    adms = Obj["Roles_Adms"]
    roles_name = [x.mention for x in roles]
    retorno = False
    for x in roles_name:
        if x in adms:
            retorno = True
    if not retorno:
        await ctx.send("Você não possui permissão pra usar esse comando")
    return retorno

#-----------Funcoes do Server Fim-----------

#-----------Modulos Inicio-------------

@client.command()
@commands.check(checkRoles)
async def ativar_modulo(ctx, extension):
    client.load_extension(f'Scripts.{extension}')

@client.command()
@commands.check(checkRoles)
async def desativar_modulo(ctx, extension):
    client.unload_extension(f'Scripts.{extension}')

for filename in os.listdir('./Scripts'):
    if filename.endswith('.py'):
        client.load_extension(f'Scripts.{filename[:-3]}') #Load cortando o .py do arquivo

#-----------Modulos Fim-------------

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
@commands.check(checkRoles)
async def helpadm(ctx):
    HelpAdmEmbed = EmbedsObj.get_HelpAdmCommand()
    await ctx.send(embed=HelpAdmEmbed)

#-------------Comandos Help Fim-----------

#------------Comandos Importantes Inicio-----------

@client.command()
async def ping(ctx): #Comando para testar a latencia
    await ctx.send(f'Pong, {round(client.latency * 1000)}ms')

@client.command()
@commands.is_owner()
async def set_adm(ctx, role): #Adiciona um cargo como adm
    guild = ctx.guild
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

#------------Comandos Importantes Fim-----------

#-------------Tratamento de exceção Inicio-------------------

@client.event
async def on_command_error(ctx, error): #Tratamento de exceções
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor passe todos os argumentos necessários")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado, digite help help para ver os comandos ativos")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Apenas o dono do server pode executar esse comando")
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send("Erro encontrado, reporte a algum adm urgente:erro \""+error.args[0]+"\"")
        print(error)
        print("--------------------------------")
        
#-------------Tratamento de exceção Fim-------------------

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

@client.event
async def on_raw_reaction_remove(payload): #Reacao para retirar os cargos
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    HorseEmoji = client.get_emoji(770751818158047318)

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
        elif payload.emoji.name == HorseEmoji:
            role = discord.utils.get(guild.roles, name='Breedar')
            await member.remove_roles(role)
        elif payload.emoji.name == "🆕":
            role = discord.utils.get(guild.roles, name='Updates')
            await member.remove_roles(role)

#------------Comando de roles Fim----------------

client.run(TOKENs.get_token()) #Token do bot