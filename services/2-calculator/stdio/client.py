import asyncio
from fastmcp import Client


async def main():

    client = Client("server.py")

    async with client:
        print("✅ Connected:", client.is_connected())

        resources = await client.list_resources()
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        print("\n" + "📚 Resources:", resources)
        print("\n" + "🛠️ Tools:", tools)
        print("\n" + "📝 Prompts:", prompts)

        print("\n" + "🔥 Example operations:")

        sum_result = await client.call_tool("add", {"a": 7, "b": 5})
        print("7 + 5 =", sum_result.data)

        diff_result = await client.call_tool("sub", {"a": 10, "b": 3})
        print("10 - 3 =", diff_result.data)

        prod_result = await client.call_tool("mul", {"a": 4, "b": 6})
        print("4 x 6 =", prod_result.data)

        quot_result = await client.call_tool("div", {"a": 20, "b": 4})
        print("20 ÷ 4 =", quot_result.data)

        print("\n" + "⛔ Handle a divide by zero error:")

        try:
            bad = await client.call_tool("div", {"a": 5, "b": 0})
            print("Should not see this:", bad)
        except Exception as e:
            print("Error calling div:", e)

if __name__ == "__main__":
    asyncio.run(main())
