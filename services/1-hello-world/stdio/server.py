import logging
import sys
from fastmcp import FastMCP  # Official MCP SDK import

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Instantiate the server
mcp = FastMCP("hello_server")
logging.info("✨ Server instance initialized!")


@mcp.resource("hello://world")
def hello_world_resource() -> str:
    """
    hello_world_resource()

    MCP Resource:
    URI: hello://world

    Returns:
        A greeting string "Hello, World!" when the resource is requested.
    """
    logging.info("🌍 Resource accessed: hello://world")
    return "Hello, World!"


@mcp.tool()
def display_hello_world() -> dict:
    """
    display_hello_world()

    MCP Tool:
    Returns a JSON-like dict containing a greeting message.

    Returns:
        dict: {"result": "Hello, World!"}
    """
    logging.info("👋 Tool called: display_hello_world()")
    return {"result": "Hello, World!"}


@mcp.prompt()
def prompt_hello_world() -> str:
    """
    prompt_hello_world()

    MCP Prompt:
    Generates a user-facing prompt message.

    Returns:
        str: A friendly greeting prompt string.
    """
    logging.info("💬 Prompt generated: prompt_hello_world()")
    return "Sure! Here's your message: Hello, World!"


if __name__ == "__main__":
    try:
        logging.info("🚀 Server starting... waiting for client connections!")
        logging.info("🟢 Press Ctrl+C to stop the server.")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logging.info("🛑 Server gracefully stopped by user (Ctrl+C)!")
    except Exception as e:
        logging.error(f"💥 Server stopped with error: {e}!")
    finally:
        logging.info("🔴 Server terminated!")
