import asyncio
import websockets
import json
import random


class Peer:
    def __init__(self, host, port, known_peers=None):
        self.host = host
        self.port = port
        self.known_peers = known_peers or []
        self.peers = set()

    async def start_server(self):
        async def handler(websocket, path):
            self.peers.add(websocket)
            print(f"Peer connected: {websocket.remote_address}")
            try:
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        print(f"Received from {websocket.remote_address}: {data}")
                        await self.broadcast(data, websocket)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {message}")
            except websockets.exceptions.ConnectionClosed:
                print(f"Peer disconnected: {websocket.remote_address}")
            finally:
                self.peers.remove(websocket)

        async with websockets.serve(handler, self.host, self.port):
            print(f"Server started at ws://{self.host}:{self.port}")
            await asyncio.Future()

    async def connect_to_peers(self):
        for peer_url in self.known_peers:
            try:
                websocket = await websockets.connect(peer_url)
                self.peers.add(websocket)
                print(f"Connected to peer: {peer_url}")
            except Exception as e:
                print(f"Failed to connect to {peer_url}: {e}")

    async def broadcast(self, message, sender):
        for peer in self.peers:
            if peer != sender:
                try:
                    await peer.send(json.dumps(message))
                    print(f"Forwarded to {peer.remote_address}: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print(
                        f"Failed to forward to disconnected peer: {peer.remote_address}"
                    )
                    self.peers.discard(peer)

    async def send(self, message):
        for peer in self.peers:
            try:
                await peer.send(json.dumps(message))
                print(f"Sent to {peer.remote_address}: {message}")
            except websockets.exceptions.ConnectionClosed:
                print(f"Failed to send to disconnected peer: {peer.remote_address}")
                self.peers.discard(peer)


async def main():
    host = "localhost"
    port = int(input("Enter port: "))
    known_peers = []

    if port != 5000:  # 5000 is the bootstrap node
        known_peers.append("ws://localhost:5000")

    peer = Peer(host, port, known_peers)

    server_task = asyncio.create_task(peer.start_server())
    await asyncio.sleep(1)  # give server time to start.

    if known_peers:
        await peer.connect_to_peers()

    while True:
        message = input("Enter message: ")
        await peer.send({"message": message, "from": f"{peer.host}:{peer.port}"})


if __name__ == "__main__":
    asyncio.run(main())
