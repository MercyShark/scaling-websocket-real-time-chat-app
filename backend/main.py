import os
import json
import socketio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
from contextlib import asynccontextmanager
from db import Database
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


class MessageCreateRequest(BaseModel):
    user_id: int
    channel_id: int
    message: str


db = None
sio = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global db
    global sio
    print("Starting up...")
    db = Database()

    sio = socketio.Client()

    # Event handler for successful connection
    @sio.event
    def connect():
        print("Connected to the Socket.IO server")

    # Event handler for disconnection
    @sio.event
    def disconnect():
        print("Disconnected from the Socket.IO server")

    # Event handler for receiving messages from the server
    @sio.event
    def message(data):
        print(f"Received message: {data}")

    # Event handler for connection error
    @sio.event
    def connect_error(data):
        print(f"Connection failed: {data}")

    # Connect to the Socket.IO server
    sio.connect("http://localhost:3000")

    app.state.my_resource = "Some resource"

    yield  # The application is running at this point

    # Shutdown logic here (e.g., close database connections)
    print("Shutting down...")
    db.close_all_connections()
    # Example: Clean up the resource
    del app.state.my_resource


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # HTTP methods (e.g., GET, POST)
    allow_headers=["*"],  # Allowed headers
)


@app.get("/users")
async def getUsers():
    data = []
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM users;""")
            all_rows = cur.fetchall()
            for row in all_rows:
                data.append(
                    {
                        "id": row[0],
                        "name": row[1],
                        "email": row[2],
                        "photo": row[3],
                        "password": row[4],
                        "created_at": row[5].strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": row[6].strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
        # Access the resource initialized during startup
    return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)


@app.get("/channels")
async def getUsers(user_id: int):
    data = {}
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT 
                        channels.id AS channel_id, 
                        channels.channel_type, 
                        channels.name,
                        'null' AS photo
                    FROM membership
                    JOIN channels 
                        ON channels.id = membership.channel_id 
                        AND channels.channel_type = 'group'
                    WHERE membership.user_id = %s
                    UNION
                    SELECT 
                        m.channel_id,
                        'dm' AS channel_type,
                        u.name AS name,
                        u.photo AS photo
                    FROM users u
                    JOIN (
                        SELECT user_id, channel_id
                        FROM membership
                        WHERE user_id != %s
                        AND channel_id IN (
                            SELECT channels.id
                            FROM membership
                            JOIN channels 
                                ON channels.id = membership.channel_id 
                                AND channels.channel_type = 'dm'
                            WHERE membership.user_id = %s
                        )
                    ) m 
                    ON u.id = m.user_id;
""",
                (user_id, user_id, user_id),
            )
            all_rows = cur.fetchall()
            for row in all_rows:
                print(row)
                if row[1] not in data:
                    data[row[1]] = []
                data[row[1]].append(
                    {
                        "channel_id": row[0],
                        "channel_name": row[2],
                        "photo": row[3] if row[3] != "null" else None,
                    }
                )
        # Access the resource initialized during startup
    return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)


@app.get("/message")
async def get_messages(channel_id: int):
    data = []
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """select users.name, users.photo, messages.message, messages.updated_at
                from messages
                join users on users.id = messages.user_id
                where messages.channel_id = %s
                order by messages.updated_at desc  
                limit 10""",
                (channel_id,),
            )
            all_rows = cur.fetchall()
            for row in all_rows:
                data.append(
                    {
                        "user": row[0],
                        "photo": row[1],
                        "message": row[2],
                        "updated_at": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
            # id = cur.fetchone()[0]
            # cur.execute("SELECT * FROM message_broker WHERE id = %s;", (id,))
            # receipt_id = cur.fetchone()[-1]
    return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)


@app.post("/send_message")
async def post_message(message: MessageCreateRequest):

    user_id = message.user_id
    channel_id = message.channel_id
    message = message.message
    try:

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO messages (user_id, channel_id, message) VALUES (%s, %s, %s) RETURNING id;",
                    (user_id, channel_id, message),
                )
                id = cur.fetchone()[0]

            conn.commit()

    except Exception as e:
        print(e)

    sio.emit(
        "apiservermessage",
        {"user_id": user_id, "channel_id": channel_id, "message": message},
    )
    return JSONResponse(
        content={"message": "Message sent successfully", "id": id},
        status_code=status.HTTP_200_OK,
    )


# @app.delete("/message/{receipt_handle}")
# async def delete_message(receipt_handle: str):
#     with db.get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute(
#                 "UPDATE message_broker SET deleted_at = CURRENT_TIMESTAMP WHERE receipt_handle = %s RETURNING id;",
#                 (receipt_handle,),
#             )
#             id = cur.fetchone()[0]
#     return JSONResponse(
#         content={"message": "Message deleted successfully", "id": id},
#         status_code=status.HTTP_200_OK,
#     )


# @app.get("/message")
# async def get_message():
#     with db.get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute(
#                 "SELECT * FROM message_broker WHERE deleted_at IS NULL AND picked_at IS NULL ORDER BY created_at ASC LIMIT 5 FOR UPDATE SKIP LOCKED;"
#             )
#             rows = cur.fetchall()
#             for row in rows:
#                 print("inside")
#                 if row:
#                     cur.execute(
#                         "UPDATE message_broker SET picked_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING receipt_handle;",
#                         (row[0],),
#                     )
#                     receipt_handle = cur.fetchone()[0]
#                     return JSONResponse(
#                         content={"message": row[1], "receipt_handle": receipt_handle},
#                         status_code=status.HTTP_200_OK,
#                     )
#             else:
#                 return JSONResponse(
#                     content={"message": "No message available"},
#                     status_code=status.HTTP_404_NOT_FOUND,
#                 )


if "__main__" == __name__:
    import uvicorn

    print(f"Starting Server at http://{os.getenv('HOST')}:{os.getenv('PORT')}")
    uvicorn.run("main:app", port=8080, reload=True, workers=4)
