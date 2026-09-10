import sys
import json
from client import LimitOrderBook

lob = LimitOrderBook()

def handle_call(name, arguments):
    if name == "add_order":
        oid = arguments["order_id"]
        side = arguments["side"]
        px = arguments["price"]
        sz = arguments["size"]
        trades = lob.add_limit_order(oid, side, px, sz)
        return {"trades": trades}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
