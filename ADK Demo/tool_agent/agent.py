from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name = "tool_agent",
    model = "gemini-2.0-flash",
    description="An example agent that will answer user queries based on Google Search results.",   
    instruction="""
    You are an AI Assistant that helps users with Goole search related queries.
    """,  
    tools=[google_search]
)
