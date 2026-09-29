import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_all_orders() -> dict:
    """Fetch all orders from ERP to check for delays."""
    try:
        response = requests.get("http://127.0.0.1:5003/api/erp/orders")
        return response.json()
    except Exception as e:
        return {"error": f"ERP API not reachable: {str(e)}"}

def get_warehouse_stock() -> dict:
    """Fetch current stock to detect sudden stockouts."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

def get_sales_data() -> dict:
    """Fetch sales data to detect sudden demand spikes."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

def get_external_signals() -> dict:
    """Fetch external signals for demand shift detection."""
    try:
        response = requests.get("http://127.0.0.1:5005/api/external/signals")
        return response.json()
    except Exception as e:
        return {"error": f"External API not reachable: {str(e)}"}

def trigger_alert(alert_type: str, product_name: str, message: str) -> dict:
    """Trigger an alert for exceptions detected."""
    alert = {
        "alert_type": alert_type,
        "product": product_name,
        "message": message,
        "status": "ALERT TRIGGERED",
        "action_required": True
    }
    print(f"🚨 ALERT: {alert_type} - {product_name}: {message}")
    return alert

root_agent = Agent(
    name="exception_monitor_agent",
    model="groq/openai/gpt-oss-120b",
    description="Monitors exceptions like delays, demand spikes and stockouts for FreshMart.",
    instruction="""
    You are the Exception Monitor Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_all_orders() to check for delayed or stuck orders
    2. Call get_warehouse_stock() to detect critical stockouts
    3. Call get_sales_data() to detect sudden demand spikes
    4. Call get_external_signals() to check for upcoming demand shifts
    5. For each exception found - call trigger_alert() with:
       - alert_type: DELAY / STOCKOUT / DEMAND_SPIKE / SUPPLIER_ISSUE
       - product_name: affected product
       - message: clear description of the issue
    6. Provide summary of all exceptions and recommended actions

    Be proactive - flag issues before they become critical!
    """,
    tools=[
        FunctionTool(get_all_orders),
        FunctionTool(get_warehouse_stock),
        FunctionTool(get_sales_data),
        FunctionTool(get_external_signals),
        FunctionTool(trigger_alert),
    ],
)