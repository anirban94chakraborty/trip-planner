import os
import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

load_dotenv()

app = Server("weather-planner")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather_forecast",
            description="Get the current weather and 2-day forecast for a given destination city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The destination city (e.g., Darjeeling)"}
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name != "get_weather_forecast":
        raise ValueError(f"Unknown tool: {name}")
    
    city = arguments.get("city")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return CallToolResult(content=[TextContent(type="text", text="Error: OpenWeather API key not configured.")])

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        
        forecast_summary = f"The current weather in {city} is {temp}°C with {description}. (Simulated 2-day forecast assumes similar conditions)."
        return CallToolResult(content=[TextContent(type="text", text=forecast_summary)])
        
    except Exception as e:
        return CallToolResult(content=[TextContent(type="text", text=f"Failed to retrieve weather for {city}: {str(e)}")])

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())