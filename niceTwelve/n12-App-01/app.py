import yfinance as yf
import pandas as pd
import plotly.express as px
from nicegui import ui as nui

nui.colors(primary='#555')

symbol = 'GOOGL'
data = yf.Ticker(symbol)
tdf = data.history(period='1d', start='2020-05-31', end='2022-05-31').reset_index()



with nui.header().style(
    (
        "color: ##bdbdbd;"
        "background-color: #424242;"
        "font-weight: 600;"
        "font-size: 18px"
    )
).props("elevated"):
    nui.label("Simple Stock Price App")

nui.plotly(
    px.line(
        tdf,
        x='Date',
        y='Volume',
        color_discrete_sequence=['seagreen'])
)
nui.plotly(
    px.line(
        tdf,
        x='Date',
        y='Close',
        color_discrete_sequence=['seagreen'])
)

nui.run(dark=True, port=7860)
