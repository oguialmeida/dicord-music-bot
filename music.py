import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):  #Classe que comporta as funções para tocar o aúdio desejado.
    def __init__(self, bot): #Função que contém os comandos do FFmpeg e do youtube_dl.
        self.bot = bot    
        self.is_playing = False  
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""           

    @commands.command()
    async def entrar(self,ctx): #Entra no canal caso o participante esteja em um canal de voz.
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz 🙊")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
           await voice_channel.connect()
        else: 
           await ctx.voice_client.move_to(voice_channel)  

    @commands.command()
    async def sair(self,ctx): #Desconecta o bot.
        await ctx.voice_client.disconnect()        

    def procurar(self, item): #Procura pelo nome ou link desejado no youtube.
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:                 
                cut = item
                if(item.startswith("https://www.youtube.com/")):
                    cut = item.split("&", 1)[0] #Utiliza somente o link antes do & para evitar erros.

                info = ydl.extract_info("ytsearch:%s" % cut, download=False)['entries'][0]

            except Exception: 
                return False
            print("LINK OU PESQUISA",item,"FINAL") #Mostra o link inical.
            print("LINK OU PESQUISA",cut[0],"FINAL") #Mostra o link final.

        return {'source': info['formats'][0]['url'], 'title': info['title']} 

    async def tocar(self): #Junta os comandos das bibliotecas FFmpeg com os do discord para o aúdio sair do bot.
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            self.music_queue.pop(0) #Remove o primeiro elemento que esta sendo tocado (Ainda em ajustes).

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.proxima())
        else:
            self.is_playing = False, None   

    @commands.command(name="play") #Toca o aúdio baixado.
    async def p(self, ctx, *args):
        query = " ".join(args)
        song = self.procurar(query)
        voice_channel = ctx.author.voice.channel
        if type(song) == type(True): #Caso não esteja em um canal de voz, ele conecta.
                await ctx.send("Deu ruim 😞... Tenta colocar só o nome 😣")
        else:
            await ctx.send("Adicionada à fila 😊")
            self.music_queue.append([song, voice_channel])

            if self.is_playing == False:
                await self.tocar()  #Chama o tocar e o aúdio é sai do bot como de um usuário.

    @commands.command() 
    async def q(self, ctx): #Cria uma fila e mostra o aúdio que esta tocando (ainda em desevolvimento).
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Sem música na fila 😪")                                                 
        
    @commands.command()
    async def pause(self,ctx):  #Pausa o aúdio desejado.
        await ctx.voice_client.pause() 
        await ctx.send("Parou!⏸️")  

    @commands.command()
    async def resume(self,ctx): #Volta a tocar o aúdio.
        await ctx.voice_client.resume() 
        await ctx.send("Voltou!▶️")

    @commands.command()
    async def pular(self, ctx): #Pula para a próxima música desejada.
        if self.vc != "" and self.vc:
            await ctx.send("Próxima!⏭️")
            self.vc.stop()
            await self.tocar()            
        
def setup(bot):
    bot.add_cog(Music(bot))
