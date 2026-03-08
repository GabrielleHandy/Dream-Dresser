import os
import sys
# Ensure Python can find the agents folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from ross_agent import RossAgent
from rachel_agent import RachelVisionAgent
from monica_agent import MonicaRuleAgent
from utils.rachelUtility import update_taxonomy, get_all_categories
from utils.grammarUtility import get_label_agreement

def main():
    print("\n--- 👗 WELCOME TO DREAMDRESSER AI ---")
    
    # 1. Initialize our team
    ross = RossAgent()
    ross.wake_up() 
    rachel = RachelVisionAgent()
    monica = MonicaRuleAgent() # Monica uses Winston-Salem weather

    while True:
        print("\nWhat would you like to do?")
        print("1. [Scan] Add a new photo to the closet")
        print("2. [Search] Find an outfit using words")
        print("3. [Exit]")
        
        choice = input("\nEnter choice (1, 2, or 3): ").strip()

        if choice == '1':
            img_filename = input("Enter the image filename (e.g., test_photo.jpg): ").strip()
            image_path = os.path.join("images", img_filename)

            if os.path.exists(image_path):
                print("\nRachel is scanning...")
                vector = rachel.scan_outfit(image_path)
                category, confidence = rachel.detect_category(image_path)
                
                # Fetch taxonomy for normalization
                taxonomy = get_all_categories()
                existing_parents = list(taxonomy.keys())
                
                print(f"\nRachel: 'I'm {confidence}% sure this is {category}!'")
                if existing_parents:
                    print(f"Current Menu Categories: {', '.join(existing_parents)}")
                
                correction = input(f"Accept '{category}'? (Enter to keep, or type a category from the menu): ").strip()
                final_category = correction if correction else category
                
                # Update local taxonomy
                update_taxonomy(final_category) 
                
                sub_cats = taxonomy.get(final_category, [])
                if sub_cats:
                    print(f"Existing types of {final_category}: {', '.join(sub_cats)}")
                
                sub_category = input(f"What type of {final_category} is this? (e.g., Boots): ").strip()
                if sub_category:
                    update_taxonomy(final_category, sub_category)

                # --- AUTO-NAMING WITH EDIT OPTION ---
                auto_name = rachel.generate_name(image_path, sub_category or final_category)
                print(f"\nRachel: 'I've named this: {auto_name}'")
                name_edit = input(f"Accept name? (Enter to keep, or type a new name): ").strip()
                final_name = name_edit if name_edit else auto_name

                vibe = input("What's the vibe? (e.g., 'floral', 'retro', or Enter to skip): ").strip()
                
                metadata = {
                    "item_name": final_name,
                    "category": final_category,
                    "sub_category": sub_category,
                    "vibe": vibe if vibe else "closet-staple"
                }
                
                ross.store_memory(img_filename, vector, metadata)
                print(f"✅ Success! {final_name} is now searchable in '{final_category}'.")
            else:
                print(f"❌ Error: Could not find '{image_path}' in the images folder.")

        elif choice == '2':
            # --- HIERARCHICAL SEARCH ---
            taxonomy = get_all_categories()
            categories = list(taxonomy.keys())

            print("\nWhere should Ross look?")
            print("0. Everywhere")
            for i, cat in enumerate(categories):
                print(f"{i+1}. {cat}")

            parent_choice = input("\nPick a category number: ").strip()
            selected_filter = None

            if parent_choice.isdigit() and 0 < int(parent_choice) <= len(categories):
                parent_cat = categories[int(parent_choice)-1]
                sub_cats = taxonomy.get(parent_cat, [])

                if sub_cats:
                    print(f"\nNarrow it down for {parent_cat}?")
                    print("0. Search all " + parent_cat)
                    for j, sub in enumerate(sub_cats):
                        print(f"{j+1}. {sub}")
                    
                    sub_choice = input("\nPick a sub-category (or Enter for all): ").strip()
                    if sub_choice.isdigit() and 0 < int(sub_choice) <= len(sub_cats):
                        selected_filter = sub_cats[int(sub_choice)-1]
                    else:
                        selected_filter = parent_cat
                else:
                    selected_filter = parent_cat

            query = input(f"\nSearching in {selected_filter if selected_filter else 'Everywhere'}: ")
            search_vector = rachel.model.encode(query).tolist()
            
            # Ross applies the metadata filter to the vector search
            results = ross.find_match(search_vector, category_filter=selected_filter, top_k=3)
            
            if results:
                print(f"\n✨ Ross: 'I found {len(results)} matches for you!'")
                for i, match in enumerate(results):
                    score = round(match.get('score', 0) * 100, 1)
                    item = match['metadata'].get('item_name', 'Unknown Item')
                    vibe = match['metadata'].get('vibe', 'No vibe set')
                    
                    grammar = get_label_agreement(item) # Centralized grammar
                    is_ok, message = monica.validate_outfit(vibe, item)
                    
                    status_emoji = "✅" if is_ok else "⚠️"
                    print(f"{i+1}. {status_emoji} {grammar['selector'].capitalize()} {item} {grammar['verb']} a {score}% match")
                    print(f"   Vibe: {vibe}")
                    print(f"   {message}")
            else:
                print("\nRoss: 'I couldn't find anything matching that in that category.'")

        elif choice == '3':
            print("\nGoodbye! Stay stylish. ☕️\n")
            break

if __name__ == "__main__":
    main()