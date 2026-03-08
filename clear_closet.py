import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from ross_agent import RossAgent


def clear_closet():
    print("⚠️ Warning: This will permanently delete all saved outfits.")
    confirm = input("Are you sure you want to clear the closet? (y/n): ").lower()
    
    if confirm == 'y':
        # 1. Clear Ross (Pinecone)
        ross = RossAgent()
        ross.wake_up()
        try:
            # Senior move: Delete all vectors in the index
            ross.index.delete(delete_all=True)
            print("✅ Ross: 'The museum is empty. We are starting over!'")
        except Exception as e:
            print(f"❌ Error clearing Pinecone: {e}")

        # 2. Reset Rachel (Local Taxonomy)
        config_file = "closet_config.json"
        default_data = {
            "Shirt": ["T-Shirt", "Blouse"],
            "Pants": ["Jeans", "Slacks"],
            "Shoes": ["Sneakers", "Boots", "Heels"]
        }
        
        try:
            with open(config_file, "w") as f:
                json.dump(default_data, f, indent=4)
            print(f"✅ Rachel: 'Taxonomy reset to defaults in {config_file}.'")
        except Exception as e:
            print(f"❌ Error resetting local config: {e}")
            
    else:
        print("Clear aborted. Your closet is safe!")

if __name__ == "__main__":
    clear_closet()