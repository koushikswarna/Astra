#!/usr/bin/env python3
"""Quick benchmark for generation speed.

Measures tokens/second for the configured model on the current device.
Useful for comparing CPU vs GPU performance or different models.

    python scripts/benchmark.py
"""

import time
import statistics


def main():
    from astra.models.generator import TextGenerator

    print("Loading model for benchmark...")
    gen = TextGenerator()
    print(f"Model: {gen.model_name} on {gen.device}\n")

    prompts = [
        "The meaning of life is",
        "Once upon a time in a land far away",
        "The best programming language is",
        "Artificial intelligence will",
        "In the year 2050, humans will",
    ]

    max_tokens = 50
    times = []
    token_counts = []

    print(f"Running {len(prompts)} generations ({max_tokens} tokens each)...\n")

    for i, prompt in enumerate(prompts):
        start = time.perf_counter()
        result = gen.generate(prompt, max_new_tokens=max_tokens)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        token_counts.append(result.completion_tokens)

        tokens_per_sec = result.completion_tokens / elapsed if elapsed > 0 else 0
        print(f"  [{i+1}] {elapsed:.2f}s, {result.completion_tokens} tokens, "
              f"{tokens_per_sec:.1f} tok/s")
        print(f"      {result.text[:60]}...\n")

    # summary
    avg_time = statistics.mean(times)
    total_tokens = sum(token_counts)
    total_time = sum(times)
    avg_tps = total_tokens / total_time if total_time > 0 else 0

    print(f"Average time per generation: {avg_time:.2f}s")
    print(f"Average tokens/sec: {avg_tps:.1f}")
    print(f"Total tokens generated: {total_tokens}")


if __name__ == "__main__":
    main()
