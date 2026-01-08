"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, tokenManager, type CreateTaskData } from "@/lib/api";
import { useToast } from "./Toast";

interface AddTaskFormProps {
  onTaskCreated?: () => void;
}

export function AddTaskForm({ onTaskCreated }: AddTaskFormProps) {
  const router = useRouter();
  const { addToast } = useToast();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"low" | "medium" | "high">("medium");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError("Task title is required");
      return;
    }

    const user = tokenManager.getUser();
    if (!user) {
      router.push("/login");
      return;
    }

    setIsLoading(true);

    try {
      const taskData: CreateTaskData = {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
      };

      await api.tasks.create(taskData);

      // Reset form
      setTitle("");
      setDescription("");
      setPriority("medium");
      setShowAdvanced(false);

      // Notify parent
      onTaskCreated?.();
      addToast("success", "Task created successfully");
    } catch (err: any) {
      setError(err.message || "Failed to create task. Please try again.");
      addToast("error", "Failed to create task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-neutral-900 mb-4">
        Add New Task
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {error}
          </div>
        )}

        <div>
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error && e.target.value.trim()) {
                setError(null);
              }
            }}
            placeholder="What needs to be done?"
            className={`input w-full ${
              error && !title.trim() ? "border-red-500" : ""
            }`}
            disabled={isLoading}
          />
          {error && !title.trim() && (
            <p className="text-red-600 text-sm mt-1 flex items-center gap-1">
              <svg
                className="w-4 h-4"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
              {error}
            </p>
          )}
        </div>

        {showAdvanced && (
          <div className="space-y-3 animate-fade-in">
            <div>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Add a description (optional)"
                rows={2}
                className="input w-full resize-none"
                disabled={isLoading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-1">
                Priority
              </label>
              <div className="flex gap-2">
                {(["low", "medium", "high"] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                      priority === p
                        ? p === "low"
                          ? "bg-emerald-100 text-emerald-700 border border-emerald-200"
                          : p === "medium"
                          ? "bg-amber-100 text-amber-700 border border-amber-200"
                          : "bg-red-100 text-red-700 border border-red-200"
                        : "bg-neutral-100 text-neutral-600 border border-neutral-200"
                    }`}
                  >
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-sm text-neutral-500 hover:text-neutral-700"
          >
            {showAdvanced ? "Hide options" : "Show options"}
          </button>

          <button
            type="submit"
            disabled={isLoading || !title.trim()}
            className="btn-primary"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg
                  className="animate-spin h-4 w-4"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
                Adding...
              </span>
            ) : (
              "Add Task"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
