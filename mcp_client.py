# stdio_client-> server_params -> create a client -> create a session -> initialize the session
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters,ClientSession
import asyncio
import logging

logger = logging.getLogger(__name__)

server_params = StdioServerParameters(command="uv",args= ["--directory","C:\\code\\ai_knowledge\\ai-knowledge","run","mcp_server.py"])
async def main():
    try: 
        async with stdio_client(server_params) as (read, write):
            logger.info("client connected")
            async with ClientSession(read, write) as session:
                logger.info("session created")
                await session.initialize()
                logger.info("session intialized")
                tools = await session.list_tools()
                logger.info(tools)
    except Exception as e:
        logger.error(e)
                # result = await session.call_tool("add",arguments={})

async def get_tools():
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                return tools
    except Exception as e:
        logger.error(e)
        return None
if __name__ == "__main__":
    asyncio.run(main())
