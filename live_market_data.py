import time
from tradingview_ta import TA_Handler, Interval
from colorama import init, Fore
import pandas as pd
from datetime import datetime

# Initialize colorama for colored output
init()

class MarketDataStream:
    def __init__(self, symbols, exchange="BINANCE", screener="crypto", interval=Interval.INTERVAL_1_MINUTE):
        self.symbols = symbols
        self.exchange = exchange
        self.screener = screener
        self.interval = interval
        self.handlers = {}
        
        # Initialize TA handlers for each symbol
        for symbol in symbols:
            self.handlers[symbol] = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener=screener,
                interval=interval
            )

    def get_analysis(self):
        """Get technical analysis data for all symbols"""
        results = {}
        current_timestamp = datetime.now()
        
        for symbol, handler in self.handlers.items():
            try:
                analysis = handler.get_analysis()
                results[symbol] = {
                    'timestamp': current_timestamp.isoformat(),
                    'close': analysis.indicators['close'],
                    'volume': analysis.indicators['volume'],
                    'RSI': analysis.indicators['RSI'],
                    'MACD.macd': analysis.indicators['MACD.macd'],
                    'EMA20': analysis.indicators['EMA20'],
                    'recommendation': analysis.summary['RECOMMENDATION']
                }
            except Exception as e:
                print(f"{Fore.RED}Error getting data for {symbol}: {str(e)}{Fore.RESET}")
        return results

    def display_data(self, data):
        """Display market data in a formatted way"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{Fore.CYAN}=== Market Data Update at {timestamp} ==={Fore.RESET}")
        
        for symbol, metrics in data.items():
            print(f"\n{Fore.YELLOW}{symbol}:{Fore.RESET}")
            print(f"Timestamp: {metrics.get('timestamp', 'N/A')}")
            price_color = Fore.GREEN if metrics.get('close', 0) > 0 else Fore.RED
            print(f"Price: {price_color}{metrics.get('close', 'N/A')}{Fore.RESET}")
            print(f"Volume: {metrics.get('volume', 'N/A')}")
            print(f"RSI: {metrics.get('RSI', 'N/A')}")
            print(f"MACD: {metrics.get('MACD.macd', 'N/A')}")
            print(f"EMA20: {metrics.get('EMA20', 'N/A')}")
            
            recommendation = metrics.get('recommendation', 'NEUTRAL')
            rec_color = Fore.GREEN if recommendation == 'BUY' else Fore.RED if recommendation == 'SELL' else Fore.YELLOW
            print(f"Recommendation: {rec_color}{recommendation}{Fore.RESET}")

    def stream(self, interval_seconds=60):
        """Stream market data continuously"""
        print(f"{Fore.CYAN}Starting market data stream...{Fore.RESET}")
        print(f"Monitoring symbols: {', '.join(self.symbols)}")
        
        while True:
            try:
                data = self.get_analysis()
                self.display_data(data)
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Stopping market data stream...{Fore.RESET}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Fore.RESET}")
                time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    # Example usage with popular crypto pairs
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    stream = MarketDataStream(symbols)
    
    # Get single snapshot of data
    data = stream.get_analysis()
    stream.display_data(data) 