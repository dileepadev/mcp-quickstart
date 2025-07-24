from fastmcp import Context
from tools.state import inventory
from resources.catalog import catalog


def register(mcp):
    @mcp.tool()
    async def delete_item(code: str, ctx: Context) -> dict:
        """Delete an item from the inventory.

        Args:
            code (str): Came of the item to delete.

        Returns:
            dict: Acknowledgment of deletion.

        Raises:
            ValueError: If item does not exist.
        """
        await ctx.info("🛠️ Tool called: delete_item")
        if code not in catalog:
            await ctx.error(f"Code '{code}' is not valid in catalog")
            raise ValueError({"error": "Invalid code", "code": code})
        if code not in inventory:
            await ctx.error(f"Cannot delete. Item '{code}' not found")
            raise ValueError(
                {"error": "Cannot delete. Item not found", "code": code})
        qty = inventory.pop(code)
        await ctx.info(f"Deleted item '{code}', last qty was {qty}")
        return {"action": "delete", "code": code, "qty": qty}
