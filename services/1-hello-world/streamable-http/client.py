import asyncio
from fastmcp import Client

async def main():
    # Connect to the server using Streamable HTTP transport
    async with Client("http://127.0.0.1:8000/mcp/") as client:
        # Check connection status
        print("✅ Connected:", client.is_connected())

        # List available tools, resources, and prompts
        resources = await client.list_resources()
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        print("\n" + "📚 Resources:", resources)
        print("\n" + "🛠️ Tools:", tools)
        print("\n" + "📝 Prompts:", prompts)

        # Read the hello://world resource
        res = await client.read_resource("hello://world")
        print("\n" + "📚 Resource read:", res)

        # Call the display_hello_world tool
        tool = await client.call_tool("display_hello_world", {})
        print("\n" + "🛠️ Tool result:", tool)

        # Get the prompt_hello_world prompt
        prompt = await client.get_prompt("prompt_hello_world")
        print("\n" + "📝 Prompt message:", prompt)

        # Ping the server to ensure healthy connection
        await client.ping()
        print("\n" + "📍 Ping successful!")

if __name__ == "__main__":
    asyncio.run(main())
