# server.py
from mcp.server.fastmcp import FastMCP
import os
from google import genai
from google.genai import types
import re

mcp = FastMCP("MCPSpawner")

SYSTEM_PROMPT = """
You are given a query to create a new python function based on the provided input.
Return only the Python function, with the @mcp.tool() decorator included. Exclude any inline formatting like ```python or triple backticks.
"""

@mcp.tool()
def spawn_mcp_function(query: str) -> str:
    """
    Spawns a new MCP function based on the provided query and writes it to this script.
    
    Args:
        query (str): The query to process for spawning a new MCP function.
    
    Returns:
        str: The function returned by Gemini after processing the query.
    """

    client = genai.Client(api_key="AIzaSyCsbPzvNrYKC5AakAWlwBciFS2M4MfD2aE")
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=config,
    )

    generated_code = response.candidates[0].content.parts[0].text
    print("Response from Gemini:\n", generated_code)

    script_path = os.path.abspath(__file__)
    with open(script_path, "r") as f:
        lines = f.readlines()

    # Find the index of the line with "if __name__"
    # Regular expression pattern to match the if __name__ == '__main__' or "__main__" line
    main_pattern = re.compile(r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:')

    # Find the last matching line index
    insert_index = max(
        (i for i, line in enumerate(lines) if main_pattern.match(line)),
        default=len(lines)
    )

    # Insert the generated function before the main block
    lines.insert(insert_index, f"\n{generated_code}\n\n")

    with open(script_path, "w") as f:
        f.writelines(lines)

    return generated_code


@mcp.tool()
def scrape_data_selenium(url: str) -> dict:
    """
    Scrapes data from a given URL using Selenium WebDriver.

    This function initializes a Chrome WebDriver (in headless mode for efficiency),
    navigates to the specified URL, and extracts the page title and the
    text content of the body. It then closes the browser.

    Args:
        url (str): The URL to scrape data from.

    Returns:
        dict: A dictionary containing the 'title' and 'body_text' of the page.
              Returns an empty dictionary if an error occurs during scraping.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import WebDriverException, NoSuchElementException

    scraped_data = {}
    driver = None  # Initialize driver to None

    try:
        # Configure Chrome options for headless browsing (no GUI)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary in some environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-gpu") # Applicable for Windows OS and sometimes Linux

        # Initialize the Chrome WebDriver
        # Ensure you have the appropriate WebDriver executable (e.g., chromedriver)
        # in your system's PATH or specify its path directly.
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the URL
        driver.get(url)

        # Scrape data
        scraped_data['title'] = driver.title

        try:
            body_element = driver.find_element(By.TAG_NAME, 'body')
            scraped_data['body_text'] = body_element.text
        except NoSuchElementException:
            scraped_data['body_text'] = "Body element not found."

    except WebDriverException as e:
        print(f"Selenium WebDriver error: {e}")
        # Return an empty dict or specific error info if scraping fails
        scraped_data = {"error": f"WebDriver error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        scraped_data = {"error": f"Unexpected error: {e}"}
    finally:
        # Always quit the driver to release resources
        if driver:
            driver.quit()

    return scraped_data


@mcp.tool()
def create_file(file_path: str, content: str = "") -> bool:
    """
    Creates a new file at the specified path, optionally writing initial content to it.

    Args:
        file_path (str): The full path to the file to be created.
        content (str, optional): The initial content to write to the file. Defaults to an empty string.

    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error creating file '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

@mcp.tool()
def delete_file(file_path: str) -> bool:
    """
    Deletes the specified file if it exists.

    Args:
        file_path (str): The full path to the file to be deleted.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    mcp.run()