import asyncio
import websockets

# Global variable for WebSocket connection
websocket_connection = None


async def connect_to_websocket():
    global websocket_connection  # Use the global variable
    uri = "ws://localhost:3000"  # Replace with your WebSocket server URI

    try:
        # Establish the WebSocket connection
        websocket_connection = await websockets.connect(uri)
        print("Connected to the WebSocket server")
    except Exception as e:
        print(f"Error while connecting: {e}")
        websocket_connection = None


async def send_message(message: str):
    global websocket_connection  # Use the global variable
    if websocket_connection:
        try:
            await websocket_connection.send(message)
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error while sending message: {e}")
    else:
        print("WebSocket connection is not established.")


async def disconnect_websocket():
    global websocket_connection  # Use the global variable
    if websocket_connection:
        try:
            await websocket_connection.close()
            print("Disconnected from the WebSocket server")
        except Exception as e:
            print(f"Error while disconnecting: {e}")
        finally:
            websocket_connection = None
    else:
        print("WebSocket connection is not established.")


# Main function to demonstrate usage
async def main():
    await connect_to_websocket()
    if websocket_connection:
        await send_message("Hello from Python client!")
        await disconnect_websocket()


# Run the main function
asyncio.run(main())
