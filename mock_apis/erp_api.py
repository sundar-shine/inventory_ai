from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS
from datetime import datetime
import random, json, queue, threading, os

app = Flask(__name__)
CORS(app)

ORDERS = []
SUPPLIER_ORDERS = []
ORDER_COUNTER = [1000]
freshmart_queues = []
quicksupply_queues = []
lock = threading.Lock()

PRICES = {
    "Lays Classic": 10, "Basmati Rice 5kg": 250, "Amul Milk 1L": 55,
    "Sunflower Oil 1L": 120, "Maggi Noodles": 14, "Coca Cola 2L": 80,
    "Britannia Bread": 40, "Toor Dal 1kg": 130
}

def broadcast(queues, data):
    dead = []
    for q in queues:
        try:
            q.put_nowait(json.dumps(data))
        except:
            dead.append(q)
    for d in dead:
        try:
            queues.remove(d)
        except:
            pass

@app.route('/freshmart')
def freshmart():
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(templates_dir, 'freshmart_dashboard.html')

@app.route('/quicksupply')
def quicksupply():
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(templates_dir, 'quicksupply_portal.html')

@app.route('/api/erp/orders', methods=['GET'])
def get_orders():
    return jsonify({"total_orders": len(ORDERS), "orders": ORDERS})

@app.route('/api/erp/orders/create', methods=['POST'])
def create_order():
    data = request.json
    with lock:
        oid = f"ORD-{ORDER_COUNTER[0]}"
        ORDER_COUNTER[0] += 1
    qty = data.get("quantity", 0)
    pname = data.get("product_name", "")
    order = {
        "order_id": oid,
        "product_id": data.get("product_id"),
        "product_name": pname,
        "quantity": qty,
        "supplier": "QuickSupply Co",
        "status": "PENDING",
        "created_at": datetime.now().isoformat(),
        "expected_delivery": "2-3 business days",
        "raised_by": "AI Agent",
        "total_value": qty * PRICES.get(pname, 50)
    }
    ORDERS.append(order)
    broadcast(freshmart_queues, {"type": "order_placed", "order": order})
    return jsonify({"success": True, "message": "Order created!", "order": order})

@app.route('/api/erp/orders/<order_id>/update', methods=['POST'])
def update_order(order_id):
    data = request.json
    for o in ORDERS:
        if o["order_id"] == order_id:
            o["status"] = data.get("status", o["status"])
            return jsonify({"success": True, "order": o})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/supplier/receive-order', methods=['POST'])
def receive_order():
    data = request.json
    pname = data.get("product_name", "")
    qty = data.get("quantity", 0)
    sup_order = {
        "sup_order_id": f"SUP-{random.randint(1000, 9999)}",
        "product_id": data.get("product_id"),
        "product_name": pname,
        "quantity": qty,
        "status": "CONFIRMED",
        "confirmed_at": datetime.now().isoformat(),
        "estimated_delivery": "2-3 business days",
        "total_value": qty * PRICES.get(pname, 50)
    }
    SUPPLIER_ORDERS.append(sup_order)
    broadcast(quicksupply_queues, {"type": "order_received", "order": sup_order})
    for o in ORDERS:
        if o.get("product_name") == pname and o["status"] == "PENDING":
            o["status"] = "CONFIRMED"
            broadcast(freshmart_queues, {"type": "order_confirmed", "order": o})
            break
    return jsonify({"success": True, "message": "Order confirmed by QuickSupply Co!", "order": sup_order})

@app.route('/api/supplier/orders', methods=['GET'])
def get_supplier_orders():
    return jsonify({"total": len(SUPPLIER_ORDERS), "orders": SUPPLIER_ORDERS})

@app.route('/api/freshmart/stream')
def freshmart_stream():
    q = queue.Queue()
    freshmart_queues.append(q)
    def gen():
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"
        while True:
            try:
                data = q.get(timeout=25)
                yield f"data: {data}\n\n"
            except:
                yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
    return Response(gen(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

@app.route('/api/quicksupply/stream')
def quicksupply_stream():
    q = queue.Queue()
    quicksupply_queues.append(q)
    def gen():
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"
        while True:
            try:
                data = q.get(timeout=25)
                yield f"data: {data}\n\n"
            except:
                yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
    return Response(gen(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

if __name__ == '__main__':
    app.run(port=5003, debug=False, threaded=True)