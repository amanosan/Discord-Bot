import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from io import BytesIO
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import os
import dotenv
import re

dotenv.load_dotenv()
KEY = os.getenv('COIN_MARKET_KEY')
base_url = "https://pro-api.coinmarketcap.com"
cg = CoinGeckoAPI()
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': KEY,
}
coin_list = cg.get_coins_list()


class Crypto(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        brief="Get a history of the Crpytocurrency.",
        description=(
            "Symbol: Symbol of the Cryptocurrency.\n"
            "Date: Date at which you want the information from.(dd-mm-yyyy)\n"
            "Currency: Currency Symbol, USD|INR|EUR| etc."
        )
    )
    async def cryptoHistory(self, ctx, symbol: str, date: str = "31-12-2018", currency: str = "usd"):
        async with ctx.channel.typing():
            try:
                for c in coin_list:
                    if c['symbol'].lower() == symbol.lower():
                        id = c['id']

                data = cg.get_coin_history_by_id(id=id, date=date)

                crypto_name = data['name']
                crypto_symbol = data['symbol']
                crypto_price = data['market_data']['current_price'][currency.lower()]
                crypto_thumbnail = data['image']['small']

                embed = discord.Embed(
                    title=f"History of {symbol.upper()}",
                    color=ctx.author.color
                )
                embed.set_thumbnail(url=crypto_thumbnail)
                embed.add_field(
                    name="Name",
                    value=crypto_name, inline=False
                )
                embed.add_field(
                    name="Symbol",
                    value=crypto_symbol
                )
                embed.add_field(
                    name=f"Price (in {currency.upper()})",
                    value=crypto_price, inline=False
                )
                embed.set_footer(
                    text=f"Above information is as of Date: {date}"
                )
                await ctx.send(embed=embed)
            except Exception as e:
                # await ctx.send(f"No information on {symbol.upper()}, make sure dateis in dd-mm-yyyy format")
                await ctx.send(e)

    @commands.command(
        brief="Brief Summary of the Crypto.",
        description=(
            "Symbol: Symbol of the Cryptocurrency.\n"
            "Currency: Currency Symbol, USD|INR|EUR| etc."
        )
    )
    async def cryptoSummary(self, ctx, symbol: str, currency: str = "usd"):
        async with ctx.channel.typing():
            try:
                for c in coin_list:
                    if c['symbol'].lower() == symbol.lower():
                        id = c['id']

                # getting crypto info using the id:
                data = cg.get_coin_by_id(id=id)

                # getting info
                crypto_thumbnail = data['image']['small']
                crypto_name = data['name']
                crypto_price = data['market_data']['current_price'][currency.lower()]
                crypto_symbol = data['symbol'].upper()
                crypto_hashing = data['hashing_algorithm']
                crypto_description = '. '.join(x.strip()
                                               for x in data['description']['en'].split('.')[:3]) + '.'
                crypto_description = re.sub(
                    "</?(a|A).*?>", "", crypto_description)
                # embed
                embed = discord.Embed(
                    title=crypto_name,
                    color=ctx.author.color
                )
                embed.set_thumbnail(url=crypto_thumbnail)
                embed.add_field(
                    name="Symbol",
                    value=crypto_symbol, inline=False
                )
                embed.add_field(
                    name=f"Price (in {currency.upper()})",
                    value=crypto_price, inline=False
                )
                embed.add_field(
                    name="Hashing Used",
                    value=crypto_hashing, inline=False
                )
                embed.add_field(
                    name="Description",
                    value=f"""html {crypto_description}""", inline=False
                )
                await ctx.send(embed=embed)
            except Exception as e:
                # await ctx.send(f"No information on {symbol.upper()}")
                await ctx.send(e)

    @commands.command(
        brief="Search for the symbol of cryptocurrency.",
        description=(
            "Name: Name of the Crpto to get symbol."
        )
    )
    async def cryptoSymbol(self, ctx, name: str):
        try:
            name = name.lower()

            for c in coin_list:
                if c['id'].lower() == name:
                    coin_name = c['name']
                    symbol = c['symbol'].upper()

            embed = discord.Embed(
                title=coin_name,
                color=ctx.author.color
            )
            embed.add_field(name="Symbol", value=symbol, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"No information on {name}")

    @commands.command(
        brief="A CandleStick Graph showing trends of the Crypto.",
        description=(
            "Symbol: Symbol of the Cryptocurrency.\n"
            "Days: Data up to number of days ago 1|7|14|30|90|180|365(max)\n"
            "Currency: Currency Symbol, USD|INR|EUR| etc."
        )
    )
    async def cryptoCandlePlot(self, ctx, symbol: str, days: int = 7, currency: str = "usd"):
        async with ctx.channel.typing():
            try:
                for c in coin_list:
                    if c['symbol'].lower() == symbol.lower():
                        id = c['id']
                if id is None:
                    await ctx.send(f"No information on {symbol.upper()}")
                    return

                data = cg.get_coin_ohlc_by_id(
                    id=id, vs_currency=currency, days=days)

                time_stamp = []
                open = []
                high = []
                low = []
                close = []

                for x in data:
                    time_stamp.append(float(x[0]))
                    open.append(x[1])
                    high.append(x[2])
                    low.append(x[3])
                    close.append(x[4])

                pd_dict = {
                    'time': [datetime.fromtimestamp(x/1000) for x in time_stamp],
                    'open': open,
                    'high': high,
                    'low': low,
                    'close': close
                }
                df = pd.DataFrame(pd_dict)
                df['time'] = pd.to_datetime(df['time'])
                df.set_index('time', inplace=True)
                candlestick = go.Candlestick(
                    x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']
                )
                fig = go.Figure(data=[candlestick])
                fig.update_layout(
                    xaxis_rangeslider_visible=False,
                    title=f"{symbol.upper()}",
                    yaxis_title="Price"
                )
                img_bytes = fig.to_image(format="png")
                b = BytesIO(img_bytes)
                await ctx.send(file=discord.File(b, filename=f"{symbol}.png"))
            except:
                await ctx.send(f"No information on {symbol.upper}")

    @commands.command(
        brief="A Line Graph showing trends of the Crypto",
        description=(
            "Symbol: Symbol of the Cryptocurrency.\n"
            "Days: Data up to number of days ago 1|7|14|30|90|180|365(max)\n"
            "Currency: Currency Symbol, USD|INR|EUR| etc."
        )
    )
    async def cryptoPricePlot(self, ctx, symbol: str, days: int = 7, currency: str = "usd"):
        async with ctx.channel.typing():
            try:
                for c in coin_list:
                    if c['symbol'].lower() == symbol.lower():
                        id = c['id']

                data = cg.get_coin_ohlc_by_id(
                    id, vs_currency=currency, days=days)

                time_stamp = []
                close = []
                for x in data:
                    time_stamp.append((datetime.fromtimestamp(x[0]/1000)))
                    close.append(x[4])

                df = pd.DataFrame(list(zip(time_stamp, close)),
                                  columns=['Date', 'Close Price'])
                df['Date'] = pd.to_datetime(df['Date'])
                fig = px.line(df, x="Date", y="Close Price")
                fig.update_layout(title=f"{symbol.upper()}")
                img_bytes = fig.to_image(format="png")
                b = BytesIO(img_bytes)
                await ctx.send(file=discord.File(b, filename=f"{symbol}.png"))
            except:
                await ctx.send(f"No information on {symbol.upper()}")


def setup(bot):
    bot.add_cog(Crypto(bot))
