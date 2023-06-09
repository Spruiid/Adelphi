import os
from dotenv import load_dotenv
from discord.utils import get
import discord
from hypixelapi import HypixelAPI
#from mojang import MojangAPI
import MojangAPI
import requests

load_dotenv()
TOKEN = os.getenv('ODgyNzgxMDQwODQ5MDgwMzYw.YTAX6Q.ubSheAlkN40SVsymXOYx0qWSmp4')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# hypixelapi stuff
api = HypixelAPI('d63bcf79-dfe8-4ec7-9adc-0aee21f1fb48')
#uuid = "8ab52fc6-72b9-4834-9ada-cbc39fb349a8"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    role = get(member.guild.roles, id=882756335186350120)
    await member.add_roles(role)
    print(f"{member} was given {role}")
    channel = client.get_channel(883090547181486080)
    await channel.send(f'🎆We got a new Member {member}!🎆\n'
                       f'`{member} is now a {role}`')

# ON Message
@client.event
async def on_message(message):
    if message.content.startswith('-maxdmg'): # input -maxdmg playername
        maxdmg = 0
        x = message.content
        x = x.split()
        x = x[1]
        uuidOfPlayer = MojangAPI.get_uuid(x)
        profiles = api.get_all_skyblock_profiles(uuidOfPlayer)
        profileID = 0

        while profileID < 4:
            try:
                dmg = profiles[list(profiles)[profileID]]["stats"]["highest_critical_damage"]
                profileID += 1
                if dmg >= maxdmg:
                    maxdmg = dmg
            except:
                break
        if maxdmg >= 1000000:
            maxdmg = str(round(int(maxdmg) / 1000000, 2)) + " Mil"
        elif maxdmg >= 1000:
            maxdmg = str(round(int(maxdmg) / 1000, 2)) + " k"

        await message.channel.send(f"⚔ ------Highest Damage of {x}------️⚔️\n"
                                    "Highest Critical hit is: " + str(maxdmg))

    elif message.content.startswith('-bal'): # -bal Player Profile (Mango etc.)
        x = message.content
        try:
            x = x.split()
            name = x[1]
            profile = x[2]
            if profile.upper() == "LIME":
                profile = profile.capitalize()
            response = requests.get(f"https://sky.shiiyu.moe/api/v2/coins/{name}/{profile}")
            data = response.json()
            purse = round(data["purse"])
            bank = round(data["bank"])
            overall = bank + purse

            if purse > 1000000000:
                purse = str(round(int(purse) / 1000000000, 3)) + " b"
            elif purse > 1000000:
                purse = str(round(int(purse) / 1000000, 2)) + " Mil"
            elif purse > 1000:
                purse = str(round(int(purse) / 1000, 2)) + " k"

            if bank > 1000000000:
                bank = str(round(int(bank) / 1000000000, 3)) + " b"
            elif bank > 1000000:
                bank = str(round(int(bank) / 1000000, 2)) + " Mil"
            elif bank > 1000:
                bank = str(round(int(purse) / 1000, 2)) + " k"

            if overall > 1000000000:
                overall = str(round(int(overall) / 1000000000, 3)) + " b"
            elif overall > 1000000:
                overall = str(round(int(overall) / 1000000, 2)) + " Mil"
            elif overall > 1000:
                overall = str(round(int(overall) / 1000, 2)) + " k"

            await message.channel.send(f"💰 ---Balance of {name}  --- 💰 \n"
                                       f"Bank = {bank}               \n"
                                       f"Purse = {purse}               \n"
                                       f"Overall = {overall}")
        except:
            print("error")

    elif message.content.startswith('-history'):
        await message.channel.send(("**🔥                   ------__History__------                   🔥**\n"
                                    "`🍰 Created by Spruiid on 01-09-2021 🍰 \n"
                                    "🎯 Our Main focus is Hypixel Skyblock 🎯 \n"
                                    "📚 Adelphi is Ancient Greek and means \"Brothers\" 📚`").center(25))

    elif message.content.startswith('-bz'):
        response = requests.get(f"https://sky.shiiyu.moe/api/v2/bazaar")
        data = response.json()
        x = message.content
        x = x.split()
        x.pop(0)
        item = ""
        for i in x:
            if i == x[-1]:
                item += i
            else:
                item += i + " "

        try:
            for key in data:
                if str(data[key]['name']).upper() == item.upper():
                    isot = str(round(data[key]['sellPrice'], 1))
                    ibot = str(round(data[key]['buyPrice'], 1))
                    bo = str(round(data[key]['sellPrice'], 1))
                    so = str(round(data[key]['buyPrice'], 1))
                    profitps = (float(ibot) * 64) - (float(isot) * 64)
                    profitps = round(profitps, 1)
                    if profitps >= 1000000:
                        profitps = str(profitps / 1000000) + " Mil "
                    elif profitps >= 100000:
                        profitps = str(round((profitps / 1000), 2)) + " thousand "


            await message.channel.send(f"🛑---Bazaar Stats for {item}---🛑 \n"
                                       f"`Instant Buy[1]: {ibot}$ ▶️ [64] = {float(ibot) * 64}$ `\n "
                                       f"`Instant Sell[1]: {isot}$ ▶️ [64] = {float(isot) * 64}$ `\n"
                                       f"**`Buy Order[1]: {bo}$ ▶️ [64] = {float(bo) * 64}$`** \n"
                                       f"**`Sell Order[1]: {so}$ ▶️ [64] = {float(so) * 64}$`** \n"
                                       f"--------------------------------------------------------------- \n"
                                       f"Profit per Stack = {profitps}$")
        except:
            await message.channel.send("Wrong input. #bot-commands-explained ")

    elif message.content.upper().startswith("-BAZAAR FLIPPER"):
        response = requests.get(f"https://sky.shiiyu.moe/api/v2/bazaar")
        data = response.json()

        liste = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        nameList = ["", "", "", "", "", "", "", "", "", ""]

        for key in data:
            sPrice = data[key]['sellPrice']
            profit = data[key]['buyPrice'] - sPrice

            i = 0
            for number in liste:
                if sPrice != 0:
                    if profit / sPrice * 100 > number:
                        liste[i] = round(profit / sPrice * 100,1)
                        nameList[i] = data[key]['name']
                    else:
                        i += 1

        await message.channel.send(f"**🗺️-Bazaar    Flipper    Adelphi-🗺️ **\n"
                                   f"`Full Guide in #bot-commands-explained \n"
                                   f"\n"
                                   f"1. {nameList[0]} ▶ {liste[0]} %\n"
                                   f"2. {nameList[1]} ▶ {liste[1]} %\n"
                                   f"3. {nameList[2]} ▶ {liste[2]} %\n"
                                   f"4. {nameList[3]} ▶ {liste[3]} %\n"
                                   f"5. {nameList[4]} ▶ {liste[4]} %\n"
                                   f"6. {nameList[5]} ▶ {liste[5]} %\n"
                                   f"7. {nameList[6]} ▶ {liste[6]} %\n"
                                   f"8. {nameList[7]} ▶ {liste[7]} %\n"
                                   f"9. {nameList[8]} ▶ {liste[8]} %\n"
                                   f"10. {nameList[9]} ▶ {liste[9]} %`")

client.run("ODgyNzgxMDQwODQ5MDgwMzYw.YTAX6Q.ubSheAlkN40SVsymXOYx0qWSmp4")