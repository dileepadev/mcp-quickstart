import sys
import logging
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='⚪ [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉🏽 %(message)s'
)

mcp = FastMCP("Inventory Management MCP Server")
logging.info("🚀 Server initialized")

# In-memory inventory: item name → quantity
inventory: dict[str, int] = {}


@mcp.tool()
def create_item(name: str, qty: int) -> dict:
    """Create a new inventory item with a given quantity.

    Args:
        name (str): Name of the item.
        qty (int): Quantity to initialize.

    Returns:
        dict: Acknowledgment of item creation.

    Raises:
        ValueError: If item already exists.
    """
    logging.info("🛠️ Tool called: create_item")
    if name in inventory:
        raise ValueError({"error": "Item already exists", "name": name})
    inventory[name] = qty
    logging.info(f"Created item '{name}' with qty {qty}")
    return {"action": "create", "name": name, "qty": qty}


@mcp.tool()
def read_item(name: str) -> dict:
    """Read the current quantity of a specific item.

    Args:
        name (str): Name of the item.

    Returns:
        dict: Quantity of the item.

    Raises:
        ValueError: If the item does not exist.
    """
    logging.info("🛠️ Tool called: read_item")
    if name not in inventory:
        raise ValueError({"error": "Item not found", "name": name})
    qty = inventory[name]
    logging.info(f"Read item '{name}': qty {qty}")
    return {"action": "read", "name": name, "qty": qty}


@mcp.tool()
def update_item(name: str, qty: int) -> dict:
    """Update the quantity of an existing item.

    Args:
        name (str): Name of the item.
        qty (int): New quantity to set.

    Returns:
        dict: Acknowledgment of update.

    Raises:
        ValueError: If item does not exist.
    """
    logging.info("🛠️ Tool called: update_item")
    if name not in inventory:
        raise ValueError(
            {"error": "Cannot update. Item not found", "name": name})
    inventory[name] = qty
    logging.info(f"Updated item '{name}' to qty {qty}")
    return {"action": "update", "name": name, "qty": qty}


@mcp.tool()
def delete_item(name: str) -> dict:
    """Delete an item from the inventory.

    Args:
        name (str): Name of the item to delete.

    Returns:
        dict: Acknowledgment of deletion.

    Raises:
        ValueError: If item does not exist.
    """
    logging.info("🛠️ Tool called: delete_item")
    if name not in inventory:
        raise ValueError(
            {"error": "Cannot delete. Item not found", "name": name})
    qty = inventory.pop(name)
    logging.info(f"Deleted item '{name}', last qty was {qty}")
    return {"action": "delete", "name": name, "qty": qty}


@mcp.tool()
def list_items() -> dict:
    """List all items in the inventory.

    Returns:
        dict: All inventory items sorted by name.
    """
    logging.info("🛠️ Tool called: list_items")
    inv = dict(sorted(inventory.items()))
    return {"action": "list", "inventory": inv}


@mcp.tool()
def get_inventory_stats() -> dict:
    """Return metadata about the inventory.

    Returns:
        dict: Total number of items and total quantity.
    """
    logging.info("🛠️ Tool called: get_inventory_stats")
    total_items = len(inventory)
    total_qty = sum(inventory.values())
    return {
        "action": "stats",
        "total_items": total_items,
        "total_quantity": total_qty
    }


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
