from langchain_core.tools import tool

@tool
def multiply(x: int, y: int) -> int:
    
    """
    Multiply two numbers together.

    Example:
        >>> multiply(2, 3)
        6
    """
    print("---using multiply tool---")
    return x * y

@tool 
def add(x: int, y: int) -> int:
    """
    Add two numbers together.

    Example:
        >>> add(2, 3)
        5
    """
    print("---using add tool---")
    return x + y

@tool
def subtract(x: int, y: int) -> int:
    """
    Subtract one number from another.

    Example:
        >>> subtract(2, 3)
        -1
    """
    print("--using subtract tool---")
    return x - y