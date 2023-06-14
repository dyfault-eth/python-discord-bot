import discord
from discord.ui import Button, View
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

bot = discord.Bot()
guildid = [390277332419608579, 707685554178883674, 1057609406822498395]


@bot.event
async def on_ready():  # "allumer" le bot sur le serveur
    print("bot prêt")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("read chart"))


@bot.slash_command(guild_ids=guildid)
async def crypto(ctx, cryptoid="", currencie=""):

    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        if cryptoid != "" and currencie != "":
            if cryptoid == "flag":
                flagResponse = requests.get(
                    "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + currencie + "&ids=for-loot-and-glory&order=market_cap_desc")
                flagPrice = json.loads(flagResponse.text)
                try:
                    flagCryptoPrice = flagPrice[0]["current_price"]
                    flagCryptoPrice = float(flagCryptoPrice)
                    flagDayChange = flagPrice[0]["price_change_percentage_24h"]
                    flagDayChange = float(flagDayChange)
                    await interaction.response.send_message(
                        cryptoid + " : " + "%.3f" % flagCryptoPrice + " " + currencie + " " + "%.2f" % flagDayChange + "% last 24 hours", view=view)
                except requests.exceptions.ConnectionError:
                    await interaction.response.send_message("api connection error try it later", view=view)
                except Exception:
                    await interaction.response.send_message("wrong arguments. please type /idlist to show top50 crypto id.", view=view)
            else:
                response = requests.get(
                    "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + currencie + "&ids=" + cryptoid + "&order=market_cap_desc")
                price = json.loads(response.text)
                try:
                    cryptoPrice = price[0]["current_price"]
                    cryptoPrice = str(cryptoPrice)
                    cryptoPriceF = float(cryptoPrice)
                    dayChange = price[0]["price_change_percentage_24h"]
                    dayChangeF = float(dayChange)
                    if len(str(cryptoPrice)) > 5 and cryptoPrice[0] == "0":
                        await interaction.response.send_message(
                            cryptoid + " : " + "%.4f" % cryptoPriceF + " " + currencie + " " + "%.2f" % dayChangeF + "% last 24 hours", view=view)
                    else:
                        await interaction.response.send_message(
                            cryptoid + " : " + "%.2f" % cryptoPriceF + " " + currencie + " " + "%.2f" % dayChangeF + "% last 24 hours", view=view)
                except requests.exceptions.ConnectionError:
                    await interaction.response.send_message("api connection error try it later", view=view)
                except Exception:
                    await interaction.response.send_message("wrong arguments. please type /idlist to show top50 crypto id.", view=view)
        else:
            await interaction.response.send_message(
                "this command require 2 arguments crypto id and currency.\n for example /crypto bitcoin eur", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    if cryptoid != "" and currencie != "":
        if cryptoid == "flag":
            flagResponse = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + currencie + "&ids=for-loot-and-glory&order=market_cap_desc")
            flagPrice = json.loads(flagResponse.text)
            try:
                flagCryptoPrice = flagPrice[0]["current_price"]
                flagCryptoPrice = float(flagCryptoPrice)
                flagDayChange = flagPrice[0]["price_change_percentage_24h"]
                flagDayChange = float(flagDayChange)
                await ctx.respond(
                    cryptoid + " : " + "%.3f" % flagCryptoPrice + " " + currencie + " " + "%.2f" % flagDayChange + "% last 24 hours", view=view)
            except requests.exceptions.ConnectionError:
                await ctx.respond("api connection error try it later", view=view)
            except Exception:
                await ctx.respond("wrong arguments. please type /idlist to show top50 crypto id.", view=view)
        else:
            response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + currencie + "&ids=" + cryptoid + "&order=market_cap_desc")
            price = json.loads(response.text)
            try:
                cryptoPrice = price[0]["current_price"]
                cryptoPrice = str(cryptoPrice)
                cryptoPriceF = float(cryptoPrice)
                dayChange = price[0]["price_change_percentage_24h"]
                dayChangeF = float(dayChange)
                if len(str(cryptoPrice)) > 5 and cryptoPrice[0] == "0":
                    await ctx.respond(
                        cryptoid + " : " + "%.4f" % cryptoPriceF + " " + currencie + " " + "%.2f" % dayChangeF + "% last 24 hours", view=view)
                else:
                    await ctx.respond(
                        cryptoid + " : " + "%.2f" % cryptoPriceF + " " + currencie + " " + "%.2f" % dayChangeF + "% last 24 hours", view=view)
            except requests.exceptions.ConnectionError:
                await ctx.respond("api connection error try it later", view=view)
            except Exception:
                await ctx.respond("wrong arguments. please type /idlist to show top50 crypto id.", view=view)
    else:
        await ctx.respond("this command require 2 arguments crypto id and currency.\n for example /crypto bitcoin eur ", view=view)


@bot.slash_command(guild_ids=guildid)
async def idlist(ctx):
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1")

        await ctx.respond("list of top 50 crypto and id")

        id_list = json.loads(response.text)
        for i in id_list:
            await ctx.send("symbol : " + i["symbol"] + "\n" + "id : " + i["id"])
    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later")


@bot.slash_command(guild_ids=guildid)
async def asfloor(ctx):

    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            th_response = requests.get("https://api.opensea.io/api/v1/collection/ancienttownhall/stats")
            th = json.loads(th_response.text)
            th_value = th["stats"]["floor_price"]
            th_sales = th["stats"]["one_day_sales"]
            th_volume = th["stats"]["one_day_volume"]

            th_value = "%.4f" % float(th_value)
            th_usd_value = float(price_eth) * float(th_value)
            th_usd_value = "%.2f" % float(th_usd_value)
            th_volume = "%.4f" % float(th_volume)
            th_volume_usd = float(th_volume) * float(price_eth)
            th_volume_usd = "%.2f" % float(th_volume_usd)
            await interaction.response.send_message(f"**TownHall** : {str(th_value)} ETH, USD price : " + str(th_usd_value) + "$\n" + str(
                th_sales) + " Townhall sold last 24h, for a total volume of : " + str(
                th_volume) + " ETH, USD price : " + str(th_volume_usd) + "$\n")

            lj_response = requests.get("https://api.opensea.io/api/v1/collection/ancientlumberjack/stats")
            lj = json.loads(lj_response.text)
            lj_value = lj["stats"]["floor_price"]
            lj_sales = lj["stats"]["one_day_sales"]
            lj_volume = lj["stats"]["one_day_volume"]

            lj_value = "%.4f" % float(lj_value)
            lj_usd_value = float(price_eth) * float(lj_value)
            lj_usd_value = "%.2f" % float(lj_usd_value)
            lj_volume = "%.4f" % float(lj_volume)
            lj_volume_usd = float(lj_volume) * float(price_eth)
            lj_volume_usd = "%.2f" % float(lj_volume_usd)
            await ctx.send(f"**LumberJack** : {str(lj_value)} ETH, USD price : " + str(lj_usd_value) + "$\n" + str(
                    lj_sales) + " LumberJack sold last 24h, for a total volume of : " + str(
                    lj_volume) + " ETH, USD price : " + str(lj_volume_usd) + "$\n")

            sm_response = requests.get("https://api.opensea.io/api/v1/collection/ancientstonemine/stats")
            sm = json.loads(sm_response.text)
            sm_value = sm["stats"]["floor_price"]
            sm_sales = sm["stats"]["one_day_sales"]
            sm_volume = sm["stats"]["one_day_volume"]

            sm_value = "%.4f" % float(sm_value)
            sm_usd_value = float(price_eth) * float(sm_value)
            sm_usd_value = "%.2f" % float(sm_usd_value)
            sm_volume = "%.4f" % float(sm_volume)
            sm_volume_usd = float(sm_volume) * float(price_eth)
            sm_volume_usd = "%.2f" % float(sm_volume_usd)
            await ctx.send(f"**StoneMine** : {str(sm_value)} ETH, USD price : " + str(sm_usd_value) + "$\n" + str(
                    sm_sales) + " StoneMine sold last 24h, for a total volume of : " + str(
                    sm_volume) + " ETH, USD price : " + str(sm_volume_usd) + "$\n")

            fh_response = requests.get("https://api.opensea.io/api/v1/collection/ancientfisherman/stats")
            fh = json.loads(fh_response.text)
            fh_value = fh["stats"]["floor_price"]
            fh_sales = fh["stats"]["one_day_sales"]
            fh_volume = fh["stats"]["one_day_volume"]

            fh_value = "%.4f" % float(fh_value)
            fh_usd_value = float(price_eth) * float(fh_value)
            fh_usd_value = "%.2f" % float(fh_usd_value)
            fh_volume = "%.4f" % float(fh_volume)
            fh_volume_usd = float(fh_volume) * float(price_eth)
            fh_volume_usd = "%.2f" % float(fh_volume_usd)
            if len(str(fh_value)) >= 6:
                fh_usd_value = "%.4f" % float(fh_value)
            else:
                pass
            await ctx.send(f"**FisherMan** : {str(fh_value)} ETH, USD price : " + str(fh_usd_value) + "$\n" + str(
                    fh_sales) + " FisherMan sold last 24h, for a total volume of : " + str(
                    fh_volume) + " ETH, USD price : " + str(fh_volume_usd) + "$\n")

            mine_response = requests.get("https://api.opensea.io/api/v1/collection/ancientmine/stats")
            mine = json.loads(mine_response.text)
            mine_value = mine["stats"]["floor_price"]
            mine_sales = mine["stats"]["one_day_sales"]
            mine_volume = mine["stats"]["one_day_volume"]

            mine_value = "%.4f" % float(mine_value)
            mine_value = "%.3f" % float(mine_value)
            mine_usd_value = float(price_eth) * float(mine_value)
            mine_usd_value = "%.2f" % float(mine_usd_value)
            mine_volume = "%.4f" % float(mine_volume)
            mine_volume_usd = float(mine_volume) * float(price_eth)
            mine_volume_usd = "%.2f" % float(mine_volume_usd)
            await ctx.send(f"**Miner** : {str(mine_value)} ETH, USD price : " + str(mine_usd_value) + "$\n" + str(
                    mine_sales) + " Miner sold last 24h, for a total volume of : " + str(
                    mine_volume) + " ETH, USD price : " + str(mine_volume_usd) + "$\n")

            land_response = requests.get("https://api.opensea.io/api/v1/collection/ancientland/stats")
            land = json.loads(land_response.text)
            land_value = land["stats"]["floor_price"]
            land_sales = land["stats"]["one_day_sales"]
            land_volume = land["stats"]["one_day_volume"]

            land_value = "%.4f" % float(land_value)
            land_value = "%.3f" % float(land_value)
            land_usd_value = float(price_eth) * float(land_value)
            land_usd_value = "%.2f" % float(land_usd_value)
            land_volume = "%.4f" % float(land_volume)
            land_volume_usd = float(land_volume) * float(price_eth)
            land_volume_usd = "%.2f" % float(land_volume_usd)
            await ctx.send(f"**Land** : {str(land_value)} ETH, USD price : " + str(land_usd_value) + "$\n" + str(
                    land_sales) + " Land sold last 24h, for a total volume of : " + str(
                    land_volume) + " ETH, USD price : " + str(land_volume_usd) + "$\n")

            floor_bundle = float(th_value) + float(lj_value) + float(sm_value)
            floor_bundle = "%.3f" % float(floor_bundle)
            floor_usd_bundle = float(price_eth) * float(floor_bundle)
            floor_usd_bundle = "%2.f" % float(floor_usd_bundle)
            await ctx.send(f"**Bundle** : {str(floor_bundle)} ETH, USD price : " + str(floor_usd_bundle) + "$", view=view)

        except requests.exceptions.ConnectionError:
            await ctx.respond("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        th_response = requests.get("https://api.opensea.io/api/v1/collection/ancienttownhall/stats")
        th = json.loads(th_response.text)
        th_value = th["stats"]["floor_price"]
        th_sales = th["stats"]["one_day_sales"]
        th_volume = th["stats"]["one_day_volume"]

        th_value = "%.4f" % float(th_value)
        th_usd_value = float(price_eth) * float(th_value)
        th_usd_value = "%.2f" % float(th_usd_value)
        th_volume = "%.4f" % float(th_volume)
        th_volume_usd = float(th_volume) * float(price_eth)
        th_volume_usd = "%.2f" % float(th_volume_usd)
        await ctx.respond(f"**TownHall** : {str(th_value)} ETH, USD price : " + str(th_usd_value) + "$\n" + str(th_sales) + " Townhall sold last 24h, for a total volume of : " + str(th_volume) + " ETH, USD price : " + str(th_volume_usd) + "$\n")

        lj_response = requests.get("https://api.opensea.io/api/v1/collection/ancientlumberjack/stats")
        lj = json.loads(lj_response.text)
        lj_value = lj["stats"]["floor_price"]
        lj_sales = lj["stats"]["one_day_sales"]
        lj_volume = lj["stats"]["one_day_volume"]

        lj_value = "%.4f" % float(lj_value)
        lj_usd_value = float(price_eth) * float(lj_value)
        lj_usd_value = "%.2f" % float(lj_usd_value)
        lj_volume = "%.4f" % float(lj_volume)
        lj_volume_usd = float(lj_volume) * float(price_eth)
        lj_volume_usd = "%.2f" % float(lj_volume_usd)
        await ctx.send(f"**LumberJack** : {str(lj_value)} ETH, USD price : " + str(lj_usd_value) + "$\n" + str(lj_sales) + " LumberJack sold last 24h, for a total volume of : " + str(lj_volume) + " ETH, USD price : " + str(lj_volume_usd) + "$\n")

        sm_response = requests.get("https://api.opensea.io/api/v1/collection/ancientstonemine/stats")
        sm = json.loads(sm_response.text)
        sm_value = sm["stats"]["floor_price"]
        sm_sales = sm["stats"]["one_day_sales"]
        sm_volume = sm["stats"]["one_day_volume"]

        sm_value = "%.4f" % float(sm_value)
        sm_usd_value = float(price_eth) * float(sm_value)
        sm_usd_value = "%.2f" % float(sm_usd_value)
        sm_volume = "%.4f" % float(sm_volume)
        sm_volume_usd = float(sm_volume) * float(price_eth)
        sm_volume_usd = "%.2f" % float(sm_volume_usd)
        await ctx.send(f"**StoneMine** : {str(sm_value)} ETH, USD price : " + str(sm_usd_value) + "$\n" + str(sm_sales) + " StoneMine sold last 24h, for a total volume of : " + str(sm_volume) + " ETH, USD price : " + str(sm_volume_usd) + "$\n")

        fh_response = requests.get("https://api.opensea.io/api/v1/collection/ancientfisherman/stats")
        fh = json.loads(fh_response.text)
        fh_value = fh["stats"]["floor_price"]
        fh_sales = fh["stats"]["one_day_sales"]
        fh_volume = fh["stats"]["one_day_volume"]

        fh_value = "%.4f" % float(fh_value)
        fh_usd_value = float(price_eth) * float(fh_value)
        fh_usd_value = "%.2f" % float(fh_usd_value)
        fh_volume = "%.4f" % float(fh_volume)
        fh_volume_usd = float(fh_volume) * float(price_eth)
        fh_volume_usd = "%.2f" % float(fh_volume_usd)
        if len(str(fh_value)) >= 6:
            fh_usd_value = "%.4f" % float(fh_value)
        else:
            pass
        await ctx.send(f"**FisherMan** : {str(fh_value)} ETH, USD price : " + str(fh_usd_value) + "$\n" + str(fh_sales) + " FisherMan sold last 24h, for a total volume of : " + str(fh_volume) + " ETH, USD price : " + str(fh_volume_usd) + "$\n")

        mine_response = requests.get("https://api.opensea.io/api/v1/collection/ancientmine/stats")
        mine = json.loads(mine_response.text)
        mine_value = mine["stats"]["floor_price"]
        mine_sales = mine["stats"]["one_day_sales"]
        mine_volume = mine["stats"]["one_day_volume"]

        mine_value = "%.4f" % float(mine_value)
        mine_value = "%.3f" % float(mine_value)
        mine_usd_value = float(price_eth) * float(mine_value)
        mine_usd_value = "%.2f" % float(mine_usd_value)
        mine_volume = "%.4f" % float(mine_volume)
        mine_volume_usd = float(mine_volume) * float(price_eth)
        mine_volume_usd = "%.2f" % float(mine_volume_usd)
        await ctx.send(f"**Miner** : {str(mine_value)} ETH, USD price : " + str(mine_usd_value) + "$\n" + str(mine_sales) + " Miner sold last 24h, for a total volume of : " + str(mine_volume) + " ETH, USD price : " + str(mine_volume_usd) + "$\n")

        land_response = requests.get("https://api.opensea.io/api/v1/collection/ancientland/stats")
        land = json.loads(land_response.text)
        land_value = land["stats"]["floor_price"]
        land_sales = land["stats"]["one_day_sales"]
        land_volume = land["stats"]["one_day_volume"]

        land_value = "%.4f" % float(land_value)
        land_value = "%.3f" % float(land_value)
        land_usd_value = float(price_eth) * float(land_value)
        land_usd_value = "%.2f" % float(land_usd_value)
        land_volume = "%.4f" % float(land_volume)
        land_volume_usd = float(land_volume) * float(price_eth)
        land_volume_usd = "%.2f" % float(land_volume_usd)
        await ctx.send(f"**Land** : {str(land_value)} ETH, USD price : " + str(land_usd_value) + "$\n" + str(land_sales) + " Land sold last 24h, for a total volume of : " + str(land_volume) + " ETH, USD price : " + str(land_volume_usd) + "$\n")

        floor_bundle = float(th_value) + float(lj_value) + float(sm_value)
        floor_bundle = "%.3f" % float(floor_bundle)
        floor_usd_bundle = float(price_eth) * float(floor_bundle)
        floor_usd_bundle = "%2.f" % float(floor_usd_bundle)
        await ctx.send(f"**Bundle** : {str(floor_bundle)} ETH, USD price : " + str(floor_usd_bundle) + "$", view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def cometh(ctx):

    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get("https://api.opensea.io/api/v1/collection/cometh-spaceships/stats")
            price = json.loads(response.text)
            for i in price.values():
                cometh = str(i["floor_price"])
                cometh_usd_price = float(price_eth) * float(cometh)
                cometh_usd_price = "%.2f" % cometh_usd_price
                await interaction.response.send_message("\nSpaceShip : " + cometh[0:5] + " ETH, USD price : " + str(cometh_usd_price) + "$", view=view)

        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/cometh-spaceships/stats")
        price = json.loads(response.text)
        for i in price.values():
            cometh = str(i["floor_price"])
            cometh_usd_price = float(price_eth) * float(cometh)
            cometh_usd_price = "%.2f" % cometh_usd_price
            await ctx.respond("\nSpaceShip : " + cometh[0:5] + " ETH, USD price : " + str(cometh_usd_price) + "$", view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def toonz(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get("https://api.opensea.io/api/v1/collection/degentoonz-collection/stats", view=view)
            price = json.loads(response.text)
            for i in price.values():
                toonzFloor = str(i["floor_price"])
                toonzNbrSales = str(i["one_day_sales"])
                toonzVolume = str(i["one_day_volume"])
                toonz_usd_price = float(price_eth) * float(toonzFloor)
                toonz_usd_price = "%.2f" % toonz_usd_price
                toonz_usd_volume = float(price_eth) * float(toonzVolume)
                toonz_usd_volume = "%.2f" % toonz_usd_volume
                await interaction.response.send_message("\nToonz : " + toonzFloor[0:4] + " ETH, USD price : " + str(toonz_usd_price) + "$\n" + toonzNbrSales + " Toonz sold in the last 24h\n" + "24h total volume : " + toonzVolume[0:5] + " ETH, USD price : " + str(toonz_usd_volume) + "$", view=view)
        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/degentoonz-collection/stats", view=view)
        price = json.loads(response.text)
        for i in price.values():
            toonzFloor = str(i["floor_price"])
            toonzNbrSales = str(i["one_day_sales"])
            toonzVolume = str(i["one_day_volume"])
            toonz_usd_price = float(price_eth) * float(toonzFloor)
            toonz_usd_price = "%.2f" % toonz_usd_price
            toonz_usd_volume = float(price_eth) * float(toonzVolume)
            toonz_usd_volume = "%.2f" % toonz_usd_volume
            await ctx.respond("\nToonz : " + toonzFloor[0:4] + " ETH, USD price : " + str(toonz_usd_price) + "$\n" + toonzNbrSales + " Toonz sold in the last 24h\n" + "24h total volume : " + toonzVolume[0:5] + " ETH, USD price : " + str(toonz_usd_volume) + "$", view=view)
    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def msucup(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get("https://api.opensea.io/api/v1/collection/the-wilsonz-by-metasoccer/stats")
            floor_price = json.loads(response.text)
            floor_price = floor_price["stats"]["floor_price"]
            floor_usd_price = float(price_eth) * float(floor_price)
            floor_usd_price = "%.2f" % floor_usd_price
            print(floor_usd_price)
            await interaction.response.send_message(
                "MSU worldcup floor : " + str(floor_price) + " ETH, USD price : " + str(floor_usd_price) + "$", view=view)
        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/the-wilsonz-by-metasoccer/stats")
        floor_price = json.loads(response.text)
        floor_price = floor_price["stats"]["floor_price"]
        floor_usd_price = float(price_eth) * float(floor_price)
        floor_usd_price = "%.2f" % floor_usd_price
        print(floor_usd_price)
        await ctx.respond("MSU worldcup floor : " + str(floor_price) + " ETH, USD price : " + str(floor_usd_price) + "$", view=view)
    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def blacknano(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get(
                "https://api.opensea.io/api/v1/collection/ledger-market-black-on-black-nano-x/stats")
            nano_stats = json.loads(response.text)
            nano_price = nano_stats["stats"]["floor_price"]
            nano_sold = nano_stats["stats"]["one_day_sales"]
            nano_volume = nano_stats["stats"]["one_day_volume"]

            nano_price = "%.3f" % float(nano_price)
            nano_volume = "%.3f" % float(nano_volume)

            nano_usd_price = float(nano_price) * float(price_eth)
            nano_usd_price = "%.2f" % float(nano_usd_price)
            nano_usd_volume = float(price_eth) * float(nano_volume)
            nano_usd_volume = "%.2f" % float(nano_usd_volume)
            await interaction.response.send_message(
                "Black nano NFT floor price : " + str(nano_price) + " ETH, USD price : " + str(
                    nano_usd_price) + "$ \n" + str(
                    nano_sold) + " sold last 24h, for a total volume of : " + str(
                    nano_volume) + " ETH, USD volume : " + str(
                    nano_usd_volume) + "$", view=view)

        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/ledger-market-black-on-black-nano-x/stats")
        nano_stats = json.loads(response.text)
        nano_price = nano_stats["stats"]["floor_price"]
        nano_sold = nano_stats["stats"]["one_day_sales"]
        nano_volume = nano_stats["stats"]["one_day_volume"]

        nano_price = "%.3f" % float(nano_price)
        nano_volume = "%.3f" % float(nano_volume)

        nano_usd_price = float(nano_price) * float(price_eth)
        nano_usd_price = "%.2f" % float(nano_usd_price)
        nano_usd_volume = float(price_eth) * float(nano_volume)
        nano_usd_volume = "%.2f" % float(nano_usd_volume)
        await ctx.respond(
            "Black nano NFT floor price : " + str(nano_price) + " ETH, USD price : " + str(nano_usd_price) + "$ \n" + str(
                nano_sold) + " sold last 24h, for a total volume of : " + str(nano_volume) + " ETH, USD volume : " + str(
                nano_usd_volume) + "$", view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def flagchart(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        await interaction.response.send_message("https://dex.guru/token/0x9111d6446ac5b88a84cf06425c6286658368542f-polygon", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    await ctx.respond("https://dex.guru/token/0x9111d6446ac5b88a84cf06425c6286658368542f-polygon", view=view)


@bot.slash_command(guild_ids=guildid)
async def marketcap(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        r = requests.get("https://coinmarketcap.com/")
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='cmc-global-stats__content')
        abalise = s.find_all('a')
        for i in abalise:
            if i.get('href') == "/charts/" and len(i.text) >= 16:
                await interaction.response.send_message("Total crypto capitalization : " + i.text, view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    r = requests.get("https://api.coingecko.com/api/v3/global")
    marketcap_result = json.loads(r.text)
    marketcap_global = marketcap_result["data"]["total_market_cap"]["usd"]
    marketcap_global = "%.2f" % float(marketcap_global)

    await ctx.respond("Total crypto capitalization : " + marketcap_global, view=view)


@bot.slash_command(guild_ids=guildid)
async def raider(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get("https://api.opensea.io/api/v1/collection/crypto-raiders-characters/stats")
            price = json.loads(response.text)
            raiderFloor = price["stats"]["floor_price"]

            if len(str(raiderFloor)) >= 4:
                raiderFloor = "%.4f" % float(raiderFloor)

            raider_usd_price = float(price_eth) * float(raiderFloor)
            raider_usd_price = "%.2f" % float(raider_usd_price)

            raiderNbrSales = price["stats"]["one_day_sales"]

            raiderVolume = price["stats"]["one_day_volume"]
            if len(str(raiderVolume)) >= 4:
                raiderVolume = "%.4f" % float(raiderVolume)
            raider_usd_volume = float(price_eth) * float(raiderVolume)
            raider_usd_volume = "%.2f" % float(raider_usd_volume)
            await interaction.response.send_message(
                "Raider : " + str(raiderFloor) + " ETH, USD price : " + str(raider_usd_price) + "$\n" + str(
                    raiderNbrSales) + " Raider sold in the last 24h\n" + "24h total volume : " + str(
                    raiderVolume) + " ETH, USD price : " + str(raider_usd_volume) + "$", view=view)

        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/crypto-raiders-characters/stats")
        price = json.loads(response.text)
        raiderFloor = price["stats"]["floor_price"]

        if len(str(raiderFloor)) >= 4:
            raiderFloor = "%.4f" % float(raiderFloor)

        raider_usd_price = float(price_eth) * float(raiderFloor)
        raider_usd_price = "%.2f" % float(raider_usd_price)

        raiderNbrSales = price["stats"]["one_day_sales"]

        raiderVolume = price["stats"]["one_day_volume"]
        if len(str(raiderVolume)) >= 4:
            raiderVolume = "%.4f" % float(raiderVolume)
        raider_usd_volume = float(price_eth) * float(raiderVolume)
        raider_usd_volume = "%.2f" % float(raider_usd_volume)
        await ctx.respond("Raider : " + str(raiderFloor) + " ETH, USD price : " + str(raider_usd_price) + "$\n" + str(raiderNbrSales) + " Raider sold in the last 24h\n" + "24h total volume : " + str(raiderVolume) + " ETH, USD price : " + str(raider_usd_volume) + "$", view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def raidermob(ctx):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            r_eth = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
            price_eth = json.loads(r_eth.text)
            price_eth = price_eth[0]["current_price"]
            price_eth = "%.2f" % float(price_eth)

            response = requests.get("https://api.opensea.io/api/v1/collection/mobskeys/stats")
            price = json.loads(response.text)
            mobFloor = price["stats"]["floor_price"]

            if len(str(mobFloor)) >= 4:
                mobFloor = "%.4f" % float(mobFloor)

            mob_usd_price = float(price_eth) * float(mobFloor)
            mob_usd_price = "%.2f" % float(mob_usd_price)

            mobNbrSales = price["stats"]["one_day_sales"]

            mobVolume = price["stats"]["one_day_volume"]
            if len(str(mobVolume)) >= 4:
                mobVolume = "%.4f" % float(mobVolume)
            mob_usd_volume = float(price_eth) * float(mobVolume)
            mob_usd_volume = "%.2f" % float(mob_usd_volume)
            await interaction.response.send_message("Raider mob : " + str(mobFloor) + " ETH, USD price : " + str(mob_usd_price) + "$\n" + str(
                mobNbrSales) + " Raider mob sold in the last 24h\n" + "24h total volume : " + str(
                mobVolume) + " ETH, USD price : " + str(mob_usd_volume) + "$", view=view)

        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        r_eth = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc")
        price_eth = json.loads(r_eth.text)
        price_eth = price_eth[0]["current_price"]
        price_eth = "%.2f" % float(price_eth)

        response = requests.get("https://api.opensea.io/api/v1/collection/mobskeys/stats")
        price = json.loads(response.text)
        mobFloor = price["stats"]["floor_price"]

        if len(str(mobFloor)) >= 4:
            mobFloor = "%.4f" % float(mobFloor)

        mob_usd_price = float(price_eth) * float(mobFloor)
        mob_usd_price = "%.2f" % float(mob_usd_price)

        mobNbrSales = price["stats"]["one_day_sales"]

        mobVolume = price["stats"]["one_day_volume"]
        if len(str(mobVolume)) >= 4:
            mobVolume = "%.4f" % float(mobVolume)
        mob_usd_volume = float(price_eth) * float(mobVolume)
        mob_usd_volume = "%.2f" % float(mob_usd_volume)
        await ctx.respond("Raider mob : " + str(mobFloor) + " ETH, USD price : " + str(mob_usd_price) + "$\n" + str(mobNbrSales) + " Raider mob sold in the last 24h\n" + "24h total volume : " + str(mobVolume) + " ETH, USD price : " + str(mob_usd_volume) + "$", view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


@bot.slash_command(guild_ids=guildid)
async def fearandgreed(ctx, days_history=""):
    button = Button(label="reload", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        try:
            button_response = requests.get(
                "https://api.alternative.me/fng/?limit=" + days_history + "&format=json&date_format=world")
            button_fear_greed = json.loads(button_response.text)
            button_fear_greed_name = button_fear_greed["name"]
            await interaction.response.send_message(str(button_fear_greed_name))
            button_fear_greed_value = button_fear_greed["data"]
            for u in button_fear_greed_value:
                button_fear_greed_nbr_value = u["value"]
                button_fear_greed_value_date = u["timestamp"]
                button_fear_greed_value_class = u["value_classification"]
                await ctx.send(
                    str(button_fear_greed_value_date) + " Fear and Greed value : " + str(button_fear_greed_nbr_value) + ", " + str(
                        button_fear_greed_value_class))

            button_dt = datetime.now().replace(microsecond=0)
            button_ts = datetime.timestamp(button_dt)

            button_r_timestamp = requests.get("https://api.alternative.me/fng/?limit=1")
            button_timestamp_load = json.loads(button_r_timestamp.text)
            button_time_left_next_update = button_timestamp_load["data"][0]["time_until_update"]
            button_next_update = int(button_ts) + int(button_time_left_next_update)
            button_dt_object = datetime.fromtimestamp(button_next_update)
            await ctx.send("Next update at : " + button_dt_object.strftime('%a %d-%m-%Y, %H:%M:%S'))

            button_diff = button_dt_object - button_dt
            await ctx.send("The next update will happen in : " + str(button_diff), view=view)

        except requests.exceptions.ConnectionError:
            await interaction.response.send_message("api connection error try it later", view=view)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    try:
        response = requests.get(
            "https://api.alternative.me/fng/?limit=" + days_history + "&format=json&date_format=world")
        fear_greed = json.loads(response.text)
        fear_greed_name = fear_greed["name"]
        await ctx.respond(str(fear_greed_name))
        fear_greed_value = fear_greed["data"]
        for i in fear_greed_value:
            fear_greed_nbr_value = i["value"]
            fear_greed_value_date = i["timestamp"]
            fear_greed_value_class = i["value_classification"]
            await ctx.send(str(fear_greed_value_date) + " Fear and Greed value : " + str(fear_greed_nbr_value) + ", " + str(fear_greed_value_class))

        dt = datetime.now().replace(microsecond=0)
        ts = datetime.timestamp(dt)

        r_timestamp = requests.get("https://api.alternative.me/fng/?limit=1")
        timestamp_load = json.loads(r_timestamp.text)
        time_left_next_update = timestamp_load["data"][0]["time_until_update"]
        next_update = int(ts) + int(time_left_next_update)
        dt_object = datetime.fromtimestamp(next_update)
        await ctx.send("Next update at : " + dt_object.strftime('%a %d-%m-%Y, %H:%M:%S'))

        diff = dt_object - dt
        await ctx.send("The next update will happen in : " + str(diff), view=view)

    except requests.exceptions.ConnectionError:
        await ctx.respond("api connection error try it later", view=view)


token = os.getenv('token')

print("Lancement du bot...")
bot.run(token)  # connection du bot sur le serveur
