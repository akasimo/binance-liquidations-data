import json
import time
import websocket
from datetime import datetime

from connectors.exchange_connector import ExchangeConnector
from database.database import Session
from database.models import Liquidation


class BinanceConnector(ExchangeConnector):
    def __init__(self):
        self.ws_url = 'wss://fstream.binance.com/ws'

    def on_open(self, _):
        print("WebSocket connection opened")

    def on_close(self, _):
        print("WebSocket connection closed")

    def on_error(self, _, error):
        print(f"WebSocket error: {error}")

    def on_message(self, _, message):
        msg = json.loads(message)
        if 'e' in msg and msg['e'] == 'forceOrder':
            print(f"Liquidation: {msg}")
            self.store_liquidation_data(msg)
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

    def on_ping(self, ws, message=None):
        """Ping handler for websocket connection
        """        
        # Automatically sends a pong frame when a ping is received
        # ws.pong()
        ws.send("pong")

    def subscribe_liquidations_stream(self):
        while True:
            try:
                self._connect()
                print("Reconnecting after 24 hours...")
                time.sleep(24 * 60 * 60)  # Reconnect every 24 hours
            except Exception as error:
                print(f"Error in subscribe_liquidations_stream: {error}")
                time.sleep(60)  # Wait 1 minute before reconnecting

    def store_liquidation_data(self, liquidation_data):
        # Create a new session
        session = Session()

        received_timestamp = datetime.utcnow()
        event_time = datetime.fromtimestamp(liquidation_data["E"]/1000)
        # Create a new Liquidation object
        new_liquidation = Liquidation(
            event_type=liquidation_data["e"],
            event_time=event_time,
            symbol=liquidation_data["o"]["s"],
            side=liquidation_data["o"]["S"],
            order_type=liquidation_data["o"]["o"],
            time_in_force=liquidation_data["o"]["f"],
            quantity=liquidation_data["o"]["q"],
            price=liquidation_data["o"]["p"],
            average_price=liquidation_data["o"]["ap"],
            order_status=liquidation_data["o"]["X"],
            last_filled_quantity=liquidation_data["o"]["l"],
            filled_accumulated_quantity=liquidation_data["o"]["z"],
            order_trade_time=datetime.fromtimestamp(liquidation_data["o"]["T"]/1000),
            received_timestamp=received_timestamp,

        )
        # Add the new Liquidation object to the session
        session.add(new_liquidation)
        # Commit the transaction
        session.commit()
        # Close the session
        session.close()
        