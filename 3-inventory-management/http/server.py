import sys
import logging
from fastmcp import FastMCP
import tools.create_item as t1
import tools.read_item as t2
import tools.update_item as t3
import tools.delete_item as t4
import tools.list_items as t5
import tools.get_inventory_stats as t6
import resources

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='⚪ [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉🏽 %(message)s'
)

mcp = FastMCP("Inventory Management MCP Server")
logging.info("🚀 Server initialized")


t1.register(mcp)
t2.register(mcp)
t3.register(mcp)
t4.register(mcp)
t5.register(mcp)
t6.register(mcp)
resources.register_all(mcp)


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
