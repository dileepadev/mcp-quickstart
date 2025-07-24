import logging
import sys
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

@mcp.resource("hello://world")
def hello_world_resource() -> str:
    """Return a simple greeting."""
    logging.info("📚 Resource accessed: hello://world")
    return "Hello, World!"

@mcp.tool()
def display_hello_world() -> dict:
    """Return greeting as a JSON-like dict."""
    logging.info("🛠️ Tool called: display_hello_world()")
    return {"result": "Hello, World!"}

@mcp.prompt()
def prompt_hello_world() -> str:
    """Generate a friendly prompt greeting."""
    logging.info("📝 Prompt generated: prompt_hello_world()")
    return "Sure! Here's your message: Hello, World!"

if __name__ == "__main__":
    try:
        logging.info("🚀 Starting SSE FastMCP server…")
        logging.info("🟢 Serving at http://127.0.0.1:8000/sse")
        mcp.run(transport="sse", host="127.0.0.1", port=8000, path="/sse")
    except KeyboardInterrupt:
        logging.info("🛑 Server shutdown by user (Ctrl+C).")
    except Exception as e:
        logging.error(f"💥 Server stopped due to error: {e}")
    finally:
        logging.info("🔴 Server terminated.")
