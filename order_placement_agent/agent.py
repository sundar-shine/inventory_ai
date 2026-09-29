import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_warehouse_stock() -> dict:
    """Fetch current stock levels to identify shortages."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

def place_order(product_id: int, product_name: str, quantity: int) -> dict:
    """Place a replenishment order in ERP system."""
    try:
        response = requests.post(
            "http://127.0.0.1:5003/api/erp/orders/create",
            json={
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity
            }
        )
        return response.json()
    except Exception as e:
        return {"error": f"ERP API not reachable: {str(e)}"}

def confirm_with_supplier(product_id: int, product_name: str, quantity: int) -> dict:
    """Confirm order with QuickSupply Co supplier."""
    try:
        response = requests.post(
            "http://127.0.0.1:5004/api/supplier/receive-order",
            json={
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity
            }
        )
        return response.json()
    except Exception as e:
        return {"error": f"Supplier API not reachable: {str(e)}"}

def get_pending_orders() -> dict:
    """Check existing orders to avoid duplicate orders."""
    try:
        response = requests.get("http://127.0.0.1:5003/api/erp/orders")
        return response.json()
    except Exception as e:
        return {"error": f"ERP API not reachable: {str(e)}"}

root_agent = Agent(
    name="order_placement_agent",
    model="groq/openai/gpt-oss-120b",
    description="Automatically places replenishment orders for FreshMart shortages.",
    instruction="""
    You are the Order Placement Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_warehouse_stock() to identify products with shortages
    2. Call get_pending_orders() to check if orders already exist
    3. For each shortage product - calculate order quantity:
       - Order quantity = maximum_stock - current_stock
    4. Call place_order() to create order in ERP system
    5. Call confirm_with_supplier() to confirm with QuickSupply Co
    6. Provide summary of all orders placed

    Important rules:
    - Only order for products where current_stock < minimum_stock
    - Do not duplicate orders already pending
    - Always confirm with supplier after placing ERP order
    - Report order ID, quantity, and expected delivery for each order
    """,
    tools=[
        FunctionTool(get_warehouse_stock),
        FunctionTool(get_pending_orders),
        FunctionTool(place_order),
        FunctionTool(confirm_with_supplier),
    ],
)