import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
from ross_agent import RossAgent
from rachel_agent import RachelVisionAgent

def main():
    # 1. Initialize our team
    ross = RossAgent()
    rachel = RachelVisionAgent()

    ross.wake_up()  # Ross wakes up and connects to Pinecone
    # 2. The Task: Rachel scans an outfit
    # Make sure you have a photo (like 'mom_blazer.jpg') in your folder!
    image_path = "images/test_photo.jpg" 
    
    if os.path.exists(image_path):
        # Rachel turns pixels into a 768-dimension vector
        outfit_vector = rachel.scan_outfit(image_path)
        
        # 3. Ross stores it in the cloud museum
        # We'll add some metadata so Chandler can track it
        metadata = {
            "item_name": "White Graphic Tshirt",
            "owner": "Mom",
            "vibe": "chill",
            "color": "White"
        }
        
        ross.store_memory("outfit_001", outfit_vector, metadata)
        print("Success: Rachel scanned it, Ross stored it!")

        # ... (Keep your previous code that uploads the photo) ...

    # 4. The Search: Let's see if Rachel can find what we just stored
    search_query = "something chill to wear" # You can change this to "white tshirt" too!
    print(f"Mom: 'Rachel, find me {search_query}.'")

    # Rachel turns the words into a vector
    search_vector = rachel.model.encode(search_query).tolist()

    # Ross 'pivots' through the database to find the closest match
    # (Check your ross_agent.py for a function like 'query' or 'recall_memory')
    results = ross.recall_memory(search_vector, top_k=1) 

    if results:
        match = results[0]
        print(f"Ross: 'I found it! It's the {match['metadata']['item_name']}.'")
        print(f"Vibe check: {match['metadata']['vibe']}")
    else:
        print(f"Rachel: 'Ugh, I can't find the file {image_path}. Is it at the dry cleaners?'")

# if __name__ == "__main__":
#     main()
