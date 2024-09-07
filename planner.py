from pymongo import MongoClient
import json

from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from the .env file.

from crewai_tools import BaseTool

# Replace the following with your actual MongoDB connection details
# mongo_uri = "mongodb+srv://consultingleera:Ane0JM3Rx928APks@cluster0.zwxqtpt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# database_name = "sapience"
# collection_name = "plan"
mongo_uri = 'mongodb://localhost:27017/'
database_name = 'Spark_AI'
collection_name = 'planner'
# Establishing the connection to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]
from pymongo import MongoClient
import json

from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from the .env file.

from crewai_tools import BaseTool



def store_task_output_in_mongodb(task_output):
    """
    Store the output of the planning task into a MongoDB collection.

    Args:
    task_output (TaskOutput): Output object of the planning task.
    """
    # Assuming task_output.data is the actual data you want to store and it's in JSON format
    try:
        # If the output is already a dictionary
        if isinstance(task_output, dict):
            task_data = task_output
        else:
            # Convert the JSON string to a Python dictionary
            task_data = json.loads(task_output)
        
        # Insert the data into the MongoDB collection
        collection.insert_many(task_data if isinstance(task_data, list) else [task_data])

        print("Data successfully inserted into MongoDB.")
    except Exception as e:
        print(f"An error occurred: {e}")


# class PlanningTool(BaseTool):
#     name: str = "Planner"
#     description: str = "Tool to decompose objectives into a series of scheduled tasks."

#     def _run(self, objective: str, time_frame: int) -> list:
#         # Placeholder for task planning logic
#         # This should return a list of tasks with estimated completion times
#         return self.plan_tasks(objective, time_frame)

#     def plan_tasks(self, objective, time_frame):
#         # Example simplistic breakdown for demonstration purposes
#         number_of_tasks = 5  # Divide the objective into 5 tasks
#         task_duration = time_frame // number_of_tasks
#         tasks = []
#         for i in range(number_of_tasks):
#             task_description = f"Task {i+1} of {number_of_tasks}: Part of {objective}"
#             tasks.append({'description': task_description, 'duration': task_duration})
#         return tasks

from crewai import Agent

planner_agent = Agent(
    role='Planner',
    goal='Generate a detailed plan for given objectives within a specified timeframe.',
    # tools=[PlanningTool()],
    backstory="Expert in breaking down complex objectives into manageable tasks.",
    verbose=True,
    memory=True  # Enable memory if you need to keep track of previous planning sessions
)

from crewai import Task

planning_task = Task(
    description="Create a detailed plan for creating a personal brand on medium as an ai influencer in 90 days.",
    expected_output="""A set of scheduled tasks in a json format. The output should not have any text whatsoever, it should only be a json object.
    For example, if today's date is 19th April, 2024, the expected output shall be a json of the kind:
    [
        {
            startDate: 27th April 2024,
            endDate: 2nd May 2024,
            task: 'Organise the content to write on your blogs'
        },
        {
            startDate: 3rd May 2024,
            endDate: 14th May 2024,
            task: 'Spend time in following the accounts similar to you.'
        }
    ]
    """,
    # tools=[PlanningTool()],
    agent=planner_agent,
    # callback=store_task_output_in_mongodb
)


# Initialize Large Language Model (LLM)
from langchain_openai import ChatOpenAI
openai = ChatOpenAI(model_name="gpt-3.5-turbo")

from crewai import Crew, Process

planning_crew = Crew(
    agents=[planner_agent],
    tasks=[planning_task],
    process=Process.sequential,
    verbose=True
)

# # Assume user inputs are collected elsewhere and passed here
# user_objective = "Create a personal brand on medium as an ai influencer."
# user_time_frame = 90  # days

# Execute the crew
plan_result = planning_crew.kickoff()
if plan_result:
    store_task_output_in_mongodb(plan_result)
print(plan_result)
