#!/usr/bin/env python3
"""
Query script for Ollama RAG.
Computes similarity between query vector and index embeddings,
gathers context, and invokes local Ollama LLM to generate answers.
"""

import os
import json
import requests
import numpy as np
from dotenv import load_dotenv

# Load environment configurations
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "qwen2.5:1.5b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "qwen2-embedding:0.6b")
INDEX_PATH = os.path.join("data", "rag_index.json")

# Global variables to cache vector index
_index_cache = None


def load_vector_index():
    """
    Load vector index from data/rag_index.json.
    """
    global _index_cache
    if _index_cache is not None:
        return _index_cache
        
    if not os.path.exists(INDEX_PATH):
        print(f"⚠️ Vector index file {INDEX_PATH} not found. Please run ingest_rag.py first.")
        return []
        
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            _index_cache = json.load(f)
        print(f"Loaded {len(_index_cache)} chunks from vector index.")
        return _index_cache
    except Exception as e:
        print(f"Error loading vector index: {e}")
        return []


def cosine_similarity(v1, v2):
    """
    Calculate cosine similarity between two vectors.
    """
    a = np.array(v1)
    b = np.array(v2)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def get_query_embedding(query):
    """
    Fetch query embedding vector from Ollama API.
    """
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {
        "model": OLLAMA_EMBED_MODEL,
        "prompt": query
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json().get("embedding")
    except Exception as e:
        print(f"Error fetching embedding for query from Ollama: {e}")
        return None


def query_grounded_answer(query, category=None):
    """
    Retrieves top chunks matching the query and prompts Ollama LLM to generate
    a grounded guided response. Returns the text response or None if failed.
    """
    index = load_vector_index()
    if not index:
        return None
        
    query_vector = get_query_embedding(query)
    if not query_vector:
        return None
        
    # 1. Compute similarities
    scored_chunks = []
    for chunk in index:
        sim = cosine_similarity(query_vector, chunk["embedding"])
        scored_chunks.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "similarity": sim
        })
        
    # 2. Sort by similarity desc and select top-k
    scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
    top_chunks = scored_chunks[:4]
    
    # Check if similarity is too low (e.g. less than 0.20), meaning no relevance found
    if not top_chunks or top_chunks[0]["similarity"] < 0.15:
        print(f"⚠️ Low similarity threshold (top: {top_chunks[0]['similarity'] if top_chunks else 0.0}). RAG context skipped.")
        return None
        
    # 3. Format Context and Citations list
    context_parts = []
    citations = []
    seen_sources = set()
    
    for i, chunk in enumerate(top_chunks):
        context_parts.append(f"[Document {i+1}]: {chunk['content']}")
        src = chunk["source"]
        if src not in seen_sources:
            seen_sources.add(src)
            citations.append(src)
            
    context_str = "\n\n".join(context_parts)
    citations_str = ", ".join(citations)
    
    category_context = f"The primary category identified for this issue is: {category.replace('_', ' ').upper()}." if category else ""
    
    # 4. Formulate generation prompt
    prompt = f"""You are Judi, a supportive, expert student legal aid assistant in India.
Your task is to provide a grounded, compassionate, and structured legal preliminary guidance report based ONLY on the provided Legal Context and User Query.

Rules:
1. Do not make up or hallucinate any laws, sections, or details.
2. Only discuss the rules, sections, or procedures mentioned in the Legal Context below.
3. If the context does not contain enough information to address the query, state that and refer the user to the local police (112) or legal counsel.
4. Keep your explanation structured using bullet points, short paragraphs, and bold text.
5. Emphasize user safety, minor confidentiality under POCSO (if applicable), and clear action steps.

=============================
LEGAL CONTEXT (Grounded Sources)
=============================
{context_str}

=============================
ADDITIONAL CONTEXT
=============================
{category_context}

=============================
USER QUERY
=============================
{query}

=============================
JUDI GUIDED PRELIMINARY REPORT
=============================
"""

    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=45)
        response.raise_for_status()
        answer = response.json().get("response", "").strip()
        
        # Add citations format at the bottom
        citation_block = f"\n\n#### 🏛️ SOURCES & CITATIONS\n*Retrieved from grounded index:* {citations_str}"
        return f"{answer}{citation_block}"
    except Exception as e:
        print(f"Error generating answer from local Ollama: {e}")
        return None


def check_is_complaint_via_llm(query: str) -> bool:
    """
    Checks if the user query describes a legal complaint, violation, crime, 
    harassment, discrimination, or institutional misconduct.
    Returns True if it is a complaint, False otherwise.
    """
    lower_text = query.lower().strip()
    
    # Common greetings and simple sentiment phrases
    greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "how are you", "help", "info"}
    if lower_text in greetings:
        return False
        
    # Common non-complaint questions or opinions
    non_complaint_phrases = [
        "i don't like my college", "i dont like my college", 
        "i like my college", "i love my college",
        "who are you", "what is your name", "what do you do",
        "tell me a joke", "what is the capital", "how to study",
        "what is law", "what is ragging", "what is posho", "what is posh", "what is pocso"
    ]
    for phrase in non_complaint_phrases:
        if lower_text == phrase or lower_text.startswith(phrase + " ") or lower_text.endswith(" " + phrase):
            return False
            
    # If the text is very short (e.g. less than 3 words) and doesn't contain complaint indicators
    words = lower_text.split()
    if len(words) < 3:
        # Check if it contains critical keywords
        complaint_keywords = {"ragged", "ragging", "punched", "hit", "abuse", "abused", "harassed", "harassment", "assault", "assaulted", "threat", "threatened", "bribe", "bribed", "stolen", "steal", "doxxed", "doxx", "blackmail", "blackmailed"}
        if not any(w in complaint_keywords for w in words):
            return False

    url = f"{OLLAMA_BASE_URL}/api/generate"
    prompt = f"""Analyze the user query below. Determine if the user is describing a specific legal violation, incident, threat, harassment, abuse, discrimination, crime, or institutional grievance/misconduct that they want help with.
If the query is a simple greeting, general question, subjective opinion (like "I don't like my college"), statement of personal mood, or off-topic question, answer NO.
If it describes a specific incident of crime, abuse, harassment, discrimination, or violation, answer YES.

User Query: "{query}"

Answer ONLY "YES" or "NO":"""
    
    payload = {
        "model": OLLAMA_LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 5
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        answer = response.json().get("response", "").strip().upper()
        if "NO" in answer:
            return False
        return True
    except Exception as e:
        print(f"Ollama complaint validation skipped or failed: {e}")
        return True


if __name__ == "__main__":
    test_q = "my senior punched me on the campus and threatened me"
    print(f"Testing local query: '{test_q}'")
    ans = query_grounded_answer(test_q, "physical_assault")
    if ans:
        print("\n--- OLLAMA RAG RESPONSE ---")
        print(ans)
    else:
        print("Failed to run local RAG query. Ensure Ollama is running and ingest_rag.py has been executed.")
