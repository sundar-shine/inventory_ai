from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# FreshMart Warehouse - Current Stock Levels
WAREHOUSE_STOCK = {
    1: {"product_name": "Lays Classic", "current_stock": 50, "minimum_stock": 100, "maximum_stock": 500},
    2: {"product_name": "Basmati Rice 5kg", "current_stock": 200, "minimum_stock": 150, "maximum_stock": 800},
    3: {"product_name": "Amul Milk 1L", "current_stock": 30, "minimum_stock": 100, "maximum_stock": 400},
    4: {"product_name": "Sunflower Oil 1L", "current_stock": 80, "minimum_stock": 80, "maximum_stock": 300},
    5: {"product_name": "Maggi Noodles", "current_stock": 25, "minimum_stock": 100, "maximum_stock": 500},
    6: {"product_name": "Coca Cola 2L", "current_stock": 60, "minimum_stock": 80, "maximum_stock": 400},
    7: {"product_name": "Britannia Bread", "current_stock": 20, "minimum_stock": 50, "maximum_stock": 200},
    8: {"product_name": "Toor Dal 1kg", "current_stock": 150, "minimum_stock": 100, "maximum_stock": 600},
}

@app.route('/api/warehouse/stock', methods=['GET'])
def get_stock():
    stock_list = []
    for product_id, stock in WAREHOUSE_STOCK.items():
        shortage = stock["current_stock"] < stock["minimum_stock"]
        stock_list.append({
            "product_id": product_id,
            "product_name": stock["product_name"],
            "current_stock": stock["current_stock"],
            "minimum_stock": stock["minimum_stock"],
            "maximum_stock": stock["maximum_stock"],
            "shortage": shortage,
            "shortage_amount": max(0, stock["minimum_stock"] - stock["current_stock"])
        })
    return jsonify({
        "warehouse": "FreshMart Central Warehouse",
        "last_updated": datetime.now().isoformat(),
        "stock_data": stock_list
    })

@app.route('/api/warehouse/stock/<int:product_id>', methods=['GET'])
def get_product_stock(product_id):
    if product_id in WAREHOUSE_STOCK:
        stock = WAREHOUSE_STOCK[product_id]
        return jsonify({
            "product_id": product_id,
            "product_name": stock["product_name"],
            "current_stock": stock["current_stock"],
            "shortage": stock["current_stock"] < stock["minimum_stock"]
        })
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/warehouse/update', methods=['POST'])
def update_stock():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    if product_id in WAREHOUSE_STOCK:
        WAREHOUSE_STOCK[product_id]["current_stock"] += quantity
        return jsonify({
            "success": True,
            "message": f"Stock updated for product {product_id}",
            "new_stock": WAREHOUSE_STOCK[product_id]["current_stock"]
        })
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)