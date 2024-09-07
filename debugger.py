# from autogen import ConversableAgent

# # Initialize the Tester agent
# coder = ConversableAgent(
#     "tester",
#     system_message="You are responsible for testing code and identifying bugs.",
#     llm_config={"config_list": [{"model": "gpt-4", "api_key": "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"}]},
#     human_input_mode="NEVER"
# )

# # Initialize the Coder agent
# tester = ConversableAgent(
#     "coder",
#     system_message="You are responsible for fixing bugs identified by the tester.",
#     llm_config={"config_list": [{"model": "gpt-4", "api_key": "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"}]},
#     human_input_mode="NEVER"
# )

# def automated_testing_and_debugging_cycle(initial_code):
#     code = initial_code
#     bugs_found = True

#     while bugs_found:
#         # Tester tests the code
#         test_result = tester.initiate_chat(
#             recipient=coder,
#             message=f"Test this code: \n{code}",
#             max_turns=1
#         ).chat_history[-1]['content']

#         if "no bugs found" in test_result.lower():
#             bugs_found = False
#         else:
#             # Coder fixes the code based on the test results
#             code = coder.initiate_chat(
#                 recipient=tester,
#                 message=f"Fix the bugs in this code based on the following feedback: \n{test_result}",
#                 max_turns=1
#             ).chat_history[-1]['content']

#     return code, "All bugs fixed and code is fully functional."

# # Example of how the system might be started with some initial code
# initial_code_snippet = """
# def check_prime(num):
#     for i in range(2, num):
#         if num % i == 0:
#             return False
#     return True
# """

# final_code, status = automated_testing_and_debugging_cycle(initial_code_snippet)
# print("Final Code:\n", final_code)
# print("Status:\n", status)


from autogen import AssistantAgent, GroupChat, GroupChatManager

# Shared LLM configuration
llm_config = {
    "seed": 43,
    "config_list": [
        {'model': 'gpt-3.5-turbo-16k', 'api_key': '##'}
    ],
    "temperature": 0.5,
}

# Define the agents
coder = AssistantAgent(
    name="Coder",
    system_message="I develop software based on detailed specifications.",
    llm_config=llm_config
)

debugger = AssistantAgent(
    name="Debugger",
    system_message="I analyze code and provide debugging solutions.",
    llm_config=llm_config
)

executor = AssistantAgent(
    name="Executor",
    system_message='''Executor. Execute the code written by the coder and try the execute the test cases written by tester.''',
    # system_message='''Executor. Execute the test cases written by tester.''',
    code_execution_config={"last_n_messages": 3, "work_dir": "feedback", "use_docker":False}
)

# Assuming llm_config has been defined as shared configuration for language model capabilities
# executor = AssistantAgent(
#     name="Executor",
#     system_message='''
#     Executor. I execute provided code within a controlled environment and return the results. 
#     My execution environment is configured to handle Python scripts safely, ensuring that operations 
#     are contained and do not affect the underlying system or data inappropriately.
#     ''',
#     code_execution_config={
#         "last_n_messages": 3,
#         "work_dir": "executor_work_dir",  # Temporary directory for execution
#         "use_docker": False  # Use Docker for an isolated execution environment
#     },
#     llm_config=llm_config
# )

tester = AssistantAgent(
    name="Tester",
    system_message="I generate test cases to validate the functionality of the code written by the coder.",
    llm_config=llm_config
)


planner = AssistantAgent(
    name="Planner",
    system_message="I plan and organize the project's tasks and workflows.",
    llm_config=llm_config
)

critic = AssistantAgent(
    name="Critic",
    system_message="I review all outputs and provide critical feedback to improve quality.",
    llm_config=llm_config
)

# Setup the group chat
# Adding the Tester to the existing group chat setup along with the other agents
agents = [coder, debugger, executor, planner, critic, tester]
group_chat = GroupChat(agents=agents, messages=[], max_round=10)
group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)


def start_project(specifications):
    # Planning phase
    plan = planner.initiate_chat(group_chat_manager, message=specifications)

    # Coding phase
    code = coder.initiate_chat(group_chat_manager, message=plan.chat_history[-1]['content'])

    # Testing phase
    test_cases = tester.initiate_chat(group_chat_manager, message=f"Create test cases for this code: \n{code.chat_history[-1]['content']}")
    test_results = tester.initiate_chat(group_chat_manager, message=f"Run test cases on the following code: \n{code.chat_history[-1]['content']}")

    # Debugging phase
    debugged_code = debugger.initiate_chat(group_chat_manager, message=code.chat_history[-1]['content'])

    # Execution phase
    results = executor.initiate_chat(group_chat_manager, message=debugged_code.chat_history[-1]['content'])

    # Review phase
    feedback = critic.initiate_chat(group_chat_manager, message=results.chat_history[-1]['content'])

    return {
        "Plan": plan.chat_history[-1]['content'],
        "Code": debugged_code.chat_history[-1]['content'],
        "Test Cases": test_cases.chat_history[-1]['content'],
        "Test Results": test_results.chat_history[-1]['content'],
        "Results": results.chat_history[-1]['content'],
        "Feedback": feedback.chat_history[-1]['content']
    }


# Example usage
project_specifications = "Develop a python program which can identify whether the given string is palindrome or not."
# project_specifications = "Develop a simple web application using Flask."
# project_specifications = "Develop a basic web application to manage a to-do list. The application should be built using Flask and SQLite3 for the backend."
# project_specifications = "I would like to build a simple website that collects feedback from consumers via forms. We can just use a flask application that creates an html website with forms and has a single question if they liked their customer experience and then keepsd that answer. I need a thank you html page called admin that gives a nice table layout of all of the records from the database. Just use sqlite3 as the database, keep it simple. Add bootstrap for the css styling. Write the html code as well. Write the integration of python with sqlite3 as well.."
project_outcomes = start_project(project_specifications)
print("++++++++++++++++++++++++++++++++++++++",project_outcomes)
