from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.memory import RedisMemory
import redis
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Redis for memory persistence (ensure Redis is running)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize memory storage with Redis
redis_memory = RedisMemory(redis_client, prefix="langchain-agent")

# Initialize OpenAI LLM (you can replace it with other models if needed)
llm = OpenAI(model="gpt-4", temperature=0.7)

# Example of creating a tool for the agent to use, in this case, checking GPU usage
def gpu_status_tool(query):
    # Example: In a production setup, integrate with your GPU monitoring system
    logger.info(f"Received query for GPU status: {query}")
    gpu_data = {"A100": 2, "T4": 10, "RTX 4090": 0}  # Example data (can be dynamic)
    return gpu_data

# Define the tool that the agent will use
gpu_status_tool = Tool(
    name="GPUStatus",
    func=gpu_status_tool,
    description="Use this tool to check the available GPUs in the system."
)

# Define other necessary tools (for example, billing tool, task submission, etc.)

def billing_check_tool(query):
    logger.info(f"Received billing check request: {query}")
    # Example: Check if the user has enough balance for the requested job
    balance = 100  # Example balance (this can be dynamic based on user data)
    if balance > 50:
        return "Sufficient balance for the task."
    else:
        return "Insufficient balance."

# Define the billing tool
billing_check_tool = Tool(
    name="BillingCheck",
    func=billing_check_tool,
    description="Use this tool to check the user's balance and billing status."
)

# Define a prompt for the agent to use (you can customize this as needed)
prompt = PromptTemplate(
    input_variables=["query"],
    template="The user has asked: {query}. Please respond with relevant information."
)

# Create an LLM chain
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Initialize the agent with tools and memory
tools = [gpu_status_tool, billing_check_tool]
agent = initialize_agent(
    tools, llm_chain, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, memory=redis_memory
)

# Example function to handle a task submission from the sandbox or another service
def submit_task_to_agent(user_query):
    logger.info(f"Submitting task to agent: {user_query}")
    response = agent.run(user_query)
    logger.info(f"Agent response: {response}")
    return response

# Sample task submission (You can call this function when a task is submitted in the sandbox or dashboard)
if __name__ == "__main__":
    # Example user query for testing
    user_query = "What is the current status of available GPUs?"
    agent_response = submit_task_to_agent(user_query)
    logger.info(f"Agent Response: {agent_response}")
