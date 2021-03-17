#Meus arquivos .py
from Scripts import TOKENs

#Bibliotecas python
import discord
from discord import client
from discord.ext.commands.help import HelpCommand

class EpicHealperEmbeds:
    
    #Construtores
    def __init__(self, client):
        self.client = client
        self.HorseEmoji = self.client.get_emoji(770751818158047318) #emoji :HorseT8:
        self.prefix = TOKENs.get_prefix()
        if type(self.prefix) is list:
            self.prefix = self.prefix[0]

    def get_HelpCommand(self):#Embed Command help

        HelpCommand = discord.Embed(
            title = "Comandos",
            description = "Bot feito para ajudar os jogadores do rpg epic\n\u200b",
            colour = 0xBF00FF,
        )

        HelpCommand.add_field(
            name="📄Server Comandos📄", 
            value = "`"+self.prefix+"roles` - para adquirir um cargo\n"
            "`"+self.prefix+"ping` - para testar a latência\n"
            "`"+self.prefix+"helpadm || hadm` - comando help para adms **Apenas ADMs**\n\u200b",
            inline = False
        )

        HelpCommand.add_field(
            name="🍪Arena Comandos🍪",
            value = "`a join` - Entrar na arena\n"
            "`a leave` - Sair da arena\n"
            "\nBot em construção, mais comandos serão adicionados no futuro"
        )

        HelpCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        HelpCommand.set_author(name="EPIC HEALPER", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return HelpCommand

    def get_HelpAdmCommand(self): #Emd Commnad helpadm
        
        HelpAdmCommand = discord.Embed(
            title = "Comandos Adms",
            description = "Bot feito para ajudar os jogadores do rpg epic\n\u200b",
            colour = 0xBF00FF,
        )

        HelpAdmCommand.add_field(
            name="📄Server Comandos📄", 
            value = "`"+self.prefix+"set_adm <cargo ou cargos>` - Setar cargos como adms, para adicionar mais de um coloque juntos e separados por uma virgula\n\u200b",
            inline = False
        )

        HelpAdmCommand.add_field(
            name="🍪Arena Comandos🍪",
            value = "`a reset` - Reinicia a arena\n"
            "`a list` - Mostra a lista da arena\n"
            "`"+self.prefix+"set_arena_commands <menção do canal>` - Setar canal em que comandos da arena serão executados\n"
            "`"+self.prefix+"set_arena_execute <menção do canal>` - Setar canal em a arena será executada (Por padrão é o mesmo que a Arena_Commands)\n"
            "\nBot em construção, mais comandos serão adicionados no futuro"
        )

        HelpAdmCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        HelpAdmCommand.set_author(name="EPIC HEALPER", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return HelpAdmCommand

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

    def get_ArenaExecute(self, ArenaList): #Embed Execute arena
        
        descrisao = "**Copie e cole as menções retirando a sua:**\nrpg miniboss"
        for x in ArenaList:
            descrisao += " `"+x.mention+"`\u200b"
        descrisao += "\n\n**Os membros estão nessa ordem caso não saiba seu id:**\n"
        for x in ArenaList:
            descrisao += str(x)+", "
            ArenaExecute = discord.Embed(
                title="⚔️🍪 Arena 🍪⚔️",
                description=descrisao,
                color=0xFFBF00
            )
        ArenaExecute.set_footer(text="Epic Healper - bot em desenvolvimento", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return ArenaExecute