import requests
import os
import discord

from discord.ext import commands


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
INSTANCE_ID = os.getenv("INSTANCE_ID")
SCALEWAY_TOKEN = os.getenv("SCALEWAY_TOKEN")
SCALEWAY_ZONE = os.getenv("SCALEWAY_ZONE")
SCALEWAY_HEADERS = {
    "X-Auth-Token": SCALEWAY_TOKEN,
    "Content-Type": "application/json",
}


bot = commands.Bot(command_prefix='>', description="TEDmkBOT")


async def start_server(ctx):
    await ctx.send("Starting the server...")
    data = {"action": "poweron"}
    requests.post(f"https://api.scaleway.com/instance/v1/zones/{SCALEWAY_ZONE}/servers/{INSTANCE_ID}/action", headers=SCALEWAY_HEADERS, json=data)
    await server_status(ctx)


async def stop_server(ctx):
    await ctx.send("Stoping the server...")
    data = {"action": "poweroff"}
    requests.post(f"https://api.scaleway.com/instance/v1/zones/{SCALEWAY_ZONE}/servers/{INSTANCE_ID}/action", headers=SCALEWAY_HEADERS, json=data)
    await server_status(ctx)


async def server_status(ctx):
    res = requests.get(f"https://api.scaleway.com/instance/v1/zones/{SCALEWAY_ZONE}/servers/{INSTANCE_ID}", headers=SCALEWAY_HEADERS).json()
    embed = discord.Embed(title=f"TerrariaServer VM", description=res["server"]["id"], color=discord.Color.blue())
    embed.add_field(name="status", value=res["server"]["state"])
    await ctx.send(embed=embed)


@bot.command()
async def terraria(ctx, command):
    trans_map = {
        "start": start_server,
        "stop": stop_server,
        "status": server_status,
    }
    if command not in trans_map:
        await ctx.send("Command not found")
        return
    await trans_map[command](ctx)


@bot.event
async def on_ready():
    print('Bot is ready...')


bot.run(DISCORD_TOKEN)
