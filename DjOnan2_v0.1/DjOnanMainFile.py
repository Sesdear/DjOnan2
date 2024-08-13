import discord
from discord.ext import commands
import json


def DjOnan():
    # Загрузка конфигурации
    with open("config/config.json", "r") as conf:
        config_file = json.load(conf)

    # Настраиваем intents
    intents = discord.Intents.default()
    intents.message_content = True

    # Получаем префикс из конфигурационного файла
    prefix = config_file.get('prefix', '!')

    # Создание экземпляра бота с заданным префиксом
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    async def load_cogs():
        # Загрузка всех расширений (COG'ов) из папки commands
        try:
            await bot.load_extension('commands.music')
            print("Cogs loaded successfully")
        except Exception as e:
            print(f"Error loading cogs: {e}")

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print(f'Prefix: {bot.command_prefix}')
        await load_cogs()
    return bot
