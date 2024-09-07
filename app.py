# import autogen 

# config_list=[
#     {
#         'model': 'gpt-3.5-turbo-16k',
#         'api_key':'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'
#     }
# ]

# llm_config={
#     "request_timeout":600,
#     "seed":42,
#     "config_list":config_list,
#     "temperature":0
# }

# assisstant=autogen.AssistantAgent(
#     name="assistant",
#     llm_config=llm_config
# )

import autogen
from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "gpt-4", "api_key": "xxx"}
assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Plot a chart of NVDA and TESLA stock price change YTD.",
)