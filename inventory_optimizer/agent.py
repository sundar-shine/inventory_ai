import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_demand_analysis() -> dict:
    """Get real-time demand analysis from POS and external signals."""
    try:
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        promotions = requests.get("http://127.0.0.1:5001/api/pos/promotions").json()
        external = requests.get("http://127.0.0.1:5005/api/external/signals").json()
        return {"sales": sales, "promotions": promotions, "external_signals": external}
    except Exception as e:
        return {"error": str(e)}

def get_forecast() -> dict:
    """Get 7-day demand forecast."""
    try:
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        external = requests.get("http://127.0.0.1:5005/api/external/signals").json()
        stock = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        return {"sales_history": sales, "external_signals": external, "current_stock": stock}
    except Exception as e:
        return {"error": str(e)}

def get_inventory_status() -> dict:
    """Get current inventory levels and shortage analysis."""
    try:
        stock = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        orders = requests.get("http://127.0.0.1:5003/api/erp/orders").json()
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        return {"stock": stock, "pending_orders": orders, "sales": sales}
    except Exception as e:
        return {"error": str(e)}

def place_replenishment_orders() -> dict:
    """Check shortages and place orders for all shortage products."""
    try:
        stock_data = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        orders_placed = []
        for item in stock_data.get("stock_data", []):
            if item["shortage"]:
                quantity = item["maximum_stock"] - item["current_stock"]
                erp_response = requests.post(
                    "http://127.0.0.1:5003/api/erp/orders/create",
                    json={
                        "product_id": item["product_id"],
                        "product_name": item["product_name"],
                        "quantity": quantity
                    }
                ).json()
                supplier_response = requests.post(
                    "http://127.0.0.1:5004/api/supplier/receive-order",
                    json={
                        "product_id": item["product_id"],
                        "product_name": item["product_name"],
                        "quantity": quantity
                    }
                ).json()
                orders_placed.append({
                    "product": item["product_name"],
                    "quantity": quantity,
                    "erp_order": erp_response,
                    "supplier_confirmation": supplier_response
                })
        return {"orders_placed": orders_placed, "total_orders": len(orders_placed)}
    except Exception as e:
        return {"error": str(e)}

def monitor_exceptions() -> dict:
    """Monitor for stockouts, delays and demand spikes."""
    try:
        stock = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        orders = requests.get("http://127.0.0.1:5003/api/erp/orders").json()
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        external = requests.get("http://127.0.0.1:5005/api/external/signals").json()
        return {"stock": stock, "orders": orders, "sales": sales, "external": external}
    except Exception as e:
        return {"error": str(e)}

def get_price_recommendations() -> dict:
    """Get pricing recommendations based on stock and demand."""
    try:
        stock = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        supplier = requests.get("http://127.0.0.1:5004/api/supplier/products").json()
        external = requests.get("http://127.0.0.1:5005/api/external/signals").json()
        return {"stock": stock, "sales": sales, "supplier_prices": supplier, "external": external}
    except Exception as e:
        return {"error": str(e)}

def generate_daily_report() -> dict:
    """Generate comprehensive daily inventory report."""
    try:
        sales = requests.get("http://127.0.0.1:5001/api/pos/sales").json()
        stock = requests.get("http://127.0.0.1:5002/api/warehouse/stock").json()
        orders = requests.get("http://127.0.0.1:5003/api/erp/orders").json()
        external = requests.get("http://127.0.0.1:5005/api/external/signals").json()
        supplier = requests.get("http://127.0.0.1:5004/api/supplier/products").json()
        return {"sales": sales, "stock": stock, "orders": orders, "external": external, "supplier": supplier}
    except Exception as e:
        return {"error": str(e)}

root_agent = Agent(
    name="inventory_optimizer",
    model="groq/openai/gpt-oss-120b",
    description="Master AI agent for complete FreshMart inventory optimization.",
    instruction="""
    You are the Master Inventory Optimization Agent for FreshMart, Chennai.
    You have 7 powerful tools to manage the entire inventory lifecycle.

    When user asks about DEMAND:
    - Call get_demand_analysis() and provide insights on high demand products

    When user asks about FORECAST:
    - Call get_forecast() and predict next 7 days demand

    When user asks about INVENTORY or STOCK:
    - Call get_inventory_status() and report shortages and healthy stock

    When user asks to PLACE ORDERS:
    - Call place_replenishment_orders() and report all orders placed with supplier confirmations

    When user asks about EXCEPTIONS or ALERTS:
    - Call monitor_exceptions() and report all issues found

    When user asks about PRICING:
    - Call get_price_recommendations() and suggest discounts and price protection

    When user asks for REPORT or SUMMARY:
    - Call generate_daily_report() and provide comprehensive daily report

    When user says RUN COMPLETE OPTIMIZATION:
    - Call ALL 7 tools one by one
    - Present results from each tool clearly
    - Give final executive summary

    Always give clear, specific, actionable responses with actual numbers.
    """,
    tools=[
        FunctionTool(get_demand_analysis),
        FunctionTool(get_forecast),
        FunctionTool(get_inventory_status),
        FunctionTool(place_replenishment_orders),
        FunctionTool(monitor_exceptions),
        FunctionTool(get_price_recommendations),
        FunctionTool(generate_daily_report),
    ],
)