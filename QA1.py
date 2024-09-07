from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': '###'
    }
]

llm_config = {
    # "request_timeout" : 600,
    "seed": 43,
    "config_list": config_list,
    "temperature": 0,
}

user_interface_agent = AssistantAgent(
    name="User_Interface",
    system_message="Hello! Please describe the project you're planning to build.",
    llm_config=llm_config
)

inquiry_agent = AssistantAgent(
    name="Inquiry",
    system_message='''Analyzing your project description to ask further questions. Our team is dedicated to delivering a solution that
      precisely addresses the user's needs. To ensure seamless alignment between user requirements and our planning process, you will 
      formulate a series of targeted questions. These questions are designed to unearth crucial insights, allowing us to bridge any gaps
        between user expectations and our planning strategy''',
    llm_config=llm_config,
    # human_input_mode="ALWAYS"
)

response_processing_agent = AssistantAgent(
    name="Response_Processor",
    system_message="Processing your answers to refine the project requirements...",
    llm_config=llm_config
)

planning_and_design_agent = AssistantAgent(
    name="Planner_Designer",
    system_message="Generating a detailed plan or blueprint and design for your project, which will lead to solve the problem",
    llm_config=llm_config
)

quality_assurance_agent = AssistantAgent(
    name="Quality_Assurance",
    system_message="Reviewing the questions and the final project plan for quality assurance...",
    llm_config=llm_config
)

group_chat = GroupChat(
    agents=[
        user_interface_agent,
        inquiry_agent,
        # response_processing_agent,
        planning_and_design_agent,
        quality_assurance_agent
    ],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
initial_problem_statement = input("What would you like to build? Describe your project: ")
user_interface_agent.initiate_chat(manager, message=initial_problem_statement)
