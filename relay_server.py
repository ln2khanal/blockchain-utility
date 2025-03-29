import asyncio

clients = []


async def handle_client(reader, writer):
    clients.append(writer)
    try:
        while data := await reader.read(1024):
            message = data.decode()
            print(f"Received message: {message}")
            for client in clients:
                if client != writer:
                    client.write(data)
                await client.drain()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(writer)
        writer.close()


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 9000)
    print("Server started on 127.0.0.1:9000")
    async with server:
        await server.serve_forever()


asyncio.run(main())
