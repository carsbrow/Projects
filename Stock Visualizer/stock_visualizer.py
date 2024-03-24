import pandas as pd
import matplotlib.pyplot as plt


def stock_visualizer(stock_name, start_date, end_date):
    """
    Visualizes the stock data for the given stock name and date range.

    Paramters:
        stock_name: str
            The name of the stock to visualize.
        start_date: str
            The start date to visualize the stock. (Format: MM-DD-YYYY)
        end_date: str
            The end date to visualize the stock. (Format: MM-DD-YYYY)
        Price: bool
            If True, visualize the stock price.
        Volume: bool
            If True, visualize the stock volume.

    Returns:
        None
    """

    stock_df = pd.read_csv("Stock Market Dataset.csv")
    # Getting the data for the given stock_name
    stock_df = stock_df.filter(regex=stock_name + '|Date')
    # Reformating the date to match the date format in the dataset
    stock_df['Date'] = pd.to_datetime(stock_df['Date'], format='%d-%m-%Y')

    # Filtering the data for the given date range
    stock_df = stock_df[(stock_df['Date'] >= start_date) & (stock_df['Date'] <= end_date)]

    # Converting the Price and Volume columns to numeric
    stock_df[stock_name + '_Vol.'] = stock_df[stock_name + '_Vol.'].astype(str)
    stock_df[stock_name + '_Vol.'] = stock_df[stock_name + '_Vol.'].str.replace(',', '').astype(float)

    stock_df[stock_name + '_Price'] = stock_df[stock_name + '_Price'].astype(str)
    stock_df[stock_name + '_Price'] = stock_df[stock_name + '_Price'].str.replace(',', '').astype(float)
    
    # Replace zeros with NaN
    stock_df.replace(0, float('nan'), inplace=True)
    
    # Grouping by Year-Month with mean values
    stock_df_grouped = stock_df[[stock_name + '_Price', stock_name + '_Vol.']].groupby([stock_df['Date'].dt.to_period('M')]).mean()
    stock_df_grouped.interpolate(method='linear', inplace=True) # Interpolating the missing values

    # Gouping by date
    stock_df = stock_df[[stock_name + '_Price', stock_name + '_Vol.']].groupby(stock_df['Date']).mean()
    stock_df.interpolate(method='linear', inplace=True) # Interpolating the missing values

    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Line graph for price
    stock_df[stock_name + '_Price'].plot(kind='line', ax=ax1) 
    stock_df_grouped[stock_name + '_Price'].plot(kind='line', ax=ax1)
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Price')
    ax1.set_title(f'{stock_name} Stock Price by Month')
    ax1.legend(['Daily Price', 'Monthly Average Price'])

    # Bar graph for monthy volume
    volume_comparison = stock_df_grouped[stock_name + '_Vol.'].diff()
    # List comprehension to color the bars based on the volume change
    stock_df_grouped[stock_name + '_Vol.'].plot(kind='bar', ax=ax2, width=1, edgecolor='black', color=[
        'g' if vol > 0 else 'r' for vol in volume_comparison]) # Red if the volume decreased, Green if the volume increased
    
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Volume')
    ax2.set_title(f'{stock_name} Stock Volume by Month')
    ax2.legend('Monthy Average Volume')

    plt.tight_layout()
    plt.show()
    

def main():
    """Test cases for the stock_visualizer function."""
    stock_visualizer("Natural_Gas", "04-02-2019", "02-02-2024")
    stock_visualizer("Gold", "04-02-2019", "02-02-2024")
    stock_visualizer("Ethereum", "04-02-2019", "02-02-2024")
    stock_visualizer("Bitcoin", "04-02-2019", "02-02-2024")


if __name__ == "__main__":
    main()

