from connectors.exchanges.binance_connector import BinanceConnector

def main():
    binance_connector = BinanceConnector()
    binance_connector.subscribe_liquidations_stream()

if __name__ == "__main__":
    main()