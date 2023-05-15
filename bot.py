import discord
from discord import app_commands
import configparser
import random
from pasta import *
from steam import *
import os.path
from discord.ext import tasks
import datetime
import sqlite3

# get secrets from config.ini
CONFIG_PATH = 'config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)
DISCORD_TOKEN = CONFIG.get('discord', 'DISCORD_TOKEN')
GUILD_ID = CONFIG.get('discord', 'GUILD_ID')


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

print("loading all " + str(num_pastas()) + " types of pasta...")

@tree.command(name = "vibecheck", description = "check vibes", guild=discord.Object(id=GUILD_ID))
async def vibe_check(interaction: discord.Interaction, member: discord.Member=None):
    vibe = " passed" if random.randint(0, 100)>50 else " failed"
    if member is None:
        member = interaction.user
    await interaction.response.send_message(member.mention + str(vibe) + " the vibe check")

@tree.command(name = "fact", description = "get a pasta fact", guild=discord.Object(id=GUILD_ID))
async def pasta_fact(interaction: discord.Interaction ):
    await interaction.response.send_message(get_fact())
    
@tree.command(name = "pasta", description = "get a pasta", guild=discord.Object(id=GUILD_ID))
async def pasta_pasta(interaction: discord.Interaction ):
    pasta = get_pasta()
        
    embed_msg=discord.Embed(title=pasta['Type'], color=0xFF0000)
    if pasta['Description'] :
        embed_msg.add_field(name="Description", value=pasta['Description'], inline=False)
    if pasta['Translation'] : 
        embed_msg.add_field(name="Translation", value=pasta['Translation'], inline=False)
    if pasta['Origin'] :
         embed_msg.add_field(name="Origin", value=pasta['Origin'], inline=False)

    path = "images\\"+pasta['Type'] + ".jpg"
        
    if os.path.isfile(path):
        embed_msg.set_thumbnail(url="attachment://"+os.path.basename(path))
        file = discord.File(path, filename=os.path.basename(path))
        await interaction.response.send_message(file=file, embed=embed_msg)
    else:
        await interaction.response.send_message(embed=embed_msg)

@tree.command(name="server", description="serve server stats", guild=discord.Object(id=GUILD_ID))
async def pasta_server(interaction: discord.Interaction):
    # Check if a response has already been sent
    if interaction.response.is_done():
        return
    
    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER)")

    # Check if the message already exists in the database
    cursor.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    print(result)

    if result is None:
        # If the message does not exist, create the initial embed post
        embed = discord.Embed(title='Initial Embed', description='This is the initial embed post.')
        try:
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            print(f"Embed message posted {msg.id}")

            # Insert the message ID and channel ID into the database
            cursor.execute("INSERT INTO messages VALUES (?, ?)", (msg.id, msg.channel.id))
            conn.commit()
        except Exception as e:
            print(F"Failed to send message: {e}")
            return
    else:
        # If the message exists, fetch the message object
        channel_id = result[1]
        channel = interaction.guild.get_channel(channel_id)
        try:
            msg = await channel.fetch_message(msg.id)
        except discord.errors.NotFound:
            # If the message does not exist in the channel, remove it from the database and return
            cursor.execute("DELETE FROM messages WHERE id=?", (msg.id,))
            conn.commit()
            print(f"Message {msg.id} not found in channel")
            return
        
        # If the message exists and the update_embed task is already running, return
        if update_embed.is_running():
            print(f"update_embed task already running for message {msg.id}")
            return
        
    # Close the database connec tion
    conn.close()
    
    # Start the update_embed task with the message object
    update_embed.start(msg)

@tasks.loop(seconds=5)
async def update_embed(msg):
    if msg is None:
        return
    server_info = server_update()

    if server_info:
        embed = discord.Embed(title=f"{server_info['server_name']} ({server_info['ip_address']})", description=f"Map: {server_info['map_name']}\nPlayers: {server_info['player_count']}", color=discord.Color.green())
        #embed.set_thumbnail(url="https://i.imgur.com/nf6UcKT.png") # Replace this with the URL to your server icon or logo
        embed.set_footer(text="Server status as of " + str(datetime.datetime.now()))   
    else:
        print("Failed to retrieve server information.")
    try:
        await msg.edit(embed=embed)
        print(f"Embed message updated")
    except Exception as e:
        print(f"Failed to update message: {e}")
        print("Stopping auto update")
        update_embed.stop()

#print ready
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1095540463328575580))
    print("Ready!")

client.run(DISCORD_TOKEN)


