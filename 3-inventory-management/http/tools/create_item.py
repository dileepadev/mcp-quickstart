from fastmcp import Context
from tools.state import inventory


def register(mcp):
    @mcp.tool()
    async def create_item(name: str, qty: int, ctx: Context) -> dict:
        """Create a new inventory item with a given quantity.

        Args:
            name (str): Name of the item.
            qty (int): Quantity to initialize.

        Returns:
            dict: Acknowledgment of item creation.

        Raises:
            ValueError: If item already exists.
        """
        await ctx.info("🛠️ Tool called: create_item")
        if name in inventory:
            await ctx.error(f"Item '{name}' already exists")
            raise ValueError({"error": "Item already exists", "name": name})
        inventory[name] = qty
        await ctx.info(f"Created item '{name}' with qty {qty}")
        return {"action": "create", "name": name, "qty": qty}
