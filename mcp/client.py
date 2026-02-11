from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from log import logger
import asyncio

server_params = StdioServerParameters(command="uv",args= ["run","mcp_s.py"])

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
if __name__ == "__main__":
    asyncio.run(main())