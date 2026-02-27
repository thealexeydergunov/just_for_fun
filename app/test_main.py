import asyncio
import os

from tests.load_fake_data import load_fake_data

if __name__ == "__main__":
    if os.getenv("LOAD_FAKE_DATA"):
        asyncio.run(load_fake_data())
