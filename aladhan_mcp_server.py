#!/usr/bin/env python3
"""
Aladhan API MCP Server
Provides Islamic prayer times, Qibla direction, and Hijri date conversion
"""

import sys
import json
import asyncio
import requests
import datetime
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import (
    Resource, 
    Tool, 
    TextContent, 
    ImageContent, 
    EmbeddedResource, 
    LoggingLevel
)
import mcp.server.stdio

# Aladhan API configuration
ALADHAN_API_BASE_URL = "http://api.aladhan.com/v1"

# Create server instance
server = Server("aladhan-api")

def call_aladhan_api(endpoint: str, params: dict = None) -> dict:
    """Generic helper to call the Aladhan API."""
    try:
        url = f"{ALADHAN_API_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "details": "Failed to connect to Aladhan API"}
    except ValueError:
        return {"error": "Invalid JSON response from Aladhan API"}

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for the Aladhan API."""
    return [
        Tool(
            name="get_prayer_times_by_city",
            description="Get Islamic prayer times for a specific city and date",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city (e.g., London)"
                    },
                    "country": {
                        "type": "string", 
                        "description": "Name of the country (e.g., UK)"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "method": {
                        "type": "integer",
                        "description": "Calculation method ID (optional, 1-15)"
                    },
                    "school": {
                        "type": "integer",
                        "enum": [0, 1],
                        "description": "Asr juristic method: 0 for Shafi, 1 for Hanafi (optional)"
                    }
                },
                "required": ["city", "country"]
            }
        ),
        Tool(
            name="get_prayer_times_by_coordinates",
            description="Get Islamic prayer times for specific geographic coordinates and date",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location"
                    },
                    "longitude": {
                        "type": "number", 
                        "description": "Longitude of the location"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "method": {
                        "type": "integer",
                        "description": "Calculation method ID (optional, 1-15)"
                    },
                    "school": {
                        "type": "integer",
                        "enum": [0, 1],
                        "description": "Asr juristic method: 0 for Shafi, 1 for Hanafi (optional)"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        ),
        Tool(
            name="convert_gregorian_to_hijri",
            description="Convert a Gregorian date to Hijri (Islamic) date",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Gregorian date in DD-MM-YYYY format (e.g., 20-07-2024)",
                        "pattern": "^\\d{2}-\\d{2}-\\d{4}$"
                    }
                },
                "required": ["date"]
            }
        ),
        Tool(
            name="get_qibla_direction",
            description="Get the Qibla direction (degrees from North) for given coordinates",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        ),
        Tool(
            name="get_calculation_methods",
            description="Get available prayer time calculation methods",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for the Aladhan API."""
    
    try:
        if name == "get_prayer_times_by_city":
            city = arguments["city"]
            country = arguments["country"]
            date_str = arguments.get("date")
            method = arguments.get("method")
            school = arguments.get("school")
            
            # Handle date
            if date_str:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_obj = datetime.date.today()
            
            api_date_str = date_obj.strftime("%d-%m-%Y")
            
            # Build parameters
            params = {"city": city, "country": country}
            if method is not None:
                params["method"] = method
            if school is not None:
                params["school"] = school
            
            result = call_aladhan_api(f"timingsByCity/{api_date_str}", params=params)
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            if "data" in result and "timings" in result["data"]:
                data = result["data"]
                timings = data["timings"]
                date_info = data["date"]
                
                response = f"🕌 Prayer Times for {city}, {country}\n"
                response += f"📅 Date: {date_info['readable']} ({date_info['hijri']['date']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']} AH)\n\n"
                
                prayer_names = {
                    "Fajr": "🌅 Fajr (Dawn)",
                    "Sunrise": "☀️ Sunrise", 
                    "Dhuhr": "🌞 Dhuhr (Noon)",
                    "Asr": "🌤️ Asr (Afternoon)",
                    "Sunset": "🌇 Sunset",
                    "Maghrib": "🌆 Maghrib (Evening)",
                    "Isha": "🌙 Isha (Night)"
                }
                
                for prayer, time in timings.items():
                    if prayer in prayer_names:
                        response += f"{prayer_names[prayer]}: {time}\n"
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(type="text", text="No prayer time data found in response")]
        
        elif name == "get_prayer_times_by_coordinates":
            latitude = arguments["latitude"]
            longitude = arguments["longitude"]
            date_str = arguments.get("date")
            method = arguments.get("method")
            school = arguments.get("school")
            
            # Handle date
            if date_str:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_obj = datetime.date.today()
            
            api_date_str = date_obj.strftime("%d-%m-%Y")
            
            # Build parameters
            params = {"latitude": latitude, "longitude": longitude}
            if method is not None:
                params["method"] = method
            if school is not None:
                params["school"] = school
            
            result = call_aladhan_api(f"timings/{api_date_str}", params=params)
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            if "data" in result and "timings" in result["data"]:
                data = result["data"]
                timings = data["timings"]
                date_info = data["date"]
                
                response = f"🕌 Prayer Times for coordinates ({latitude}, {longitude})\n"
                response += f"📅 Date: {date_info['readable']} ({date_info['hijri']['date']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']} AH)\n\n"
                
                prayer_names = {
                    "Fajr": "🌅 Fajr (Dawn)",
                    "Sunrise": "☀️ Sunrise",
                    "Dhuhr": "🌞 Dhuhr (Noon)", 
                    "Asr": "🌤️ Asr (Afternoon)",
                    "Sunset": "🌇 Sunset",
                    "Maghrib": "🌆 Maghrib (Evening)",
                    "Isha": "🌙 Isha (Night)"
                }
                
                for prayer, time in timings.items():
                    if prayer in prayer_names:
                        response += f"{prayer_names[prayer]}: {time}\n"
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(type="text", text="No prayer time data found in response")]
        
        elif name == "convert_gregorian_to_hijri":
            date_str = arguments["date"]
            
            result = call_aladhan_api("gToH", params={"date": date_str})
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            if "data" in result and "hijri" in result["data"]:
                hijri = result["data"]["hijri"]
                gregorian = result["data"]["gregorian"]
                
                response = f"📅 Date Conversion\n\n"
                response += f"Gregorian: {gregorian['date']} {gregorian['month']['en']} {gregorian['year']}\n"
                response += f"Hijri: {hijri['date']} {hijri['month']['en']} {hijri['year']} AH\n"
                response += f"Islamic Month: {hijri['month']['ar']} ({hijri['month']['en']})\n"
                response += f"Weekday: {hijri['weekday']['en']}\n"
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(type="text", text="No date conversion data found")]
        
        elif name == "get_qibla_direction":
            latitude = arguments["latitude"]
            longitude = arguments["longitude"]
            
            result = call_aladhan_api(f"qibla/{latitude}/{longitude}")
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            if "data" in result and "direction" in result["data"]:
                direction = result["data"]["direction"]
                
                response = f"🧭 Qibla Direction\n\n"
                response += f"📍 Location: ({latitude}, {longitude})\n"
                response += f"🕋 Qibla Direction: {direction:.2f}° from North\n\n"
                
                # Add compass direction description
                if 337.5 <= direction or direction < 22.5:
                    compass = "North"
                elif 22.5 <= direction < 67.5:
                    compass = "Northeast"
                elif 67.5 <= direction < 112.5:
                    compass = "East"
                elif 112.5 <= direction < 157.5:
                    compass = "Southeast"
                elif 157.5 <= direction < 202.5:
                    compass = "South"
                elif 202.5 <= direction < 247.5:
                    compass = "Southwest"
                elif 247.5 <= direction < 292.5:
                    compass = "West"
                else:
                    compass = "Northwest"
                
                response += f"Compass Direction: {compass}"
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(type="text", text="No Qibla direction data found")]
        
        elif name == "get_calculation_methods":
            result = call_aladhan_api("methods")
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            if "data" in result:
                methods = result["data"]
                
                response = "🕌 Prayer Time Calculation Methods\n\n"
                
                for method_id, method_info in methods.items():
                    if isinstance(method_info, dict) and "name" in method_info:
                        response += f"{method_id}. {method_info['name']}\n"
                        if "params" in method_info:
                            params = method_info["params"]
                            if "Fajr" in params:
                                response += f"   - Fajr: {params['Fajr']}°\n"
                            if "Isha" in params:
                                response += f"   - Isha: {params['Isha']}°\n"
                        response += "\n"
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(type="text", text="No calculation methods data found")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
