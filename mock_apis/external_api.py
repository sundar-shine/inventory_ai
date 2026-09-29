from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/external/signals', methods=['GET'])
def get_external_signals():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "weather": {
            "city": "Chennai",
            "condition": "Hot and Humid",
            "temperature": 35,
            "rain_expected": False,
            "demand_impact": {
                "Beverages": "HIGH",
                "Ice Cream": "HIGH",
                "Umbrella": "LOW"
            }
        },
        "festivals": {
            "upcoming": "Tamil New Year",
            "days_remaining": 15,
            "demand_impact": {
                "Sweets": "VERY HIGH",
                "Rice": "HIGH",
                "Oil": "HIGH",
                "Snacks": "HIGH"
            }
        },
        "events": {
            "ipl_match_today": True,
            "demand_impact": {
                "Snacks": "HIGH",
                "Beverages": "VERY HIGH",
                "Coca Cola 2L": "VERY HIGH",
                "Lays Classic": "HIGH"
            }
        },
        "overall_demand_multiplier": 1.4
    })

@app.route('/api/external/weather', methods=['GET'])
def get_weather():
    return jsonify({
        "city": "Chennai",
        "temperature": 35,
        "condition": "Hot and Humid",
        "rain_expected": False
    })

@app.route('/api/external/festivals', methods=['GET'])
def get_festivals():
    return jsonify({
        "upcoming_festival": "Tamil New Year",
        "days_remaining": 15,
        "high_demand_products": ["Rice", "Oil", "Sweets", "Snacks"]
    })

if __name__ == '__main__':
    app.run(port=5005, debug=True)