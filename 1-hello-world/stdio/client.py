# client.py
import asyncio
from fastmcp import Client

async def main():
    # Connects to the server by running it as a subprocess
    async with Client("server.py") as client:
        # Check connection
        print("✅ Connected:", client.is_connected())

        # List available tools, resources, prompts
        resources = await client.list_resources()
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        print("\n" + "📚 Resources:", resources)
        print("\n" + "🛠️ Tools:", tools)
        print("\n" + "📝 Prompts:", prompts)

        # Read the hello://world resource
        res = await client.read_resource("hello://world")
        print("\n" + "📚 Resource read:", res)

        # Call the display_hello_world tool (returns dict)
        tool = await client.call_tool("display_hello_world", {})
        print("\n" + "🛠️ Tool result:", tool)

        # Get prompt_hello_world prompt
        prompt = await client.get_prompt("prompt_hello_world")
        print("\n" + "📝 Prompt message:", prompt)

        # Ping to ensure healthy connection
        await client.ping()
        print("\n" + "📍 Ping successful!")

if __name__ == "__main__":
    asyncio.run(main())
