from mcp.server.fastmcp import FastMCP
from tools import load_tools
from prompt import load_prompts
from resources import load_resources
import argparse
import logging
logger = logging.getLogger(__name__)
mcp = FastMCP()


if __name__ == "__main__":
    print("helo")
    load_tools(mcp)
    load_prompts(mcp)
    load_resources(mcp)
    # mcp.run()
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--mode", choices=["stdio", "streamable-http"],
        default="stdio",
        help="mcp server mode")
    args = parser.parse_args()
    mode = args.mode
    logger.info(f"starting mcp in {mode} mode")
    if mode == 'streamable-http':
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
