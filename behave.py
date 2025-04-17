from PromptOptimizer.database import fetch_relevant_data
from google.adk.agents import Agent
from google.genai import types

generate_content_config = types.GenerateContentConfig(
    temperature=0.3,         # Controls randomness; lower values make output more deterministic
    max_output_tokens=1500,   # Increases the maximum length of the response
    top_p=0.95               # Controls diversity via nucleus sampling
)

prompt ="""
On the basis of user input, think and ask about the behaviour or past data of user from the TOOL : fetch_relevant_data, for optimizing the prompt.
~ Return the behaviour of user to the parent agent [root_agent -> Name = Optimizer] .
~ Do not ask the user - use the tool and return the behaviour to Parent agent only.
~ Try five to six questions.
~ Ask questions relevant to User's Message.
Notes:
    # It may return "Database Do not Exist" if database is empty > it will happen only if it is executed for the first time.
    # Do not show anything to the user !
    # You are retrieving the data from a Vector data base so build up your questions accordingly for best results.
"""

behaviour_agent = Agent(
    name = "Behaviour_finder",
    model = "gemini-2.0-flash",
    description = (
        "Agent to find the behaviour and past data the of user for optimizing ,personalizing and answering the prompt."
    ),
    instruction = prompt,
    tools = [fetch_relevant_data],
    generate_content_config=generate_content_config
    )



