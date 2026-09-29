import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_external_signals() -> dict:
    """Fetch weather, festival and IPL match signals."""
    try:
        response = requests.get("http://127.0.0.1:5005/api/external/signals")
        return response.json()
    except Exception as e:
        return {"error": f"External API not reachable: {str(e)}"}

def get_sales_data() -> dict:
    """Fetch current sales data to compare with external signals."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

def get_warehouse_stock() -> dict:
    """Fetch stock levels to check if prepared for demand changes."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

root_agent = Agent(
    name="external_signal_agent",
    model="groq/openai/gpt-oss-120b",
    description="Analyzes external signals like weather, festivals and IPL to adjust demand planning.",
    instruction="""
    You are the External Signal Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_external_signals() to get weather, festival and IPL data
    2. Call get_sales_data() to see current sales trends
    3. Call get_warehouse_stock() to check current stock levels
    4. Analyze external factors and provide:
       - Weather impact on demand (hot weather → beverages up)
       - Festival impact (Tamil New Year → rice, oil, sweets up)
       - IPL match impact (match day → snacks, beverages up)
       - Demand multiplier per product category
       - Stock adequacy check for upcoming events
       - Recommended additional stock for each event

    Always give specific product recommendations with quantities.
    """,
    tools=[
        FunctionTool(get_external_signals),
        FunctionTool(get_sales_data),
        FunctionTool(get_warehouse_stock),
    ],
)