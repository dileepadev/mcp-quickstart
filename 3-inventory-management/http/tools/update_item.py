from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def update_item(name: str, qty: int, ctx: Context) -> dict:
        """Update the quantity of an existing item.

        Args:
            name (str): Name of the item.
            qty (int): New quantity to set.

        Returns:
            dict: Acknowledgment of update.

        Raises:
            ValueError: If item does not exist.
        """
        await ctx.info("🛠️ Tool called: update_item")
        if name not in inventory:
            await ctx.error(f"Cannot update. Item '{name}' not found")
            raise ValueError(
                {"error": "Cannot update. Item not found", "name": name})
        inventory[name] = qty
        await ctx.info(f"Updated item '{name}' to qty {qty}")
        return {"action": "update", "name": name, "qty": qty}
