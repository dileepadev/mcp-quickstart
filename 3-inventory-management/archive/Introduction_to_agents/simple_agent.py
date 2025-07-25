import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool, ToolSet
from tools import get_company_details


def setup_project_client():
    ENDPOINT = os.getenv("ENDPOINT")
    MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
    if not ENDPOINT:
        raise ValueError("ENDPOINT is not set in the .env file.")
    if not MODEL_DEPLOYMENT_NAME:
        raise ValueError("MODEL_DEPLOYMENT_NAME is not set in the .env file.")
    try:
        project_client = AIProjectClient(
            endpoint=ENDPOINT,
            credential=DefaultAzureCredential(),
        )
    except Exception as e:
        print(f"❌ Error initializing AIProjectClient: {e}")
        raise
    return project_client, MODEL_DEPLOYMENT_NAME


def setup_toolset():
    user_functions = {
        get_company_details
    }
    functions = FunctionTool(user_functions)
    toolset = ToolSet()
    toolset.add(functions)
    print(f"🔵 User toolset defined: {toolset}")
    return toolset


def create_agent(project_client, model_deployment_name):
    try:
        toolset = setup_toolset()
        project_client.agents.enable_auto_function_calls(toolset)
        agent = project_client.agents.create_agent(
            model=model_deployment_name,
            name="Agent 001",
            instructions="You are a helpful AI Agent that provide service to the users about the company.",
            description="This is a test agent",
            toolset=toolset,
        )
        print(f"🔵 Agent created! ID: {agent.id}")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        raise
    return agent


def create_thread(project_client):
    try:
        thread = project_client.agents.threads.create()
        print(f"🔵 Thread created! ID: {thread.id}")
    except Exception as e:
        print(f"❌ Error creating thread: {e}")
        raise
    return thread


def get_agent(project_client, agent_id):
    try:
        toolset = setup_toolset()
        project_client.agents.enable_auto_function_calls(toolset)
        agent = project_client.agents.get_agent(agent_id)
        if not agent or 'id' not in agent:
            print("❌ No agent found.")
            return None
        print(f"🔵 Get Agent: {agent}")
        print(f"🔵 Agent ID: {agent['id']}")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        raise
    return agent


def get_thread(project_client, thread_id):
    thread = project_client.agents.threads.get(thread_id)
    if not thread or 'id' not in thread:
        print("❌ No thread found.")
        return None
    print(f"🔵 Get Thread: {thread}")
    print(f"🔵 Thread ID: {thread['id']}")
    return thread


def _get_or_create_agent(project_client, model_deployment_name, agent_id):
    if not agent_id:
        print("🔍 AGENT_ID not found in .env. Creating a new...")
        try:
            print("🔵 Create a new agent!")
            agent = create_agent(project_client, model_deployment_name)
            print(f"✅ New Agent ID: {agent.id}")
            print("⚠️  Please update your .env file with AGENT_ID for future runs.")
            return agent
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            raise
    print("🔁 Using existing AGENT_ID from .env")
    try:
        print("🔵 Use already created agent!")
        agent = get_agent(project_client, agent_id)
        if agent is not None:
            print(f"✅ Already created Agent ID: {agent.id}")
        else:
            print("❌ Agent retrieval failed; agent is None.")
        return agent
    except Exception as e:
        print(f"❌ Error retrieving agent: {e}")
        raise


def _get_or_create_thread(project_client, thread_id):
    if not thread_id:
        print("🔍 THREAD_ID not found in .env. Creating a new...")
        try:
            print("🔵 Create a new thread!")
            thread = create_thread(project_client)
            print(f"✅ New Thread ID: {thread.id}")
            print("⚠️  Please update your .env file with THREAD_ID for future runs.")
            return thread
        except Exception as e:
            print(f"❌ Error creating agent/thread: {e}")
            raise
    print("🔁 Using existing THREAD_ID from .env")
    try:
        print("🔵 Use already created thread!")
        thread = get_thread(project_client, thread_id)
        if thread is not None:
            print(f"✅ Already created Thread ID: {thread.id}")
        else:
            print("❌ Agent retrieval failed; agent is None.")
        return thread
    except Exception as e:
        print(f"❌ Error retrieving thread: {e}")
        raise


def get_or_create_agent_and_thread(project_client, model_deployment_name):
    agent_id = os.getenv("AGENT_ID")
    thread_id = os.getenv("THREAD_ID")
    agent = _get_or_create_agent(
        project_client, model_deployment_name, agent_id)
    thread = _get_or_create_thread(project_client, thread_id)
    return agent, thread


def send_user_message(project_client, thread, user_message):
    try:
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )
        print(f"🔵 Message created! ID: {message['id']}")
    except Exception as e:
        print(f"❌ Error creating message: {e}")
        return False
    return True


def extract_tool_calls(run):
    ra = run.required_action
    submit_tool_outputs = None
    tool_calls = []
    if ra:
        if hasattr(ra, "submit_tool_outputs"):
            submit_tool_outputs = getattr(ra, "submit_tool_outputs")
        elif isinstance(ra, dict) and "submit_tool_outputs" in ra:
            submit_tool_outputs = ra["submit_tool_outputs"]
    if submit_tool_outputs:
        if hasattr(submit_tool_outputs, "tool_calls"):
            tool_calls = submit_tool_outputs.tool_calls
        elif isinstance(submit_tool_outputs, dict) and "tool_calls" in submit_tool_outputs:
            tool_calls = submit_tool_outputs["tool_calls"]

    return tool_calls, ra


def handle_tool_output(tool_call):
    tool_name = tool_call.name
    tool_id = tool_call.id

    if tool_name == "get_company_details":
        output = get_company_details()

    else:
        return None

    return {"tool_call_id": tool_id, "output": output}


def handle_tool_calls(run, project_client, thread):
    tool_outputs = []
    tool_calls, ra = extract_tool_calls(run)
    if not tool_calls:
        print(
            f"❌ Could not access tool_calls. run.required_action: {ra}")
    for tool_call in tool_calls:
        result = handle_tool_output(tool_call)
        if result:
            tool_outputs.append(result)
    if tool_outputs:
        project_client.agents.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)


def process_run(project_client, thread, agent):
    try:
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, agent_id=agent.id
        )
        print(f"🔵 Run created! ID: {run.id}")
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.runs.get(
                thread_id=thread.id, run_id=run.id)
            if run.status == "requires_action":
                handle_tool_calls(run, project_client, thread)
        print(f"✅ Run completed with status: {run.status}")
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        return False
    return True


def display_latest_assistant_message(project_client, thread):
    try:
        messages = project_client.agents.messages.list(thread_id=thread.id)
        recent_assistant_message = next(
            (m for m in messages if m["role"] == "assistant"), None)
        if recent_assistant_message:
            for content_item in recent_assistant_message["content"]:
                if content_item.get("type") == "text":
                    value = content_item["text"].get("value")
                    if value:
                        print(f"[🤖 AIAgent]:  {value}")
    except Exception as e:
        print(f"❌ Error listing messages: {e}")


def delete_agent(project_client, agent):
    """ Optionally, delete the agent after use.

    Args:
        project_client (_type_): Project client to be deleted
        agent (_type_): Agent to be deleted
    """
    project_client.agents.delete_agent(agent.id)
    print("✅ Agent Deleted")


def delete_thread(project_client, thread):
    """ Optionally, delete the thread after use.

    Args:
        project_client (_type_): Project client to be deleted
        thread (_type_): Thread to be deleted
    """
    project_client.agents.threads.delete(thread_id=thread.id)
    print("✅ Thread Deleted")


def run_cli():
    project_client, model_deployment_name = setup_project_client()
    agent, thread = get_or_create_agent_and_thread(
        project_client, model_deployment_name)
    print("\nType 'exit', 'q', or press Enter on an empty line to stop the conversation.\n")
    while True:
        user_message = input("✨ Enter your message for the agent!\n[🧑 You]: ")
        if user_message.strip().lower() in ("exit", "q", ""):
            print("👋 Conversation ended by user.")
            break
        if not send_user_message(project_client, thread, user_message):
            continue
        if not process_run(project_client, thread, agent):
            continue
        display_latest_assistant_message(project_client, thread)

    # Optionally, delete the agent after use
    # delete_agent(project_client, agent)
    # delete_thread(project_client, thread)


if __name__ == "__main__":
    run_cli()
