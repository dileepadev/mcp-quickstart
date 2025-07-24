from fastmcp import Context
from tools.state import inventory
from resources.catalog import catalog


def register(mcp):
    @mcp.tool()
    async def create_item(code: str, qty: int, ctx: Context) -> dict:
        """Create a new inventory item with a given quantity.

        Args:
            code (str): Code of the item.
            qty (int): Quantity to initialize.

        Returns:
            dict: Acknowledgment of item creation.

        Raises:
            ValueError: If item already exists.
        """
        await ctx.info("🛠️ Tool called: create_item")
        if code not in catalog:
            await ctx.error(f"Code '{code}' is not valid in catalog")
            raise ValueError({"error": "Invalid code", "code": code})
        if code in inventory:
            await ctx.error(f"Item '{code}' already exists")
            raise ValueError({"error": "Item already exists", "code": code})
        inventory[code] = qty
        await ctx.info(f"Created item '{code}' with qty {qty}")
        return {"action": "create", "code": code, "qty": qty}
