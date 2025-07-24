from fastmcp import Context
from tools.state import inventory
from datetime import datetime


def register(mcp):
    @mcp.resource("inventory://metadata")
    async def get_inventory_metadata(ctx: Context) -> dict:
        """
        Provide metadata about the inventory system.

        Args:
            ctx (Context): The MCP execution context.

        Returns:
            dict: Metadata including total items, total quantity, last updated timestamp.
        """
        await ctx.info("📊 Resource called: get_inventory_metadata")
        return {
            "updated_by": "Admin",
            "total_items": len(inventory),
            "total_quantity": sum(inventory.values()),
            "last_updated": datetime.now(),
        }
