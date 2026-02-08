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


