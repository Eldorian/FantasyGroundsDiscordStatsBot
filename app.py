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
    attacksCount, hitCount, missCount, averageRoll = count_player_attack_outcomes(playerName)

    embed = discord.Embed(title=f"{playerName} Combat Attack Statistics", color=discord.Color.blue())
    embed.add_field(name="Total Attacks", value=str(attacksCount), inline=False)
    embed.add_field(name="Average Attack Roll", value=str(averageRoll), inline=False)
    embed.add_field(name="Total Hits", value=str(hitCount), inline=False)
    embed.add_field(name="Total Misses", value=str(missCount), inline=False)
    await interaction.response.send_message(embed = embed)

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the initiative roll of.")
async def initiative(interaction: discord.Interaction, playerName: str):
    actions_count, average_init = count_player_initiatives(playerName)

    embed = discord.Embed(title=f"{playerName} Initiative Statistics", color=discord.Color.blue())
    embed.add_field(name="Total Initiative Rolls", value=str(actions_count), inline=False)
    embed.add_field(name="Average Roll", value=str(average_init), inline=False)

    await interaction.response.send_message(embed = embed)

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the attacks of.")
async def criticalhits(interaction: discord.Interaction, playerName: str):
    actions_count = count_player_criticalhits(playerName)

    embed = discord.Embed(title=f"{playerName} Critical Hits Statistics", color=discord.Color.blue())
    embed.add_field(name="Total Critical Hits", value=str(actions_count), inline=False)

    await interaction.response.send_message(embed = embed)

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to get the spells of.")
async def castspells(interaction: discord.Interaction, playerName: str):
    total_casts, unique_spells, most_cast_spell = track_player_spell_casts(playerName)

    embed = discord.Embed(title=f"{playerName} Spell Statistics", color=discord.Color.blue())
    embed.add_field(name="Total Casts", value=str(total_casts), inline=False)

    spell_list = "\n".join(f"- {spell}" for spell in unique_spells)
    embed.add_field(name="List of Cast Spells", value=spell_list, inline=False)
    embed.add_field(name="Most Popular Spell", value=most_cast_spell, inline=False)

    await interaction.response.send_message(embed = embed)

@client.tree.command()
@app_commands.rename(playerName='text')
@app_commands.describe(playerName="The name of the player to Souls Stolen")
async def soulsstolen(interaction: discord.Interaction, playerName: str):
    kills = souls_stolen(playerName)
    total_kills = sum(kills.values())

    embed = discord.Embed(title=f"{playerName} Souls Stolen Statistics", color=discord.Color.red())
    embed.add_field(name="Total Souls Stolen", value=str(total_kills), inline=False)

    victim_list = "\n".join(f"- {victim}" for victim, count in kills.items())
    embed.add_field(name="Victims", value=victim_list, inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/Msz83qU.png")

    await interaction.response.send_message(embed=embed)

client.run(token)