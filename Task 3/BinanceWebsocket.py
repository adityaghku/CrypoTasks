import asyncio
import json
import websockets
import threading


class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

    def update_bid(self, price, quantity):
        if quantity == 0:
            self.bids = [bid for bid in self.bids if bid[0] != price]
        else:
            for i, bid in enumerate(self.bids):
                if bid[0] == price:
                    self.bids[i] = (price, quantity)
                    break
            else:
                self.bids.append((price, quantity))
            self.bids.sort(reverse=True)

    def update_ask(self, price, quantity):
        if quantity == 0:
            self.asks = [ask for ask in self.asks if ask[0] != price]
        else:
            for i, ask in enumerate(self.asks):
                if ask[0] == price:
                    self.asks[i] = (price, quantity)
                    break
            else:
                self.asks.append((price, quantity))
            self.asks.sort()

    @property
    def bid_prices(self):
        return [bid[0] for bid in self.bids]

    @property
    def bid_quantities(self):
        return [bid[1] for bid in self.bids]

    @property
    def ask_prices(self):
        return [ask[0] for ask in self.asks]

    @property
    def ask_quantities(self):
        return [ask[1] for ask in self.asks]

    def to_dict(self):
        return {
            "bids": self.bids,
            "asks": self.asks,
        }


class BinanceOrderBookStream:
    def __init__(self, ticker):
        self.ticker = ticker
        self.orderbook = OrderBook()
        self.websocket = None

    async def stream_orderbook(self):
        url = f"wss://stream.binance.com:9443/ws/{self.ticker.lower()}@depth5"
        async with websockets.connect(url) as websocket:
            self.websocket = websocket
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if "bids" in data:
                        for bid in data["bids"]:
                            self.orderbook.update_bid(float(bid[0]), float(bid[1]))
                    if "asks" in data:
                        for ask in data["asks"]:
                            self.orderbook.update_ask(float(ask[0]), float(ask[1]))

                    # Save orderbook to file
                    await self.save_orderbook_to_file()

                except websockets.ConnectionClosed:
                    print(f"WebSocket connection closed for {self.ticker}")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
                    continue

    async def save_orderbook_to_file(self):
        loop = asyncio.get_running_loop()
        filename = f"{self.ticker.lower()}_orderbook.json"
        orderbook_dict = self.orderbook.to_dict()
        with open(filename, "w") as f:
            await loop.run_in_executor(None, json.dump, orderbook_dict, f)

    def start_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.stream_orderbook())

    def start(self):
        thread = threading.Thread(target=self.start_event_loop)
        thread.start()

    async def close(self):
        if self.websocket is not None:
            await self.websocket.close()
            print(f"WebSocket connection closed for {self.ticker}")
        else:
            print(f"No WebSocket connection found for {self.ticker}")


async def main():
    ticker = "BTCUSDT"
    stream = BinanceOrderBookStream(ticker)
    stream.start()

    # Wait for the WebSocket connection to start
    await asyncio.sleep(2)

    # Print the current bid and ask prices
    print(f"Bids: {stream.orderbook.bid_prices}")
    print(f"Asks: {stream.orderbook.ask_prices}")

    await stream.close()


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()

    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        # If there's already an event loop running, create a task for the main function
        tsk = loop.create_task(main())

    else:
        # If there's no event loop running, create a new one and run the main function
        result = asyncio.run(main())
