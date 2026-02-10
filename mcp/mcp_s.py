from mcp.server.fastmcp import FastMCP
from tools import load_tools
from prompt import load_prompts
from resources import load_resources
mcp = FastMCP()


if __name__ == "__main__":
    load_tools(mcp)
    load_prompts(mcp)
    load_resources(mcp)
    mcp.run()