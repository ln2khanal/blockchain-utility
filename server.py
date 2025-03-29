import asyncio
import websockets
import json


async def handle_connection(websocket):
    """Handles incoming WebSocket connections."""
    print(f"Connection from {websocket.remote_address}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received: {data}")

                # Process the received message (example: echo back)
                response = {"message": f"Echo: {data.get('message', 'No message')}"}
                await websocket.send(json.dumps(response))

            except json.JSONDecodeError:
                print(f"Invalid JSON: {message}")
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                print(f"Error processing message: {e}")
                await websocket.send(json.dumps({"error": "Internal server error"}))

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed normally from {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed abnormally from {websocket.remote_address}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print(f"Connection with {websocket.remote_address} closed.")


async def main():
    """Starts the WebSocket server."""
    host = "localhost"  # Or "0.0.0.0" to listen on all interfaces
    port = 8765

    async with websockets.serve(handle_connection, host, port):
        print(f"WebSocket server started at ws://{host}:{port}")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
