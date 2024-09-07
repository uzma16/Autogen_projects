from pymongo import MongoClient
from datetime import datetime
from autogen import Agent, AssistantAgent, UserProxyAgent
import uuid

# MongoDB Configuration
mongo_uri = "mongodb://localhost:27017"
mongo_db_name = "SparkAI"
mongo_collection_name = "Questions_Answer"

# Setup MongoDB client and collection
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client[mongo_db_name]
questions_answer_collection = mongo_db[mongo_collection_name]

# GPT-3.5 Turbo API Configuration
config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': '##'
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

# Function to save messages to MongoDB
def save_messages_to_mongo(recipient, messages, sender, config):
    message_content = {
        "timestamp": datetime.now(),
        "content": messages[-1],
        "role": recipient.name if sender.name == "User_proxy" else "interviewer"
    }
    
    session_id = config.get("session_id", None)
    if session_id is None:
        # Start new session
        session_id = str(uuid.uuid4())  # Generate new session ID
        interview_data = {
            "_id": session_id,
            "session_id": session_id,
            "start_time": datetime.now(),
            "messages": [message_content],
            "status": "In Progress"
        }
        questions_answer_collection.insert_one(interview_data)
        config["session_id"] = session_id  # Store session ID in the config
    else:
        # Update existing session
        questions_answer_collection.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": message_content},
                "$set": {"end_time": datetime.now()}
            }
        )
    
    # Continue the agent communication flow
    return False, None

# UserProxyAgent to simulate user input
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="You are now interacting with the interview system.",
    code_execution_config={"use_docker": False},
)

# InterviewerAgent to ask questions and process responses
interviewer = AssistantAgent(
    name="Interviewer",
    system_message= '''My first question would be 'Tell me the problem that you want to solve' then going forward
    I will ask another question related to user's problem only, because my work is to collect all the info about user problem by asking questions. So that 
    when my planner team works to solve the problem or plan the solution, it will have all the information given by the user. I will also ask about the timeline of completion of the problem''',
    llm_config=llm_config
)

# Register agents with the MongoDB saving function
user_proxy.register_reply([Agent, None], reply_func=save_messages_to_mongo, config={"session_id": None})
interviewer.register_reply([Agent, None], reply_func=save_messages_to_mongo, config={"session_id": None})

# Start the chat
user_proxy.initiate_chat(interviewer, message="Please proceed with my interview")
