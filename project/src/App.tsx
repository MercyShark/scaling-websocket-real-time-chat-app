import { MessageInput } from '@/components/chat/message-input';
import { MessageList } from '@/components/chat/message-list';
import { Sidebar } from '@/components/layout/sidebar';

function App() {
  return (
    <div className="flex h-screen bg-zin-c-950">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <div className="h-14 border-b border-zinc-800 flex items-center px-4">
          <h1 className="text-xl font-semibold ">#general</h1>
        </div>
        <MessageList />
        <MessageInput />
      </main>
    </div>
  );
}

export default App;