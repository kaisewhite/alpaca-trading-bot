**🧠 RSI-Based TSLA Trading Bot in Python**

> Build a trading bot in **Python** using:
> - `taapi` (for RSI)
> - `langchain` + `openai` (for trading decisions)
> - `alpaca_trade_api` (to place buy/sell orders)

---

### 🔁 Bot Logic (every 2 minutes)

1. Fetch 1-min RSI for **TSLA** using TAAPI  
2. Send this prompt to **ChatGPT** via Langchain:
   ```
   The current relative strength index (RSI) for TSLA (Tesla Stock) is {rsi}. 
   Based on this, should I buy, sell, or do nothing? 
   You are a world expert at stock trading.
   ```
3. Analyze the response:
   - If the reply includes **"buy"** → call `buy_stock()`
   - If the reply includes **"sell"** → call `sell_stock()`
   - Else → take no action

---

### 🧩 Functions to Implement

```python
# 1. Fetch RSI for TSLA
def fetch_rsi(symbol: str) -> float:
    pass

# 2. Send prompt to OpenAI via Langchain and return response
def ask_chatgpt(rsi: float) -> str:
    pass

# 3. Normalize response to: "buy" | "sell" | "nothing"
def interpret_response(text: str) -> str:
    pass

# 4. Get current portfolio value from Alpaca
def get_portfolio_value() -> float:
    pass

# 5. Market buy TSLA using 2% of portfolio value
def buy_stock(symbol: str) -> None:
    pass

# 6. Sell all TSLA shares
def sell_stock(symbol: str) -> None:
    pass

# 7. Main bot function
def run_trading_cycle():
    rsi = fetch_rsi("TSLA")
    reply = ask_chatgpt(rsi)
    action = interpret_response(reply)

    if action == "buy":
        buy_stock("TSLA")
    elif action == "sell":
        sell_stock("TSLA")
```

---

### ⏱ Run Every 2 Minutes

Use:
```python
import time

while True:
    run_trading_cycle()
    time.sleep(120)  # wait 2 minutes
```

---

Let me know if you want the actual Python implementation scaffolded for each function.