import logging
import sys
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='[%(asctime)s - %(levelname)s] %(message)s'
)

mcp = FastMCP("Simple Calculator HTTP Server")
logging.info("✨ Server instance initialized!")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Define the 'add' tool that takes two integers and returns their sum.

    Args:
        a (int): Number
        b (int): Number

    Returns:
        int: a + b
    """
    logging.info("🛠️ Tool called: add")
    return a + b


@mcp.tool()
def sub(a: int, b: int) -> int:
    """Define the 'sub' tool that takes two integers and returns their difference.

    Args:
        a (int): Number
        b (int): Number

    Returns:
        int: a - b
    """
    logging.info("🛠️ Tool called: sub")
    return a - b


@mcp.tool()
def mul(a: int, b: int) -> int:
    """Define the 'mul' tool that takes two integers and returns their product.

    Args:
        a (int): Number
        b (int): Number

    Returns:
        int: a * b
    """
    logging.info("🛠️ Tool called: mul")
    return a * b


@mcp.tool()
def div(a: int, b: int) -> float:
    """Define the 'div' tool that takes two integers and returns their quotient. Raises an error if division by zero is attempted.

    Args:
        a (int): Number
        b (int): Number

    Returns:
        int: a / b
    """
    logging.info("🛠️ Tool called: div")
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


if __name__ == "__main__":
    try:
        logging.info("🚀 Starting Streamable HTTP FastMCP server…")
        logging.info("🟢 Serving at http://127.0.0.1:8000/mcp/")
        mcp.run(
            transport="streamable-http",
            host="127.0.0.1",
            port=8000,
            path="/mcp/"
        )
    except KeyboardInterrupt:
        logging.info("🛑 Server shutdown by user (Ctrl+C).")
    except Exception as e:
        logging.error(f"💥 Server stopped due to error: {e}")
    finally:
        logging.info("🔴 Server terminated.")
