import { SendHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

export function MessageInput() {
  return (
    <div className="p-4 border-t border-zinc-800">
      <div className="flex gap-2">
        <Textarea
          placeholder="Message #general"
          className="min-h-[80px] text-zinc-300 border-zinc-700"
        />
        <Button size="icon" className="h-auto">
          <SendHorizontal className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}