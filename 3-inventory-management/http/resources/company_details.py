import logging
from fastmcp import Context

name: str = "Tech Supplies Co."
address: str = "123 Innovation Drive, Tech City"
contact: str = "+94123456789"
email: str = "contact@dileepa.dev"
website: str = "https://mcp-inventory.dileepa.dev"
privacy_policy: str = f"{website}/privacy-policy"
terms_and_conditions: str = f"{website}terms-and-conditions"
mission: str = "To provide high-quality tech supplies to businesses worldwide."
vision: str = "To be the leading supplier of innovative tech solutions."
values: list[str] = [
    "Customer Satisfaction",
    "Innovation",
    "Integrity",
    "Sustainability"
]

details = {
    "name": name,
    "address": address,
    "contact": contact,
    "email": email,
    "website": website,
    "privacy_policy": privacy_policy,
    "terms_and_conditions": terms_and_conditions,
    "mission": mission,
    "vision": vision,
    "values": values
}


def register(mcp):
    @mcp.resource("company://details")
    async def get_company_details(ctx: Context) -> dict:
        """
        Provide company information for the inventory system.

        Args:
            ctx (Context): The MCP execution context.

        Returns:
            dict: Company details including name, address, contact info.
        """
        logging.info("🌐 Resource called: get_company_details")
        await ctx.info("🌐 Resource called: get_company_details")
        return details
