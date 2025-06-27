# Our AI client that uses MCP to call tools
from google import genai
from google.genai import types

# ClientSession: Manages the communication session between our client/app and the MCP server.
from mcp import ClientSession

# StdioServerParameters: stdio allows the server to be language-neutral and easily embedded in different environments.
from mcp import StdioServerParameters

# stdio_client: Provides a way to connect to the MCP server using standard input/output streams.
from mcp.client.stdio import stdio_client

import asyncio

# Connect Google GenAI client
client = genai.Client(api_key="")

# Launch and communicate with MCP server using stdio
server_params = StdioServerParameters(
    command="python",
    args=["image_server.py"],
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            prompt = input("Enter your prompt: ")
            await session.initialize() # Initialize the session handshake with the MCP server

            tools = await session.list_tools() # List all tools exposed by the server
            print("Available tools:", [tool.name for tool in tools.tools])

            # This step converts the MCP tool definition into Gemini's function_declaration format
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in tools.tools
            ]
            config = types.GenerateContentConfig(tools=tools)
            
            # Get response from Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config,
            )

            tool_call = response.candidates[0].content.parts[0].function_call

            # Use MCP client to call the tool and get result
            tool_name = tool_call.name
            tool_args = tool_call.args

            result = await session.call_tool(tool_name, arguments=tool_args)

            print("Tool Result:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run())