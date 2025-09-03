from langchain_core.tools import tool

@tool
def your_tool_name(input: str) -> str:
    """
    Your tool description here.
    
    Args:
        input (str): Input string for the tool.
    
    Returns:
        str: Processed output string.
    """
    # ! Your tool logic here
    return f"Processed: {input}"