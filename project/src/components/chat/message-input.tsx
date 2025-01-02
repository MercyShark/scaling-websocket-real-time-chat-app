import { SendHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useRef } from "react";

import { useSocketStore } from "@/store";

export function MessageInput() {
  const inputTextRef = useRef<HTMLTextAreaElement>(null);
  const addMessage = useSocketStore((state) => state.addMessage);
  return (
    <div className="p-4 border-t border-zinc-800">
      <div className="flex gap-2">
        <Textarea
          placeholder="Message #general"
          className="min-h-[80px] text-zinc-300 border-zinc-700"
          ref={inputTextRef}
        />
        <Button
          size="icon"
          className="h-auto"
          onClick={() => {
            const message = inputTextRef.current?.value; // return undefined if null
            if (message) {
              addMessage(message);
              inputTextRef.current!.value = ""; // it tells ts that you are sure that it will not be null
            }
          }}
        >
          <SendHorizontal className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
