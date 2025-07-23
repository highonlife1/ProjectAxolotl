import discord
import os

from ranker import calculate_score, get_rank

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Trigger on "!rank" command with a video attachment
    if message.content.startswith("!rank") and message.attachments:
        attachment = message.attachments[0]
        if not attachment.filename.endswith((".mp4", ".mov", ".webm")):
            await message.channel.send("❌ Please upload a valid video file (.mp4, .mov, .webm).")
            return

        # Save the video temporarily
        file_path = f"downloads/{attachment.filename}"
        os.makedirs("downloads", exist_ok=True)

        try:
            await message.channel.send("📥 Downloading and analyzing your clip...")
            await attachment.save(file_path)

            score = calculate_score(file_path)
            rank = get_rank(score)

            await message.channel.send(
                f"🧠 PvP Performance Score: **{score}**\n🏅 Assigned Rank: **{rank.upper()}**"
            )
        except Exception as e:
            print("Error during processing:", e)
            await message.channel.send("⚠️ Something went wrong while analyzing the video.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

client.run(DISCORD_TOKEN)
