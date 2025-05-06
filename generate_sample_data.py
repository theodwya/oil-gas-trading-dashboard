import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_market_data(start_date, days, commodity):
    dates = [start_date + timedelta(days=i) for i in range(days)]
    # Generate synthetic price data with some randomness
    np.random.seed(42)  # For reproducibility
    base_price = 70 if commodity == 'oil' else 3  # Sample base prices
    prices = base_price + np.random.normal(0, 2, days).cumsum()
    volumes = np.random.randint(1000, 5000, days)

    data = {
        'Date': dates,
        'Commodity': [commodity] * days,
        'Price': np.round(prices, 2),
        'Volume': volumes
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    start_date = datetime(2023, 1, 1)
    days = 365  # One year of data

    oil_data = generate_market_data(start_date, days, 'oil')
    gas_data = generate_market_data(start_date, days, 'gas')

    # Combine datasets
    combined = pd.concat([oil_data, gas_data], ignore_index=True)

    # Save to CSV
    combined.to_csv('sample_oil_gas_market_data.csv', index=False)
    print("Sample oil and gas market data generated and saved to 'sample_oil_gas_market_data.csv'")
