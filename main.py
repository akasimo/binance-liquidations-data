from connectors.exchanges.binance_connector import BinanceConnector

# from dotenv import load_dotenv

# load_dotenv()

# The rest of your code


def main():
    binance_connector = BinanceConnector()
    binance_connector.subscribe_liquidations_stream()


if __name__ == "__main__":
    main()
