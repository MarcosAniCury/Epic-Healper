#Meus arquivos .py
from discord import channel
from Main import EmbedsObj, checkRoles
from Armazenamento import CRUD
from Armazenamento import EmbedsEpicHealper

#Bibliotecas python
import discord
import asyncio
from discord.ext import commands

global ListMiniboss #Conjuto de MinibossList
listMiniboss = []

class Miniboss(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.Crud()
        self.MinibossList = None
        self.EmbedsObj = EmbedsEpicHealper.EpicHealperEmbeds(client)
        self.EmbedAnterior = None
        self.MaiorLevel = None

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo Miniboss Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect(erro):
        print("Modulo desconectado")
        print("---------------------")

    #-------------------ADM Commands Inicio--------------------------

    @commands.command()
    @commands.check(checkRoles)
    async def set_miniboss_commands(self, ctx, canal):
        if await channel_Exist(ctx, canal): #Verifica se o canal existe
            Obj = self.banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Miniboss_Commands"] = canal
            self.banco.ServidoresCheck(Obj,"Channel_Miniboss_Commands") #Armazenamento
            if Obj["Channel_Miniboss_Execute"] == "None":
                await ctx.send("use o comando **set_miniboss_execute** para setar o local de execução do miniboss", delete_after=10) 
            await ctx.send("Comandos do Miniboss setado para o canal "+canal, delete_after=10)
        else:
            raise commands.CheckFailure

    @commands.command()
    @commands.check(checkRoles)
    async def set_miniboss_execute(self, ctx , canal):
        if await channel_Exist(ctx, canal): #Verifica se o canal existe
            Obj = self.banco.read_ServidoresById(ctx.guild.id)
            Obj["Channel_Miniboss_Execute"] = canal
            self.banco.ServidoresCheck(Obj,"Channel_Miniboss_Execute") #Armazenamento
            await ctx.send("Execução do Miniboss setado para o canal "+canal, delete_after=10)
        else:
            raise commands.CheckFailure

    #------------ADM Commands Fim-----------------

    @commands.Cog.listener()
    async def on_message(self,message):
        #Variaveis importantes
        guild = message.guild
        member = guild.get_member(message.author.id)

        channel = self.banco.read_ServidoresById(guild.id)
        if message.author.id != self.client.user.id:
            if channel["Channel_Miniboss_Commands"] == message.channel.mention: #Verificar se os comandos estão habilitados nesse chat
                
                await message.delete()
                if message.content.lower().startswith("mb join"): #Entrar na lista
                    isNumero = True
                    level = message.content.split(" ")
                    try:
                        level = int(level[2])
                    except ValueError:
                        isNumero = False
                    except IndexError:
                        isNumero = False
                    if isNumero:
                        if self.MinibossList != None and len(self.MinibossList) < 10: #Verifica se ela está vazia ou cheia
                            if True:
                                if self.MaiorLevel[1] < level: #Pegar Maior Level
                                    self.MaiorLevel = [member,level]
                                self.MinibossList.append([member,level]) #Adicionar ao Miniboss
                                await message.channel.delete_messages([self.EmbedAnterior]) #Apagar menssagem anterior
                                embed_M_List = self.EmbedsObj.get_MinibossCommand(self.MinibossList,self.MaiorLevel) 
                                self.EmbedAnterior = await message.channel.send(embed=embed_M_List)
                                if len(self.MinibossList) == 10: #Limite máximo de players
                                    await message.channel.send("Miniboss enviado para "+channel["Channel_Miniboss_Execute"], delete_after=20)
                                    await enviarMiniboss(guild,self.banco,self.MinibossList,self.MaiorLevel,self.EmbedsObj)
                                    await message.channel.delete_messages([self.EmbedAnterior])
                                    self.MinibossList = None
                                    self.MaiorLevel = None
                            else:
                                await message.channel.send("Você já está no Miniboss", delete_after=10)
                        else:
                            self.MinibossList = [[member, level]]
                            self.MaiorLevel = [member,level]
                            embed_M_List = self.EmbedsObj.get_MinibossCommand(self.MinibossList, self.MaiorLevel)
                            if self.EmbedAnterior != None:
                                await message.channel.delete_messages([self.EmbedAnterior])
                            self.EmbedAnterior = await message.channel.send(embed=embed_M_List)
                    else:
                        await message.channel.send("Level inválido, digite novamente", delete_after=10)

                elif message.content.lower().startswith("mb leave"): #Sair da lista
                    if self.MinibossList == None:
                        await message.channel.send("Miniboss Vazio, para criar uma digite \"mb join\"", delete_after=10)
                    elif isInList(self.MinibossList,member):
                        memberRemovido = None
                        for x in self.MinibossList:
                            if x[0] == member:
                                memberRemovido = x
                        self.MinibossList.remove(memberRemovido) #Remover da lista
                        if memberRemovido == self.MaiorLevel:
                            self.MaiorLevel[1] = 0
                            for x in self.MinibossList: #Reverificar o MaiorLevel
                                if x[1] > self.MaiorLevel[1]: 
                                    self.MaiorLevel = x
                        embed_M_List = self.EmbedsObj.get_MinibossCommand(self.MinibossList,self.MaiorLevel)
                        await message.channel.delete_messages([self.EmbedAnterior])
                        self.EmbedAnterior = await message.channel.send(embed=embed_M_List)
                        if len(self.MinibossList) <= 0:
                                self.MinibossList = None
                        await message.channel.send("Você saiu do Miniboss", delete_after=10)
                    else:
                        await message.channel.send("Você não entrou no Miniboss digite \"mb join\" para entrar", delete_after=10)

                elif message.content.lower().startswith("mb list"): #Verificar a lista
                    if checkRolesMiniboss(message,self.banco): #Verifica se o user possui permissão
                        if self.MinibossList == None: #Verifica se a lista está vazia
                            await message.channel.send("Miniboss Vazio, digite \"mb join\" para entrar no Miniboss", delete_after=10) #comando para verificar self.MinibossList
                        else:
                            embed_M_List = self.EmbedsObj.get_MinibossCommand(self.MinibossList,self.MaiorLevel)
                            await message.channel.send(embed=embed_M_List, delete_after=60) 
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")

                elif message.content.lower().startswith("mb reset"): #Resetar a lista
                    if checkRolesMiniboss(message,self.banco): #Verifica se o user possui permissão
                        if self.MinibossList == None: #Verifica se está vazia
                            await message.channel.send("Miniboss Vazio, digite \"mb join\" para entrar no Miniboss", delete_after=10)
                        else:
                            self.MinibossList = None
                            self.MaiorLevel = None
                            await message.channel.delete_messages([self.EmbedAnterior])
                            self.EmbedAnterior = None
                            await message.channel.send("Miniboss Resetado", delete_after=10)
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")

                elif message.content.lower().startswith("mb send"): #Enviar a lista
                    if checkRolesMiniboss(message,self.banco): #Verifica se o user possui permissão
                        if self.MinibossList == None: #Verifica se a lista está vazia
                            await message.channel.send("Miniboss Vazio", delete_after=10) #comando para verificar self.MinibossList
                        elif len(self.MinibossList) < 2:
                            await message.channel.send("Miniboss com menos de 2 players não é permitido", delete_after=10) #comando para verificar se tem menos de 2 players
                        else:
                            MinibossListTemp = self.MinibossList.copy()
                            self.MinibossList = None
                            await enviarMiniboss(guild, self.banco, MinibossListTemp, self.MaiorLevel, self.EmbedsObj) 
                            await message.channel.delete_messages([self.EmbedAnterior])
                            self.EmbedAnterior = None
                    else:
                        await message.channel.send("Você não possui permissão pra usar esse comando")
            else:
                if message.content.lower().startswith("mb "):
                    MinibossCommands = self.banco.read_ServidoresById(guild.id)
                    MinibossCommands = MinibossCommands["Channel_Miniboss_Commands"]
                    await message.channel.send("Comando do Miniboss só podem ser feitos no "+MinibossCommands, delete_after=10)

    #------------Miniboss Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(Miniboss(client))

#-----------Funcoes do Cog Inicio-----------

def checkRolesMiniboss(msg,banco): #Verifica se os cargos tem permissão de ADM
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


async def enviarMiniboss(guild,banco,MinibossList,MaiorLevel,EmbedsObj): #Funcao para enviar a Miniboss para outro chat
        obj = banco.read_ServidoresById(guild.id) #Pegar do bd o canal para executar a Miniboss
        channel = None

        role = discord.utils.get(guild.roles, name='🐉Miniboss Fight')
        for x in MinibossList:
            await x[0].add_roles(role)

        for x in guild.channels:
            if obj["Channel_Miniboss_Execute"] == x.mention:
                channel = x
                break

        Miniboss = EmbedsObj.get_MinibossExecute(MinibossList,MaiorLevel)

        await channel.send(embed=Miniboss)

        await removerCargo(guild,MinibossList)

async def removerCargo(guild,MinibossList):
    listMiniboss.append(MinibossList)
    await asyncio.sleep(20)
    Miniboss = listMiniboss[0]
    listMiniboss.remove(Miniboss) 
    role = discord.utils.get(guild.roles, name='🐉Miniboss Fight')
    for x in Miniboss:
        await x[0].remove_roles(role)

def isInList(MinibossList, member):
        isInlist = False
        for x in MinibossList:
            if member == x[0]:
                isInlist = True
        return isInlist

 #-----------Funcoes do Cog Fim-----------