from io import BytesIO
import discord
from discord.ext import commands
import aiohttp
from discord.ext.commands.core import command
import dotenv
import os
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


dotenv.load_dotenv()
KEY = os.getenv('YAHOO_KEY')
HOST = os.getenv('RAPID_HOST')
SYMBOL_KEY = os.getenv('SYMBOL_API')
rapid_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2"

headers = {
    'x-rapidapi-key': KEY,
    'x-rapidapi-host': HOST
}


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Brief Summary of Stocks"
    )
    async def stockSummary(self, ctx, symbol: str, region: str = "us"):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession(headers=headers) as cs:
                async with cs.get(rapid_url + f"/get-summary?symbol={symbol.upper()}&region={region.upper()}") as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send(f"No information on {symbol.upper()}, try again")
                            return

                        stock_symbol = data['symbol'].upper()
                        stock_company = data['price']['longName']
                        stock_price_symbol = data['price']['currencySymbol']
                        stock_price = data['price']['regularMarketPrice']['raw']
                        stock_high = data['price']['regularMarketDayHigh']['raw']
                        stock_low = data['price']['regularMarketDayLow']['raw']

                        embed = discord.Embed(
                            title=stock_symbol,
                            color=ctx.author.color
                        )
                        embed.add_field(name="Company Name",
                                        value=stock_company, inline=False)
                        embed.add_field(name="Current Price",
                                        value=f"{stock_price_symbol} {stock_price}", inline=False)
                        embed.add_field(name="Day High",
                                        value=f"{stock_price_symbol} {stock_high}", inline=False)
                        embed.add_field(name="Day Low",
                                        value=f"{stock_price_symbol} {stock_low}", inline=False)

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"There is some problem, please try after some time.")

    @commands.command(
        brief="A Candlestick Graph showing trends of Stock",
        description=(
            "Symbol: The Symbol of the Stock.\n"
            "Interval(optional): Time Interval, One of the following is allowed - 1m|2m|5m|15m|60m|1d.\n"
            "Range(optional): One of the following is allowed 1d|5d|1mo|3mo|6mo|1y|2y.\n"
            "Region(optional): One of the following is allowed US|BR|AU|CA|FR|DE|HK|IN|IT|ES|GB|SG."

        )
    )
    async def plotCandle(self, ctx, symbol: str, interval: str = "15m", range: str = "1d", region: str = "US"):
        symbol = symbol.upper()
        region = region.upper()
        async with ctx.channel.typing():
            async with aiohttp.ClientSession(headers=headers) as cs:
                url = rapid_url + \
                    f"/get-chart?interval={interval}&symbol={symbol}&range={range}&region={region}"
                async with cs.get(url) as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send(f"No information on {symbol}, try again")
                            return

                        time_stamps = data['chart']['result'][0]['timestamp']
                        open_price = data['chart']['result'][0]['indicators']['quote'][0]['open']
                        close_price = data['chart']['result'][0]['indicators']['quote'][0]['close']
                        high_price = data['chart']['result'][0]['indicators']['quote'][0]['high']
                        low_price = data['chart']['result'][0]['indicators']['quote'][0]['low']

                        # plotting the data:
                        df_dict = {
                            'date': [datetime.fromtimestamp(x) for x in time_stamps],
                            'open': open_price,
                            'high': high_price,
                            'low': low_price,
                            'close': close_price
                        }
                        df = pd.DataFrame(df_dict)
                        df['date'] = pd.to_datetime(df['date'])
                        df.set_index('date', inplace=True)

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
                            title=f"{symbol}",
                            yaxis_title="Price"
                        )
                        img_bytes = fig.to_image(format="png")
                        b = BytesIO(img_bytes)
                        await ctx.send(file=discord.File(b, filename=f"{symbol}.png"))
                    else:
                        await ctx.send("There is some problem, please try after some time.")

    @commands.command(
        brief="A Line Graph showing trends of Stock Price",
        description=(
            "Symbol: The Symbol of the Stock.\n"
            "Interval(optional): Time Interval, One of the following is allowed - 1m|2m|5m|15m|60m|1d.\n"
            "Range(optional): One of the following is allowed 1d|5d|1mo|3mo|6mo|1y|2y.\n"
            "Region(optional): One of the following is allowed US|BR|AU|CA|FR|DE|HK|IN|IT|ES|GB|SG."

        )
    )
    async def plotPrice(self, ctx, symbol: str, interval: str = '60m', range: str = "1mo", region: str = "US"):
        symbol = symbol.upper()
        region = region.upper()
        url = rapid_url + \
            f"/get-chart?interval={interval}&symbol={symbol}&range={range}&region={region}"
        async with ctx.channel.typing():
            async with aiohttp.ClientSession(headers=headers) as cs:
                async with cs.get(url) as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send("No information on {symbol}, try again")
                            return

                        time_stamp = data['chart']['result'][0]['timestamp']
                        close_price = data['chart']['result'][0]['indicators']['quote'][0]['close']
                        time_stamp = [datetime.fromtimestamp(
                            x) for x in time_stamp]

                        df = pd.DataFrame(list(zip(time_stamp, close_price)),
                                          columns=['Date', 'Close Price'])

                        df['Date'] = pd.to_datetime(df['Date'])

                        fig = px.line(df, x='Date', y='Close Price')
                        fig.update_layout(title=f"{symbol}",)
                        img_bytes = fig.to_image(format='png')
                        b = BytesIO(img_bytes)
                        await ctx.send(file=discord.File(b, filename=f"{symbol}.png"))
                    else:
                        await ctx.send("There is some problem, please try after some time.")

    @commands.command(
        brief="Search for Symbol of Companies."
    )
    async def stockSymbol(self, ctx, name: str):
        query = name.lower()
        url = f"https://financialmodelingprep.com/api/v3/search?query={query}&limit=5&exchange=NASDAQ&apikey={SYMBOL_KEY}"
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    if r.status == 200:
                        data = await r.json(content_type=None)

                        if data is None:
                            await ctx.send(f"No Information about {query.capitalize()}, try again.")
                            return

                        embed = discord.Embed(
                            title="Search Results:",
                            color=ctx.author.color
                        )
                        # adding search results:
                        for i in range(len(data)):
                            embed.add_field(name=data[i]['name'],
                                            value=data[i]['symbol'], inline=False)

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("There is some problem, please try after some time.")


def setup(bot):
    bot.add_cog(Stocks(bot))
