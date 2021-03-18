#Meus arquivos .py
from Armazenamento import CRUD
from Armazenamento import EmbedsEpicHealper

#Bibliotecas python
import discord
from discord.ext import commands

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
    async def on_message(self,message):
        #Variaveis importantes
        guild = message.guild
        member = guild.get_member(message.author.id)

        channel = self.banco.read_ServidoresById(guild.id)
        if channel["Channel_Arena_Commands"] == message.channel.mention: #Verificar se os comandos estão habilitados nesse chat
            if message.content.lower().startswith("a join"): #Entrar na lista
                if self.ArenaList != None and len(self.ArenaList) < 10: #Verifica se ela está vazia ou cheia
                    self.ArenaList.append(member)
                    embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                    await message.channel.delete_messages([self.EmbedAnterior])
                    self.EmbedAnterior = await message.channel.send(embed=embed_A_List, delete_after=20)
                    if len(self.ArenaList) == 10:
                        await message.channel.send("Arena enviada para"+channel["Channel_Arena_Execute"], delete_after=20)
                        Arena = self.EmbedsObj.get_ArenaExecute(self.ArenaList)
                        await enviarArena(guild,self.banco).send(embed=Arena)
                else:
                    self.ArenaList = [member]
                    embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                    self.EmbedAnterior =  await message.channel.send(embed=embed_A_List)
                await message.delete()

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

            elif message.content.lower().startswith("a reset"): #Resetar a lista
                if compareAdms_withRoles(guild,member.roles,self.banco): #Verifica se o user possui permissão
                    if self.ArenaList == None: #Verifica se está vazia
                        await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10)
                    else:
                        self.ArenaList = None
                        await message.channel.delete_messages([self.EmbedAnterior])
                        await message.channel.send("Arena Resetada", delete_after=10)
                else:
                    await message.channel.send("Você não tem acesso a esse comando", delete_after=10)
                await message.delete()

            elif message.content.lower().startswith("a list"): #Verificar a lista
                if compareAdms_withRoles(guild,member.roles,self.banco): #Verifica se o user possui permissão
                    if self.ArenaList == None: #Verifica se a lista está vazia
                        await message.channel.send("Arena Vazia, digite \"a join\" para entrar na arena", delete_after=10) #comando para verificar self.ArenaList
                    else:
                        embed_A_List = self.EmbedsObj.get_ArenaCommand(self.ArenaList)
                        await message.channel.send(embed=embed_A_List) 
                else:
                    await message.channel.send("Você não tem acesso a esse comando", delete_after=10)  
                await message.delete()

    #-------------------ADM Commands--------------------------

    @commands.command()
    async def set_arena_commands(self, ctx, canal):
        if compareAdms_withRoles(ctx.guild,ctx.author.roles,self.banco): #Verifica se o user possui permissão
            if channel_Exist(ctx.guild, canal): #Verifica se o canal existe
                Obj = self.banco.read_ServidoresById(ctx.guild.id)
                Obj["Channel_Arena_Commands"] = canal
                self.banco.ServidoresCheck(Obj,"Channel_Arena_Commands") #Armazenamento
                await ctx.send("Comandos da arena setada para o canal "+canal, delete_after=10)
            else:
                await ctx.send("Esse canal não existe", delete_after=10)
        else:
            await ctx.send("Você não tem acesso a esse comando", delete_after=10)  

    @commands.command()
    async def set_arena_execute(self, ctx , canal):
        if compareAdms_withRoles(ctx.guild,ctx.author.roles,self.banco): #Verifica se o user possui permissão
            if channel_Exist(ctx.guild, canal): #Verifica se o canal existe
                Obj = self.banco.read_ServidoresById(ctx.guild.id)
                Obj["Channel_Arena_Execute"] = canal
                self.banco.ServidoresCheck(Obj,"Channel_Arena_Execute") #Armazenamento
                await ctx.send("Execução da arena setada para o canal "+canal, delete_after=10)
            else:
                await ctx.send("Esse canal não existe", delete_after=10)
        else:
            await ctx.send("Você não tem acesso a esse comando", delete_after=10)

    @commands.Cog.listener() #Tratamento de exceção
    async def cog_command_error(ctx, error):
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

#------------Arena Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(Arena(client))

#-----------Funcoes do Cog Inicio-----------

def compareAdms_withRoles(guild,roles,banco): #Verifica se os cargos tem permissão de ADM
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

def enviarArena(guild,banco): #Funcao para enviar a arena para outro chat
        obj = banco.read_ServidoresById(guild.id) #Pegar do bd o canal para executar a arena
        retorno = None

        for x in guild.channels:
            if obj["Channel_Arena_Execute"] == x.mention:
                retorno = x

        return retorno

 #-----------Funcoes do Cog Fim-----------