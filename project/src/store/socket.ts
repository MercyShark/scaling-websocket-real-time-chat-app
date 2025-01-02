import { create } from "zustand";
import { io, Socket } from "socket.io-client";
import useAuthStore from "./auth";
import axois from "axios";
interface SocketState {
  socket: Socket | null;
  messages: string[];
  connect: () => void;
  disconnect: () => void;
  addMessage: (message: string) => void;
}

const useSocketStore = create<SocketState>((set, get) => ({
  socket: null,
  messages: [],
  connect: () => {
    const socket = io("http://localhost:3000", {
      transports: ["websocket"], // Ensure WebSocket transport
    });

    const user = useAuthStore.getState().user;
    if (!user) return;

    console.log(user);
    const data = {
      email: user["email"],
      connectedChannels: user["connectedChannels"]["group"]
        .map((channel) => channel["channel_id"])
        .concat(
          user["connectedChannels"]["dm"].map(
            (channel) => channel["channel_id"]
          )
        ),
    };
    socket.emit("initialData", data);

    socket.on("message", (message) => {
      console.log("Received message", message);
      set((state) => ({ messages: [...state.messages, message] }));
    });

    console.log("Connected to server");

    set({ socket });
  },
  disconnect: () => {
    const socket = get().socket;
    socket?.disconnect();
    set((state) => {
      return { socket: null, messages: [] };
    });
  },
  addMessage: async (message) => {
    const socket = get().socket;
    const user = useAuthStore.getState().user;
    if (!socket || !user) return;

    // persistant of message is important
    axois
      .post("http://localhost:8080/send_message", {
        message,
        channel_id: user["selectedChannel"],
        user_id: user["id"],
      })
      .then((response) => {
        set((state) => ({ messages: [...state.messages, message] }));
      });

    // socket.emit("message", {
    //   channel: selectedChannel,
    //   message: message,
    // });
  },
}));

export default useSocketStore;
