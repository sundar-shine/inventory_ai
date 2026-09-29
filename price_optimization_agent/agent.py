import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_warehouse_stock() -> dict:
    """Fetch stock levels to identify overstock and understock."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

def get_sales_data() -> dict:
    """Fetch sales data to understand demand patterns."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

def get_supplier_prices() -> dict:
    """Fetch supplier pricing data."""
    try:
        response = requests.get("http://127.0.0.1:5004/api/supplier/products")
        return response.json()
    except Exception as e:
        return {"error": f"Supplier API not reachable: {str(e)}"}

def get_external_signals() -> dict:
    """Fetch external signals for demand-based pricing."""
    try:
        response = requests.get("http://127.0.0.1:5005/api/external/signals")
        return response.json()
    except Exception as e:
        return {"error": f"External API not reachable: {str(e)}"}

root_agent = Agent(
    name="price_optimization_agent",
    model="groq/openai/gpt-oss-120b",
    description="Optimizes pricing for FreshMart based on stock levels and demand.",
    instruction="""
    You are the Price Optimization Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_warehouse_stock() to identify overstock and understock items
    2. Call get_sales_data() to understand current demand patterns
    3. Call get_supplier_prices() to know cost price of each product
    4. Call get_external_signals() to factor in festivals and events
    5. Provide pricing recommendations:

    For OVERSTOCK items (current > maximum * 0.8):
       - Suggest discount percentage (5% to 30%)
       - Reason: clear stock before expiry

    For UNDERSTOCK items (current < minimum):
       - Suggest price protection (no discount)
       - Reason: high demand, protect margins

    For FESTIVAL season items:
       - Suggest strategic pricing
       - Balance between demand and margins

    Always provide: product name, current price, recommended price, discount %, reason.
    """,
    tools=[
        FunctionTool(get_warehouse_stock),
        FunctionTool(get_sales_data),
        FunctionTool(get_supplier_prices),
        FunctionTool(get_external_signals),
    ],
)