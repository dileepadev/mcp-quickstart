import sys
import logging
from fastmcp import FastMCP
import tools
import resources
import prompts

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='⚪ [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉🏽 %(message)s'
)

mcp = FastMCP("Inventory Management MCP Server")
logging.info("🚀 Server initialized")


tools.register_all(mcp)
resources.register_all(mcp)
prompts.register_all(mcp)


if __name__ == "__main__":
    try:
        logging.info("🟢 Starting HTTP server on http://127.0.0.1:8000/mcp/")
        mcp.run(
            transport="streamable-http",
            host="127.0.0.1",
            port=8000,
            path="/mcp/"
        )
    except KeyboardInterrupt:
        logging.info("🛑 Server shutdown via Ctrl+C")
    except Exception as e:
        logging.error(f"💥 Server error: {e}")
    finally:
        logging.info("🔴 Server terminated")
