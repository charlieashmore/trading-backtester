from src.data.market_data import get_market_data

def main():
    ticker = 'AAPL'
    start = '2023-01-01'
    end = '2023-02-01'

    data = get_market_data(ticker, start, end)
    print(data)

if __name__ == "__main__":
    main()