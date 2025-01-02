import express from "express";
import http from "http";
import { Server } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new Server(server); // Initialize socket.io with the server

// Serve static files (if needed)
// app.use(express.static("public"));

// When a client connects

const onlineUser = {};

io.on("connection", (socket) => {
  // onlineUser[socket.id] = socket.id

  socket.on("initialData", (data) => {
    console.log(typeof data);
    console.log(data);
    onlineUser[socket.id] = {
      socket: socket,
      userEmail: data["email"],
      connectedChannels: data["connectedChannels"],
    };
  });

  //   console.log()

  // Emit a welcome message to the client
  socket.emit("message", "Welcome to the Socket.IO server!");

  socket.on("apiservermessage", (data) => {
    console.log(data);

    console.log("logging online user", onlineUser);
    Object.values(onlineUser).forEach((user) => {
      // console.log("logging user", user);
      // console.log(user);
      if (user.connectedChannels.includes(data.channel_id)) {
        console.log("sending message to user", user.userEmail);
        user.socket.emit("message", data.message);
      }
    });
  });
  // Listen for messages from the client
  socket.on("message", (data: { message: string; channel: number }) => {
    // console.log("Message from client:", data);
    // if(socket)
    // Broadcast message to all clients
    // io.emit("message", data);
  });

  // When the client disconnects
  socket.on("disconnect", () => {
    console.log("a user disconnected");
  });
});

// Start the server
server.listen(3000, () => {
  console.log("Server is running on http://localhost:3000");
});
