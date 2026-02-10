from pathlib import Path
from config import config
from mcp.server.fastmcp import FastMCP
def load_resources(mcp:FastMCP):
    @mcp.resource("workspace://file/{path}")
    def get_file_content(path:str)->str:
        """
        Fetches the file content

        Args:
            file (str): The name of the file for which the user wants the content

        Returns:
            The contents of the file
        """
        try:
            f = Path(config.base_dir, path)
            if not f.is_file():
                return f"The provided input: {path} is not a file"
            with open(f) as file:
                return file.read()
        except Exception as e:
            logger.error("Error: %s", e)
            return "Failed to fetch file content"