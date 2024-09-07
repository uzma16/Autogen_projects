from flask import Flask, request, jsonify
from autogen import ConversableAgent

app = Flask(__name__)

# Define the Coder agent
tester = ConversableAgent(
    "coder",
    system_message="You are a coder responsible for writing test cases for the code that is developed by coder.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "#####"}]},
    human_input_mode="NEVER"
)

# Define the Tester agent
coder = ConversableAgent(
    "tester",
    system_message="You are a tester responsible for evaluating the functionality and correctness of the code written by the coder.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "###"}]},
    human_input_mode="NEVER"
)

# Define the Executor agent
executor = ConversableAgent(
    "executor",
    system_message="You are an executor responsible for executing the code and verifying its functionality.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "######"}]},
    human_input_mode="NEVER"
)

@app.route('/simulate-development-cycle/', methods=['POST'])
def simulate_development_cycle():
    data = request.get_json()
    requirements_description = data.get('requirements')
    if not requirements_description:
        return jsonify({"error": "Requirements description is required"}), 400

    code_result = ""
    test_result = ""
    exec_result = ""
    max_attempts = 1 # Limit the number of attempts to prevent infinite loops
    attempts = 0

    while attempts < max_attempts:
        # The coder generates code based on the given requirements
        code_response = coder.initiate_chat(
            recipient=tester, # Tester will evaluate the code
            message=f"Please write code to: {requirements_description}",
            max_turns=1
        )

        if code_response.chat_history:
            last_message = code_response.chat_history[-1] # Assuming the last message is the one you need
            code_result = last_message['content'] if 'content' in last_message else "No code generated"
        else:
            code_result = "No code generated"

        # The tester tests the generated code
        test_response = tester.initiate_chat(
            recipient=coder, # Coder will receive feedback if any corrections are needed
            message=f"Test this code for functionality and correctness: '{code_result}'",
            max_turns=1
        )

        if test_response.chat_history:
            last_message = test_response.chat_history[-1] # Assuming the last message is the one you need
            test_result = last_message["content"] if 'content' in last_message else "No test result"
        else:
            test_result = "No test result"

        # The executor executes the code and provides feedback
        exec_response = executor.initiate_chat(
            recipient=coder, # Coder will receive feedback if any corrections are needed
            message=f"Execute this code and verify its functionality: '{code_result}'",
            max_turns=1
        )

        if exec_response.chat_history:
            last_message = exec_response.chat_history[-1] # Assuming the last message is the one you need
            exec_result = last_message["content"] if 'content' in last_message else "No execution result"
        else:
            exec_result = "No execution result"

        # Check if the code passed all tests and execution
        if "all tests passed" in test_result.lower() and "execution successful" in exec_result.lower():
            break # Exit loop if tests are passed and execution is successful
        attempts += 1

    return jsonify({
        "Code Generated": code_result,
        "Test Results": test_result,
        "Execution Results": exec_result,
        "Attempts": attempts
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
