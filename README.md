# 🤖 RSI-Based TSLA Trading Bot

An automated trading bot that uses RSI (Relative Strength Index) and ChatGPT to make trading decisions for Tesla (TSLA) stock.

## 🔑 Prerequisites

You'll need API keys from:
- [TAAPI.io](https://taapi.io/) for RSI data
- [OpenAI](https://platform.openai.com/) for ChatGPT
- [Alpaca](https://alpaca.markets/) for trading (paper trading account recommended for testing)

## 🚀 Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your API keys

## 💫 Usage

Run the bot:
```bash
python trading_bot.py
```

The bot will:
1. Check TSLA's RSI every 2 minutes
2. Ask ChatGPT for trading advice based on the RSI
3. Execute buy/sell orders on Alpaca based on ChatGPT's recommendation
4. Use 2% of your portfolio value for each buy order
5. Sell all shares when receiving a sell signal

## ⚠️ Disclaimer

This is a demonstration bot. Please use paper trading for testing and understand the risks before using real money.

https://api.taapi.io/rsi?secret=API_KEY&type=stocks&symbol=TSLA&interval=1m

https://taapi.io/documentation/integration/direct/

langchain
openai
taapi
alpaca




TRADE TSLA
So we get real time information every minute as function will run every 2 minutes 
POLL every 2 minutes
Pass the information from taapi to chatGPT
message = the current relative strength index (RSI) for TSLA (Tesla Stock) is ${value from taapi}
based on this decide if you should buy sell or do nothing
you are a world expert at stock trading 

Filter the reply
if the text matches buy or the reply from chatpt is sell then continue
create two functions - one function that will buy and one fucnctoin that will sell
we will use a qunatity of 2% of our portfolio. 
if it comes back with nothing then don't do anything. 
if we choose to buy then we need to place an order with alpaca with 2% of our portfolio
or we will sell the stocks we have