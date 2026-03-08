def get_label_agreement(item_name: str):
    """
    Determines the correct grammatical agreement for clothing items.
    Prevents 'Pants is' or 'Dress are' errors.
    """
    name_lower = item_name.lower().strip()
    
    # Logic: Words ending in 's' are usually plural (Pants, Shoes, Jeans)
    # Exception: Words ending in 'ss' are usually singular (Dress, Glass)
    if (name_lower.endswith('s') and not name_lower.endswith('ss')) or "pair" in name_lower:
        return {
            "selector": "these",
            "verb": "are",
            "pronoun": "them"
        }
    
    return {
        "selector": "this",
        "verb": "is",
        "pronoun": "it"
    }