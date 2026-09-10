from client import LimitOrderBook

def main():
    print("=== Testing L3 Limit Order Book Matcher ===")
    lob = LimitOrderBook()

    lob.add_limit_order("ask_1", "sell", price=100.5, size=20)
    lob.add_limit_order("bid_1", "buy", price=99.5, size=15)

    # Cross the spread
    trades = lob.add_limit_order("market_buy", "buy", price=101.0, size=5)
    print("Executed trades on cross:", trades)
    assert len(trades) == 1
    assert trades[0] == ("market_buy", "ask_1", 100.5, 5)
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
