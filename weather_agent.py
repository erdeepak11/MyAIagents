import json
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
from git import Repo, GitCommandError, InvalidGitRepositoryError


load_dotenv()

client = OpenAI()

def query_db(sql):
    pass

def run_command(command):
    #execute command on users system
    #return result
    result = os.system(command=command)
    return result

# print(run_command("ls"))

def get_weather (city:str):
    #TODO: Do an actual API call
    print("🧰 Tool called:get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    headers = {
        "User-Agent": "curl/7.81.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"⚠️ Could not retrieve weather for {city}. Status code: {response.status_code}"




available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes the city name as input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    }
    
    
}

system_prompt = """
    You are an helpful AI assistant who is specialized  in resolving user query. 
    You work on star, plan, action, observe mode.
    For the given user query and available tools, analyze the plan the step by step execution, based on the planning 
    select the relevant tool from the available tool. And based on the tool selection you perform an action to call the tool. 
    Wait for the observation and based on the observation from the tool called resolve the user query.

    Rules:
    - Follow the output JSON Format.
    - Always perform one step at a time and wait for next input 
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step":"string", 
        "content": "string",
        "function": "The name of function if the step is action",
        "input":  "The input parameter for the function",
    }}

    Available Tools: 
    -get_weather: Takes city name as an input and returns the current weather for the city
    -run_command: Takes a command as input to execute on system and returns output
    
    Example: 
    User Query: What is the weather of New York?
    Output: {{"step": "plan", "content": "The user is interested in weather data of New York" }}
    Output: {{"step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{"step": "action", "function": "get_weather", "input": "New York"}}
    Output: {{"step": "observe", "output": "12 Degree Cel"}}
    Output: {{"step": "output", "content": "The weather for New York seems to be 12 degrees."}}
"""

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_query = input ('>')
    messages.append({"role": "user", "content":user_query})
    while True:
        response = client.chat.completions.create(
            model = "gpt-4o",
            response_format = {"type" : "json_object"},
            messages = messages

        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}" )
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖 :{parsed_output.get('content')}")
            break


'''
response = client.chat.completions.create(
    model = "gpt-4o",
    response_format = {"type" : "json_object"},
    messages = [

        {"role": "system", "content": system_prompt},
        {"role": "user", "content":"What is the current weather of Patiala?" },
        {"role":"assistant", "content":json.dumps({"step": "plan", "content": "The user is interested in the current weather data of Patiala."})},
        {"role":"assistant", "content":json.dumps({"step": "plan", "content": "From the available tools I should call get_weather to retrieve the weather information for Patiala."})},
        {"role":"assistant", "content":json.dumps({"step": "action", "function": "get_weather", "input": "Patiala"})},
        {"role":"assistant", "content":json.dumps({"step": "observe", "output": "31 degree celcius"})}
        
    ]
)

print(response.choices[0].message.content)'''