import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import sqlite3

profile_db = sqlite3.connect('database/status.db', timeout=40)
profile = profile_db.cursor()

class profileplus(nextcord.ui.Modal):
    def __init__(self):
        super().__init__('Установить статус')

        self.status = nextcord.ui.TextInput(label = 'Новый статус', min_length=1, max_length=10, required=True, placeholder='Только давай без пошлостей^^', style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.status)


    async def callback(self, interaction: nextcord.Interaction) -> None:
        stat = self.status.value


        profile.execute(f"UPDATE profile SET status='{stat}' where id={interaction.user.id} and guild_id={interaction.guild.id}")
        profile_db.commit()

        emb = nextcord.Embed(description=f'Ваш новый статус: `{stat}`', color = 0x2f3136)
        emb.set_thumbnail(url=interaction.user.display_avatar)

        await interaction.send(embed=emb, ephemeral = True)

class page(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    
    @nextcord.slash_command(description="Статус участника на банере")
    async def status(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(profileplus())
        
    @nextcord.slash_command(description="Выдать всем unverify")
    async def add_role(self, ctx, *, role: nextcord.Role):
        for member in ctx.guild.members:
            if role in member.roles:
                continue
            await member.add_roles(role)
        await ctx.send(f"Все участники получили роль {role}!")



    @commands.Cog.listener()
    async def on_message(self, message):
        banner_db = sqlite3.connect('database/banner.db', timeout=10)
        banner = banner_db.cursor()   
        if message.author == self.bot.user:
            return 
        else:
            banner.execute(f"UPDATE act SET message = message + 1 where id={message.author.id} and guild_id={message.guild.id}")
            banner_db.commit()    


def setup(bot):
    bot.add_cog(page(bot))