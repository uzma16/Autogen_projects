import autogen
from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "gpt-4", "api_key": "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"}
assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Write code for making a simple get api in django.",
)