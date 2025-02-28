from typing import List
from pydantic import BaseModel


class Block(BaseModel):
    index: int
    timestamp: float
    transactions: List[str]
    previousHash: str
    hash: str
    nonce: int
