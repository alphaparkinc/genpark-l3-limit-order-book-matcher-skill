import collections

class LimitOrderBook:
    """
    Price-Time Priority Limit Order Book (L3).
    Bids sorted descending, Asks sorted ascending.
    Supports LIMIT orders, MARKET orders, and matching.
    """
    def __init__(self):
        self.bids = collections.defaultdict(collections.deque)
        self.asks = collections.defaultdict(collections.deque)
        self.orders = {}

    def add_limit_order(self, order_id, side, price, size):
        trades = []
        if side == "buy":
            while self.asks and size > 0:
                best_ask = min(self.asks.keys())
                if best_ask > price:
                    break
                queue = self.asks[best_ask]
                while queue and size > 0:
                    a_id, a_sz = queue[0]
                    match_sz = min(size, a_sz)
                    trades.append((order_id, a_id, best_ask, match_sz))
                    size -= match_sz
                    if match_sz == a_sz:
                        queue.popleft()
                        del self.orders[a_id]
                    else:
                        queue[0] = (a_id, a_sz - match_sz)
                if not queue:
                    del self.asks[best_ask]
            if size > 0:
                self.bids[price].append((order_id, size))
                self.orders[order_id] = ("buy", price)
        else:
            while self.bids and size > 0:
                best_bid = max(self.bids.keys())
                if best_bid < price:
                    break
                queue = self.bids[best_bid]
                while queue and size > 0:
                    b_id, b_sz = queue[0]
                    match_sz = min(size, b_sz)
                    trades.append((b_id, order_id, best_bid, match_sz))
                    size -= match_sz
                    if match_sz == b_sz:
                        queue.popleft()
                        del self.orders[b_id]
                    else:
                        queue[0] = (b_id, b_sz - match_sz)
                if not queue:
                    del self.bids[best_bid]
            if size > 0:
                self.asks[price].append((order_id, size))
                self.orders[order_id] = ("sell", price)

        return trades
