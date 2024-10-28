import requests
import pandas as pd
import datetime as dt

# Replace with actual API endpoint for crypto historical data
API_URL = "https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"

def fetch_crypto_data(crypto_id, vs_currency="usd", days="max"):
    """
    Fetch daily historical data for a specific cryptocurrency pair.
    Args:
        crypto_id (str): ID of the cryptocurrency (e.g., 'bitcoin').
        vs_currency (str): Currency to compare (default: 'usd').
        days (str): Duration (default: 'max' for all available data).
    Returns:
        DataFrame: Historical data with Date, Open, High, Low, Close.
    """
    params = {
        "vs_currency": vs_currency,
        "days": days,
    }
    response = requests.get(API_URL.format(crypto_id=crypto_id), params=params)
    data = response.json()
    
    # Process and format data
    df = pd.DataFrame(data["prices"], columns=["Date", "Price"])
    df["Date"] = pd.to_datetime(df["Date"], unit='ms')
    df = df.set_index("Date")
    df["Open"] = df["Price"]
    df["High"] = df["Price"]
    df["Low"] = df["Price"]
    df["Close"] = df["Price"]
    return df.drop("Price", axis=1)

def calculate_metrics(data, variable1=7, variable2=5):
    """
    Calculate historical and future metrics.
    Args:
        data (DataFrame): Historical data for calculations.
        variable1 (int): Look-back period (e.g., 7 days).
        variable2 (int): Look-forward period (e.g., 5 days).
    Returns:
        DataFrame: Data with calculated metrics.
    """
    df = data.copy()
    df[f"High_Last_{variable1}_Days"] = df["High"].rolling(window=variable1).max()
    df[f"Days_Since_High_Last_{variable1}_Days"] = (
        df["High"].expanding().apply(lambda x: (x.index[-1] - x.idxmax()).days)
    )
    df[f"%_Diff_From_High_Last_{variable1}_Days"] = (
        (df["Close"] - df[f"High_Last_{variable1}_Days"]) / df[f"High_Last_{variable1}_Days"] * 100
    )
    df[f"Low_Last_{variable1}_Days"] = df["Low"].rolling(window=variable1).min()
    df[f"Days_Since_Low_Last_{variable1}_Days"] = (
        df["Low"].expanding().apply(lambda x: (x.index[-1] - x.idxmin()).days)
    )
    df[f"%_Diff_From_Low_Last_{variable1}_Days"] = (
        (df["Close"] - df[f"Low_Last_{variable1}_Days"]) / df[f"Low_Last_{variable1}_Days"] * 100
    )
    df[f"High_Next_{variable2}_Days"] = df["High"].shift(-variable2).rolling(window=variable2).max()
    df[f"%_Diff_From_High_Next_{variable2}_Days"] = (
        (df["Close"] - df[f"High_Next_{variable2}_Days"]) / df[f"High_Next_{variable2}_Days"] * 100
    )
    df[f"Low_Next_{variable2}_Days"] = df["Low"].shift(-variable2).rolling(window=variable2).min()
    df[f"%_Diff_From_Low_Next_{variable2}_Days"] = (
        (df["Close"] - df[f"Low_Next_{variable2}_Days"]) / df[f"Low_Next_{variable2}_Days"] * 100
    )
    return df

def save_to_excel(df, filename="crypto_data.xlsx"):
    """Save DataFrame to an Excel file."""
    df.to_excel(filename, engine="xlsxwriter")

# Example usage
if __name__ == "__main__":
    crypto_data = fetch_crypto_data("bitcoin")
    metrics_data = calculate_metrics(crypto_data)
    save_to_excel(metrics_data)
