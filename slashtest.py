import discord
from discord import app_commands
import configparser
import random
import json

# get secrets from config.ini
CONFIG_PATH = 'config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)
DISCORD_TOKEN = CONFIG.get('discord', 'DISCORD_TOKEN')
GUILD_ID = CONFIG.get('discord', 'GUILD_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "vibecheck", description = "check vibes", guild=discord.Object(id=GUILD_ID))
async def vibe_check(interaction: discord.Interaction, member: discord.Member=None):
    vibe = " passed" if random.randint(0, 100)>50 else " failed"
    if member is None:
        member = interaction.user
    await interaction.response.send_message(member.mention + str(vibe) + " the vibe check")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1095540463328575580))
    print("Ready!")

client.run(DISCORD_TOKEN)

    