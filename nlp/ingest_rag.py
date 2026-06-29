#!/usr/bin/env python3
"""
Ingestion script for Ollama RAG.
Parses local legal Markdown documents and existing JSON databases,
generates embeddings using the local Ollama API, and saves the vector index.
"""

import os
import json
import re
import requests
import numpy as np
from dotenv import load_dotenv

# Load environment configurations
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "qwen2-embedding:0.6b")
INDEX_PATH = os.path.join("data", "rag_index.json")
DOCS_DIR = os.path.join("data", "legal_docs")


def split_text(text, chunk_size=700, overlap=120):
    """
    Split text into overlapping chunks, attempting to split at sentences or paragraphs.
    """
    # Clean up excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Simple sliding window chunker
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
            
        # Try to find a sentence boundary or space to split on
        split_pos = -1
        # Look backwards up to 80 chars for a period or newline
        for pos in range(end, max(start, end - 80), -1):
            if text[pos] in ['.', '?', '!', '\n']:
                split_pos = pos + 1
                break
        
        if split_pos == -1:
            # Fall back to space boundary
            for pos in range(end, max(start, end - 40), -1):
                if text[pos] == ' ':
                    split_pos = pos
                    break
        
        if split_pos == -1:
            split_pos = end
            
        chunks.append(text[start:split_pos].strip())
        start = split_pos - overlap
        
    return chunks


def get_embedding(text):
    """
    Get embedding vector for a given text prompt from local Ollama API.
    """
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {
        "model": OLLAMA_EMBED_MODEL,
        "prompt": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("embedding")
    except Exception as e:
        print(f"Error fetching embedding for text '{text[:30]}...': {e}")
        return None


def main():
    print("Starting RAG Ingestion Pipeline...")
    print(f"Ollama URL: {OLLAMA_BASE_URL}")
    print(f"Embedding Model: {OLLAMA_EMBED_MODEL}")
    
    documents = []
    
    # 1. Parse markdown legal documents from data/legal_docs/
    if os.path.exists(DOCS_DIR):
        for filename in os.listdir(DOCS_DIR):
            if filename.endswith(".md"):
                file_path = os.path.join(DOCS_DIR, filename)
                print(f"Reading doc: {filename}...")
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                chunks = split_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "content": chunk,
                        "source": f"{filename} (Section {i+1})"
                    })
    else:
        print(f"Warning: Document directory {DOCS_DIR} not found.")

    # 2. Parse existing JSON knowledge base as a starter index
    # Law mappings
    law_map_path = os.path.join("data", "law_mapping_enhanced.json")
    if os.path.exists(law_map_path):
        print("Parsing law_mapping_enhanced.json...")
        with open(law_map_path, encoding="utf-8") as f:
            law_data = json.load(f)
        for cat, mapping in law_data.items():
            category_clean = cat.replace("_", " ").title()
            for law in mapping.get("laws", []):
                content = f"Category: {category_clean}. Act: {law.get('act', '')}. Section: {law.get('section', '')}. Title: {law.get('title', '')}. Description: {law.get('description', '')}"
                documents.append({
                    "content": content,
                    "source": f"law_mapping_enhanced.json ({category_clean} - Section {law.get('section', '')})"
                })
            steps = " -> ".join(mapping.get("filing_procedure", []))
            if steps:
                documents.append({
                    "content": f"Filing procedure for {category_clean}: {steps}",
                    "source": f"law_mapping_enhanced.json ({category_clean} - Procedures)"
                })

    # Resources
    resources_path = os.path.join("data", "resources.json")
    if os.path.exists(resources_path):
        print("Parsing resources.json...")
        with open(resources_path, encoding="utf-8") as f:
            res_data = json.load(f)
        for cat, contacts in res_data.items():
            category_clean = cat.replace("_", " ").title()
            for contact_type in ["police_stations", "helplines", "legal_aid"]:
                for item in contacts.get(contact_type, []):
                    content = f"Support Resource for {category_clean}. Name: {item.get('name', '')}. Details: {item.get('description', '')}. Contact: {item.get('contact', '')}. URL: {item.get('link', '')}"
                    documents.append({
                        "content": content,
                        "source": f"resources.json ({category_clean} - {contact_type})"
                    })

    # Case laws
    case_laws_path = os.path.join("data", "case_laws.json")
    if os.path.exists(case_laws_path):
        print("Parsing case_laws.json...")
        with open(case_laws_path, encoding="utf-8") as f:
            case_data = json.load(f)
        for cat, cases in case_data.items():
            category_clean = cat.replace("_", " ").title()
            for case in cases:
                if isinstance(case, str):
                    documents.append({
                        "content": f"Landmark Case Law for {category_clean}: {case}",
                        "source": f"case_laws.json ({category_clean})"
                    })
                elif isinstance(case, dict):
                    content = f"Landmark Case Law for {category_clean}. Case: {case.get('name', '') or case.get('title', '')}. Details: {case.get('description', '') or case.get('summary', '')}"
                    documents.append({
                        "content": content,
                        "source": f"case_laws.json ({category_clean})"
                    })

    print(f"Total documents/chunks parsed: {len(documents)}")
    
    # 3. Fetch embeddings and index chunks
    indexed_data = []
    print("\nGenerating embeddings via Ollama (this might take a few minutes)...")
    for idx, doc in enumerate(documents):
        if idx % 50 == 0:
            print(f"Processing chunk {idx}/{len(documents)}...")
            
        vector = get_embedding(doc["content"])
        if vector is not None:
            indexed_data.append({
                "content": doc["content"],
                "source": doc["source"],
                "embedding": vector
            })
            
    # 4. Save to json file
    if indexed_data:
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(indexed_data, f, ensure_ascii=False, indent=2)
        print(f"\nIndex successfully created! Saved {len(indexed_data)} items to {INDEX_PATH}")
    else:
        print("\nFailed to generate any embeddings. Make sure Ollama is running and the model is pulled.")


if __name__ == "__main__":
    main()
