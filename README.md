# MCP Study Jams

This project is a collection of examples demonstrating how to use the `mcp` library to create and expose tools that can be called by a client. The client uses Google's Generative AI to determine which tool to call based on a user's prompt.

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your environment:**

    Create a `.env` file in the root of the project and add your Google Generative AI API key:

    ```
    GOOGLE_API_KEY=<your_api_key>
    ```

## Usage

### Running the Servers

There are several servers in the `servers` directory. To run a server, navigate to the `servers` directory and run the desired server file:

```bash
python servers/<server_file>.py
```

Here are the available servers:

-   **`server.py`**: A server with tools to read from a CSV file, list files in a directory, and fetch user data from a mock database.
-   **`server_new.py`**: A simple server with a tool to add two integers.
-   **`image_server.py`**: A server with tools to read from a CSV file, a PDF file, and a tool to read an image and send it to Gemini for processing.
-   **`multiprimitive_server.py`**: A server with tools to read from a CSV file, a PDF file, an image, and a resource to get a user profile.
-   **`multitool_server.py`**: A server with tools to read from a CSV file and list files in a directory.
-   **`mcp_spawner.py`**: A server with a tool that can create new MCP functions.

### Running the Clients

There are two clients in the `clients` directory. To run a client, navigate to the `clients` directory and run the desired client file:

```bash
python clients/<client_file>.py
```

Here are the available clients:

-   **`client.py`**: A client that can connect to any of the servers and use the available tools.
-   **`multiprimitive_client.py`**: A client that is specifically designed to work with the `multiprimitive_server.py` and can also list available prompts and resources.

The client will prompt you to enter a prompt. The client will then use Google's Generative AI to determine which tool to call based on your prompt and the available tools on the running server.
