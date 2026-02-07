"use client";

import { useState, useEffect } from "react";
import { MessageSquare, X } from "lucide-react";
import ChatPanel from "./ChatPanel";
import { useAuth } from "@/lib/auth";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || !isAuthenticated) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* Chat Window */}
      {isOpen && (
        <div className="mb-4 w-[380px] h-[550px] rounded-xl shadow-2xl border border-neutral-200 overflow-hidden bg-white flex flex-col transition-all duration-300 transform origin-bottom-right">
          <div className="bg-blue-600 px-4 py-3 flex justify-between items-center text-white">
            <div className="flex items-center gap-2">
              <MessageSquare size={18} />
              <span className="font-medium text-sm">AI Assistant</span>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="hover:bg-white/20 p-1 rounded-full"
            >
              <X size={18} />
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatPanel />
          </div>
        </div>
      )}

      {/* FAB */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 rounded-full shadow-lg flex items-center justify-center bg-blue-600 text-white hover:bg-blue-700 transition-all active:scale-90"
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </button>
    </div>
  );
}