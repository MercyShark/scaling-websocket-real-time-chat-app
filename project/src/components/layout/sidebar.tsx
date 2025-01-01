import { Hash, MessageSquare, Users } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

interface Channel {
  id: string;
  name: string;
}

interface DirectMessage {
  id: string;
  name: string;
  online: boolean;
}

const channels: Channel[] = [
  { id: '1', name: 'general' },
  { id: '2', name: 'random' },
  { id: '3', name: 'announcements' },
];

const directMessages: DirectMessage[] = [
  { id: '1', name: 'Sarah Johnson', online: true },
  { id: '2', name: 'Mike Chen', online: false },
  { id: '3', name: 'Alex Kim', online: true },
];

export function Sidebar() {
  return (
    <div className="w-64 bg-zinc-900 h-screen flex flex-col">
      <div className="p-4">
        <h2 className="text-xl font-bold text-white">Bolt Workspace</h2>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-4">
          <div className="mb-4">
            <h3 className="flex items-center text-sm font-semibold text-zinc-400 mb-2">
              <MessageSquare className="mr-2 h-4 w-4" />
              Channels
            </h3>
            {channels.map((channel) => (
              <button
                key={channel.id}
                className="flex items-center w-full px-2 py-1 text-zinc-400 hover:bg-zinc-800 rounded"
              >
                <Hash className="mr-2 h-4 w-4" />
                {channel.name}
              </button>
            ))}
          </div>
          <Separator className="my-4 bg-zinc-800" />
          <div>
            <h3 className="flex items-center text-sm font-semibold text-zinc-400 mb-2">
              <Users className="mr-2 h-4 w-4" />
              Direct Messages
            </h3>
            {directMessages.map((dm) => (
              <button
                key={dm.id}
                className="flex items-center w-full px-2 py-1 text-zinc-400 hover:bg-zinc-800 rounded"
              >
                <div className="relative mr-2">
                  <div className="w-2 h-2 rounded-full absolute -right-1 -bottom-1 bg-zinc-900">
                    <div
                      className={`w-1.5 h-1.5 rounded-full ${
                        dm.online ? 'bg-green-500' : 'bg-zinc-500'
                      }`}
                    />
                  </div>
                  <div className="w-4 h-4 bg-zinc-700 rounded-full" />
                </div>
                {dm.name}
              </button>
            ))}
          </div>
        </div>
      </ScrollArea>
    </div>
  );
}