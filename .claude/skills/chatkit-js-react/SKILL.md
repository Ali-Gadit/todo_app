---
name: ChatKit JS React
description: ChatKit React UI library for building real-time chat interfaces with streaming support. Use when building React applications that need (1) chat UI components, (2) real-time message streaming, (3) theme customization, (4) client tool callbacks for UI actions, (5) integration with chat APIs, or (6) production-ready chat interfaces. Provides useChatKit React hook, ChatKit component, theme system, and event handling patterns.
---

# ChatKit JS React

OpenAI's ChatKit React library for building production-ready chat interfaces with real-time streaming, theming, and client tool support.

## Quick Start

### Installation

```bash
npm install @openai/chatkit-react
```

### Basic Setup

```typescript
import { useChatKit, ChatKit } from "@openai/chatkit-react";

function ChatApp() {
  const chatkit = useChatKit({
    api: {
      url: "http://localhost:8000/chatkit",
      domainKey: "your-domain-key"
    },
    theme: {
      colorScheme: "light",
      color: {
        grayscale: { hue: 220, tint: 6, shade: -4 },
        accent: { primary: "#0f172a", level: 1 },
      },
      radius: "round",
    },
    startScreen: {
      greeting: "Welcome to ChatKit!",
      prompts: ["Hello", "Help me", "Show options"],
    },
    onClientTool: handleClientTools,
    onError: handleErrors,
  });

  return <ChatKit control={chatkit.control} className="h-full w-full" />;
}
```

## Core Components

### useChatKit Hook

Initialize ChatKit with configuration. Returns control object for managing the chat instance.

```typescript
const chatkit = useChatKit(config);
chatkit.control.sendMessage(text);
```

### ChatKit Component

Renders the chat UI. Pass the control object from useChatKit.

```typescript
<ChatKit
  control={chatkit.control}
  className="h-full w-full"
/>
```

## Configuration

### API Configuration

```typescript
api: {
  url: "http://localhost:8000/chatkit",    // Backend endpoint
  domainKey: "your-domain-key",             // Domain allowlist key
  headers?: {                               // Optional headers
    "Authorization": "Bearer token"
  }
}
```

### Theme Configuration

```typescript
theme: {
  colorScheme: "light" | "dark" | "auto",   // Theme mode
  color: {
    grayscale: {
      hue: 0-360,                           // Hue rotation
      tint: 1-12,                           // Number of tint levels
      shade: -4 to 4,                       // Shade adjustment
    },
    accent: {
      primary: "#0f172a",                   // Primary accent color
      secondary?: "#64748b",                // Optional secondary
      level: 1,                             // Accent intensity
    },
  },
  radius: "round" | "moderate" | "sharp",   // Border radius style
}
```

### Start Screen Configuration

```typescript
startScreen: {
  greeting: "Welcome!",                     // Greeting message
  description?: "How can we help?",         // Optional description
  prompts: [                                // Quick start prompts
    "Tell me about yourself",
    "I need help",
    "Show me options",
  ],
}
```

### Event Callbacks

```typescript
{
  onClientTool: async (invocation) => ({   // Handle client-side tools
    success: boolean;
    [key: string]: any;
  }),
  onError: ({ error }) => void,            // Handle errors
  onMessage?: (message) => void,           // On message event
  onConnectionChange?: (connected) => void, // Connection status
}
```

## Client Tool Handling

Handle UI actions and local operations:

```typescript
async function handleClientTools(invocation) {
  switch (invocation.name) {
    case "switch_theme":
      document.documentElement.setAttribute(
        "data-theme",
        invocation.params.theme
      );
      return { success: true };

    case "save_preference":
      localStorage.setItem(
        "preference",
        JSON.stringify(invocation.params)
      );
      return { success: true };

    case "show_notification":
      console.log(invocation.params.message);
      // toast.success(invocation.params.message);
      return { success: true };

    default:
      return { success: false };
  }
}
```

## Error Handling

```typescript
function handleErrors({ error }) {
  console.error("ChatKit error:", error);

  if (error instanceof TypeError) {
    console.error("Connection error:", error.message);
  } else if (error instanceof ReferenceError) {
    console.error("Configuration error:", error.message);
  } else {
    console.error("Unexpected error:", error.message);
  }
}
```

## Project Setup

### Vite + React Setup

Create new project:

```bash
npm create vite@latest my-chat-app -- --template react
cd my-chat-app
npm install
npm install @openai/chatkit-react
```

### Development Server

Start dev server:

```bash
npm run dev
```

Server runs on `http://localhost:5173` by default.

### Configuration

Edit `vite.config.ts` for API proxy:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/chatkit': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

## Complete Example

Production-ready component:

```typescript
import React, { useState, useEffect } from "react";
import { useChatKit, ChatKit } from "@openai/chatkit-react";

export function ChatApp() {
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    return (localStorage.getItem("theme") || "light") as "light" | "dark";
  });

  useEffect(() => {
    localStorage.setItem("theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const chatkit = useChatKit({
    api: {
      url: process.env.REACT_APP_API_URL || "http://localhost:8000",
      domainKey: process.env.REACT_APP_DOMAIN_KEY || "default",
    },
    theme: {
      colorScheme: theme,
      color: {
        grayscale: {
          hue: 220,
          tint: 6,
          shade: theme === "dark" ? -1 : -4,
        },
        accent: {
          primary: theme === "dark" ? "#f1f5f9" : "#0f172a",
          level: 1,
        },
      },
      radius: "round",
    },
    startScreen: {
      greeting: "Welcome to ChatKit!",
      prompts: [
        "Tell me about yourself",
        "How can you help me?",
        "Show available options",
      ],
    },
    onClientTool: async (invocation) => {
      if (invocation.name === "switch_theme") {
        const newTheme = invocation.params.theme;
        setTheme(newTheme);
        return { success: true };
      }
      return { success: false };
    },
    onError: ({ error }) => {
      console.error("ChatKit Error:", error);
    },
  });

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-white dark:bg-gray-800 p-4 border-b">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Chat</h1>
          <button
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            className="px-3 py-1 rounded bg-gray-200 dark:bg-gray-700"
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-hidden">
        <ChatKit control={chatkit.control} className="h-full w-full" />
      </main>
    </div>
  );
}

export default ChatApp;
```

## Environment Variables

Required `.env`:

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DOMAIN_KEY=your-domain-key
```

## TypeScript Types

```typescript
interface ChatKitConfig {
  api: {
    url: string;
    domainKey: string;
    headers?: Record<string, string>;
  };
  theme: {
    colorScheme: "light" | "dark" | "auto";
    color: {
      grayscale: { hue: number; tint: number; shade: number };
      accent: { primary: string; secondary?: string; level: number };
    };
    radius: "round" | "moderate" | "sharp";
  };
  startScreen?: {
    greeting: string;
    description?: string;
    prompts: string[];
  };
  onClientTool?: (invocation: ClientToolInvocation) => Promise<ToolResult>;
  onError?: (error: { error: Error }) => void;
  onMessage?: (message: Message) => void;
  onConnectionChange?: (connected: boolean) => void;
}

interface ClientToolInvocation {
  name: string;
  params: Record<string, any>;
}

interface ToolResult {
  success: boolean;
  [key: string]: any;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp?: number;
}
```

## Styling

ChatKit uses CSS custom properties for styling:

```css
.chatkit-container {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  border-radius: 12px;
}

.chatkit-message {
  padding: 12px 16px;
  border-radius: 8px;
}

.chatkit-message--user {
  background-color: #0f172a;
  color: white;
}

.chatkit-message--assistant {
  background-color: #f1f5f9;
  color: #0f172a;
}

@media (prefers-color-scheme: dark) {
  .chatkit-message--assistant {
    background-color: #1e293b;
    color: #f1f5f9;
  }
}
```

## Common Patterns

### Theme Toggle

```typescript
const [theme, setTheme] = useState("light");

useEffect(() => {
  localStorage.setItem("chatkit-theme", theme);
}, [theme]);

// In config:
theme: { colorScheme: theme, ... }
```

### Error Boundary

```typescript
class ChatKitErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>Chat error occurred. Please reload.</div>;
    }
    return this.props.children;
  }
}

// Usage:
<ChatKitErrorBoundary>
  <ChatApp />
</ChatKitErrorBoundary>
```

### Custom Input Component

Override message input by extending ChatKit configuration:

```typescript
const chatkit = useChatKit({
  ...config,
  // Additional customization options
});
```

## Best Practices

1. **Always set domain key** for production API security
2. **Load theme from localStorage** for persistence across sessions
3. **Implement error boundaries** to catch rendering errors
4. **Use environment variables** for API configuration
5. **Handle network errors** in onError callback
6. **Test client tools thoroughly** before deployment
7. **Use TypeScript** for better type safety

## Troubleshooting

**Connection errors**: Check API URL and domain key match backend configuration

**Styling not applied**: Verify ChatKit CSS is imported and has sufficient specificity

**Client tools not firing**: Ensure onClientTool callback returns `{ success: true }` for successful tools

**Theme not persisting**: Verify localStorage is writable and useEffect dependencies are correct

## Production Deployment

For production:

1. Use environment variables for API URL and domain key
2. Enable CORS on backend
3. Set proper domain allowlist in backend
4. Add error tracking (Sentry, etc.)
5. Implement rate limiting on frontend
6. Cache theme preference locally
7. Monitor performance metrics

## Resources

- GitHub: https://github.com/openai/openai-chatkit-advanced-samples
- NPM: https://www.npmjs.com/package/@openai/chatkit-react
- OpenAI Agents: For backend integration
