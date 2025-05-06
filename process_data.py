import pandas as pd


def load_and_clean(file_path):
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    # Calculate a 7-day moving average price
    df['MA_7'] = df['Price'].rolling(window=7).mean()
    return df


if __name__ == "__main__":
    data_file = 'oil_gas_prices.csv'  # Place your CSV here
    cleaned_df = load_and_clean(data_file)
    cleaned_df.to_csv('cleaned_oil_gas_prices.csv', index=False)
    print("Data cleaned and saved to cleaned_oil_gas_prices.csv")
