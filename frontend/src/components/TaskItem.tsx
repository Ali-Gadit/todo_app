"use client";

import { useState } from "react";
import { type Task } from "@/lib/api";
import { useToast } from "./Toast";

interface TaskItemProps {
  task: Task;
  index: number;
  onToggleComplete: (taskId: number, completed: boolean) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (taskId: number, data: Partial<Task>) => void;
}

export function TaskItem({
  task,
  index,
  onToggleComplete,
  onDelete,
  onUpdate,
}: TaskItemProps) {
  const { addToast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || "");

  const handleSave = () => {
    if (editTitle.trim()) {
      onUpdate(task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      });
      setIsEditing(false);
      addToast("success", "Task updated successfully");
    }
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(task.id);
    addToast("success", "Task deleted");
  };

  const handleToggle = () => {
    onToggleComplete(task.id, false);
  };

  const priorityColors = {
    low: "bg-emerald-100 text-emerald-700 border-emerald-200",
    medium: "bg-amber-100 text-amber-700 border-amber-200",
    high: "bg-red-100 text-red-700 border-red-200",
  };

  const statusColors = {
    pending: "bg-neutral-100 text-neutral-600",
    in_progress: "bg-blue-100 text-blue-700",
    completed: "bg-emerald-100 text-emerald-700",
  };

  const statusLabels = {
    pending: "Pending",
    in_progress: "In Progress",
    completed: "Completed",
  };

  return (
    <div
      className={`card transition-all duration-200 ${
        task.status === "completed" ? "opacity-60" : ""
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
            task.status === "completed"
              ? "bg-emerald-500 border-emerald-500 text-white"
              : task.status === "in_progress"
              ? "bg-blue-500 border-blue-500 text-white"
              : "border-neutral-300 hover:border-primary-400"
          }`}
          title={
            task.status === "pending"
              ? "Click to start working on this task"
              : task.status === "in_progress"
              ? "Click to mark as completed"
              : "Click to uncheck"
          }
        >
          {task.status === "completed" && (
            <svg
              className="w-3 h-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
          {task.status === "in_progress" && (
            <svg
              className="w-3 h-3"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <circle cx="12" cy="12" r="3" />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="input w-full"
                autoFocus
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                placeholder="Add a description..."
                rows={2}
                className="input w-full resize-none"
              />
              <div className="flex gap-2">
                <button onClick={handleSave} className="btn-primary text-sm py-1.5">
                  Save
                </button>
                <button
                  onClick={handleCancel}
                  className="btn-secondary text-sm py-1.5"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <h3
                className={`font-medium text-neutral-900 ${
                  task.status === "completed" ? "line-through" : ""
                }`}
              >
                <span className="text-neutral-400 mr-2 font-mono text-sm">{index + 1}.</span>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-sm text-neutral-600 mt-1">
                  {task.description}
                </p>
              )}

              {/* Meta info */}
              <div className="flex items-center gap-3 mt-3 flex-wrap">
                <span
                  className={`badge ${priorityColors[task.priority]}`}
                >
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
                <span
                  className={`badge ${statusColors[task.status]}`}
                >
                  {statusLabels[task.status]}
                </span>
                <span className="text-xs text-neutral-400">
                  {new Date(task.created_at).toLocaleDateString()}
                </span>
              </div>
            </>
          )}
        </div>

        {/* Actions */}
        {!isEditing && (
          <div className="flex items-center gap-1">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100 rounded-lg transition-colors"
              title="Edit"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              className="p-2 text-neutral-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
