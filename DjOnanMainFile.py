import discord
from discord.ext import commands
import json
import colorama


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
            await bot.load_extension('commands.fun')
            print(colorama.Fore.GREEN + "Cogs loaded successfully" + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED + f"Error loading cogs: {e}" + colorama.Style.RESET_ALL)

    @bot.event
    async def on_ready():
        print(colorama.Fore.GREEN + f'Logged in as {bot.user.name}' + colorama.Style.RESET_ALL)
        print(colorama.Fore.GREEN + f'Prefix: {bot.command_prefix}' + colorama.Style.RESET_ALL)
        await load_cogs()
    return bot
