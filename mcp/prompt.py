from mcp.server.fastmcp import FastMCP
def load_prompts(mcp:FastMCP):
    @mcp.prompt()
    def master_prompt():
        """
        Prompt for the Workspace MCP Gateway

        Returns:
            str: Master Prompt for the MCP Gateway
        """
        prompt = """
        Set workspace base directory = .
        Get list of all files in the directory
        Create a test.txt with content "Mahabharata is the paragon of Itihasas"
        """
        return prompt