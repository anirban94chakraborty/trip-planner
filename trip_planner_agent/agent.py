import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import MCPToolset
from mcp import StdioServerParameters
from dotenv import load_dotenv

# 1. Load variables
load_dotenv()

# 2. Get the absolute path of the directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_SCRIPT_PATH = os.path.join(BASE_DIR, "weather_mcp.py")

# 3. Define the connection
server_params = StdioServerParameters(
    command="python",
    args=[MCP_SCRIPT_PATH]
)

# 4. Wrap the connection
weather_toolset = MCPToolset(connection_params=server_params)

# 4. Define the root agent with the tool attached
root_agent = Agent(
    model='gemini-2.5-flash',
    name='trip_planner_agent',
    description='An AI travel assistant that generates itineraries based on live weather data.',
    instruction="""
    You are an expert regional travel planner. 
    When a user asks to plan a trip, you MUST use the get_weather_forecast tool to check the weather at their destination.
    Once you have the weather data, generate a realistic 2-day itinerary tailored to those specific conditions.
    """,
    tools=[weather_toolset]
)