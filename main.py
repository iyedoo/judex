import discord
from discord.ext import commands
import os, dotenv

dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]
IYED_ID = os.environ["IYED_ID"]

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


        
        try:
            await msg.author.send(
                "⚠️ You have been automatically removed from the server "
                "because your account triggered the spam protection system.\n\n"
                "If this was a mistake, please contact a server administrator."
            )
        except discord.Forbidden:
            print(f"⚠️ Could not DM {msg.author}")

        try:
            await msg.guild.kick(
                msg.author,
                reason="Spam/Compromised account"
            )
            print(f"Kicked {msg.author}")

        except discord.Forbidden:
            print(
                f"❌ FAILED TO KICK {msg.author}: "
                "Missing permissions or bot role is too low."
            )
            return

        owner = await bot.fetch_user(int(IYED_ID))

        await owner.send(
            f"🚨 **Honeypot triggered**\n"
            f"**User:** {msg.author} (`{msg.author.id}`)\n"
            f"**Server:** {msg.guild.name} (`{msg.guild.id}`)\n"
            f"**Channel:** #{msg.channel.name}\n"
            f"**Action:** Kicked"
        )

        return

bot.run(TOKEN)