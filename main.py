import discord
from discord.ext import commands
import os, dotenv

dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user}")

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if msg.channel.name == "gulag":
        print(f"Triggered by {msg.author}")

        await msg.delete()

        for channel in msg.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel)):
                async for msgg in channel.history(limit=100):
                    if msgg.author.id == msg.author.id:
                        await msgg.delete()
                        break

        await msg.guild.kick(msg.author, reason = "Spam/Compromised account")
        print(f"Kicked {msg.author}")

        return

bot.run(TOKEN)