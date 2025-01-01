import { ScrollArea } from '@/components/ui/scroll-area';

interface Message {
  id: string;
  user: {
    name: string;
    avatar: string;
  };
  content: string;
  timestamp: string;
}

const messages: Message[] = [
  {
    id: '1',
    user: {
      name: 'Sarah Johnson',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
    },
    content: 'Hey everyone! Just wanted to share that we\'ll be having our team meeting tomorrow at 10 AM.',
    timestamp: '11:30 AM',
  },
  {
    id: '2',
    user: {
      name: 'Mike Chen',
      avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=100&h=100&fit=crop',
    },
    content: 'Thanks for the heads up! I\'ll prepare the project updates.',
    timestamp: '11:32 AM',
  },
  {
    id: '3',
    user: {
      name: 'Alex Kim',
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&h=100&fit=crop',
    },
    content: 'Perfect timing. I have some exciting news to share about the new feature launch.',
    timestamp: '11:35 AM',
  },
];

export function MessageList() {
  return (
    <ScrollArea className="flex-1 p-4">
      <div className="space-y-6">
        {messages.map((message) => (
          <div key={message.id} className="flex items-start">
            <img
              src={message.user.avatar}
              alt={message.user.name}
              className="w-10 h-10 rounded mr-3"
            />
            <div>
              <div className="flex items-baseline">
                <span className="font-semibold mr-2">{message.user.name}</span>
                <span className="text-sm text-zinc-500">{message.timestamp}</span>
              </div>
              <p className="text-zinc-900">{message.content}</p>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
}