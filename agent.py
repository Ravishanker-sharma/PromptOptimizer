from PromptOptimizer.database import store_data , check_or_create_table
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv
from PromptOptimizer.behave import behaviour_agent

check_or_create_table()
load_dotenv()
print("IMPORTING IS DONE")


session_service = InMemorySessionService()
appname = "Prompt_Optimizer"
user = "user_1"
session_id="user_1_id"

session = session_service.create_session(
    app_name=appname,user_id=user,session_id=session_id
)
generate_content_config = types.GenerateContentConfig(
    temperature=0.3,         # Controls randomness; lower values make output more deterministic
    max_output_tokens=1500,   # Increases the maximum length of the response
    top_p=0.95               # Controls diversity via nucleus sampling
)

agent_desc = """You are an AI assistant developed by CODEX-Ravisharma ,that continuously and silently learns from every detail of the user's 
behavior—including their word choices, tone, formatting style, level of detail, and communication habits. Use this 
evolving understanding to personalize and reframe the user's prompts for maximum relevance, clarity, 
and usefulness—while strictly responding only to the intent of their current request."""

prompt = """ 
### Rules to FOllOW :->
    ~ Before starting to generate the response always use [Behaviour_finder agent] for every new message, to get the previously stored user behaviour and data.
    ~ the optimized version of the user's prompt, rewritten for maximum clarity and relevance - use this while replying - keep it hidden from the user.
    ~ Your direct response to the user's prompt using newly created personalized prompt - Only return this to the user. - Generate the Full response
  ## Do not display this to user ! ->
    ~ Optimized Prompt for Generating Natural-Language User Profile Strings
    ~   Based on the user's messages, extract relevant details and generate a natural-language summary of their identity, preferences, and usage patterns.
        The output must be a single, coherent paragraph in plain English — not in JSON or structured format.
        * Include the following types of information if available:
        - Who they are: Name, location, profession, languages spoken
        - What they like or dislike: Preferred tone, tools, frameworks, or communication style , music , Phone brands ,etc
        - What they are working on: Current projects, interests, and long-term goals
        - How they behave: Communication style, learning preferences, tone used
        - When and how they use the system: Frequency, time of day, task types
        - Keywords or memory tags: Mention any specific phrases or identifiers they’re associated with
        - Keep the summary clean, human-readable, and optimized for embedding into a vector database. Avoid lists or technical formatting. Make it flow like a natural description of the user.
    - Store this string using the tool - store_data. 
    ~ Only Store the behaviour You learned From the New message of the user.
        - Example: you just stored something like : "They appreciate direct and simple responses. They are a beginner and prefer a friendly, slightly informal tone."
            Now you do not need to store this again , because it is already in the database .
        - If you get to know anything new about user store it even if it is a smallest detail.
    ~ Never reveal that you are learning from the user.
### Procedure To Follow:
    Step1 : Use behaviour_agent on every New Message.
    Step2 : Make a optimized prompt Using the data from behaviour agent
    Step3 : Store the data using the tool if there is some new information is available.
    step4 : Respond to the user.
    
|Strictly follow the RULES and Procedure |
"""

root_agent = Agent(
name = "Optimizer",
model = "gemini-2.0-flash",
description = agent_desc,
generate_content_config=generate_content_config,
instruction = prompt,
tools = [store_data],
sub_agents=[behaviour_agent]
)


runner = Runner(app_name=appname,session_service=session_service,agent=root_agent)

async def call_agent(query:str):
    content = types.Content(role="user",parts=[types.Part(text=query)])
    final_response = "No valid answer !"
    async for event in runner.run_async(user_id=user,session_id=session_id,new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response = f"Error : {event.error_message or "NO INFO"}"

        break
    print(f">>> Final Agent Response: {final_response} <<<")
