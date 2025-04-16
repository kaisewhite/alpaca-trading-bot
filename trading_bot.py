import os
import datetime
import time
from typing import Literal
from dotenv import load_dotenv
import requests
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import alpaca_trade_api as tradeapi
import logging


# Set up logging with INFO level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize API clients
TAAPI_API_KEY = os.getenv('TAAPI_API_KEY')
llm = ChatOpenAI(model="gpt-4", temperature=0)
alpaca = tradeapi.REST(
    os.getenv('ALPACA_API_KEY'),
    os.getenv('ALPACA_SECRET_KEY'),
    base_url=os.getenv('ALPACA_BASE_URL')
)

def fetch_rsi(symbol: str) -> float:
    """Fetch RSI for the given symbol using TA API."""
    try:
        logger.info(f"Fetching RSI for {symbol}...")
        url = f"https://api.taapi.io/rsi"
        params = {
            "secret": TAAPI_API_KEY,
            "type": "stocks",
            "symbol": symbol,
            "interval": "1d"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data.get('value', 50.0))  # Default to 50.0 if value is not found
    except Exception as e:
        logger.error(f"Error fetching RSI: {e}")
        return 50.0  # Return neutral value on error

def ask_chatgpt(rsi: float) -> str:
    """Send prompt to OpenAI via Langchain and return response."""
    prompt = f"""The current relative strength index (RSI) for TSLA (Tesla Stock) is {rsi}. 
    Based on this, should I buy, sell, or do nothing? 
    You are a world expert at stock trading."""
    
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content

def interpret_response(text: str) -> Literal["buy", "sell", "nothing"]:
    """Normalize response to: 'buy' | 'sell' | 'nothing'."""
    text = text.lower()
    if "buy" in text:
        return "buy"
    elif "sell" in text:
        return "sell"
    return "nothing"

def get_portfolio_value() -> float:
    """Get current portfolio value from Alpaca."""
    try:
        account = alpaca.get_account()
        return float(account.portfolio_value)
    except Exception as e:
        logger.error(f"Error getting portfolio value: {e}")
        return 0.0

def buy_stock(symbol: str) -> None:
    """Market buy symbol using 2% of portfolio value."""
    try:
        portfolio_value = get_portfolio_value()
        investment_amount = portfolio_value * 0.02
        current_price = float(alpaca.get_latest_trade(symbol).price)
        qty = int(investment_amount / current_price)
        
        if qty > 0:
            logger.info(f"[SIMULATION] Would buy {qty} shares of {symbol}")
            logger.info(f"[SIMULATION] Investment amount: ${investment_amount:.2f}")
            logger.info(f"[SIMULATION] Current price: ${current_price:.2f}")
            alpaca.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
    except Exception as e:
        logger.error(f"Error in buy simulation: {e}")

def sell_stock(symbol: str) -> None:
    """Sell all shares of the given symbol."""
    try:
        position = alpaca.get_position(symbol)
        if float(position.qty) > 0:
            logger.info(f"[SIMULATION] Would sell {position.qty} shares of {symbol}")
            logger.info(f"[SIMULATION] Current position value: ${float(position.market_value):.2f}")
            alpaca.submit_order(
                symbol=symbol,
                qty=position.qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
    except Exception as e:
        logger.error(f"[SIMULATION] No position in {symbol} to sell")

def run_trading_cycle(alpaca_api, logger):
    """Main bot function to execute one trading cycle."""
    try:
        logger.info("\n--- Starting Trading Cycle ---")
        rsi = fetch_rsi("TSLA")
        logger.info(f"Current RSI: {rsi}")
        
        reply = ask_chatgpt(rsi)
        logger.info(f"ChatGPT Response: {reply}")
        
        action = interpret_response(reply)
        logger.info(f"Interpreted Action: {action}")

        if action == "buy":
            buy_stock("TSLA")
        elif action == "sell":
            sell_stock("TSLA")
        else:
            logger.info("No action taken")
            
    except Exception as e:
        logger.error(f"Error in trading cycle: {e}")

def main():
    """Main function to run the trading bot."""
    try:
        # Initialize API clients
        alpaca_api = tradeapi.REST(
            os.getenv('ALPACA_API_KEY'),
            os.getenv('ALPACA_SECRET_KEY'),
            os.getenv('ALPACA_BASE_URL'),
            api_version='v2'
        )
        
        # Initialize logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # Run for 20 minutes with 2-minute intervals
        total_minutes = 20
        interval_minutes = 2
        
        logger.info("Starting trading bot...")
        
        for i in range(total_minutes // interval_minutes):
            current_time = datetime.datetime.now()
            logger.info(f"Running trading cycle at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            run_trading_cycle(alpaca_api, logger)
            
            # Wait for the next interval unless it's the last cycle
            if i < (total_minutes // interval_minutes - 1):
                time.sleep(interval_minutes * 60)
        
        logger.info("Trading bot completed all cycles.")
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()