import random
import string


def generate_sku(brand: str, category: str, slug: str, unit: str) -> str:
    """
    Generates a short, unique SKU:
    Example: 'Bengal Meat', 'Beef', 'premium-beef', '500g'
    Result: BE-BE-PRE-50-X92
    """
    # 1. Clean and take first 2-3 chars of each
    # Use .upper() for that professional "warehouse" look
    b = (brand[:2] if brand else "XX").upper()
    c = (category[:2] if category else "XX").upper()

    # Take first 3 of slug, but remove dashes first
    clean_slug = slug.replace("-", "")
    s = (clean_slug[:3] if clean_slug else "PRD").upper()

    # Take first 2 of unit
    u = (unit[:2] if unit else "UN").upper()

    # 2. Add 3 random characters (Letters + Numbers) to guarantee uniqueness
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))

    return f"{b}{c}-{s}{u}-{suffix}"
