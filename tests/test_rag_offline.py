#!/usr/bin/env python3
"""
Offline dry-run and mock test for local Ollama RAG integration.
Mocks HTTP calls to verify embedding generation, vector similarity search,
and RAG prompt formatting.
"""

import sys
import os
import unittest
import requests
from unittest.mock import patch, MagicMock

# Insert nlp directory into path for local imports
sys.path.insert(0, "nlp")
sys.path.insert(0, ".")

import ingest_rag
import query_rag


class TestLocalRAGMocked(unittest.TestCase):

    def setUp(self):
        self.test_query = "my senior punched me in the hostel"
        self.dummy_embedding = [0.1] * 1024  # 1024-dim dummy vector
        self.dummy_rag_response = "This is a mocked legal response."

    @patch('requests.post')
    def test_get_embedding(self, mock_post):
        # Setup mock response for Ollama embeddings endpoint
        mock_response = MagicMock()
        mock_response.json.return_value = {"embedding": self.dummy_embedding}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        vector = ingest_rag.get_embedding("test text")
        self.assertEqual(vector, self.dummy_embedding)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_query_grounded_answer(self, mock_post):
        # Setup mock responses for embeddings and generate endpoints
        mock_embed_resp = MagicMock()
        mock_embed_resp.json.return_value = {"embedding": self.dummy_embedding}
        mock_embed_resp.raise_for_status = MagicMock()
        
        mock_gen_resp = MagicMock()
        mock_gen_resp.json.return_value = {"response": "Guided report details"}
        mock_gen_resp.raise_for_status = MagicMock()
        
        mock_post.side_effect = [mock_embed_resp, mock_gen_resp]
        
        # Setup mock vector index in memory
        query_rag._index_cache = [
            {
                "content": "Seniors ragged me in the hostel.",
                "source": "ugc_rules.md",
                "embedding": self.dummy_embedding
            }
        ]
        
        ans = query_rag.query_grounded_answer(self.test_query, "ragging")
        self.assertIsNotNone(ans)
        self.assertIn("Guided report details", ans)
        self.assertIn("SOURCES & CITATIONS", ans)


if __name__ == "__main__":
    print("Running Offline Mock Test Suite for Local RAG...")
    unittest.main()
