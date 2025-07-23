import discord
import os
import aiohttp
import asyncio

from ranker import calculate_score, get_rank

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!rank") and message.attachments:
        attachment = message.attachments[0]

        if not attachment.filename.endswith((".mp4", ".mov", ".webm")):
            await message.channel.send("❌ Please upload a valid video file (.mp4, .mov, .webm).")
            return

        # Save the video temporarily
        video_path = f"temp_{attachment.filename}"
        await attachment.save(video_path)
        await message.channel.send("🧠 Analyzing your PvP clip...")

        try:
            score = calculate_score(video_path)
            rank = get_rank(score)

            await message.channel.send(
                f"**🧠 PvP Score:** `{score}`\n"
                f"**🏅 Assigned Rank:** `{rank.upper()}`"
            )
        except Exception as e:
            await message.channel.send("❌ Error while analyzing the video.")
            print("Error:", e)
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)

client.run(DISCORD_TOKEN)
