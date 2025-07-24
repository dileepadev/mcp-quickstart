import logging
from fastmcp import Context


def register(mcp):
    @mcp.prompt(name="greeting_message", description="A friendly greeting to the user")
    async def greeting_message(user_name: str, ctx: Context) -> str:
        """
        Prompt to greet the user by name.

        Args:
            user_name (str): Name of the user to greet.

        Returns:
            str: A greeting message.
        """
        logging.info("📝 Prompt called: greeting_message")
        await ctx.info("📝 Prompt called: greeting_message")
        return f"Hello {user_name}! 👋 Welcome to the Inventory Management system. How can I assist you today?"
