from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

# Define a directory for storing executable code files
CODE_DIR = "./code_files"
if not os.path.exists(CODE_DIR):
    os.makedirs(CODE_DIR)

def execute_python_code(code: str) -> str:
    """Execute Python code from a string input and return the output or errors."""
    # Extract Python code portion
    code_lines = code.split("```")[1].split("\n")[1:-1]
    python_code = "\n".join(code_lines)

    file_name = os.path.join(CODE_DIR, f"{uuid.uuid4()}.py")
    with open(file_name, 'w') as code_file:
        code_file.write(python_code)

    try:
        result = subprocess.run(['python', file_name], capture_output=True, text=True, timeout=5)
        output = result.stdout
        error = result.stderr
        if error:
            return f"Execution Error: {error}" 
        return output
    except subprocess.TimeoutExpired:
        return "Execution Timed Out"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
    finally:
        os.remove(file_name)

# Define the Coder, Tester, and Executor agents
from autogen import ConversableAgent

coder = ConversableAgent(
    "coder",
    system_message="You are a coder responsible for writing code based on given specifications.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "##"}]},
    human_input_mode="NEVER"
)

tester = ConversableAgent(
    "tester",
    system_message="You are a tester responsible for writing the test cases for the code that is developed by coder.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "##"}]},
    human_input_mode="NEVER"
)

executor = ConversableAgent(
    "executor",
    system_message="You are an executor responsible for executing the code within a specified system environment and verifying its functionality.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.5, "api_key": "##"}]},
    human_input_mode="NEVER"
)

@app.route('/simulate-development-cycle/', methods=['POST'])
def simulate_development_cycle():
    data = request.get_json()
    requirements_description = data.get('requirements')
    if not requirements_description:
        return jsonify({"error": "Requirements description is required"}), 400

    # The coder generates code based on the given requirements
    code_result = coder.initiate_chat(
        recipient=tester,  # Tester will evaluate the code
        message=f"Please write code to: {requirements_description}",
        max_turns=1
    ).chat_history[-1]['content']  # Assuming chat_history and content are correctly structured

    # The tester tests the generated code
    test_result = tester.initiate_chat(
        recipient=coder,  # Coder will receive feedback if any corrections are needed
        message=f"Test this code for functionality and correctness: '{code_result}'",
        max_turns=1
    ).chat_history[-1]['content']  # Assuming chat_history and content are correctly structured

    # Execute the generated code and capture the results
    exec_result = execute_python_code(code_result)

    return jsonify({
        "Code Generated": code_result,
        "Test Results": test_result,
        "Execution Results": exec_result,
        "System Configuration": data.get('system_configuration', 'default configuration')
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
