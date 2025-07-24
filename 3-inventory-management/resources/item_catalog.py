import logging
from fastmcp import Context
from resources.catalog import catalog


def register(mcp):
    @mcp.resource("company://item_catalog")
    async def item_catalog(ctx: Context) -> dict:
        """
        Provide a catalog of available laptops with codes and brand names.

        Args:
            ctx (Context): The MCP execution context.

        Returns:
            dict: A dictionary mapping laptop codes to laptop brand/model names.
        """
        logging.info("📚 Resource called: item_catalog",)
        await ctx.info("📚 Resource called: item_catalog",)
        return {"action": "catalog", "items": catalog}
