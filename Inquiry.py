from autogen import Agent, AssistantAgent, UserProxyAgent

config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': '#####'
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

def print_messages(recipient, messages, sender, config): 
    if "callback" in config and  config["callback"] is not None:
        callback = config["callback"]
        callback(sender, recipient, messages[-1])
    
    with open('result.txt', 'a') as file:
        file.write(f"{messages[len(messages)-1]} \n")
    return False, None  # required to ensure the agent communication flow continues

# UserProxyAgent to simulate the user input from terminal
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="You are now interacting with the interview system.",
    code_execution_config={"use_docker":False},
)

# InterviewerAgent to ask questions and process responses
interviewer = AssistantAgent(
    name="Interviewer",
    system_message= '''My first question would be 'Tell me the problem that you want to solve' then going forward
    I will ask another question related to user's problem only, because my work is to collect all the info about user problem by asking question. So that 
    when my planner team works to solve the problem or plan the solution it will have all the information given by user.I will also ask about the timeline of completion of problem''',
    llm_config=llm_config,
)

user_proxy.register_reply(
    [Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

interviewer.register_reply(
    [Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 

user_proxy.initiate_chat(
    interviewer,
    message="Please proceed with my interview",
)


