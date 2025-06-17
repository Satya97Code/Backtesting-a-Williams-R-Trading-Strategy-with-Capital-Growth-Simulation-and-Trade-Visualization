import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === STEP 1: Load CSV ===
file_path = r"E:\Code\HCLTECH.csv"  # replace with your filename
data = pd.read_csv(file_path)

# === STEP 2: Preprocess ===
data.columns = data.columns.str.strip()
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# FIX: Ensure chronological order
data.sort_index(inplace=True)

# Convert prices
for col in ['HIGH', 'LOW', 'close']:
    data[col] = data[col].astype(str).str.replace(',', '').astype(float)

# Rename columns
data = data[['HIGH', 'LOW', 'close']].rename(columns={
    'HIGH': 'High',
    'LOW': 'Low',
    'close': 'Close'
})

# === STEP 3: Calculate 14-day Williams %R ===
data['High14'] = data['High'].rolling(window=14).max()
data['Low14'] = data['Low'].rolling(window=14).min()
data['Williams_%R'] = (data['High14'] - data['Close']) / (data['High14'] - data['Low14']) * -100
data.dropna(subset=['Williams_%R'], inplace=True)

# === STEP 4: Generate Buy/Sell Signals ===
data['Signal'] = 0
data.loc[data['Williams_%R'] < -80, 'Signal'] = 1    # Buy
data.loc[data['Williams_%R'] > -20, 'Signal'] = -1   # Sell

# === STEP 5: Backtest Logic ===
position = 0
entry_price = 0
returns = []

for i in range(1, len(data)):
    if data['Signal'].iloc[i] == 1 and position == 0:
        entry_price = data['Close'].iloc[i]
        position = 1
    elif data['Signal'].iloc[i] == -1 and position == 1:
        exit_price = data['Close'].iloc[i]
        returns.append((exit_price - entry_price) / entry_price)
        position = 0

# === Parameters ===
initial_capital = 100000  # ₹1 lakh
slippage_pct = 0.001      # 0.1% slippage per trade
fee_pct = 0.0015          # 0.15% round-trip cost

# === Data Assumptions (your data should already be prepared as 'data') ===
# Columns: ['Close', 'Signal', 'High14', 'Low14', 'Williams_%R']
capital = initial_capital
position = 0
entry_price = 0
entry_date = None

# Tracking
trade_log = []
equity_curve = [capital]
daily_returns = []

# Backtest Loop
for i in range(1, len(data)):
    current_date = data.index[i]
    close_price = data['Close'].iloc[i]
    signal = data['Signal'].iloc[i]

    # BUY
    if signal == 1 and position == 0:
        entry_price = close_price * (1 + slippage_pct)  # slippage on entry
        entry_date = current_date
        position = capital / entry_price  # full capital
        capital = 0  # fully invested

    # SELL
    elif signal == -1 and position > 0:
        exit_price = close_price * (1 - slippage_pct)  # slippage on exit
        exit_value = position * exit_price
        trade_return = (exit_value - initial_capital) / initial_capital - fee_pct

        # Log trade
        trade_log.append({
            'Entry Date': entry_date,
            'Exit Date': current_date,
            'Entry Price': entry_price,
            'Exit Price': exit_price,
            'Return (%)': round(trade_return * 100, 2),
            'Net PnL': round(exit_value - initial_capital, 2)
        })

        capital = exit_value
        equity_curve.append(capital)
        daily_returns.append(trade_return)
        position = 0

# Convert logs
trade_df = pd.DataFrame(trade_log)
equity_series = pd.Series(equity_curve, name='Equity')

# === Metrics ===
total_trades = len(trade_df)
profitable_trades = len(trade_df[trade_df['Return (%)'] > 0])
win_rate = (profitable_trades / total_trades) * 100 if total_trades else 0
avg_return = trade_df['Return (%)'].mean() if total_trades else 0
cumulative_return = (equity_series.iloc[-1] - initial_capital) / initial_capital * 100

# Risk Metrics
if len(daily_returns) > 1:
    sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
else:
    sharpe = 0

drawdown = equity_series.cummax() - equity_series
max_drawdown = drawdown.max()

# === Print Summary ===
print(f"\n=== Backtest Summary ===")
print(f"Initial Capital: ₹{initial_capital}")
print(f"Final Equity: ₹{equity_series.iloc[-1]:.2f}")
print(f"Total Trades: {total_trades}")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Average Return per Trade: {avg_return:.2f}%")
print(f"Cumulative Return: {cumulative_return:.2f}%")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Max Drawdown: ₹{max_drawdown:.2f}")

# === Optional: Display Trade Log ===
print("\nTrade Log:")
print(trade_df)

# === STEP 6: Plot ===
# === Plot Backtest Results ===
plt.figure(figsize=(14, 6))
plt.plot(data.index, data['Close'], label='Close Price', alpha=0.7)
plt.scatter(data[data['Signal'] == 1].index, data[data['Signal'] == 1]['Close'], marker='^', color='green', label='Buy Signal')
plt.scatter(data[data['Signal'] == -1].index, data[data['Signal'] == -1]['Close'], marker='v', color='red', label='Sell Signal')
plt.title('Williams %R Backtest')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show(block=True)

# === Plot Equity Curve ===
plt.figure(figsize=(12, 5))
plt.plot(equity_series.index, equity_series.values, label="Equity Curve", linewidth=2)
plt.title("Backtest Equity Curve")
plt.xlabel("Trade #")
plt.ylabel("Equity (₹)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show(block=True)
# === Plot Trade Entry & Exit Prices
plt.figure(figsize=(14, 6))
plt.plot(data.index, data['Close'], label='Close Price', color='steelblue', linewidth=2)

# Plot Buy and Sell points with clearer annotations
for i, row in trade_df.iterrows():
    # Buy marker and label
    plt.scatter(row['Entry Date'], row['Entry Price'], marker='^', color='green', s=120, zorder=3)
    plt.annotate('Buy',
                 (row['Entry Date'], row['Entry Price']),
                 textcoords="offset points",
                 xytext=(0, 12),
                 ha='center',
                 color='green',
                 fontsize=9,
                 fontweight='bold')

    # Sell marker and label
    plt.scatter(row['Exit Date'], row['Exit Price'], marker='v', color='red', s=120, zorder=3)
    plt.annotate('Sell',
                 (row['Exit Date'], row['Exit Price']),
                 textcoords="offset points",
                 xytext=(0, -15),
                 ha='center',
                 color='red',
                 fontsize=9,
                 fontweight='bold')

# Final plot setup
plt.title("Williams %R Strategy - Trade Entry & Exit Points", fontsize=14, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (₹)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.legend(['Close Price'], loc='upper left')
plt.tight_layout()
plt.show(block=True)