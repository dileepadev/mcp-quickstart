from . import create_item, read_item, update_item, delete_item, list_items, get_inventory_stats


def register_all(mcp):
    create_item.register(mcp)
    read_item.register(mcp)
    update_item.register(mcp)
    delete_item.register(mcp)
    list_items.register(mcp)
    get_inventory_stats.register(mcp)
