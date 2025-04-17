import logging
import redis
from langchain.memory import RedisMemory
from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from autogen import Agent, TaskManager

# Setting up logging for better traceability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis Setup for Memory Persistence
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
redis_memory = RedisMemory(redis_client, prefix="autogen-agent")

# Initialize LLM (using OpenAI GPT-4 for the language model)
llm = OpenAI(model="gpt-4", temperature=0.7)

# --- Utility functions for managing agents ---

def create_tool(name, func, description):
    """
    Create a new tool with the given name, function, and description.
    """
    tool = Tool(name=name, func=func, description=description)
    logger.info(f"Tool {name} created successfully.")
    return tool

def initialize_agent_with_tools(tools):
    """
    Initialize an agent with a list of tools.
    """
    try:
        agent = initialize_agent(
            tools,
            llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=redis_memory
        )
        logger.info("Agent initialized with tools successfully.")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise

def submit_task_to_agent(agent, task):
    """
    Submit a task to the given agent and get the response.
    """
    try:
        response = agent.run(task)
        logger.info(f"Task submitted successfully. Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to submit task to agent: {e}")
        return None

def create_autogen_agent(name, tools):
    """
    Create an AutoGen agent that can process tasks with multiple tools.
    """
    agent = AutoGenAgent(name=name, tools=tools)
    logger.info(f"AutoGen agent {name} created successfully.")
    return agent

def process_agent_task(agent, task):
    """
    Process a task with the provided agent.
    """
    try:
        response = agent.process_task(task)
        logger.info(f"Task processed by agent: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to process task: {e}")
        return None

def get_agent_memory(agent):
    """
    Get the memory of the agent to review its context and history.
    """
    try:
        memory_data = agent.memory.retrieve_memory()
        logger.info(f"Memory retrieved for agent: {memory_data}")
        return memory_data
    except Exception as e:
        logger.error(f"Failed to retrieve memory: {e}")
        return None

# --- Example tool functions ---

def gpu_status_tool(query):
    """
    Simulate a tool that checks GPU status.
    """
    logger.info(f"Querying GPU status for: {query}")
    gpu_data = {"A100": 2, "T4": 10, "RTX 4090": 0}  # Simulated data
    return gpu_data

def billing_check_tool(query):
    """
    Simulate a tool that checks the user's billing balance.
    """
    logger.info(f"Checking billing status for query: {query}")
    balance = 100  # Mock balance
    if balance > 50:
        return "Sufficient balance for the task."
    else:
        return "Insufficient balance."

# --- Example of task submission ---

def submit_task_example():
    """
    A simple function to demonstrate task submission using an agent.
    """
    # Example task to check GPU status
    task = "What is the current GPU status?"
    
    # Create tools
    gpu_tool = create_tool("GPUStatus", gpu_status_tool, "Check GPU availability and status.")
    billing_tool = create_tool("BillingCheck", billing_check_tool, "Check user billing balance.")
    
    # Initialize agent
    tools = [gpu_tool, billing_tool]
    agent = initialize_agent_with_tools(tools)
    
    # Submit task to the agent
    response = submit_task_to_agent(agent, task)
    if response:
        logger.info(f"Response from agent: {response}")
    else:
        logger.error("No response received from agent.")

if __name__ == "__main__":
    submit_task_example()
