/**
 * TypeScript type definitions for the Todo application.
 * Centralized type definitions for consistency across the codebase.
 */

// ============================================
// User Types
// ============================================

export interface User {
  id: number;
  email: string;
  username: string;
  created_at?: string;
  updated_at?: string;
}

export interface UserProfile extends User {
  task_count?: number;
  completed_task_count?: number;
}

// ============================================
// Task Types
// ============================================

export type TaskStatus = "pending" | "in_progress" | "completed";

export type TaskPriority = "low" | "medium" | "high";

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  user_id: number;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority?: TaskPriority;
  due_date?: string;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

export interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  search?: string;
}

// ============================================
// API Response Types
// ============================================

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  has_more: boolean;
}

export interface ErrorResponse {
  detail: string;
  code?: string;
  validation_errors?: Record<string, string[]>;
}

// ============================================
// Auth Types
// ============================================

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
  user: User;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface Session {
  user: User;
  access_token: string;
  expires_at: number;
}

// ============================================
// UI State Types
// ============================================

export interface LoadingState {
  isLoading: boolean;
  error?: string;
}

export interface FormState<T> extends LoadingState {
  data?: T;
  isSubmitting: boolean;
}

export interface Toast {
  id: string;
  type: "success" | "error" | "warning" | "info";
  message: string;
  duration?: number;
}

export type FilterOption = "all" | "pending" | "in_progress" | "completed";

// ============================================
// Component Props Types
// ============================================

export interface ButtonProps {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  isLoading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
}

export interface InputProps {
  label?: string;
  error?: string;
  placeholder?: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  required?: boolean;
}

export interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

// ============================================
// Navigation Types
// ============================================

export interface NavItem {
  label: string;
  href: string;
  icon?: React.ReactNode;
  requiresAuth?: boolean;
}

// ============================================
// Environment Types
// ============================================

export interface Environment {
  NEXT_PUBLIC_API_URL: string;
  BETTER_AUTH_URL: string;
  BETTER_AUTH_SECRET: string;
  BETTER_AUTH_LOGGER?: string;
}
