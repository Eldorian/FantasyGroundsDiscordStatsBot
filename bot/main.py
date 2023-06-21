from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from parse import *

load_dotenv()

token = os.environ.get("DISCORD_TOKEN")
guiildId = os.environ.get("DISCORD_GUILD")

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
    attacksCount, hitCount, missCount, averageRoll = count_player_attack_outcomes(playerName)
    await interaction.response.send_message(f"{playerName} has made {attacksCount} total attacks. They have an average attack roll of {averageRoll}. They have hit {hitCount} times and missed {missCount} times. NOTE: Hits and Misses are only counted if rolled against a target")

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def initiative(interaction: discord.Interaction, playerName: str):
    """Gives stats of the player inputted"""
    actions_count, average_init = count_player_initiatives(playerName)
    await interaction.response.send_message(f"{playerName} has rolled initiave {actions_count} total times. They have an average initiative roll of {average_init}.")

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def criticalhits(interaction: discord.Interaction, playerName: str):
    """Gives stats of the player inputted"""
    actions_count = count_player_criticalhits(playerName)
    await interaction.response.send_message(f"{playerName} has rolled {actions_count} critical hits.")

client.run(token)