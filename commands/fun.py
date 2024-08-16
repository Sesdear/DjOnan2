import io

import aiohttp
import discord
from discord.ext import commands
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='shit')
    async def shit(self, ctx, mode: str = None):
        if mode == "yourself":
            print('Try to request')
            response = requests.get("https://evilinsult.com/generate_insult.php",
                                    params={"lang": "ru", "type": "json"})
            insult = response.json()
            print('Request done output: ' + insult['insult'])
            await ctx.send(insult['insult'])

    @commands.command(name='globalRename')
    async def global_rename(self, ctx: commands.Context, name: str, type: int = 1):
        if type not in [0, 1, 2, 3]:
            await ctx.send("❌ Недопустимый тип. Используйте 0, 1, 2 или 3.")
            return



        guild = ctx.guild
        bot_role = ctx.guild.me.top_role
        members = guild.members
        await ctx.send("✔ Участники сервера успешно переименованы!")

        for memder in members:
            for role in memder.roles:
                self.role = role

        for member in members:

            if member.id == 642771569440981042:
                print(f"Пропускаем {member.name} ({member.id}), так как у него/нее роль выше, чем у бота.")
                continue
            else:
                print("else:")
                try:
                    if type == 1:
                        await member.edit(nick=name)
                    elif type == 2:
                        if member.nick is None:
                            m_name = member.name
                        else:
                            m_name = member.nick
                        if " " in m_name:
                            a_name = name + " " + m_name[m_name.index(" "):]
                            if len(a_name) > 32:
                                a_name = name
                        else:
                            a_name = name + " " + m_name
                            if len(a_name) > 32:
                                a_name = name
                        await member.edit(nick=a_name)
                    elif type == 3:
                        if member.nick is None:
                            m_name = member.name
                        else:
                            m_name = member.nick
                        if " " in m_name:
                            a_name = m_name[0:m_name.index(" ", 1)] + " " + name
                            if len(a_name) > 32:
                                a_name = name
                        else:
                            a_name = m_name + " " + name
                            if len(a_name) > 32:
                                a_name = name
                        await member.edit(nick=a_name)
                    elif type == 0:
                        if member.nick is not None:
                            await member.edit(nick=None)
                except discord.Forbidden:
                    print(f"Не удалось изменить никнейм для {member.name} ({member.id}) из-за недостаточных прав.")
                    await ctx.send(
                        f"❌ Не удалось изменить никнейм для {member.name} ({member.id}) из-за недостаточных прав.")
                except discord.HTTPException as e:
                    print(f"Произошла HTTP ошибка для {member.name} ({member.id}): {e}")
                    await ctx.send(f"❌ Произошла HTTP ошибка при изменении никнейма для {member.name} ({member.id}): {e}")
                except Exception as e:
                    print(f"Произошла непредвиденная ошибка с {member.name} ({member.id}): {e}")
                    await ctx.send(f"❌ Произошла непредвиденная ошибка с {member.name} ({member.id}): {e}")

    @commands.command(name='globalSpam')
    async def global_spam(self, ctx: commands.Context, text: str, file: str = "-1"):
        guild = ctx.guild
        members = guild.members
        channel = ctx.channel
        visible = True  # Параметр `ephemeral` не используется в текстовых командах, можно убрать.

        await ctx.send("✔", delete_after=5)  # Отправляет сообщение и удаляет его через 5 секунд.

        for user in members:
            try:
                if file == "-1":
                    await user.send(text)
                else:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(file) as resp:
                            if resp.status != 200:
                                return await ctx.send("Не удалось загрузить файл...", delete_after=5)
                            data = io.BytesIO(await resp.read())
                            await user.send(content=text, file=discord.File(data, 'picrelated.png'))
            except discord.HTTPException:
                print(f"Не удалось отправить сообщение {user.name} ({user.id}) - Пользователь может быть заблокирован.")
            except Exception as ex_:
                print(f"Произошла ошибка: {ex_}")


async def setup(bot):
    await bot.add_cog(Fun(bot))