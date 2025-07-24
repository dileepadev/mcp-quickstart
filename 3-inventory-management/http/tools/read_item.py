from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def read_item(name: str, ctx: Context) -> dict:
        """Read the current quantity of a specific item.

        Args:
            name (str): Name of the item.

        Returns:
            dict: Quantity of the item.

        Raises:
            ValueError: If the item does not exist.
        """
        await ctx.info("🛠️ Tool called: read_item")
        if name not in inventory:
            await ctx.error(f"Item '{name}' not found")
            raise ValueError({"error": "Item not found", "name": name})
        qty = inventory[name]
        await ctx.info(f"Read item '{name}': qty {qty}")
        return {"action": "read", "name": name, "qty": qty}
