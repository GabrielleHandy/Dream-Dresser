from sentence_transformers import SentenceTransformer, util
from PIL import Image
import torch
import logging

logger = logging.getLogger("RachelVisionAgent")

class RachelVisionAgent:
    def __init__(self):
        logger.info("Rachel: 'Putting on my designer glasses...'")
        # Uses the 768-dimension CLIP model for high-fidelity "vision"
        self.model = SentenceTransformer('clip-ViT-L-14')
        
        # Rachel's "Style Dictionary" - Added Floral for your search fix
        self.descriptors = ["Floral", "Striped", "Solid", "Cotton", "Leather", "Denim", "Vintage"]
        self.colors = ["Black", "White", "Red", "Blue", "Green", "Pink", "Yellow"]
        self.categories = ["Shirt", "Pants", "Skirt", "Dress", "Jacket", "Shoes", "Hat"]

    def detect_category(self, image_path):
        """Rachel identifies the type of clothing with a confidence score."""
        img = Image.open(image_path)
        img_emb = self.model.encode(img, convert_to_tensor=True)
        text_embs = self.model.encode(self.categories, convert_to_tensor=True)
        
        hits = util.semantic_search(img_emb, text_embs, top_k=1)[0]
        best_hit = hits[0]
        category_name = self.categories[best_hit['corpus_id']]
        confidence = round(best_hit['score'] * 100, 1)
        
        return category_name, confidence

    def scan_outfit(self, image_path):
        """Generates the 768-d vector for Ross to store in Pinecone."""
        img = Image.open(image_path)
        embedding = self.model.encode(img)
        return embedding.tolist()

    def generate_name(self, image_path, category):
        """Rachel suggests a descriptive name by checking colors and patterns."""
        img = Image.open(image_path)
        img_emb = self.model.encode(img, convert_to_tensor=True)

        # 1. Find the best color match
        color_embs = self.model.encode(self.colors, convert_to_tensor=True)
        color_hit = util.semantic_search(img_emb, color_embs, top_k=1)[0][0]
        best_color = self.colors[color_hit['corpus_id']]

        # 2. Find the best descriptor (e.g., Floral, Striped)
        desc_embs = self.model.encode(self.descriptors, convert_to_tensor=True)
        desc_hit = util.semantic_search(img_emb, desc_embs, top_k=1)[0][0]
        best_desc = self.descriptors[desc_hit['corpus_id']]
        
        # Senior Logic: If confidence is high, include the descriptor (like Floral)
        # Otherwise, stick to Color + Category to avoid 'hallucinations'
        if desc_hit['score'] > 0.22:
            return f"{best_color} {best_desc} {category}"
        
        return f"{best_color} {category}"