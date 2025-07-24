from . import company_details, inventory_metadata, item_catalog


def register_all(mcp):
    company_details.register(mcp)
    inventory_metadata.register(mcp)
    item_catalog.register(mcp)
