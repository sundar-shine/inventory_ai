import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_warehouse_stock() -> dict:
    """Fetch current stock levels for report."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

def get_all_orders() -> dict:
    """Fetch all orders placed today."""
    try:
        response = requests.get("http://127.0.0.1:5003/api/erp/orders")
        return response.json()
    except Exception as e:
        return {"error": f"ERP API not reachable: {str(e)}"}

def get_sales_data() -> dict:
    """Fetch today's sales data."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

def get_external_signals() -> dict:
    """Fetch external signals for report context."""
    try:
        response = requests.get("http://127.0.0.1:5005/api/external/signals")
        return response.json()
    except Exception as e:
        return {"error": f"External API not reachable: {str(e)}"}

def get_supplier_info() -> dict:
    """Fetch supplier information for report."""
    try:
        response = requests.get("http://127.0.0.1:5004/api/supplier/products")
        return response.json()
    except Exception as e:
        return {"error": f"Supplier API not reachable: {str(e)}"}

root_agent = Agent(
    name="reporting_agent",
    model="groq/openai/gpt-oss-120b",
    description="Generates comprehensive daily inventory reports for FreshMart management.",
    instruction="""
    You are the Reporting Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_sales_data() to get today's sales summary
    2. Call get_warehouse_stock() to get current inventory status
    3. Call get_all_orders() to get all orders placed today
    4. Call get_external_signals() to get market context
    5. Call get_supplier_info() to get supplier details

    Generate a comprehensive Daily Inventory Report with these sections:

    SECTION 1 - EXECUTIVE SUMMARY
    - Overall store health score (0-100)
    - Key highlights of the day
    - Critical actions needed

    SECTION 2 - SALES PERFORMANCE
    - Top 3 selling products today
    - Products with demand spikes
    - Overall revenue estimate

    SECTION 3 - INVENTORY STATUS
    - Critical shortage products
    - Low stock warnings
    - Healthy stock products

    SECTION 4 - ORDERS PLACED TODAY
    - Total orders count
    - Products ordered and quantities
    - Expected delivery summary

    SECTION 5 - EXTERNAL FACTORS
    - Weather impact
    - Festival impact (Tamil New Year)
    - IPL match impact

    SECTION 6 - RECOMMENDATIONS
    - Top 3 urgent actions for tomorrow
    - Stock preparation for upcoming events

    Make the report clear, professional and actionable.
    """,
    tools=[
        FunctionTool(get_sales_data),
        FunctionTool(get_warehouse_stock),
        FunctionTool(get_all_orders),
        FunctionTool(get_external_signals),
        FunctionTool(get_supplier_info),
    ],
)