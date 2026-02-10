from pathlib import Path
from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel
from config import config
import logging

logger = logging.getLogger(__name__)
# class config(BaseModel):
#     base_dir: str | None
def load_tools(mcp:FastMCP):
    @mcp.tool()
    def greet_user(name:str)->str:
        """
        Greet user 
        Args:
            name: user name
        """
        return f"Good to meet you {name}"
    @mcp.tool()
    def set_base_dir(dir: str):
        """
            Sets a base directory for all operations in the server

            Args:
                dir (str): The base directory

            Returns:
                str: Confirmation message
        """
        config.base_dir = dir
        return "Base dir has been set successfully"
    @mcp.tool()
    def create_file(filename: str, content: str):
        """
        Creates file with provided content and filename
        Args:
            file_name (str): File name
            content (str): Content of the file

        Returns:
            Confirmation message after the file is created
        """
        try:
           base_dir = Path(config.base_dir)
           with open(base_dir / filename,"w") as f:
             f.write(content)
           return "file created successfully"
        except Exception as e:
            logger.info(e)
            return "file cannot be created"
