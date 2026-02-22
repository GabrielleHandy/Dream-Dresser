# 👗 DreamDresser AI
### *Multi-Agent AI Orchestrator for Intelligent Fashion Retrieval*

---

## 🚀 Overview
DreamDresser AI is an agentic system designed to solve the "I have nothing to wear" problem using modern AI infrastructure. Instead of simple keyword matching, it uses **Semantic Search** to understand the "vibe" and utility of a closet.

## 🧠 The "Friends" Architecture
This project utilizes a multi-agent orchestration pattern where specialized agents handle distinct parts of the logic:

* **Vision Agent (Rachel):** Implements **CLIP (ViT-L/14)** via Hugging Face `sentence-transformers` for multi-modal feature extraction. She "sees" clothing items and converts them into 768-dimension vector embeddings.
* **Knowledge Agent (Ross):** Manages the long-term memory layer using a **Pinecone Serverless Vector Database**. Handles high-dimensional indexing, metadata filtering, and upsert operations.
* **Rule Agent (Monica - *In Progress*):** The logic guardrail. She integrates with external APIs (OpenWeatherMap) to validate clothing suggestions against real-world constraints.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **AI Models:** OpenAI CLIP (via Sentence-Transformers)
- **Database:** Pinecone (Vector DB)
- **Infrastructure:** Serverless Architecture
- **Environment:** Dotenv for secure API management

## 📈 Why I Built This
This project serves as a technical demonstration of **Retrieval-Augmented Generation (RAG)** concepts and **Multi-Agent Orchestration**. It moves beyond basic "chatbots" to show how AI can interact with private datasets (a personal closet) and external real-world data (weather) to provide actionable insights.
