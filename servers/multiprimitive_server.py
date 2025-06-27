# server.py
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import fitz
from google import genai
from google.genai import types
import json

mcp = FastMCP("DocumentReader") 

@mcp.tool("read_csv")
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
    
@mcp.tool("read_pdf")
def read_pdf(file_path: str, page_number: int) -> str:
    """
    Reads text from a specific page of a PDF file.

    Args:
        file_path (str): The absolute path to the PDF file.
        page_number (int): The 1-indexed page number to read.

    Returns:
        str: Text content of the specified page or error message.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    if os.path.splitext(file_path)[1].lower() != ".pdf":
        return f"Error: Unsupported file type. Only PDF is supported."

    if page_number < 1:
        return f"Error: page_number must be >= 1, got {page_number}"

    try:
        with fitz.open(file_path) as doc:
            if page_number > len(doc):
                return f"Error: Page {page_number} does not exist. Total pages: {len(doc)}"

            page = doc.load_page(page_number - 1)
            text = page.get_text()

            return f"Text from page {page_number}:\n\n{text.strip() if text.strip() else '[No readable text]'}"

    except Exception as e:
        return f"Error reading PDF: {e}"
    
@mcp.tool("read_image")
def read_image(image_path: str, query: str) -> str:
    """
    Reads an image and sends it with a query to Gemini for processing.

    Args:
        image_path (str): The path to the image file.
        query (str): Instruction or question about the image.

    Returns:
        str: Response from Gemini based on the query.
    """

    # Connect Google GenAI client
    client = genai.Client(api_key="AIzaSyCsbPzvNrYKC5AakAWlwBciFS2M4MfD2aE")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        # Send to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-pro-preview-03-25",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                query
            ]
        )

        return response.text

    except Exception as e:
        raise RuntimeError(f"Error processing image: {e}")
    
@mcp.resource("users://{user_id}/profile", title="User Profile")
async def get_user_profile(user_id: str) -> dict:
    """
    Returns the profile of a user by user_id.
    This function returns a JSON-serializable dict.
    """
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load users.json: {e}"}

    for user in users:
        if str(user.get('user_id')) == user_id:
            return {"user_id": user_id, "name": user.get('name', 'Unknown')}

    return {"error": f"No user found with ID {user_id}"}


# To run this server:
# python server.py

if __name__ == "__main__":
    mcp.run()