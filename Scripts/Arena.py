#Meus arquivos .py
from discord import channel
from Main import EmbedsObj, checkRoles
from Armazenamento import CRUD
from Armazenamento import EmbedsEpicHealper

#Bibliotecas python
import discord
import asyncio
from discord.ext import commands

global ListArena #Conjuto de ArenaList
listArena = []

class Arena(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.Crud()
        self.ArenaList = None
        self.EmbedsObj = EmbedsEpicHealper.EpicHealperEmbeds(client)
        self.EmbedAnterior = None

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo Arena Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo desconectado")
        print("---------------------")

    @commands.Cog.listener()
    async def on_message(self,message):
        #Variaveis importantes
        guild = message.guild
        member = guild.get_member(message.author.id)

        channel = self.banco.read_ServidoresById(guild.id)
        if message.author.id != self.client.user.id:
            if channel["Channel_Arena_Commands"] == message.channel.mention: #Verificar se os comandos estão habilitados nesse chat

                await message.delete()
                if message.content.lower().startswith("a join"): #Entrar na lista
                    if self.ArenaList != None and len(self.ArenaList) < 10: #Verifica se ela está vazia ou cheia
                        if not member in self.ArenaList:
                            self.ArenaList.append(member)
                            embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                            await message.channel.delete_messages([self.EmbedAnterior])
                            self.EmbedAnterior = await message.channel.send(embed=embed_A_List)
                            if len(self.ArenaList) == 10:
                                await message.channel.send("Arena enviada para "+channel["Channel_Arena_Execute"], delete_after=20)
                                await enviarArena(guild,self.banco,self.ArenaList,self.EmbedsObj)
                                await message.channel.delete_messages([self.EmbedAnterior])
                                self.ArenaList = None
                        else:
                            await message.channel.send("Você já está na arena", delete_after=10)
                    else:
                        self.ArenaList = [member]
                        embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                        if self.EmbedAnterior != None:
                            await message.channel.delete_messages([self.EmbedAnterior])
                        self.EmbedAnterior = await message.channel.send(embed=embed_A_List)

                elif message.content.lower().startswith("a leave"): #Sair da lista
                    if self.ArenaList == None:
                        await message.channel.send("Arena Vazia, para criar uma digite \"a join\"", delete_after=10)
                    elif member in self.ArenaList:
                        self.ArenaList.remove(member)
                        embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                        await message.channel.delete_messages([self.EmbedAnterior])
                        self.EmbedAnterior = await message.channel.send(embed=embed_A_List)
                        if len(self.ArenaList) <= 0:
                                self.ArenaList = None
                        await message.channel.send("Você saiu da arena", delete_after=10)
                    else:
                        await message.channel.send("Você não entrou na arena digite \"a join\" para entrar", delete_after=10)

                elif message.content.lower().startswith("a list"): #Verificar a lista
                    if checkRolesArena(message,self.banco): #Verifica se o user possui permissão
                        if self.ArenaList == None: #Verifica se a lista está vazia
                            await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10) #comando para verificar self.ArenaList
                        else:
                            embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                            await message.channel.send(embed=embed_A_List, delete_after=60) 
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")

                elif message.content.lower().startswith("a reset"): #Resetar a lista
                    if checkRolesArena(message,self.banco): #Verifica se o user possui permissão
                        if self.ArenaList == None: #Verifica se está vazia
                            await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10)
                        else:
                            self.ArenaList = None
                            await message.channel.delete_messages([self.EmbedAnterior])
                            self.EmbedAnterior = None
                            await message.channel.send("Arena Resetada", delete_after=10)
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")

                elif message.content.lower().startswith("a send"): #Enviar a lista
                    if checkRolesArena(message,self.banco): #Verifica se o user possui permissão
                        if self.ArenaList == None: #Verifica se a lista está vazia
                            await message.channel.send("Arena Vazia", delete_after=10) #comando para verificar self.ArenaList
                        elif len(self.ArenaList) < 2:
                            await message.channel.send("Arena com menos de 2 players não é permitido enviar", delete_after=10) #comando para verificar se tem menos de 2 players
                        else:
                            ArenaListTemp = self.ArenaList.copy()
                            self.ArenaList = None
                            await enviarArena(guild, self.banco, ArenaListTemp, self.EmbedsObj) 
                            await message.channel.delete_messages([self.EmbedAnterior])
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")
            else:
                if message.content.lower().startswith("a "):
                    ArenaCommands = self.banco.read_ServidoresById(guild.id)
                    ArenaCommands = ArenaCommands["Channel_Arena_Commands"]
                    await message.channel.send("Comando da arena só podem ser feitos no "+ArenaCommands, delete_after=10)

    #-------------------ADM Commands--------------------------

    @commands.command()
    @commands.check(checkRoles)
    async def set_arena_commands(self, ctx, canal):
        if await channel_Exist(ctx, canal): #Verifica se o canal existe
            Obj = self.banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Arena_Commands"] = canal
            self.banco.ServidoresCheck(Obj,"Channel_Arena_Commands") #Armazenamento
            await ctx.send("Comandos da arena setada para o canal "+canal, delete_after=10)
        else:
            raise commands.CheckFailure

    @commands.command()
    @commands.check(checkRoles)
    async def set_arena_execute(self, ctx , canal):
        if await channel_Exist(ctx, canal): #Verifica se o canal existe
            Obj = self.banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Arena_Execute"] = canal
            self.banco.ServidoresCheck(Obj,"Channel_Arena_Execute") #Armazenamento
            await ctx.send("Execução da arena setada para o canal "+canal, delete_after=10)
        else:
            raise commands.CheckFailure

#------------Arena Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(Arena(client))

#-----------Funcoes do Cog Inicio-----------

def checkRolesArena(msg,banco): #Verifica se os cargos tem permissão de ADM
        guild = msg.guild
        roles = msg.author.roles
        Obj = banco.read_ServidoresById(guild.id)
        adms = Obj["Roles_Adms"]
        roles_name = [x.mention for x in roles]
        retorno = False
        for x in roles_name:
            if x in adms:
                retorno = True
        return retorno

async def channel_Exist(ctx, canal): #Verifica se o canal existe
    guild = ctx.guild
    channel_mentions = [x.mention for x in guild.channels]
    retorno = canal in channel_mentions
    if not retorno:
        await ctx.send("Esse canal não existe", delete_after=10)
    return retorno


async def enviarArena(guild,banco,ArenaList,EmbedsObj): #Funcao para enviar a arena para outro chat
        obj = banco.read_ServidoresById(guild.id) #Pegar do bd o canal para executar a arena
        channel = None

        role = discord.utils.get(guild.roles, name='Arena Fight')
        for x in ArenaList:
            await x.add_roles(role)

        for x in guild.channels:
            if obj["Channel_Arena_Execute"] == x.mention:
                channel = x
                break

        Arena = EmbedsObj.get_ArenaExecute(ArenaList)

        await channel.send(embed=Arena)

        await removerCargo(guild,ArenaList)

async def removerCargo(guild,ArenaList):
    listArena.append(ArenaList)
    await asyncio.sleep(5*60)
    Arena = listArena[0]
    listArena.remove(Arena) 
    role = discord.utils.get(guild.roles, name='Arena Fight')
    for x in Arena:
        await x.remove_roles(role)

 #-----------Funcoes do Cog Fim-----------