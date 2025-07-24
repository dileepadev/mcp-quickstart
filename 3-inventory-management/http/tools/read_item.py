from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def read_item(code: str, ctx: Context) -> dict:
        """Read the current quantity of a specific item.

        Args:
            code (str): Code of the item.

        Returns:
            dict: Quantity of the item.

        Raises:
            ValueError: If the item does not exist.
        """
        await ctx.info("🛠️ Tool called: read_item")
        if code not in inventory:
            await ctx.error(f"Item '{code}' not found")
            raise ValueError({"error": "Item not found", "code": code})
        qty = inventory[code]
        await ctx.info(f"Read item '{code}': qty {qty}")
        return {"action": "read", "code": code, "qty": qty}
