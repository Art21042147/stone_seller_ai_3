import yfinance as yf


def get_usd_to_rub_rate():
    ticker = yf.Ticker("USDRUB=X")
    today_data = ticker.history(period="1d")

    return today_data['Close'].iloc[0]
