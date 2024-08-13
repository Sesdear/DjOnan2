import json
import asyncio
from DjOnanMainFile import DjOnan

with open("config/config.json", "r") as conf:
    config_file = json.load(conf)

async def main():
    bot = DjOnan()
    await bot.start(config_file["tokenOnan"])

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
