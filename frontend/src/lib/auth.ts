/**
 * Better Auth configuration for the Todo application.
 * Provides authentication state management and hooks.
 */

"use client";

import { tokenManager, type User } from "./api";

// Authentication helper functions
export const auth = {
  // Check if user is signed in
  isSignedIn: (): boolean => {
    return tokenManager.isAuthenticated();
  },

  // Get current user
  getUser: (): User | null => {
    return tokenManager.getUser();
  },

  // Sign up with email/password
  signUp: async (data: {
    email: string;
    username: string;
    password: string;
  }): Promise<{ user: User; token: string }> => {
    const response = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: data.email,
        password: data.password,
        username: data.username,
      }),
    });

    const result = await response.json();
    if (result.user && result.access_token) {
      tokenManager.setToken(result.access_token);
      tokenManager.setUser(result.user);
    }

    return { user: result.user, token: result.access_token } as { user: User; token: string };
  },

  // Sign in with email/password
  signIn: async (data: {
    email: string;
    password: string;
  }): Promise<{ user: User; token: string }> => {
    const response = await fetch("http://localhost:8000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: data.email,
        password: data.password,
      }),
    });

    const result = await response.json();
    if (result.user && result.access_token) {
      tokenManager.setToken(result.access_token);
      tokenManager.setUser(result.user);
    }

    return { user: result.user, token: result.access_token } as { user: User; token: string };
  },

  // Sign out
  signOut: async (): Promise<void> => {
    try {
      await fetch("http://localhost:8000/api/auth/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
    } catch (error) {
      console.error("Sign out error:", error);
    } finally {
      tokenManager.clearAuth();
    }
  },

  // Get session
  getSession: async () => {
    try {
      const response = await fetch("http://localhost:8000/api/auth/me", {
        headers: {
          Authorization: `Bearer ${tokenManager.getToken()}`,
        },
      });
      return await response.json();
    } catch {
      return null;
    }
  },
};

// React hook for authentication (simplified version)
export function useAuth() {
  const user = tokenManager.getUser();
  const isAuthenticated = tokenManager.isAuthenticated();

  return {
    user,
    isAuthenticated,
    isLoading: false,
  };
}
