import discord
from discord.ext import commands
import os
import dotenv
from datetime import datetime, timedelta, timezone

dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user}")


@bot.event
async def on_message(msg):

    if msg.author.bot: return

    if msg.channel.name != "gulag": return

    print(f"🚨 Triggered by {msg.author}")

    try:
        await msg.delete()
    except discord.Forbidden:
        print(f"⚠️ Could not delete message in #{msg.channel.name}")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=1)

    for channel in msg.guild.text_channels:
        try:
            async for old_msg in channel.history(limit=None, after=cutoff):
                if old_msg.author.id == msg.author.id:
                    try: await old_msg.delete()
                    except discord.Forbidden:
                        print(f"⚠️ Could not delete message in #{channel.name}")

        except discord.Forbidden:
            print(f"⚠️ Could not access #{channel.name}")

    try: await msg.author.send("⚠️ You have been automatically removed from the server because your account triggered the spam protection system.\n\nIf this was a mistake, please contact a server administrator.")
    except discord.Forbidden: print(f"⚠️ Could not DM {msg.author}")

    try:
        await msg.guild.kick(msg.author, reason="Spam/Compromised account")
        print(f"✅ Kicked {msg.author}")

    except discord.Forbidden:
        print(f"❌ FAILED TO KICK {msg.author}: Missing permissions or bot role is too low.")

    alert = (
        "🚨 **Honeypot triggered**\n"
        f"**User:** {msg.author} (`{msg.author.id}`)\n"
        f"**Server:** {msg.guild.name} (`{msg.guild.id}`)\n"
        f"**Channel:** #{msg.channel.name}\n"
    )

    for admin_id in [1120335649610944512, 916749109065551952]: # Iyed, Elyas
        try:
            admin = await bot.fetch_user(admin_id)
            await admin.send(alert)
            print(f"📨 Alert sent to {admin}")

        except discord.Forbidden:
            print(f"⚠️ Could not DM user {admin_id}")

    return


bot.run(TOKEN)