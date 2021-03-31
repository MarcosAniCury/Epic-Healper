#Meus arquivos .py
from discord.colour import Color
from Armazenamento import TOKENs

#Bibliotecas python
import discord
from discord import client
from discord.ext.commands.help import HelpCommand

class EpicHealperEmbeds:
    
    #Construtores
    def __init__(self, client):
        self.client = client
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
            value ="`"+self.prefix+"ping` - para testar a latência\n"
            "`"+self.prefix+"helpadm || hadm` - comando help para adms **Apenas ADMs**\n"
            "`"+self.prefix+"credits` - créditos e agradecimentos\n\u200b",
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
            colour = 0xBF00FF, #laranja
        )

        HelpAdmCommand.add_field(
            name="📄Server Comandos📄", 
            value = "`"+self.prefix+"add_adm <cargo ou cargos>` - adicionar cargos como adms\n"
            "`"+self.prefix+"remove_adm <cargo ou cargos>` - remover cargos como adms\n"
            "`"+self.prefix+"list_adm <cargo ou cargos>` - listar todos os cargos setados como adms\n\u200b",
            inline = False
        )

        HelpAdmCommand.add_field(
            name="🍪Arena Comandos🍪",
            value = "`a reset` - Reinicia a arena\n"
            "`a list` - Mostra a lista da arena\n"
            "`a send` - Forçar envio da lista da arena\n"
            "`"+self.prefix+"set_arena_commands <menção do canal>` - Setar canal em que comandos da arena serão executados\n"
            "`"+self.prefix+"set_arena_execute <menção do canal>` - Setar canal em a arena será executada (Por padrão é o mesmo que a Arena_Commands)\n"
            "\nBot em construção, mais comandos serão adicionados no futuro"
        )

        HelpAdmCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        HelpAdmCommand.set_author(name="EPIC HEALPER", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return HelpAdmCommand
    
    def get_Credits(self): #Embed Command Credits

        Credits = discord.Embed(
            title = "Agradecimentos",
            description = "Bom antes de tudo, agradeço a todos os que participaram o desenvolvimento da primeira versão beta do bot."
            "Esse bot foi um sonho de um jovem em aprender e se divertir ao mesmo tempo e esse foi só o começo ainda vamos melhorar muito junto, obrigado a todos que nos ajudaram jogando ou testando."
            "Obrigado",
            Color = 0xFE2EF7 #Roxo
        )

        Credits.add_field(
            name = "Agradecimentos aos ajudantes desenvolvedores", 
            value = "**NOX#4504**, Um grande amigo que sempre me ajudou na parte de programação, e é claro que ele não ficou de fora\n"
            "**Infinity#9473**, Minha companheira e pessoa muito importânte me ajudou muito no desenvolvimento tanto com ideias como com apoio\n"
            "**Snarloff#2055**, Mesmo que ela não vá olhar kkk, me ajudou muito na programação e uma pessoa muito boa" ,
            inline = False
        )

        Credits.add_field(
            name = "Agradecimentos a Staff do Server", 
            value = "**Noryamr#1783**, Um grande amigo que sempre está lá(real pinga ai pra tu ver), e que nos ajudou no crescimento do server, e com certeza merece ser lembrado\n"
            "**Infinity#9473**, Também parte da Staff uma das pessoas que mais sonha em como a nossa comunidade vai crescer e como vai fazer novos amigos\n"
            "**Otakinho#6823**, Novo na Staff, mas bem antigo no server. Sempre on nos ajudando e dando boas risadas\n",
            inline = False
        )

        Credits.add_field(
            name = "Agradecimentos aos Tester", 
            value = "**Toda a Staff**(fiquei com preguiça ^_^): Obrigados a todos vocês que apoiaram a ideia louca de criar um bot\n"
            "**NOX#4504**, Um irmão que a gente grita socorro e aparece pra solucionar seus problemas kkkk\n"
            "**Joaohtop#4045**, Um dos novos Tester e que concerteza mais me ajudou nessa etapa, a animação dele me contagiou tanto que tinha dias que eu vinha feliz programar sabendo que alguém ia gostar\n",
            inline = False
        )

        Credits.add_field(
            name = "OBRIGADO", 
            value = "Obrigado a todos presentes no server que não só apoiaram como são uma das melhores comunidades que alguém poderia fazer parte(as vezes até me pergunto se é real, uma comunidade não toxica na internet kkkk)"
            ".Tenham certeza que tudo isso é graças a vocês que jogam no server e que nos apoiam, __**OBRIGADO POR TUDO**__",
            inline = False
        )

        Credits.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        Credits.set_author(name="EPIC HEALPER", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return Credits

    def get_ArenaCommand(self, ArenaList): #Embed Command arena
        
        descrisao = "Digite \"a join\" para se juntar a arena"
        i=1
        for x in ArenaList:
            descrisao += "\n"+str(i)+"-**"+str(x)+"**"
            i += 1
        ArenaCommand = discord.Embed(
                title="⚔️🍪 Arena "+str(len(ArenaList))+"/"+"10 🍪⚔️",
                description=descrisao,
                color=0xFFBF00 #laranja
            )
        ArenaCommand.set_footer(text="Epic Healper - bot em desenvolvimento", icon_url=f'{self.client.get_user(819262080200736840).avatar_url}')

        return ArenaCommand

    def get_ArenaExecute(self, ArenaList): #Embed Execute arena
        
        descrisao = "**Copie e cole as menções retirando a sua:**\nrpg arena"
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