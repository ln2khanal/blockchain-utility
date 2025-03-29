from pydantic import BaseModel


class Block(BaseModel):
    index: int
    timestamp: float
    previousHash: str
    hash: str
    nonce: int
