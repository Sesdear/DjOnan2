import json
import discord
from discord.ext import commands
import asyncio
import re
import os
from commands.yt_downloader import download_yt_mp3

class Music(commands.Cog):
    with open("config/config.json", "r") as conf:
        config_file = json.load(conf)
    def __init__(self, bot):
        with open("config/config.json", "r") as conf:
            config_file = json.load(conf)
        self.bot = bot
        self.music_queue = []
        self.is_playing = False
        self.current_voice_client = None
        self.music_folder = config_file["temp_music_dir"]

        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

    async def play_next(self, ctx):
        if self.music_queue:
            temp_dir = self.config_file["temp_music_dir"]
            url_or_file = self.music_queue.pop(0)
            print(f"Playing: {url_or_file}")

            if self.is_youtube_url(url_or_file):
                mp3_file = download_yt_mp3(url_or_file, temp_dir)
                print(f"Downloaded file: {mp3_file}")
            else:
                mp3_file = url_or_file

            try:
                self.current_voice_client.play(discord.FFmpegPCMAudio(mp3_file),
                                               after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
                self.is_playing = True
                print(f"Playing file: {mp3_file}")
            except Exception as e:
                print(f"Error playing file: {e}")
                await ctx.send(f"Ошибка воспроизведения: {e}")
                await self.check_queue_and_disconnect(ctx)

    async def check_queue_and_disconnect(self, ctx):
        """
        Проверяет, есть ли треки в очереди, и отключается от голосового канала, если очередь пуста.
        """
        if not self.music_queue and self.current_voice_client and self.current_voice_client.is_connected():
            self.is_playing = False
            await self.current_voice_client.disconnect()
            print("Disconnected from voice channel.")

    @commands.command(name='play')
    async def play(self, ctx, url_or_name: str = None):
        if url_or_name:
            if self.is_youtube_url(url_or_name):
                self.music_queue.append(url_or_name)
            else:
                music_files = os.listdir(self.music_folder)
                matched_files = [file for file in music_files if url_or_name.lower() in file.lower()]
                if len(matched_files) == 1:
                    file_path = os.path.join(self.music_folder, matched_files[0])
                    self.music_queue.append(file_path)
                    await ctx.send(f"Файл '{matched_files[0]}' добавлен в очередь.")
                elif len(matched_files) > 1:
                    file_list = "\n".join([f"{i + 1}. {file}" for i, file in enumerate(matched_files)])
                    await ctx.send(
                        f"Найдено несколько файлов с похожим названием:\n{file_list}\nСкопируйте название и вставьте его.")
                    self.current_matches = matched_files
                else:
                    await ctx.send(f"Файл с названием '{url_or_name}' не найден.")
                    return
        elif ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            file_path = os.path.join(self.music_folder, attachment.filename)
            await attachment.save(file_path)
            self.music_queue.append(file_path)
            await ctx.send(f"Файл добавлен в очередь: {attachment.filename}")
        else:
            await ctx.send("Укажите URL YouTube, название песни или загрузите файл.")

        if self.current_voice_client is None or not self.current_voice_client.is_connected():
            voice_channel = ctx.author.voice.channel
            if not voice_channel:
                await ctx.send("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
                return
            try:
                self.current_voice_client = await voice_channel.connect()
            except Exception as e:
                await ctx.send(f"Не удалось подключиться к голосовому каналу: {e}")
                return

        if not self.is_playing:
            await self.play_next(ctx)

    @commands.command(name='stop')
    async def stop(self, ctx):
        if self.current_voice_client and self.current_voice_client.is_playing():
            self.current_voice_client.stop()
            self.music_queue = []
            self.is_playing = False
            await ctx.send("Музыка остановлена и очередь очищена.")
        else:
            await ctx.send("Музыка не проигрывается.")

        # Отключаемся от голосового канала
        if self.current_voice_client and self.current_voice_client.is_connected():
            await self.current_voice_client.disconnect()
            self.current_voice_client = None
            print("Disconnected from voice channel.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        if self.current_voice_client and self.current_voice_client.is_playing():
            self.current_voice_client.stop()
            self.is_playing = False
            await ctx.send("Песня пропущена.")
            # Ждём немного, чтобы убедиться, что воспроизведение остановилось
            await asyncio.sleep(1)
        else:
            await ctx.send("Сейчас ничего не играет.")
        # Запускаем воспроизведение следующего трека
        await self.play_next(ctx)

    @commands.command(name='list')
    async def queue(self, ctx):
        if self.music_queue:
            queue_list = "\n".join(
                [f"{i + 1}. {os.path.basename(url_or_file)}" for i, url_or_file in enumerate(self.music_queue)])
            await ctx.send(f"Текущая очередь:\n{queue_list}")
        else:
            await ctx.send("Очередь пуста.")

    @commands.command(name='remove')
    async def remove(self, ctx, index: int):
        """
        - Удаляет трек из очереди по индексу.
        """
        if 0 <= index < len(self.music_queue):
            removed = self.music_queue.pop(index)
            await ctx.send(f"Трек {os.path.basename(removed)} удален из очереди.")
        else:
            await ctx.send("Неверный индекс трека.")

    @commands.command(name='help')
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Help DjOnan2",
            description=f'''
                    ## Команды бота DjOnan2
                    > ### {self.config_file["prefix"]}play - url/file
                    > ### {self.config_file["prefix"]}stop
                    > ### {self.config_file["prefix"]}list - Список треков в очереди
                    > ### {self.config_file["prefix"]}remove - Удаляет по индексу трек из очереди 1 = 0
                ''',
            colour=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    def is_youtube_url(self, url: str) -> bool:
        youtube_regex = re.compile(
            r"(https?:\/\/)?(www\.)?((youtube\.com\/(watch\?v=|v\/)|youtu\.be\/))([a-zA-Z0-9_-]{11})",
            re.IGNORECASE
        )
        return youtube_regex.match(url) is not None

async def setup(bot):
    await bot.add_cog(Music(bot))