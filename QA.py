# import os
# from autogen import ConversableAgent

# # Initialize the conversational agent
# project_assistant = ConversableAgent(
#     "project_assistant",
#     system_message='''Hello, I'm here to ask questions within your problem statement. Please tell me about the problem you're trying 
#                         to solve. I will ask set of questions related to that which will help engineers to design your solution & will help 
#                         in design the workflow technically in a effective manner''',
#     llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": "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"}]},
#     human_input_mode="NEVER"
# )

# def gather_requirements(initial_statement):
#     questions_to_ask = []
#     current_message = initial_statement
#     result = project_assistant.initiate_chat(message=current_message, recipient=project_assistant, max_turns=1)
#     return result

# # initial_user_statement = "I want to build a machine learning model to predict stock prices."
# initial_user_statement = input("What you want to build?")
# questions = gather_requirements(initial_user_statement)
# print("*******************************************************************************************")
# print("Questions to ask the user:")
# print(questions.summary)





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

requirement = AssistantAgent(
    name="Requirement_Ask",
    llm_config=llm_config,
    system_message='''Requirement_Ask. Our team is dedicated to delivering a solution that precisely addresses the user's needs. To ensure seamless alignment between user requirements and our planning process, you will formulate a series of targeted questions. These questions are designed to unearth crucial insights, allowing us to bridge any gaps between user expectations and our planning strategy.'''
#     system_message='''Requirement_Ask. You will provide a set of questions related to the problem statement which will help planner to plan better. Make sure our team will solve the given user problem & for that
#       you have to ask the questions until the gap of user requirement & planner is filled.'''
)


planner = AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on the feedback from the admin and critic, until admin approval. The plan may involve an engineer who can write code and an executor and critic who doesn't write code. Explain the plan first. Be clear which step is performed by an engineer, executor and critic.''',
    llm_config=llm_config
)


critic = AssistantAgent(
    name="Critic",
    system_message='''Critic. Provide feedback on the checking questions provided by the requirement agent.''',
    llm_config=llm_config
)

grouchat = GroupChat(agents=[user_proxy,requirement,critic], messages=[], max_round=50)
manager = GroupChatManager(groupchat=grouchat, llm_config=llm_config)

problem=input("Waht you want to biuld?")
# user_proxy.initiate_chat(manager, message='''I would like to build a simple website that collects feedback from consumers via forms. We can just use a flask application that creates an html website with forms and has a single question if they liked their customer experience and then keepsd that answer. I need a thank you html page called admin that gives a nice table layout of all of the records from the database. Just use sqlite3 as the database, keep it simple. Add bootstrap for the css styling. Write the html code as well. Write the integration of python with sqlite3 as well.''')
user_proxy.initiate_chat(manager,message=problem)