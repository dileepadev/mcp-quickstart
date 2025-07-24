from fastmcp import Context


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
        await ctx.info("🛠️ Resource called: item_catalog")
        catalog = {
            "LAP001": "ASUS ROG Zephyrus G14",
            "LAP002": "HP Omen Max 16",
            "LAP003": "Dell XPS 15",
            "LAP004": "Acer Predator Helios 500",
            "LAP005": "MSI Raider A18 HX",
            "LAP006": "Microsoft Surface Laptop 5G",
            "LAP007": "Apple MacBook Pro 16-inch",
            "LAP008": "ASUS ZenBook 14",
            "LAP009": "Dell Inspiron 14",
            "LAP010": "HP Omen 16"
        }
        return {"action": "catalog", "items": catalog}
