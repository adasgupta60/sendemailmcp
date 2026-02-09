import argparse
import asyncio
import json

from fastmcp import Client


async def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal MCP client to test send_gmail tool.")
    parser.add_argument("--url", default="http://127.0.0.1:8000/mcp", help="MCP server URL")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--body", required=True, help="Email body text")
    parser.add_argument("--subject", default="Test from minimal MCP client", help="Email subject")
    args = parser.parse_args()

    async with Client(args.url) as client:
        tools = await client.list_tools()
        print("Tools on server:")
        print(json.dumps([tool.name for tool in tools], indent=2))

        result = await client.call_tool(
            "send_gmail",
            {
                "recipient_email": args.to,
                "body": args.body,
                "subject": args.subject,
            },
        )
        print("\nTool response:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
