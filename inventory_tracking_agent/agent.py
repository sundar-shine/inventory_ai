import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_warehouse_stock() -> dict:
    """Fetch current stock levels from warehouse."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

def get_pending_orders() -> dict:
    """Fetch all pending orders from ERP system."""
    try:
        response = requests.get("http://127.0.0.1:5003/api/erp/orders")
        return response.json()
    except Exception as e:
        return {"error": f"ERP API not reachable: {str(e)}"}

def get_sales_data() -> dict:
    """Fetch today's sales to calculate stock consumption rate."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

root_agent = Agent(
    name="inventory_tracking_agent",
    model="groq/openai/gpt-oss-120b",
    description="Tracks inventory levels and detects shortages for FreshMart.",
    instruction="""
    You are the Inventory Tracking Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_warehouse_stock() to get current stock levels
    2. Call get_pending_orders() to check if any orders are already placed
    3. Call get_sales_data() to understand daily consumption rate
    4. Analyze and report:
       - Products with CRITICAL shortage (below minimum stock)
       - Products with LOW stock (within 20% of minimum)
       - Products with HEALTHY stock levels
       - Estimated days until stockout for critical items
       - Any pending orders that will resolve shortages

    Always provide a clear stock health summary with specific numbers.
    """,
    tools=[
        FunctionTool(get_warehouse_stock),
        FunctionTool(get_pending_orders),
        FunctionTool(get_sales_data),
    ],
)