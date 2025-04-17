import redis
import json
from langchain.memory import RedisMemory
from langchain.agents import AgentExecutor
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Redis client setup for memory persistence
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class AgentMemory:
    """
    This class handles the agent's memory using Redis to persist interactions.
    """
    
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.memory = RedisMemory(redis_client, prefix=f"{agent_name}:memory")
        self.history_key = f"{agent_name}:history"
        self.init_agent_memory()

    def init_agent_memory(self):
        """
        Initialize the memory for the agent. If no memory exists, create one.
        """
        if not self.memory.retrieve_memory():
            self.memory.save_memory({"history": []})
            print(f"Initialized memory for agent: {self.agent_name}")
        else:
            print(f"Memory exists for agent: {self.agent_name}")
    
    def add_to_memory(self, data):
        """
        Add new data to the agent's memory.
        """
        history = self.memory.retrieve_memory().get('history', [])
        history.append(data)
        self.memory.save_memory({"history": history})
        print(f"Added new data to memory: {data}")
    
    def get_memory(self):
        """
        Retrieve the agent's memory.
        """
        memory = self.memory.retrieve_memory()
        return memory.get('history', [])
    
    def clear_memory(self):
        """
        Clear the agent's memory.
        """
        self.memory.save_memory({"history": []})
        print(f"Memory cleared for agent: {self.agent_name}")
        
    def update_memory(self, new_data):
        """
        Update agent's memory with new data.
        """
        self.add_to_memory(new_data)
        print(f"Updated memory with new data: {new_data}")

# --- Example Memory Functions ---

def fetch_agent_memory(agent_memory):
    """
    Example function to fetch and display the memory of a specific agent.
    """
    memory_data = agent_memory.get_memory()
    if memory_data:
        print("Agent Memory:")
        for entry in memory_data:
            print(f"- {entry}")
    else:
        print("No memory found for this agent.")

def process_agent_task_with_memory(agent_name, task, agent_memory):
    """
    Example function to process a task with the agent's memory context.
    This simulates an agent's task processing and memory updates.
    """
    # Creating a simulated response
    response = f"Processing task: {task}. Using memory context..."
    print(f"Response: {response}")

    # Add task to memory
    agent_memory.add_to_memory(task)
    print(f"Task '{task}' added to memory.")
    
    return response

# --- Example Agent Setup ---

def setup_agent_with_memory(agent_name):
    """
    Set up an agent with memory capabilities, allowing for task processing with memory persistence.
    """
    agent_memory = AgentMemory(agent_name)
    
    task = "What is the current status of the GPU?"
    response = process_agent_task_with_memory(agent_name, task, agent_memory)
    
    fetch_agent_memory(agent_memory)
    return response

if __name__ == "__main__":
    agent_name = "TestAgent"
    setup_agent_with_memory(agent_name)
