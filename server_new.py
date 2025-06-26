from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Addition")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Adds two integers and returns the result.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

if __name__ == "__main__":
    mcp.run()