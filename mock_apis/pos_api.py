from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# FreshMart - Fake Store Products
PRODUCTS = [
    {"id": 1, "name": "Lays Classic", "category": "Snacks"},
    {"id": 2, "name": "Basmati Rice 5kg", "category": "Grocery"},
    {"id": 3, "name": "Amul Milk 1L", "category": "Dairy"},
    {"id": 4, "name": "Sunflower Oil 1L", "category": "Grocery"},
    {"id": 5, "name": "Maggi Noodles", "category": "Snacks"},
    {"id": 6, "name": "Coca Cola 2L", "category": "Beverages"},
    {"id": 7, "name": "Britannia Bread", "category": "Bakery"},
    {"id": 8, "name": "Toor Dal 1kg", "category": "Grocery"},
]

@app.route('/api/pos/sales', methods=['GET'])
def get_sales():
    sales = []
    for product in PRODUCTS:
        sales.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "units_sold_today": random.randint(10, 100),
            "units_sold_yesterday": random.randint(10, 100),
            "units_sold_last_week": random.randint(50, 500),
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({
        "store": "FreshMart Chennai",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sales_data": sales
    })

@app.route('/api/pos/promotions', methods=['GET'])
def get_promotions():
    return jsonify({
        "active_promotions": [
            {"product": "Lays Classic", "discount": "10%", "valid_till": "2026-03-20"},
            {"product": "Coca Cola 2L", "discount": "15%", "valid_till": "2026-03-18"},
        ]
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)