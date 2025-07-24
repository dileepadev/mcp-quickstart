from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def get_inventory_stats(ctx: Context) -> dict:
        """Return metadata about the inventory.

        Returns:
            dict: Total number of items and total quantity.
        """
        await ctx.info("🛠️ Tool called: get_inventory_stats")
        total_items = len(inventory)
        total_qty = sum(inventory.values())
        return {
            "action": "stats",
            "total_items": total_items,
            "total_quantity": total_qty
        }
