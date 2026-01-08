/**
 * API client configuration for the Todo application.
 * Handles JWT token injection and request/response handling.
 */

import axios, { AxiosInstance, AxiosError } from "axios";

// API configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance with default config
export const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor - add JWT token to requests
apiClient.interceptors.request.use(
  (config) => {
    // Get token from storage
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const { status, data } = error.response;

      // Handle specific error cases
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          if (typeof window !== "undefined") {
            localStorage.removeItem("auth_token");
            localStorage.removeItem("user");
            // Only redirect if not already on login page
            if (!window.location.pathname.includes("/login")) {
              window.location.href = "/login";
            }
          }
          break;
        case 403:
          console.error("Forbidden: You don't have permission to access this resource");
          break;
        case 404:
          console.error("Resource not found");
          break;
        case 500:
          console.error("Server error: Please try again later");
          break;
      }

      return Promise.reject({
        status,
        message: (data as any)?.detail || "An error occurred",
        data,
      });
    } else if (error.request) {
      return Promise.reject({
        status: 0,
        message: "Network error: Please check your connection",
      });
    }

    return Promise.reject(error);
  }
);

// API helper functions
export const api = {
  // Auth endpoints
  auth: {
    register: (data: RegisterData) =>
      apiClient.post<AuthResponse>("/auth/register", data),
    login: (data: LoginData) =>
      apiClient.post<AuthResponse>("/auth/login", data),
    logout: () => apiClient.post("/auth/logout"),
    me: () => apiClient.get<User>("/auth/me"),
  },

  // Task endpoints
  tasks: {
    getAll: (userId: number) =>
      apiClient.get<Task[]>(`/tasks`, { params: { user_id: userId } }),
    getById: (taskId: number, userId: number) =>
      apiClient.get<Task>(`/tasks/${taskId}`, { params: { user_id: userId } }),
    create: (data: CreateTaskData) =>
      apiClient.post<Task>("/tasks", data),
    update: (taskId: number, data: UpdateTaskData) =>
      apiClient.patch<Task>(`/tasks/${taskId}`, data),
    delete: (taskId: number) =>
      apiClient.delete(`/tasks/${taskId}`),
    toggleComplete: (taskId: number, status: "pending" | "in_progress" | "completed") =>
      apiClient.patch<Task>(`/tasks/${taskId}`, { status }),
  },

  // User endpoints
  users: {
    getMe: () => apiClient.get<User>("/users/me"),
  },
};

// Type definitions
export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface User {
  id: number;
  email: string;
  username: string;
  created_at?: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  user_id: number;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  status?: "pending" | "in_progress" | "completed";
  priority?: "low" | "medium" | "high";
  due_date?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  status?: "pending" | "in_progress" | "completed";
  priority?: "low" | "medium" | "high";
  due_date?: string;
}

// Token management utilities
export const tokenManager = {
  getToken: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("auth_token");
  },

  setToken: (token: string): void => {
    if (typeof window === "undefined") return;
    localStorage.setItem("auth_token", token);
  },

  removeToken: (): void => {
    if (typeof window === "undefined") return;
    localStorage.removeItem("auth_token");
  },

  getUser: (): User | null => {
    if (typeof window === "undefined") return null;
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  },

  setUser: (user: User): void => {
    if (typeof window === "undefined") return;
    localStorage.setItem("user", JSON.stringify(user));
  },

  removeUser: (): void => {
    if (typeof window === "undefined") return;
    localStorage.removeItem("user");
  },

  clearAuth: (): void => {
    tokenManager.removeToken();
    tokenManager.removeUser();
  },

  isAuthenticated: (): boolean => {
    return !!tokenManager.getToken();
  },
};
