# 📈 Williams %R Strategy Backtesting with Trade Visualization

This project performs a complete backtest of a trading strategy based on the **Williams %R** momentum oscillator using historical OHLC data from the Indian stock market (e.g., HCLTECH). It simulates realistic trading with slippage, fees, capital growth, and visualizes trades, equity curve, and indicator behavior.

---

## 🧩 Features

- ✅ Reads historical stock data from CSV
- ✅ Calculates **14-day Williams %R** indicator
- ✅ Generates buy/sell signals:
  - Buy when `%R < -80` (oversold)
  - Sell when `%R > -20` (overbought)
- ✅ Simulates trades with:
  - Slippage and transaction fees
  - Full capital allocation per trade
- ✅ Calculates:
  - Win rate, average return, cumulative return
  - Sharpe Ratio, max drawdown
- ✅ Produces multiple plots:
  - Price chart with Buy/Sell markers
  - Equity curve over trades
  - Annotated trade log on price chart

---

## 📂 Project Structure

```
.
├── HCLTECH.csv               # Your input OHLC CSV file
├── backtest_williamsR.py     # Main Python script
├── README.md                 # This documentation
```

---

## 🛠️ Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

1. Replace the `file_path` in the script with the path to your CSV file.
2. Run the script using:

```bash
python backtest_williamsR.py
```

3. Review output:
   - Terminal shows trade summary and metrics
   - Matplotlib shows:
     - Strategy performance on price chart
     - Capital growth (equity curve)
     - Annotated trade entries/exits

---

## 📊 Sample Output Metrics

```
=== Backtest Summary ===
Initial Capital: ₹100000
Final Equity: ₹160532.45
Total Trades: 7
Win Rate: 71.43%
Average Return per Trade: 8.93%
Cumulative Return: 60.53%
Sharpe Ratio: 1.81
Max Drawdown: ₹9210.33
```

---

## 📈 Strategy Logic

- Williams %R is a momentum oscillator ranging from -100 to 0.
- This strategy interprets:
  - `%R < -80`: Oversold → Buy
  - `%R > -20`: Overbought → Sell
- The system enters a trade on a Buy signal and exits on the next Sell.

---

## 🧾 Trade Simulation Details

| Parameter            | Value           |
|----------------------|-----------------|
| Slippage             | ±0.1% per trade |
| Transaction Fees     | 0.15% round trip |
| Position Sizing      | 100% capital per trade |
| Performance Metrics  | PnL, Sharpe, Win Rate, Drawdown |

---

## 📌 Future Improvements

- Add support for short selling
- Add support for other indicators (RSI, MACD)
- Export logs and metrics to Excel
- Build a Streamlit dashboard

---

## 🧑‍💻 Author

Developed by [Your Name]  
Feel free to fork, star, or contribute.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
