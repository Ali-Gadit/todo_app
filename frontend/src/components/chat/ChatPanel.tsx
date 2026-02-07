"use client";

import React, { useEffect, useState, useMemo } from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useAuth } from "@/lib/auth";

const LOCAL_STORAGE_THREAD_ID_KEY = 'todo_chatkit_thread_id';

export default function ChatPanel() {
  const { user } = useAuth();
  const [initialThread, setInitialThread] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Official OpenAI ChatKit CDN - must be loaded for the component to work
    const SCRIPT_URL = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js";
    const existingScript = document.querySelector(`script[src="${SCRIPT_URL}"]`);
    
    if (!existingScript) {
      const script = document.createElement("script");
      script.src = SCRIPT_URL;
      script.async = true;
      document.head.appendChild(script);
    }

    const savedThread = typeof window !== 'undefined' 
      ? localStorage.getItem(`${LOCAL_STORAGE_THREAD_ID_KEY}_${user?.id}`) 
      : null;
    setInitialThread(savedThread);
    setIsReady(true);
  }, [user?.id]);

  const chatConfig = useMemo(() => ({
    api: {
      // Using the exact property names from your working example
      url: `http://localhost:8000/api/chat/${user?.id}/chat`,
      // Some versions require a domainKey starting with 'domain_pk_' to pass validation
      domainKey: 'domain_pk_placeholder_for_local_dev',
    },
    initialThreadId: initialThread || undefined,
    theme: {
      colorScheme: 'light' as const,
      color: {
        accent: { primary: '#2563eb', level: 1 },
      },
    },
    startScreen: {
      greeting: "Hello! I'm your Todo Assistant. How can I help you today?",
      prompts: [
        { label: "Show my tasks", prompt: "Show me all my tasks" },
        { label: "Add a task", prompt: "Add a task to buy groceries" },
      ],
    },
    onError: ({ error }: { error: any }) => {
      console.error('ChatKit error:', error);
    },
  }), [user?.id, initialThread]);

  const { control, threadId } = useChatKit(chatConfig);

  // Save threadId whenever it changes
  useEffect(() => {
    if (threadId && typeof window !== 'undefined' && user?.id) {
      localStorage.setItem(`${LOCAL_STORAGE_THREAD_ID_KEY}_${user.id}`, threadId);
    }
  }, [threadId, user?.id]);

  if (!isReady || !user) {
    return (
      <div className="h-full w-full flex items-center justify-center text-neutral-400 text-sm">
        Loading Chat...
      </div>
    );
  }

  return (
    <div className="h-full w-full bg-white relative">
      {/* 
        The ChatKit component from @openai/chatkit-react 
        internally handles the <openai-chatkit> web component.
      */}
      <ChatKit control={control} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}