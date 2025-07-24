from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def delete_item(name: str, ctx: Context) -> dict:
        """Delete an item from the inventory.

        Args:
            name (str): Name of the item to delete.

        Returns:
            dict: Acknowledgment of deletion.

        Raises:
            ValueError: If item does not exist.
        """
        await ctx.info("🛠️ Tool called: delete_item")
        if name not in inventory:
            await ctx.error(f"Cannot delete. Item '{name}' not found")
            raise ValueError(
                {"error": "Cannot delete. Item not found", "name": name})
        qty = inventory.pop(name)
        await ctx.info(f"Deleted item '{name}', last qty was {qty}")
        return {"action": "delete", "name": name, "qty": qty}
