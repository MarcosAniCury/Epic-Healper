#Meus arquivos .py
from Armazenamento import TOKENs
from Armazenamento import EmbedsEpicHealper
from Armazenamento import CRUD

#Bibliotecas python
import discord
import os
import threading
import random
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
async def on_disconnect(erro):
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
    permissão = ctx.channel.permissions_for(ctx.author)
    if permissão.administrator:
        retorno = True
    else:
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
async def credits(ctx): #Comando de agredecimento aos tester
    await ctx.send(embed=EmbedsObj.get_Credits())

@client.command()
async def d(ctx, number, loops): #Comando para rodar um dado
    randomizar = []
    number = int(number)
    for x in range(20):
        randomizar.append(random.randint(0,999))
    for x in range(int(loops)):
        result = random.randint(1, number)
        random.seed(random.randint(random.choice(randomizar),999))
        returnFunc = None 
        if result == number:
            returnFunc = "**"+str(result)+"** <- d"+str(number)+" **CRITÍCO, `dano pra carai`**"
        elif result == 1:
            returnFunc = "**"+str(result)+"** <- d"+str(number)+" **FALHA CRÍTICA**, `se fudeu`"
        else:
            returnFunc = "`"+str(result)+"` <- d"+str(number)
        await ctx.send(returnFunc)

@client.command()
@commands.is_owner()
async def add_adm(ctx, role): #Adiciona um cargo como adm
    guild = ctx.guild
    role_mentions = [x.mention for x in guild.roles] 
    if role in role_mentions: #Verifica se o cargo existe
        Obj = banco.read_ServidoresById(guild.id)
        if Obj["Roles_Adms"] != None:
            lista = Obj["Roles_Adms"]
            lista.append(role)
            Obj["Roles_Adms"] = lista
        else:
            Obj["Roles_Adms"] = [role]
        banco.ServidoresCheck(Obj,"Roles_Adms")
        retorno = "O seguinte cargo foi adicionado como adms: "+role
        await ctx.send(retorno, delete_after=20)
    else:
        await ctx.send("Esse cargo não existe", delete_after=10)
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def remove_adm(ctx, role): #Adiciona um cargo como adm
    guild = ctx.guild
    role_mentions = [x.mention for x in guild.roles] 
    if role in role_mentions: #Verifica se o cargo existe
        Obj = banco.read_ServidoresById(guild.id)
        if role in Obj["Roles_Adms"]:
            lista = Obj["Roles_Adms"]
            lista.remove(role)
            Obj["Roles_Adms"] = lista
            banco.ServidoresCheck(Obj,"Roles_Adms")
            retorno = "O seguinte cargo foi removido como adms: "+role
            await ctx.send(retorno, delete_after=20)
        else:
            await ctx.send("Esse cargo não é um administrador", delete_after=10)
    else:
        await ctx.send("Esse cargo não existe", delete_after=10)
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def list_adm(ctx): #Adiciona um cargo como adm
    guild = ctx.guild
    Obj = banco.read_ServidoresById(guild.id)
    if Obj["Roles_Adms"] != None:
        retorno = "Os cargos setados como adms são:"
        for x in Obj["Roles_Adms"]:
            retorno+=x+" \u200b"
        await ctx.send(retorno, delete_after=20)
    else:
        await ctx.send("Você não registrou nenhum cargo como adm, Digite \""+TOKENs.get_prefix()[0]+" add_adm\" para adicionar")
    await ctx.message.delete()
#------------Comandos Importantes Fim-----------

#-------------Tratamento de exceção Inicio-------------------

@client.event
async def on_command_error(ctx, error): #Tratamento de exceções
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Por favor passe todos os argumentos necessários", delete_after = 20)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado, digite help help para ver os comandos ativos", delete_after = 20)
        channel = banco.read_ServidoresById(ctx.guild.id)
        if channel["Channel_Arena_Commands"] == ctx.message.channel.mention and ctx.author.id != 819262080200736840: #Verificar se os comandos estão habilitados nesse chat
            ctx.message.delete()
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Apenas o dono do server pode executar esse comando", delete_after = 20)
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send("Erro encontrado, reporte a algum adm urgente:erro \""+error.args[0]+"\"", delete_after = 60)
        print(error)
        print("--------------------------------")
        
#-------------Tratamento de exceção Fim-------------------

client.run(TOKENs.get_token()) #Token do bot