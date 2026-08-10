"""Benchmark: memory."""
import time
import asyncio

async def run_benchmark():
    start = time.time()
    # Benchmark logic
    await asyncio.sleep(0.1)
    elapsed = time.time() - start
    print(f"[memory] {elapsed:.3f}s")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
