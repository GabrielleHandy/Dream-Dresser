import os
import time
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Pinecone Client (v3.0+)
from pinecone import Pinecone, ServerlessSpec, PineconeException

# Configure structured logging (Senior trait: Observability)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RossAgent")

# FIX 1: Changed class name to match main.py and test block
class RossAgent:
    """
    Ross manages the long-term memory (Vector Database) for DreamDresser.
    He handles index creation, connection, and memory storage/retrieval.
    """

    def __init__(self, index_name: str = "dreamdresser-main", dimension: int = 768):
        """Initialize the Knowledge Agent."""
        load_dotenv() # Load environment variables from .env file
        
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            logger.critical("PINECONE_API_KEY not found in environment variables.")
            raise ValueError("Ross is on a break! (Missing API Key)")
            
        try:
            self.pc = Pinecone(api_key=self.api_key)
            self.index_name = index_name
            self.dimension = dimension
            self.index = None
            logger.info("Ross initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {e}")
            raise

    def wake_up(self) -> None:
        """Connects to Pinecone and ensures the specific index exists."""
        logger.info(f"Checking status of index: '{self.index_name}'...")
        try:
            existing_indexes = [i.name for i in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                logger.warning(f"Index '{self.index_name}' not found. Creating new index...")
                self._create_index()
            else:
                logger.info(f"Index '{self.index_name}' found. Connecting...")

            self.index = self.pc.Index(self.index_name)
        except PineconeException as e:
            logger.error(f"Pinecone connection error: {e}")
            raise

    def _create_index(self) -> None:
        """Internal method to handle index creation logic."""
        try:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)
            logger.info(f"Index '{self.index_name}' created and ready.")
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise


    def store_memory(self, vector_id: str, vector_values: List[float], metadata: Dict[str, Any] = None) -> bool:
        """Upserts a vector into the database (Creates/Updates)."""
        if not self.index:
            logger.error("Attempted to store memory before waking up Ross.")
            return False

        logger.info(f"Storing memory ID: {vector_id}")
        try:
            self.index.upsert(
                vectors=[{"id": vector_id, "values": vector_values, "metadata": metadata or {}}]
            )
            logger.info("Memory stored successfully.")
            return True
        except Exception as e:
            logger.error(f"Pivot! Failed to upsert memory: {e}")
            return False


    def find_match(self, search_vector: list, category_filter: str = None, top_k: int = 3):
        """Search with a verified return path."""
        query_filter = None
        
        if category_filter:
            query_filter = {
                "$or": [
                    {"category": {"$eq": category_filter}},
                    {"sub_category": {"$eq": category_filter}}
                ]
            }

        try:
            response = self.index.query(
                vector=search_vector,
                filter=query_filter,
                top_k=top_k,
                include_metadata=True
            )
            # Senior Move: Always check if matches exist before returning
            return response.get('matches', [])
            
        except Exception as e:
            logger.error(f"Ross: 'Pivot! Search failed: {e}'")
            return []


    def recall_memory(self, vector_id: str) -> Optional[Dict]:
        """Fetches a vector by ID to verify storage."""
        if not self.index:
            logger.error("Attempted to recall memory before waking up Ross.")
            return None

        logger.info(f"Recalling memory ID: {vector_id}...")
        try:
            result = self.index.fetch(ids=[vector_id])
            if result and result.vectors and vector_id in result.vectors:
                logger.info(f"Memory found. Metadata: {result.vectors[vector_id].metadata}")
                return result.vectors[vector_id]
            else:
                logger.warning("I have no memory of that.")
                return None
        except Exception as e:
            logger.error(f"Error recalling memory: {e}")
            return None



if __name__ == "__main__":
    import random
    
    # 1. Initialize
    ross = RossAgent(index_name="dreamdresser-v1")
    
    # 2. Connect
    ross.wake_up()

    # 3. Generate Dummy Data (Simulating Rachel's output)
    dummy_vector = [random.random() for _ in range(768)]
    test_id = "test_outfit_001"
    test_meta = {
        "description": "Red Sweater",
        "category": "Top",
        "owner": "Mom",
        "weather_suitability": "Cold"
    }
    
    # 4. Test Operations
    if ross.store_memory(test_id, dummy_vector, test_meta):
        time.sleep(2) 
        ross.recall_memory(test_id)