import asyncio
from fastmcp import Client


async def display_resources(client: Client):
    print("\n" + "\n" + "=" * 100)
    print("📚 RESOURCES")
    print("=" * 100)

    print("\n" + "*" * 10 + " List Resources " + "*" * 10)
    resources = await client.list_resources()
    for res in resources:
        print("\n" + "🔵", res)

    print("\n" + "*" * 10 + " Read Resources " + "*" * 10)

    print("\n🟡 Company Info:")
    company_info = await client.read_resource("company://details")
    print(company_info)

    print("\n🟡 Catalog:")
    catalog = await client.read_resource("company://item_catalog")
    print(catalog)

    print("\n🟡 Inventory Metadata:")
    metadata = await client.read_resource("inventory://metadata")
    print(metadata)


async def display_tools(client: Client):
    print("\n" + "\n" + "=" * 100)
    print("🛠️ TOOLS")
    print("=" * 100)

    print("\n" + "*" * 10 + " List Tools " + "*" * 10)
    tools = await client.list_tools()
    for tool in tools:
        print("\n" + "🔵", tool)

    print("\n" + "*" * 10 + " Call Tools " + "*" * 10)

    print("\n🟡 Current Inventory:")
    inventory = await client.call_tool("list_items", {})
    print(inventory.data)

    try:
        print("\n🟡 Create Item:")
        result = await client.call_tool("create_item", {"code": "LAP003", "qty": 10})
        print("✅ Created item:", result.data)
    except Exception as e:
        print("❌ Error creating item:", e)

    try:
        print("\n🟡 Read Item:")
        read_result = await client.call_tool("read_item", {"code": "LAP003"})
        print("✅ Read item:", read_result.data)
    except Exception as e:
        print("❌ Error reading item:", e)

    try:
        print("\n🟡 Update Item:")
        update_result = await client.call_tool("update_item", {"code": "LAP003", "qty": 15})
        print("✅ Updated item:", update_result.data)
    except Exception as e:
        print("❌ Error updating item:", e)

    print("\n🟡 Inventory Stats:")
    stats = await client.call_tool("get_inventory_stats", {})
    print(stats.data)

    try:
        print("\n🟡 Delete Item:")
        delete_result = await client.call_tool("delete_item", {"code": "LAP003"})
        print("✅ Deleted item:", delete_result.data)
    except Exception as e:
        print("❌ Error deleting item:", e)

    inventory = await client.call_tool("list_items", {})
    print("\n🟡 Inventory After Deletion:", inventory.data)


async def display_prompts(client: Client):
    print("\n" + "\n" + "=" * 100)
    print("📝 PROMPTS")
    print("=" * 100)

    print("\n" + "*" * 10 + " List Prompts " + "*" * 10)
    prompts = await client.list_prompts()
    for prompt in prompts:
        print("\n" + "🔵", prompt)

    print("\n" + "*" * 10 + " Get Prompt " + "*" * 10)
    greeting = await client.get_prompt("greeting_message", {"user_name": "Dileepa"})
    print("\n🟡 Greeting Prompt:", greeting)


async def main():
    client = Client("http://127.0.0.1:8000/mcp/")

    async with client:
        print("✅ Connected:", client.is_connected())
        await display_resources(client)
        await display_tools(client)
        await display_prompts(client)


if __name__ == "__main__":
    asyncio.run(main())
