# server.py
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import fitz

mcp = FastMCP("DocumentReader")

@mcp.tool()
def read_csv(file_path: str, nth_row: int) -> str:
    """
    Reads a specific nth row from a CSV file and returns it along with 
    the number of rows remaining after that row.

    Args:
        file_path (str): The absolute path to the file to read.
        nth_row (int): The 1-indexed row number to retrieve. Must be >= 1.

    Returns:
        str: A string representation of the nth row (with column headers) 
             and the number of remaining rows. Returns error message if 
             the file is invalid or row doesn't exist.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension != ".csv":
        return f"Error: Unsupported file type '{file_extension}'. Only CSV is supported."

    if nth_row < 1:
        return f"Error: nth_row must be >= 1, got {nth_row}"

    try:
        df = pd.read_csv(file_path)

        if nth_row > len(df):
            return f"Error: Row {nth_row} does not exist in the file. Total rows: {len(df)}"

        row = df.iloc[[nth_row - 1]]  # get as DataFrame to preserve header
        remaining_rows = len(df) - nth_row

        return f"{row.to_string(index=False)}\n\nRows remaining: {remaining_rows}"

    except Exception as e:
        return f"Error reading file: {e}"
    
@mcp.tool()
def list_files_in_directory(directory_path):
    """
    Lists all files (not directories) in the given directory path.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        List[str]: A list of file names in the directory.
    """
    try:
        # List all entries in the directory
        entries = os.listdir(directory_path)
        # Filter out only files
        files = [f for f in entries if os.path.isfile(os.path.join(directory_path, f))]
        return files
    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# To run this server:
# python server.py

if __name__ == "__main__":
    mcp.run()