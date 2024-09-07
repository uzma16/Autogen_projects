from flask import Flask, request, jsonify
from autogen import AssistantAgent, GroupChat, GroupChatManager

app = Flask(__name__)

# Shared LLM configuration
llm_config = {
    "seed": 43,
    "config_list": [
        {'model': 'gpt-3.5-turbo-16k', 'api_key': '##'}
    ],
    "temperature": 0.5,
}

# Define the agents
agents = [
    AssistantAgent(name="Coder", system_message="I develop software based on detailed specifications.", llm_config=llm_config),
    AssistantAgent(name="Debugger", system_message="I analyze code and provide debugging solutions.", llm_config=llm_config),
    AssistantAgent(name="Executor", system_message="I execute the code written by the coder and try the execute the test cases written by tester.", llm_config=llm_config),
    AssistantAgent(name="Tester", system_message="I generate test cases to validate the functionality of the code written by the coder.", llm_config=llm_config),
    AssistantAgent(name="Planner", system_message="I plan and organize the project's tasks and workflows.", llm_config=llm_config),
    AssistantAgent(name="Critic", system_message="I review all outputs and provide critical feedback to improve quality.", llm_config=llm_config)
]

# Setup the group chat
group_chat = GroupChat(agents=agents, messages=[], max_round=50)
group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# @app.route('/start-project/', methods=['POST'])
def start_project(specifications):
    # data = request.get_json()
    # specifications = data.get('specifications')
    specifications = specifications
    if not specifications:
        return jsonify({"error": "Project specifications are required"}), 400

    # Simulate the project planning phase
    plan = agents[4].initiate_chat(group_chat_manager, message=specifications)

    # Simulate the project coding phase
    code = agents[0].initiate_chat(group_chat_manager, message=plan.chat_history[-1]['content'])

    # Simulate the project testing phase
    test_cases = agents[3].initiate_chat(group_chat_manager, message=f"Create test cases for this code: \n{code.chat_history[-1]['content']}")
    test_results = agents[3].initiate_chat(group_chat_manager, message=f"Run test cases on the following code: \n{code.chat_history[-1]['content']}")

    # Simulate the project debugging phase
    debugged_code = agents[1].initiate_chat(group_chat_manager, message=code.chat_history[-1]['content'])

    # Simulate the project execution phase
    results = agents[2].initiate_chat(group_chat_manager, message=debugged_code.chat_history[-1]['content'])

    # Simulate the project review phase
    feedback = agents[5].initiate_chat(group_chat_manager, message=results.chat_history[-1]['content'])

    return jsonify({
        "Plan": plan.chat_history[-1]['content'],
        "Code": debugged_code.chat_history[-1]['content'],
        "Test Cases": test_cases.chat_history[-1]['content'],
        "Test Results": test_results.chat_history[-1]['content'],
        "Results": results.chat_history[-1]['content'],
        "Feedback": feedback.chat_history[-1]['content']
    })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)


project_specifications = "Develop a simple web application using Flask."
project_outcomes = start_project(project_specifications)
print("++++++++++++++++++++++++++++++++++++++",project_outcomes)