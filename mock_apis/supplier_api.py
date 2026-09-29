from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# QuickSupply Co - Supplier Database
SUPPLIER_PRODUCTS = {
    1: {"product_name": "Lays Classic", "price_per_unit": 10, "available_stock": 5000, "lead_time_days": 2},
    2: {"product_name": "Basmati Rice 5kg", "price_per_unit": 250, "available_stock": 3000, "lead_time_days": 1},
    3: {"product_name": "Amul Milk 1L", "price_per_unit": 55, "available_stock": 4000, "lead_time_days": 1},
    4: {"product_name": "Sunflower Oil 1L", "price_per_unit": 120, "available_stock": 2000, "lead_time_days": 2},
    5: {"product_name": "Maggi Noodles", "price_per_unit": 14, "available_stock": 6000, "lead_time_days": 2},
    6: {"product_name": "Coca Cola 2L", "price_per_unit": 80, "available_stock": 3000, "lead_time_days": 1},
    7: {"product_name": "Britannia Bread", "price_per_unit": 40, "available_stock": 2000, "lead_time_days": 1},
    8: {"product_name": "Toor Dal 1kg", "price_per_unit": 130, "available_stock": 4000, "lead_time_days": 2},
}

# Received Orders
RECEIVED_ORDERS = []

@app.route('/api/supplier/products', methods=['GET'])
def get_products():
    return jsonify({
        "supplier": "QuickSupply Co",
        "location": "Chennai",
        "products": SUPPLIER_PRODUCTS
    })

@app.route('/api/supplier/receive-order', methods=['POST'])
def receive_order():
    data = request.json
    
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    
    if product_id not in SUPPLIER_PRODUCTS:
        return jsonify({"error": "Product not available"}), 404
    
    product = SUPPLIER_PRODUCTS[product_id]
    
    if product["available_stock"] < quantity:
        return jsonify({
            "success": False,
            "message": "Insufficient stock at supplier!"
        }), 400
    
    # Reduce supplier stock
    SUPPLIER_PRODUCTS[product_id]["available_stock"] -= quantity
    
    order = {
        "order_id": f"SUP-{random.randint(1000, 9999)}",
        "product_id": product_id,
        "product_name": product["product_name"],
        "quantity": quantity,
        "total_price": quantity * product["price_per_unit"],
        "status": "CONFIRMED",
        "estimated_delivery": f"{product['lead_time_days']} days",
        "confirmed_at": datetime.now().isoformat()
    }
    
    RECEIVED_ORDERS.append(order)
    
    return jsonify({
        "success": True,
        "message": "Order confirmed by QuickSupply Co!",
        "order": order
    })

@app.route('/api/supplier/orders', methods=['GET'])
def get_received_orders():
    return jsonify({
        "supplier": "QuickSupply Co",
        "total_orders": len(RECEIVED_ORDERS),
        "orders": RECEIVED_ORDERS
    })

if __name__ == '__main__':
    app.run(port=5004, debug=True)