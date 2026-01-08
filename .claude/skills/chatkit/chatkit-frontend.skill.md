---
name: chatkit-frontend
description: Creates ChatKit React frontend with complete configuration - hooks, theming, session management, popup layouts, and imperative helpers for AI chat interfaces.
---

# ChatKit Frontend Skill

This skill creates production-ready ChatKit React frontends with comprehensive configuration options, theming, and session management.

## Installation

```bash
npm install @openai/chatkit-react react react-dom
# or
yarn add @openai/chatkit-react react react-dom
```

## Project Structure

```
frontend/
├── index.html              # HTML with CDN script (REQUIRED)
├── package.json
├── vite.config.ts
├── tsconfig.json
└── src/
    ├── main.tsx            # Entry point
    ├── App.tsx             # Chat component
    └── components/
        └── Chat.tsx        # Reusable chat component
```

## Complete Chat Component

```tsx
// src/App.tsx - Full ChatKit implementation
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';

interface ChatProps {
  initialThreadId?: string;
  onThreadChange?: (threadId: string | null) => void;
}

export default function App({ initialThreadId, onThreadChange }: ChatProps) {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  // Restore thread from localStorage or props
  useEffect(() => {
    const saved = localStorage.getItem('chatkit-thread-id');
    setThreadId(saved || initialThreadId || null);
    setIsReady(true);
  }, [initialThreadId]);

  const { control, sendUserMessage, focusComposer, setThreadId, setComposerValue } = useChatKit({
    api: {
      // REQUIRED: Get client secret from backend
      async getClientSecret(existingSecret?: string) {
        if (existingSecret) {
          // Refresh expired session
          const res = await fetch('/api/chatkit/refresh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: existingSecret }),
          });
          const { client_secret } = await res.json();
          return client_secret;
        }

        // Create new session
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    // Optional: Start with specific thread
    initialThread: threadId,
    // Theme customization
    theme: {
      colorScheme: 'dark',
      color: {
        accent: { primary: '#4cc9f0', level: 1 },
        grayscale: { hue: 220, tint: 6, shade: -1 },
        surface: {
          background: '#16213e',
          foreground: '#ffffff',
        },
      },
      radius: 'round',
      density: 'normal',
      typography: {
        fontFamily: 'Inter, system-ui, sans-serif',
        baseSize: 16,
      },
    },
    // Start screen configuration
    startScreen: {
      greeting: 'Hello! How can I help you today?',
      prompts: [
        { label: 'Hello', prompt: 'Say hello and introduce yourself' },
        { label: 'Help', prompt: 'What can you help me with?' },
        { label: 'Code', prompt: 'Help me write some Python code' },
      ],
    },
    // Composer configuration
    composer: {
      placeholder: 'Type a message...',
      tools: [
        { id: 'format', label: 'Format', icon: 'text', pinned: true },
        { id: 'image', label: 'Image', icon: 'image' },
      ],
    },
    // Header customization
    header: {
      leftAction: {
        icon: 'settings-cog',
        onClick: () => console.log('Settings clicked'),
      },
    },
    // Handle thread changes
    onThreadChange: ({ threadId }) => {
      if (threadId) {
        localStorage.setItem('chatkit-thread-id', threadId);
        onThreadChange?.(threadId);
      } else {
        localStorage.removeItem('chatkit-thread-id');
        onThreadChange?.(null);
      }
    },
    // Error handling
    onError: ({ error }) => {
      console.error('ChatKit error:', error);
    },
  });

  if (!isReady) {
    return (
      <div style={{
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#1a1a2e',
        color: '#4cc9f0',
      }}>
        Loading ChatKit...
      </div>
    );
  }

  return <ChatKit control={control} className="h-screen w-full" />;
}
```

## index.html - REQUIRED CDN Script

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ChatKit App</title>
    <!-- CRITICAL: CDN script required for ChatKit -->
    <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #root { height: 100%; width: 100%; }
      body {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: #1a1a2e;
      }
      .h-screen { height: 100vh; }
      .w-full { width: 100%; }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## Reusable Chat Component

```tsx
// src/components/Chat.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useCallback } from 'react';

interface ChatProps {
  apiUrl?: string;
  theme?: 'dark' | 'light';
  height?: string;
  width?: string;
  onError?: (error: Error) => void;
}

export function Chat({
  apiUrl = '/chatkit',
  theme = 'dark',
  height = '600px',
  width = '400px',
  onError,
}: ChatProps) {
  const { control, sendUserMessage, focusComposer, setThreadId, setComposerValue } = useChatKit({
    api: {
      url: apiUrl,
      // For production, use getClientSecret for auth
      async getClientSecret() {
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    theme: {
      colorScheme: theme,
      color: {
        accent: { primary: '#4cc9f0', level: 1 },
        grayscale: { hue: 220, tint: 6, shade: -1 },
      },
      radius: 'round',
    },
    onError: ({ error }) => {
      onError?.(new Error(error.message));
    },
  });

  // Expose helper functions
  const sendMessage = useCallback((message: string) => {
    sendUserMessage(message);
  }, [sendUserMessage]);

  const focus = useCallback(() => {
    focusComposer();
  }, [focusComposer]);

  return <ChatKit control={control} style={{ height, width }} />;
}
```

## Popup Chat Layout

```tsx
// src/components/PopupChat.tsx - Floating chat button with popup
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';

export function PopupChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('chatkit-thread-id');
    setThreadId(saved);
  }, []);

  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    initialThread: threadId,
    theme: {
      colorScheme: 'dark',
      color: {
        accent: { primary: '#4361ee', level: 1 },
      },
      radius: 'round',
    },
    onThreadChange: ({ threadId }) => {
      if (threadId) localStorage.setItem('chatkit-thread-id', threadId);
    },
  });

  return (
    <div style={{ position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 9999 }}>
      {/* Chat Popup */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            onClick={() => setIsOpen(false)}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0,0,0,0.3)',
              zIndex: -1,
            }}
          />
          {/* Popup Window */}
          <div style={{
            width: '420px',
            height: '600px',
            background: '#16213e',
            borderRadius: '1rem',
            boxShadow: '0 10px 50px rgba(0,0,0,0.5)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            animation: 'popupIn 0.2s ease-out',
          }}>
            {/* Header */}
            <div style={{
              padding: '1rem',
              background: '#0f3460',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}>
              <span style={{ color: '#4cc9f0', fontWeight: 'bold' }}>Assistant</span>
              <button
                onClick={() => {
                  localStorage.removeItem('chatkit-thread-id');
                  setThreadId(null);
                }}
                style={{
                  padding: '0.25rem 0.5rem',
                  background: '#4361ee',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.25rem',
                  cursor: 'pointer',
                  fontSize: '0.75rem',
                }}
              >
                New Chat
              </button>
            </div>
            {/* Chat */}
            <div style={{ flex: 1, overflow: 'hidden' }}>
              <ChatKit control={control} className="h-full w-full" />
            </div>
          </div>
        </>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: isOpen ? '#16213e' : 'linear-gradient(135deg, #4361ee, #4cc9f0)',
          border: 'none',
          cursor: 'pointer',
          boxShadow: '0 4px 20px rgba(76, 201, 240, 0.4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4cc9f0" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        ) : (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        )}
      </button>

      <style>{`
        @keyframes popupIn {
          from { opacity: 0; transform: scale(0.9) translateY(20px); }
          to { opacity: 1; transform: scale(1) translateY(0); }
        }
      `}</style>
    </div>
  );
}
```

## Imperative Helpers

```tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';

function ChatWithControls() {
  const {
    control,
    sendUserMessage,
    focusComposer,
    setThreadId,
    setComposerValue,
    fetchUpdates,
    sendCustomAction,
  } = useChatKit({
    api: { url: '/chatkit' },
  });

  const handleSendQuickMessage = () => {
    sendUserMessage('Hello! Quick test message.');
  };

  const handleFocus = () => {
    focusComposer();
  };

  const handleSetValue = () => {
    setComposerValue('Pre-filled message...');
  };

  const handleNewThread = () => {
    setThreadId(null); // Creates new thread
  };

  const handleRefresh = async () => {
    await fetchUpdates(); // Refresh thread data
  };

  return (
    <div>
      <ChatKit control={control} className="h-[600px] w-[400px]" />
      <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
        <button onClick={handleSendQuickMessage}>Send Test</button>
        <button onClick={handleFocus}>Focus Input</button>
        <button onClick={handleSetValue}>Set Value</button>
        <button onClick={handleNewThread}>New Thread</button>
        <button onClick={handleRefresh}>Refresh</button>
      </div>
    </div>
  );
}
```

## Theme Configuration

```typescript
const { control } = useChatKit({
  api: { url: '/chatkit' },
  theme: {
    colorScheme: 'dark', // 'dark' or 'light'
    color: {
      accent: {
        primary: '#4cc9f0', // Main accent color
        level: 1, // 1-3 for shades
      },
      grayscale: {
        hue: 220, // Color hue (0-360)
        tint: 6, // Lightness adjustment
        shade: -1, // Darkness adjustment
      },
      surface: {
        background: '#16213e', // Chat background
        foreground: '#ffffff', // Text color
      },
    },
    radius: 'round', // 'round', 'soft', or 'none'
    density: 'normal', // 'compact', 'normal', or 'spacious'
    typography: {
      fontFamily: 'Inter, system-ui, sans-serif',
      baseSize: 16,
      fontSources: [
        {
          family: 'Inter',
          src: 'https://fonts.googleapis.com/css2?family=Inter:wggt@400;500;600;700',
          weight: '400 700',
          display: 'swap',
        },
      ],
    },
  },
});
```

## package.json

```json
{
  "name": "chatkit-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@openai/chatkit-react": "^1.3.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.7.2",
    "vite": "^6.0.3"
  }
}
```

## vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
});
```

## Validation Checklist

- [ ] CDN script added to index.html
- [ ] `domainKey: 'localhost'` for local dev
- [ ] Backend `/api/chatkit/session` endpoint exists
- [ ] Chat UI renders without blank screen
- [ ] Messages can be sent and received
- [ ] Thread persistence works (localStorage)
- [ ] Theming applies correctly
- [ ] Popup layout works (if used)
- [ ] Error handling is implemented

## Common Errors

| Error | Fix |
|-------|-----|
| Blank screen | Add CDN script to index.html |
| `FatalAppError: Invalid input at api` | Add `domainKey: 'localhost'` or implement `getClientSecret` |
| `Unrecognized key "name"` in prompts | Use `label` not `name` |
| `Unrecognized key "icon"` | Remove `icon` property |
| CORS error | Configure backend CORS for frontend origin |
| 401 Unauthorized | Implement proper session/auth on backend |

## Related Skills

- `chatkit-backend` - Python backend implementation
- `chatkit-store` - Conversation storage
- `chatkit-agent-memory` - Agent with conversation history
