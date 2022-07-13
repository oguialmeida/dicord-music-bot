from discord.ext import commands

bot = commands.Bot("?")  #Prefixo que define o comando para chamar o bot.

#chama os arquivos desejados.
bot.load_extension("music")
bot.load_extension("talks")     
bot.load_extension("thedice") 

#AQUI DEVE CONTER UMA CHAVE ALEATÓRIA QUE É DIFERENTE PARA CADA USUÁRIO.
bot.run('CHAVE') 

