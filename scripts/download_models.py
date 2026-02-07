#!/usr/bin/env python3
"""Pre-download all models so first run doesn't need internet.

Run this once after install:
    python scripts/download_models.py
"""

import sys


def main():
    print("Downloading models for Astra...")
    print("This might take a while on the first run.\n")

    # chat model
    print("[1/3] Chat model (distilgpt2)...")
    from transformers import AutoTokenizer, AutoModelForCausalLM
    AutoTokenizer.from_pretrained("distilgpt2")
    AutoModelForCausalLM.from_pretrained("distilgpt2")
    print("      Done.\n")

    # embedding model
    print("[2/3] Embedding model (all-MiniLM-L6-v2)...")
    from sentence_transformers import SentenceTransformer
    SentenceTransformer("all-MiniLM-L6-v2")
    print("      Done.\n")

    # sentiment model
    print("[3/3] Sentiment model (distilbert-base-uncased-finetuned-sst-2-english)...")
    from transformers import pipeline
    pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print("      Done.\n")

    print("All models downloaded. You're good to go offline now.")


if __name__ == "__main__":
    main()
