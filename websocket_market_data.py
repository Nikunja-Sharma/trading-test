import json
import websocket
from datetime import datetime
from colorama import init, Fore

# Initialize colorama for colored output
init()

class BinanceWebSocket:
    def __init__(self, symbols):
        self.symbols = [symbol.lower() for symbol in symbols]
        self.ws = None
        self.base_endpoint = "wss://stream.binance.com:9443/ws"
        
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            if data.get('e') == 'trade':
                self.display_trade(data)
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Error decoding message: {e}{Fore.RESET}")

    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"{Fore.RED}Error: {error}{Fore.RESET}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close"""
        print(f"{Fore.YELLOW}WebSocket Connection Closed{Fore.RESET}")

    def on_open(self, ws):
        """Handle WebSocket connection open"""
        print(f"{Fore.GREEN}WebSocket Connection Established{Fore.RESET}")
        
        # Subscribe to trade streams for all symbols
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol}@trade" for symbol in self.symbols],
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))

    def display_trade(self, trade_data):
        """Display trade information in a formatted way"""
        timestamp = datetime.fromtimestamp(trade_data['T'] / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        symbol = trade_data['s']
        price = float(trade_data['p'])
        quantity = float(trade_data['q'])
        is_buyer = trade_data['m']  # True if buyer is market maker

        # Color coding
        price_color = Fore.GREEN if not is_buyer else Fore.RED
        symbol_color = Fore.YELLOW
        
        print(f"{Fore.CYAN}[{timestamp}]{Fore.RESET} "
              f"{symbol_color}{symbol}{Fore.RESET} | "
              f"Price: {price_color}{price:.8f}{Fore.RESET} | "
              f"Quantity: {quantity:.8f} | "
              f"Side: {Fore.GREEN if not is_buyer else Fore.RED}{'BUY' if not is_buyer else 'SELL'}{Fore.RESET}")

    def start(self):
        """Start WebSocket connection"""
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.base_endpoint,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        print(f"{Fore.CYAN}Starting WebSocket connection...{Fore.RESET}")
        print(f"Monitoring symbols: {', '.join(self.symbols)}")
        self.ws.run_forever()

if __name__ == "__main__":
    # Example usage with popular crypto pairs
    symbols = ["btcusdt", "ethusdt", "bnbusdt"]  # symbols must be lowercase
    ws_client = BinanceWebSocket(symbols)
    ws_client.start() 