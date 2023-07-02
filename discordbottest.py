import requests
import os
import random
import discord
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

channel = client.get_channel('1124515281730011301')

api_key = "CHANGE THIS THING"
api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/walltzy"
api_url = api_url + '?api_key=' + api_key
resp = requests.get(api_url)
player_info = resp.json()
puuid = player_info['puuid']
player_account_id = player_info['accountId']

@client.event
async def call():
    await client.wait_until_ready()
    new_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/4_dw_y-KDCIL9TnoO2g3KrwyPVRYkdjZbPZ-y6BQjTfixlR3RnQsjf6DW6Xt7tNjCFJZYQeIhjvU6w/ids?start=0&count=20"
    new_url = new_url + "&api_key=" + api_key
    resp = requests.get(new_url)
    matches = resp.json()
    await channel.send('hello')        
    match = matches[0]
    match2 = matches[0]
    while True:
        time.sleep(120)
        newResponse = requests.get(new_url)
        match2 = newResponse.json()[0]
        await channel.send('Waiting...')

        if match != match2 :
            await channel.send('Match Finished')
            new1_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match2 + "?api_key=" + api_key
            matchInfo = requests.get(new1_url)
            matchData = matchInfo.json()
            indexPlayer = matchData['metadata']['participants'].index(puuid)
            #matchData['info']['participants'][indexPlayer]['championName']
            win = matchData['info']['participants'][indexPlayer]['win']

            if not win:
                await channel.send('He lost')
                print(f'he lost')

            match = match2
            
client.run(TOKEN)
client.call()
