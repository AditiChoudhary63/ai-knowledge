# stdio_client-> server_params -> create a client -> create a session -> initialize the session
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters,ClientSession
import asyncio
server_params = StdioServerParameters(command="uv",args= ["--directory","C:\\code\\ai_knowledge\\ai-knowledge","run","mcp_server.py"])
async def main():
    try: 
        async with stdio_client(server_params) as (read, write):
            print("client connected")
            async with ClientSession(read, write) as session:
                print("session created")
                await session.initialize()
                print("session intialized")
                tools = await session.list_tools()
                print(tools)
    except Exception as e:
        print(e)
                # result = await session.call_tool("add",arguments={})
if __name__ == "__main__":
    asyncio.run(main())
