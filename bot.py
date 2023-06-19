from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from parse import *

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guiildId = os.getenv("DISCORD_GUILD")

MY_GUILD = discord.Object(id=guiildId)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}. (ID: {client.user.id}))")
    print("Ready to go!")

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def attacks(interaction: discord.Interaction, playerName: str):
    """Gives stats of the player inputted"""
    actions_count = count_player_attacks(playerName)
    await interaction.response.send_message(f"{playerName} has {actions_count} total attacks.")

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def initiative(interaction: discord.Interaction, playerName: str):
    """Gives stats of the player inputted"""
    actions_count = count_player_initiatives(playerName)
    await interaction.response.send_message(f"{playerName} has rolled initiave {actions_count} total times.")

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def criticalhits(interaction: discord.Interaction, playerName: str):
    """Gives stats of the player inputted"""
    actions_count = count_player_criticalhits(playerName)
    await interaction.response.send_message(f"{playerName} has rolled {actions_count} critical hits.")

client.run(token)