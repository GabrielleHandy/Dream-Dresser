import json

def get_all_categories():
    """
    Reads the full local taxonomy.
    Returns the dictionary so main.py can offer sub-category filters.
    """
    config_file = "closet_config.json"
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default starting structure if file is missing
        return {
            "Shirt": ["T-Shirt", "Blouse"],
            "Pants": ["Jeans", "Slacks"],
            "Shoes": ["Sneakers", "Boots", "Heels"]
        }

def update_taxonomy(category, sub_category=None):
    """
    Updates the local JSON with new categories or sub-categories.
    Ensures our 'System of Record' is always fresh.
    """
    config_file = "closet_config.json"
    data = get_all_categories()

    # Add top-level category if it's new
    if category not in data:
        data[category] = []
    
    # Add sub-category if provided and unique
    if sub_category and sub_category not in data[category]:
        data[category].append(sub_category)
        with open(config_file, "w") as f:
            json.dump(data, f, indent=4)
        return True
    
    # If it was just a top-level update, save that too
    with open(config_file, "w") as f:
        json.dump(data, f, indent=4)
    return False