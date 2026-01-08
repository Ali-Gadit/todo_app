---
name: nextjs-app-router
description: Creates Next.js 16+ applications using App Router with TypeScript, Tailwind CSS, and React 19. Covers file-based routing, server components, and API routes.
---

# Next.js App Router Skill

This skill creates production-ready Next.js 16+ applications using the App Router architecture with TypeScript and modern React patterns.

## Usage

When creating a Next.js frontend for the todo app, follow these patterns:

### File-Based Routing Structure

```
frontend/src/app/
├── layout.tsx              # Root layout with Providers wrapper
├── page.tsx                # Home/dashboard page (protected route)
├── globals.css             # Global styles with Tailwind imports
├── login/
│   └── page.tsx            # Login page
├── signup/
│   └── page.tsx            # Signup page
└── api/
    └── route.ts            # Next.js API routes (optional)
```

### Root Layout Pattern

```tsx
// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Todo App",
  description: "A modern full-stack todo application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Providers Component

```tsx
// frontend/src/app/providers.tsx
"use client";

import { AuthProvider } from "@/lib/auth";

export function Providers({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}
```

### Protected Route Component

```tsx
// frontend/src/components/ProtectedRoute.tsx
"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
```

### API Client with Axios Interceptors

```tsx
// frontend/src/lib/api.ts
import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Token manager for localStorage operations
export const tokenManager = {
  getToken: () => localStorage.getItem("auth_token"),
  setToken: (token: string) => localStorage.setItem("auth_token", token),
  removeToken: () => localStorage.removeItem("auth_token"),
};

// Request interceptor - add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenManager.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenManager.removeToken();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Tailwind Configuration

```ts
// frontend/tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
        },
        secondary: {
          500: "#8b5cf6",
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### API Endpoints Helper

```ts
// frontend/src/lib/api.ts (continued)
export const apiEndpoints = {
  auth: {
    register: "/auth/register",
    login: "/auth/login",
    logout: "/auth/logout",
    me: "/auth/me",
  },
  tasks: {
    list: "/tasks",
    create: "/tasks",
    get: (id: number) => `/tasks/${id}`,
    update: (id: number) => `/tasks/${id}`,
    delete: (id: number) => `/tasks/${id}`,
    stats: "/tasks/stats/summary",
  },
  users: {
    me: "/users/me",
  },
};
```

## Validation Checklist

- [ ] `npm run dev` starts dev server on port 3000
- [ ] Pages load without hydration errors
- [ ] Client components properly marked with `"use client"`
- [ ] API calls include JWT token in Authorization header
- [ ] 401 responses redirect to login page
- [ ] Responsive layout works on mobile/desktop
- [ ] Environment variables loaded correctly (NEXT_PUBLIC_*)

## Common Errors

| Error | Fix |
|-------|-----|
| Hydration mismatch | Use `"use client"` for components using hooks |
| Module not found | Check `tsconfig.json` path aliases (`@/*`) |
| 401 on API calls | Verify Axios interceptor is adding token |
| Styles not applying | Ensure `globals.css` imports Tailwind directives |

## Related Skills

- `fastapi-backend` - Python backend API
- `better-auth` - Authentication integration
- `postgresql-neon` - Database configuration
