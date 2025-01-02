import { create } from "zustand";

interface User {
  name: string;
  email: string;
  connectedChannels: {};
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  setChannel: (channel: any) => void;
}

const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: 1,
    name: "rishabh",
    email: "rish@gmail.com",
    selectedChannel: null,
    connectedChannels: {
      group: [
        {
          channel_id: 1,
          channel_name: "tech",
          photo: null,
        },
      ],
      dm: [
        {
          channel_id: 2,
          channel_name: "sumit",
          photo:
            "https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=100&h=100&fit=crop",
        },
      ],
    },
  },
  token: null,
  isAuthenticated: false,
  setChannel: (channel) =>
    set((state) => ({ user: { ...state.user, selectedChannel: channel } })),
  login: (user, token) => set({ user, token, isAuthenticated: true }),
  logout: () => set({ user: null, token: null, isAuthenticated: false }),
}));

export default useAuthStore;
