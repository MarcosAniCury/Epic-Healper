#Meus arquivos .py
from discord import channel
from Main import EmbedsObj, checkRoles
from Armazenamento import CRUD
from Armazenamento import EmbedsEpicHealper

#Bibliotecas python
import discord
import asyncio
import random
import youtube_dl
from discord.ext import commands

global iniciativa
iniciativa = []

class Dice(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.Crud()

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo Dice Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo Dice desconectado")
        print("---------------------")

    @commands.Cog.listener()
    async def on_message(self,message):

        #Variaveis importantes
        guild = message.guild
        member = guild.get_member(message.author.id)
        channel = self.banco.read_ServidoresById(guild.id)

        if message.author.id != self.client.user.id:
            if message.content.lower().startswith("rd"):
                mensagem = message.content.split()
                number = int(mensagem[0][2:])
                if len(mensagem) == 1:
                    loops = 1
                else:
                    loops = int(mensagem[1])
                randomizar = []
                for x in range(20):
                    randomizar.append(random.randint(0,999))
                for x in range(loops):
                    result = random.randint(1, number)
                    random.seed(random.randint(random.choice(randomizar),999))
                    returnFunc = None 
                    if result == number:
                        returnFunc = "**"+str(result)+"** <- d"+str(number)+" **CRITÍCO, `dano pra carai`**"
                    elif result == 1:
                        returnFunc = "**"+str(result)+"** <- d"+str(number)+" **FALHA CRÍTICA**, `se fudeu`"
                    else:
                        returnFunc = "`"+str(result)+"` <- d"+str(number)

                    if member.id != 775461234233180180 :
                        returnFunc += " --- Player:`"+member.display_name+"`"
                    else:
                        returnFunc += " --- `Inimigo`"
                    await message.channel.send(returnFunc)
        
    @commands.command()
    async def iniciativa(self, ctx):
        
                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(Dice(client))

#-----------Funcoes do Cog Inicio-----------


#-----------Funcoes do Cog Fim-----------