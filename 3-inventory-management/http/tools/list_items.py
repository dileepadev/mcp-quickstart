from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def list_items(ctx: Context) -> dict:
        """List all items in the inventory.

        Returns:
            dict: All inventory items sorted by name.
        """
        await ctx.info("🛠️ Tool called: list_items")
        inv = dict(sorted(inventory.items()))
        return {"action": "list", "inventory": inv}
