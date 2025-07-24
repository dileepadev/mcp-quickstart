from fastmcp import Context
from tools.state import inventory
from resources.catalog import catalog


def register(mcp):
    @mcp.tool()
    async def update_item(code: str, qty: int, ctx: Context) -> dict:
        """Update the quantity of an existing item.

        Args:
            code (str): Code of the item.
            qty (int): New quantity to set.

        Returns:
            dict: Acknowledgment of update.

        Raises:
            ValueError: If item does not exist.
        """
        await ctx.info("🛠️ Tool called: update_item")
        if code not in catalog:
            await ctx.error(f"Code '{code}' is not valid in catalog")
            raise ValueError({"error": "Invalid code", "code": code})
        if code not in inventory:
            await ctx.error(f"Cannot update. Item '{code}' not found")
            raise ValueError(
                {"error": "Cannot update. Item not found", "code": code})
        inventory[code] = qty
        await ctx.info(f"Updated item '{code}' to qty {qty}")
        return {"action": "update", "code": code, "qty": qty}
