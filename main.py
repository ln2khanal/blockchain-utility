from fastapi import FastAPI, HTTPException
from models import Block

import os
import time

app = FastAPI()


blockchain = []


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


@app.get("/")
async def index():
    return {"message": "The blockchain peer app is running", "time": time.time()}


@app.post("/receiveBlock")
async def receive_block(block: Block):
    clear_screen()
    print(
        f"---\nReceived Block Index: {block.index}\nHash: {block.hash}\nNonce: {block.nonce}\n---"
    )

    # If blockchain is empty, accept the block as the first block
    if not blockchain:
        blockchain.append(block)
        return {
            "message": "Genesis block added successfully!",
            "block_index": block.index,
        }

    for i in range(len(blockchain)):
        if blockchain[i].index == block.index:
            raise HTTPException(
                status_code=400, detail="Block with this index already exists!"
            )

        if blockchain[i].index > block.index:
            if i == 0 or blockchain[i - 1].hash == block.previousHash:
                blockchain.insert(i, block)
                return {
                    "message": "Block inserted successfully!",
                    "block_index": block.index,
                }
            else:
                raise HTTPException(status_code=400, detail="Invalid previous hash!")

    if (
        blockchain[-1].hash == block.previousHash
        and blockchain[-1].index + 1 == block.index
    ):
        blockchain.append(block)
        return {"message": "Block appended successfully!", "block_index": block.index}

    raise HTTPException(status_code=400, detail="Invalid block sequence!")


@app.get("/getBlockchain")
async def get_blockchain():
    return blockchain


if __name__ == "__main__":
    import uvicorn

    print("Starting blockchain peer node...")
    uvicorn.run(__name__ + ":app", host="0.0.0.0", port=3000, reload=True)
