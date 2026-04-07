import re


def to_pascal_case(text):
    """Converts a string to PascalCase for Next.js component names."""
    # Remove special characters, split by space/hyphen, and capitalize each word
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return "".join(word.capitalize() for word in words) + "Icon"
