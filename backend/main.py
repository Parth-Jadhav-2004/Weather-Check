from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import requests

import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

#Tool Calling
@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Fetch live weather data using OpenWeatherMap API."""
    
    print(f"\n[TOOL CALLED] get_weather")
    print(f"  Location: {location}")
    print(f"  Units: {units}")

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather service is not configured."

    unit_param = "metric" if units == "celsius" else "imperial"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": unit_param
    }
    
    print(f"  Calling: {url}?q={location}&units={unit_param}")

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"  Status: {response.status_code}")

        if response.status_code != 200:
            error = response.json()
            print(f"  Error: {error}")
            return f"Could not fetch weather for {location}. {error.get('message', '')}"

        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()

        result = (
            f"Current weather in {location}:\n"
            f"- Temperature: {temp}°{'C' if units == 'celsius' else 'F'}\n"
            f"- Feels like: {feels_like}°{'C' if units == 'celsius' else 'F'}\n"
            f"- Condition: {description}"
        )
        print(f"  Success! Returning weather data\n")
        return result
        
    except Exception as e:
        print(f"  Exception: {e}\n")
        return f"Error: {str(e)}"

tools = [get_weather]

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can provide accurate and up-to-date weather information."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

@app.get("/")
def read_root():
    return {"message": "Weather API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        print(f"Received message: {request.message}")
        result = agent_executor.invoke({"input": request.message})
        print(f"Agent result: {result}")
        return ChatResponse(response=result["output"])
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)