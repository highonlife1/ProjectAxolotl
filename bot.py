import discord
import os
import aiohttp
import asyncio

from config import DISCORD_TOKEN
from ranker import calculate_score, get_rank

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Trigger on command and attachment
    if message.content.startswith("!rank") and message.attachments:
        attachment = message.attachments[0]
        if not attachment.filename.endswith((".mp4", ".mov", ".webm")):
            await message.channel.send("Please upload a valid video file (.mp4, .mov, .webm).")
            return

        # Save the video temporarily
        video_path = f"temp_{attachment.filename}"
        await attachment.save(video_path)
        await message.channel.send("Analyzing clip...")

        try:
            score = calculate_score(video_path)
            rank = get_rank(score)

            await message.channel.send(
                f"🧠 PvP Performance Score: **{score}**\n🏅 Assigned Rank: **{rank.upper()}**"
            )
        except Exception as e:
            await message.channel.send("Error while analyzing the video.")
            print(e)
        finally:
            os.remove(video_path)

client.run(DISCORD_TOKEN)
