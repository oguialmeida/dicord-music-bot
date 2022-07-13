from discord.ext import commands
from discord.ext.commands.core import command

class Talks(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() #Mensagem para saber que o bot está ligado.
    async def on_ready (self): 
        print('Bot online ---- Ohayoooo')   

    @commands.command()
    async def ajuda(self, message):      
        #Mostra os comandos do Bot
        await message.channel.send('\n ```?play -> colocar músicas \n?pular -> colocar músicas \n?entrar -> entrar no canal \n?sair -> sair do canal \n?q -> saber qual música esta tocando \n?pause -> parar a música \n?resume -> prosseguir a música \n?repita -> repete qualquer coisa dita entre aspas \n?roll -> Roda um dado, EXEMPLO: ?roll "d20" ``` ')     

    @commands.command()
    async def repita(self, message, arg):  #Repete qualquer frase escrita entre aspas.
      await message.channel.send(arg)                

def setup(bot):
    bot.add_cog(Talks(bot))
