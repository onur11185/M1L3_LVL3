import discord
from discord.ext import commands
from config import token  

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        await channel.send(f' Hoş geldiniz: , {member.mention}!')

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

import random

@bot.command()
async def coinflip(ctx):
    result = random.choice(["Yazı", "Tura"])
    await ctx.send(f"**{result}!**")

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanızı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "https://" in message.content:
        try:
            await message.guild.ban(message.author, reason="Link Gönderdi")
            await message.channel.send(f"{message.author.mention} link gönderdiği için banlandı.")
        except Exception as e:
            await message.channel.send(f"Ban başarısız: {e}")
        return  

    await bot.process_commands(message)

bot.run(token)

