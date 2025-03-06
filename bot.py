
# -*- coding: utf8 -*-
import nextcord
import pytz
from datetime import datetime
from config import *
import sqlite3
import os
from banner import banner_dop
from nextcord.ext import tasks

from nextcord.ext import commands

intents = nextcord.Intents.all()



bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

banner_db = sqlite3.connect('database/banner.db', timeout=10)
banner = banner_db.cursor()

#bot.command




@bot.event
async def on_ready():
    print('Depressed')

    banner_db = sqlite3.connect('database/banner.db', timeout=10)
    banner = banner_db.cursor()

    p_db = sqlite3.connect('database/status.db', timeout=10)
    p = p_db.cursor()

    for guild in bot.guilds:
        banner.execute(
            f"SELECT guild_id FROM bannerdop where guild_id={guild.id}")
        if banner.fetchone() is None:
            banner.execute(
                f"INSERT INTO bannerdop VALUES (0, '{guild.id}')")
        else:
            pass
        banner_db.commit()

        for member in guild.members:

            if member == bot:
                continue

            banner.execute(
                f"SELECT id FROM act where id={member.id}")
            if banner.fetchone() is None:
                banner.execute(
                    f"INSERT INTO act VALUES ('{member.id}', '{guild.id}', 0, 0)")
            else:
                pass
            banner_db.commit()

            p.execute(
                f"SELECT id FROM profile where id={member.id}")
            if p.fetchone() is None:
                p.execute(
                    f"INSERT INTO profile VALUES ('{member.id}', '{guild.id}', 'Пусто')")
            else:
                pass
            p_db.commit()        


@tasks.loop(hours=2)
async def act():
    guild = bot.get_guild(731842650897907824)
    if guild is None:
        return
    for em in banner.execute(f"SELECT id FROM act where guild_id = {guild.id} order by message desc limit 1"):
        banner.execute(f'UPDATE bannerdop SET id={int(em[0])} where guild_id={guild.id}')
        banner_db.commit()

    banner.execute("DELETE FROM act where guild_id = {}".format(guild.id))
    banner_db.commit()
    for member in guild.members:
        if member is None:
            continue
        banner.execute(
            f"SELECT id FROM act where id={member.id}")
        if banner.fetchone() is None:
            banner.execute(
                f"INSERT INTO act VALUES ('{member.id}', '{guild.id}', 0, 0)")
        else:
            pass
        banner_db.commit()

@tasks.loop(minutes=1)
async def main():
    profile_db = sqlite3.connect('database/status.db', timeout=10)
    profile = profile_db.cursor()

    guild = bot.get_guild(731842650897907824)
    if guild is None:
        return
    count = 0

    for v in guild.voice_channels:
        for member in v.members:
            count += 1
    
    for em in banner.execute(f'SELECT id FROM bannerdop where guild_id={guild.id}'):
        member = guild.get_member(int(em[0]))
        if member is None:
            for em in banner.execute(f"SELECT id FROM act where guild_id = {guild.id} order by message desc limit 1"):
                banner.execute(f'UPDATE bannerdop SET id={int(em[0])} where guild_id={guild.id}')
                banner_db.commit()

            banner.execute("DELETE FROM act where guild_id = {}".format(guild.id))
            banner_db.commit()
            for member in guild.members:

                banner.execute(
                    f"SELECT id FROM act where id={member.id}")
                if banner.fetchone() is None:
                    banner.execute(
                        f"INSERT INTO act VALUES ('{member.id}', '{guild.id}', 0, 0)")
                else:
                    pass
                banner_db.commit()          
        else:
            for prof in profile.execute(f"SELECT status FROM profile where id={member.id} and guild_id={guild.id}"):
                avatar = member.display_avatar.url
                name = member.name
                if len(name) > 11:
                    name = f'{name[:11]}...'

                time1 = datetime.now(pytz.timezone('Europe/Moscow'))
                timeout = time1.strftime("%H:%M")
                a = await banner_dop(count, timeout, avatar, name, prof[0])
                await guild.edit(banner=nextcord.File(a))
    
    profile_db.close()

       
@main.before_loop
async def before_main():
    await bot.wait_until_ready()   

@act.before_loop
async def before_act():
    await bot.wait_until_ready()   

act.start()
main.start()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(settings['token'])