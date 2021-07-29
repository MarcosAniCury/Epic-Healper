#Meus arquivos .py
from Armazenamento import TOKENs
from Armazenamento import Embeds3cm
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
    EmbedsObj = Embeds3cm.Epic3cm(client)
    banco = CRUD.Crud()

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\"")) #Alterar status do bot

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
    EmbedsObj = Embeds3cm.Epic3cm(client)
    banco = CRUD.Crud()

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\"")) #Alterar status do bot

#----------Bot Status Fim------------

#-----------Funcoes do Server Inicio-----------

async def checkPlayer(ctx):
    retorno = banco.checkPlayer(ctx.author.id)
    if not retorno:
        ctx.send("Você já possui um personagem criado.")
    return retorno

#-----------Funcoes do Server Fim-----------

#-----------Modulos Inicio-------------

@client.command()
@commands.is_owner()
async def ativar_modulo(ctx, extension):
    await ctx.send("modulo "+extension+" ativado")
    client.load_extension(f'Scripts.{extension}')

@client.command()
@commands.is_owner()
async def desativar_modulo(ctx, extension):
    await ctx.send("modulo "+extension+" desativado")
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
#-------------Comandos Help Fim-----------

#------------Comandos Importantes Inicio-----------

@client.command()
async def ping(ctx): #Comando para testar a latencia
    await ctx.send(f'Pong, {round(client.latency * 1000)}ms')

@client.command()
@client.check(checkPlayer)
async def createPlayer(ctx): #Criar player
    Player = {}

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