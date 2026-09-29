import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_sales_history() -> dict:
    """Fetch sales history from POS API for forecasting."""
    try:
        response = requests.get("http://127.0.0.1:5001/api/pos/sales")
        return response.json()
    except Exception as e:
        return {"error": f"POS API not reachable: {str(e)}"}

def get_external_signals() -> dict:
    """Fetch external signals like weather, festivals and events."""
    try:
        response = requests.get("http://127.0.0.1:5005/api/external/signals")
        return response.json()
    except Exception as e:
        return {"error": f"External API not reachable: {str(e)}"}

def get_current_stock() -> dict:
    """Fetch current warehouse stock levels."""
    try:
        response = requests.get("http://127.0.0.1:5002/api/warehouse/stock")
        return response.json()
    except Exception as e:
        return {"error": f"Warehouse API not reachable: {str(e)}"}

root_agent = Agent(
    name="forecasting_agent",
    model="groq/openai/gpt-oss-120b",
    description="Forecasts demand for FreshMart products for next 7 days.",
    instruction="""
    You are the Forecasting Agent for FreshMart, a retail store in Chennai.

    Your job:
    1. Call get_sales_history() to get current and historical sales data
    2. Call get_external_signals() to get weather, festival and IPL data
    3. Call get_current_stock() to understand current inventory levels
    4. Forecast demand for next 7 days for each product
    5. Provide:
       - Predicted units needed per product for next 7 days
       - Confidence level (HIGH/MEDIUM/LOW)
       - Key factors driving the forecast
       - Which products need urgent restocking

    Be specific with numbers. Always be concise and actionable.
    """,
    tools=[
        FunctionTool(get_sales_history),
        FunctionTool(get_external_signals),
        FunctionTool(get_current_stock),
    ],
)