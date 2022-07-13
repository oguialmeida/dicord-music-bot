from discord.ext import commands
import random

class Thedice(commands.Cog): 
   def __init__(self, bot):
        self.bot = bot

   @commands.command()
   async def roll(self,message,arg): #Comando para rolar 1 dado de n lados.
        lados = arg.split('d')[1] #Corta o comando passado, passando apenas a string que contém o número.
        result = random.randint(1,int(lados))  #Usa biblioteca random para escolher um número aleatório, e comverte a string para inteiro.
        await message.channel.send(result)

def setup(bot):
    bot.add_cog(Thedice(bot))       