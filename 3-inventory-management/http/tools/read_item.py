import logging
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
        logging.info("🛠️ Tool called: read_item")
        await ctx.info("🛠️ Tool called: read_item")
        if code not in inventory:
            logging.error(f"Item '{code}' not found")
            await ctx.error(f"Item '{code}' not found")
            raise ValueError({"error": "Item not found", "code": code})
        qty = inventory[code]
        logging.info(f"Read item '{code}': qty {qty}")
        await ctx.info(f"Read item '{code}': qty {qty}")
        return {"action": "read", "code": code, "qty": qty}
