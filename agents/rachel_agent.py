from sentence_transformers import SentenceTransformer
from PIL import Image

class RachelVisionAgent:
    def __init__(self):
        print("Rachel: 'Getting my designer glasses (Loading modern CLIP model)...'")
        # We use 'clip-ViT-L-14' because it perfectly outputs the 768 dimensions Ross needs!
        self.model = SentenceTransformer('clip-ViT-L-14')

    def scan_outfit(self, image_path):
        # Rachel looks at the photo
        img = Image.open(image_path)
        
        # She turns the photo into a 768-dimension vector
        embedding = self.model.encode(img)
        
        print(f"Rachel: 'Oh! This {image_path} is SO 90s. I've digitized it!'")
        
        # Convert to list for Ross and Pinecone
        return embedding.tolist()