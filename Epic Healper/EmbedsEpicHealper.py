import discord
from discord import client
from discord.ext.commands.help import HelpCommand

class EpicHealperEmbeds:
    
    #Construtores
    def __init__(self, client):
        self.client = client
        self.HorseEmoji = self.client.get_emoji(770751818158047318) #emoji :HorseT8:

    #Gets Embeds
    def get_HelpCommand(self):#Embed Command help

        HelpCommand = discord.Embed(
            title = "Epic Helper HELP",
            description = "Bot feito para ajudar os jogadores do rpg epic\n\n"
                        "Comandos\n"
                        "help roles - _para adquirir um cargo_\n"
                        "help ping - _para testar a latência_\n\nBot em construção, mais comandos serão adicionados no futuro",
            colour = 0xBF00FF
        )
        HelpCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')

        return HelpCommand

    def get_RolesCommand(self): #Embed Commnad roles

        RolesCommand = discord.Embed(
            title = "Reaja para ganhar os cargos",
            color = 0xFE2EF7, #Roxo
        )

        RolesCommand.description = ":evergreen_tree:-Epic Tree\n:fish:-Megalodon\n:moneybag:-Coin Rain\n:crossed_swords:-Arena\n:dragon:-Miniboss\n{}-Horse Partner\n:new:-Updates".format(self.HorseEmoji)
        
        return RolesCommand

    def get_ArenaCommand(self, ArenaList): #Embed Command arena
        
        descrisao = "Digite \"a join\" para se juntar a arena"
        i=1
        for x in ArenaList:
            descrisao += "\n"+str(i)+"-**"+str(x)+"**"
            i += 1
        ArenaCommand = discord.Embed(
                title="⚔️🍪 Arena "+str(len(ArenaList))+"/"+"10 🍪⚔️",
                description=descrisao,
                color=0xFFBF00
            )
        ArenaCommand.set_footer(text="Epic Healper - bot em desenvolvimento", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return ArenaCommand