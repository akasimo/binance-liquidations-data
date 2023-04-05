# connectors/exchange_connector.py
from abc import ABC, abstractmethod

class ExchangeConnector(ABC):
    @abstractmethod
    def subscribe_liquidations_stream(self):
        pass
