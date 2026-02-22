import os
import sys
# Ensure Python can find the agents folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from ross_agent import RossAgent
from rachel_agent import RachelVisionAgent

def main():
    print("\n--- 👗 WELCOME TO DREAMDRESSER AI ---")
    
    # 1. Initialize our team
    ross = RossAgent()
    ross.wake_up() 
    rachel = RachelVisionAgent()
    
    while True:
        print("\nWhat would you like to do?")
        print("1. [Scan] Add a new photo to the closet")
        print("2. [Search] Find an outfit using words")
        print("3. [Exit]")
        
        choice = input("\nEnter choice (1, 2, or 3): ").strip()

        if choice == '1':
            # --- SCAN MODE ---
            img_filename = input("Enter the image filename (e.g., test_photo.jpg): ").strip()
            image_path = os.path.join("images", img_filename)

            if os.path.exists(image_path):
                item_name = input("What is this item? (e.g., Red Silk Scarf): ")
                vibe = input("What's the vibe? (e.g., fancy, 90s, chill): ")
                
                print("\nRachel is scanning...")
                vector = rachel.scan_outfit(image_path)
                
                metadata = {
                    "item_name": item_name,
                    "vibe": vibe,
                    "owner": "Mom"
                }
                
                # Ross stores it
                ross.store_memory(img_filename, vector, metadata)
                print(f"✅ Success! {item_name} is now in the museum.")
            else:
                print(f"❌ Error: Could not find '{image_path}' in the images folder.")

        elif choice == '2':
            # --- SEARCH MODE ---
            query = input("\nMom, what are you looking for today? ")
            
            print(f"Searching for matches for: '{query}'...")
            search_vector = rachel.model.encode(query).tolist()
            
            # UPGRADE: We now ask for the top 3 matches
            results = ross.find_match(search_vector, top_k=3)
            
            if results and len(results) > 0:
                print(f"\n✨ Ross: 'I found {len(results)} matches for you!'")
                
                # We loop through each match found
                for i, match in enumerate(results):
                    score = round(match.get('score', 0) * 100, 1)
                    item = match['metadata'].get('item_name', 'Unknown Item')
                    vibe = match['metadata'].get('vibe', 'No vibe set')
                    
                    print(f"{i+1}. {item} ({score}% match)")
                    print(f"   Vibe: {vibe}")
            else:
                print("\nRoss: 'I couldn't find anything. Maybe it's at the dry cleaners?'")
        elif choice == '3':
            print("\nGoodbye! Stay stylish. ☕️\n")
            break
        else:
            print("Invalid choice. Please pick 1, 2, or 3.")

if __name__ == "__main__":
    main()