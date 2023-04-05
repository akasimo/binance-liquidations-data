import json
import websocket
import time
from connectors.exchange_connector import ExchangeConnector
from database.database import store_liquidation_data
# from database.database import Session
# from database.models import Liquidation


class BinanceConnector(ExchangeConnector):
    def __init__(self):
        self.ws_url = 'wss://fstream.binance.com/ws'

    def on_open(self, ws):
        print("WebSocket connection opened")

    def on_close(self, ws):
        print("WebSocket connection closed")

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_message(self, ws, message):
        msg = json.loads(message)
        if 'e' in msg and msg['e'] == 'forceOrder':
            print(f"Liquidation: {msg}")
            store_liquidation_data(msg)
        elif 'code' in msg and 'msg' in msg:
            print(f"Error code {msg['code']}: {msg['msg']}")
        else:
            print(f"Other message: {msg}")

    def _connect(self):
        stream_url = f"{self.ws_url}/!forceOrder@arr"
        ws = websocket.WebSocketApp(stream_url,
                                    on_open=self.on_open,
                                    on_close=self.on_close,
                                    on_error=self.on_error,
                                    on_message=self.on_message,
                                    on_ping=self.on_ping)
        ws.run_forever(ping_interval=60, ping_timeout=15)

    def on_ping(self, ws, message):
        # Automatically sends a pong frame when a ping is received
        # ws.pong()
        ws.send("pong")

    def subscribe_liquidations_stream(self):
        while True:
            try:
                self._connect()
                print("Reconnecting after 24 hours...")
                time.sleep(24 * 60 * 60)  # Reconnect every 24 hours
            except Exception as e:
                print(f"Error in subscribe_liquidations_stream: {e}")
                time.sleep(60)  # Wait 1 minute before reconnecting