import logging
import sys

# This refers to the official MCP Python SDK implementation: from mcp.server.fastmcp import FastMCP
# This imports the standalone FastMCP library, version 2.x.: from fastmcp import FastMCP
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Instantiate the server
mcp = FastMCP("hello_server")
logging.info("✨ Server instance initialized!")

# Resource
@mcp.resource("hello://world")
def hello_world_resource() -> str:
    logging.info("🌍 Resource accessed: hello://world")
    return "Hello, World!"

# Tool
@mcp.tool()
def display_hello_world() -> dict:
    logging.info("👋 Tool called: display_hello_world()")
    return {"result": "Hello, World!"}

# Prompt
@mcp.prompt()
def prompt_hello_world() -> str:
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
