from crewai import Agent

from pymongo import MongoClient
import os

# Set the OPENAI_API_KEY environment variable
os.environ['OPENAI_API_KEY'] = '#####'

# Now you can initialize your Crew and agents as described previously


def store_data_in_mongo(data):
    print("dataInsert++++++++++++++++++")
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Spark_AI']
        collection = db['planner']
        result = collection.insert_one(data)
        print(f"Data stored in MongoDB with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to store data: {e}")
    finally:
        client.close()


# Initialize Large Language Model (LLM)
# from langchain_openai import ChatOpenAI
# openai = ChatOpenAI(model_name="gpt-3.5-turbo")

# Creating the Planner Agent
planner_agent = Agent(
    role='Planner',
    goal='Create and manage efficient schedules and plans',
    backstory='An expert in time management and resource allocation.',
    verbose=True  # Enable detailed logging for debugging
)

from crewai import Task




# Use the safe function in the task definition
planning_task = Task(
    description='Develop a comprehensive project schedule based on the input constraints and milestones',
    agent=planner_agent,
    expected_output='A detailed Gantt chart representing the project timeline and resource allocation',
    # callback=safe_store_data_in_mongo  # Updated to use the safe wrapper function
)



from crewai import Crew, Process

# Assembling the crew with the planner agent and task
my_crew = Crew(
    agents=[planner_agent],  # List of agents in the crew
    tasks=[planning_task],   # List of tasks assigned to the crew
    process=Process.sequential,  # Process flow (tasks executed one after another)
    verbose=True  # Enable verbose output to trace execution details
)

# Kick off the crew's task execution
# result = my_crew.kickoff()
# print(result)
# Assuming `my_crew.kickoff()` is synchronous and returns the task outputs
result = my_crew.kickoff()
if result:
    store_data_in_mongo(result)
else:
    print("No output or missing 'raw_output' attribute.")
