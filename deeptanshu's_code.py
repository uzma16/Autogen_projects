from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': '##'
    }
]

llm_config = {
    # "request_timeout" : 600,
    "seed": 43,
    "config_list": config_list,
    "temperature": 0,
}

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config={"use_docker":False},
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message='''Engineer. You follow an approved plan. You write Python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if its not inteded to be executed by the executor. Don't include multiple code blocks in one response. Do not ask others to copy paste the result. Check the execution result returned by the executor. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. Whenever critic suggests you any code, you have to integrate it, it will never be optional.'''
)

planner = AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on the feedback from the admin and critic, until admin approval. The plan may involve an engineer who can write code and an executor and critic who doesn't write code. Explain the plan first. Be clear which step is performed by an engineer, executor and critic.''',
    llm_config=llm_config
)

executor = AssistantAgent(
    name="Executor",
    system_message='''Executor. Execute the code written by the engineer and report the result.''',
    code_execution_config={"last_n_messages": 3, "work_dir": "feedback", "use_docker":False}
)

critic = AssistantAgent(
    name="Critic",
    system_message='''Critic. Double check plan, claims, code from other agents and provide feedback. If I have any suggestions in the code, I will pass them to the engineer and engineer needs to integrate my feedback.''',
    llm_config=llm_config
)

grouchat = GroupChat(agents=[user_proxy, engineer, executor, critic], messages=[], max_round=50)
manager = GroupChatManager(groupchat=grouchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message='''I would like to build a simple website that collects feedback from consumers via forms. We can just use a flask application that creates an html website with forms and has a single question if they liked their customer experience and then keepsd that answer. I need a thank you html page called admin that gives a nice table layout of all of the records from the database. Just use sqlite3 as the database, keep it simple. Add bootstrap for the css styling. Write the html code as well. Write the integration of python with sqlite3 as well.''')