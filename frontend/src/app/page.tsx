"use client";

import { useRef } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { Header } from "@/components/Header";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { AddTaskForm } from "@/components/AddTaskForm";
import { TaskList } from "@/components/TaskList";

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const taskListRef = useRef<{ refreshTasks: () => void }>(null);

  const handleTaskCreated = () => {
    taskListRef.current?.refreshTasks();
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-neutral-50">
        <Header user={user} />

        <main className="max-w-3xl mx-auto px-4 py-8">
          {/* Welcome message */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-neutral-900">
              Welcome back, {user?.username || "User"}!
            </h1>
            <p className="text-neutral-600 mt-1">
              Here are your tasks for today.
            </p>
          </div>

          {/* Add task form */}
          <div className="mb-8">
            <AddTaskForm onTaskCreated={handleTaskCreated} />
          </div>

          {/* Task list */}
          <TaskList ref={taskListRef} />
        </main>
      </div>
    </ProtectedRoute>
  );
}

// Landing page for unauthenticated users
export function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-md w-full text-center space-y-8">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-neutral-900">Todo App</h1>
          <p className="text-neutral-600">
            A modern, full-stack todo application to manage your tasks
          </p>
        </div>

        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-neutral-900">
            Get Started
          </h2>
          <p className="text-sm text-neutral-600">
            Sign in or create an account to start managing your tasks.
          </p>
          <div className="flex gap-3">
            <Link href="/login" className="btn-secondary flex-1">
              Sign In
            </Link>
            <Link href="/signup" className="btn-primary flex-1">
              Sign Up
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-3 gap-4 mt-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg
                className="w-6 h-6 text-primary-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <p className="text-sm font-medium text-neutral-900">Simple</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg
                className="w-6 h-6 text-secondary-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <p className="text-sm font-medium text-neutral-900">Secure</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg
                className="w-6 h-6 text-amber-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
            </div>
            <p className="text-sm font-medium text-neutral-900">Responsive</p>
          </div>
        </div>
      </div>
    </main>
  );
}
