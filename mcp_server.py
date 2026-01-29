from mcp.server.fastmcp import FastMCP
import os
from rag import rag_instance

mcp = FastMCP()

@mcp.tool()
def fetch_note(filename: str):
    """
    Fetch user note by file name
    Args:
        filename: filename which user wants to open
    Returns:
        Text: file content
    """
    try:
        filepath = os.path.join('./documents', filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath) as file:
                note = file.read()
        return note
    except Exception as error:
        print(error)
@mcp.tool()
# def fetch_all_notes():
#     """
#     """
#     try:
        
#     except Exception as err:
#         print(err)
@mcp.tool()
def create_note(text: str) -> str:
    """
    Saves a user note in file system and returns file name
    Args:
        text: notes user wants to store
    returns:
        filename: file name
    """
    try:
        if not text or not isinstance(text, str):
            return "Error: Text must be a non-empty string"
        filepath = rag_instance.save_text_to_file(text)
        filename = os.path.basename(filepath)
        return filename
    except Exception as err:
        return f"Error: {str(err)}"

if __name__ == "__main__" :
    mcp.run()