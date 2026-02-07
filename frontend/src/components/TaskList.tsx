"use client";

import { useEffect, useState, useCallback, forwardRef, useImperativeHandle } from "react";
import { api, tokenManager, type Task, type FilterOption } from "@/lib/api";
import { TaskItem } from "./TaskItem";
import { FilterTabs } from "./FilterTabs";
import { useToast } from "./Toast";

export const TaskList = forwardRef(function TaskList(props, ref) {
  const { addToast } = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<FilterOption>("all");
  const [counts, setCounts] = useState({
    all: 0,
    pending: 0,
    in_progress: 0,
    completed: 0,
  });

  const fetchTasks = useCallback(async () => {
    const user = tokenManager.getUser();
    if (!user) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await api.tasks.getAll(user.id);
      const allTasks = response.data;

      setTasks(allTasks);

      // Calculate counts
      setCounts({
        all: allTasks.length,
        pending: allTasks.filter((t) => t.status === "pending").length,
        in_progress: allTasks.filter((t) => t.status === "in_progress").length,
        completed: allTasks.filter((t) => t.status === "completed").length,
      });
    } catch (err: any) {
      setError(err.message || "Failed to load tasks");
      addToast("error", "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useImperativeHandle(ref, () => ({
    refreshTasks: fetchTasks,
  }));

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    // Get the task to determine current status
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;

    // Determine new status based on current status
    let newStatus: "pending" | "in_progress" | "completed";
    if (task.status === "pending") {
      newStatus = "in_progress";
    } else if (task.status === "in_progress") {
      newStatus = "completed";
    } else {
      // completed → in_progress (when unchecked)
      newStatus = "in_progress";
    }

    // Optimistic update
    setTasks((prev) =>
      prev.map((t) =>
        t.id === taskId
          ? { ...t, status: newStatus }
          : t
      )
    );

    try {
      await api.tasks.toggleComplete(taskId, newStatus);
      // Update counts
      const oldStatus = task.status;
      setCounts((prev) => {
        const newCounts = { ...prev };
        newCounts[oldStatus as keyof typeof newCounts]--;
        newCounts[newStatus as keyof typeof newCounts]++;
        return newCounts;
      });
    } catch (err) {
      // Revert on error
      addToast("error", "Failed to update task");
      fetchTasks();
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    // Optimistic update
    const task = tasks.find((t) => t.id === taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));

    if (task) {
      setCounts((prev) => ({
        ...prev,
        [task.status]: prev[task.status as keyof typeof prev] - 1,
        all: prev.all - 1,
      }));
    }

    try {
      await api.tasks.delete(taskId);
      addToast("success", "Task deleted successfully");
    } catch (err) {
      // Revert on error
      addToast("error", "Failed to delete task");
      fetchTasks();
    }
  };

  const handleUpdate = async (taskId: number, data: Partial<Task>) => {
    // Optimistic update
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? { ...task, ...data } : task))
    );

    try {
      await api.tasks.update(taskId, data);
    } catch (err) {
      // Revert on error
      addToast("error", "Failed to update task");
      fetchTasks();
    }
  };

  const filteredTasks =
    filter === "all"
      ? tasks
      : tasks.filter((task) => task.status === filter);

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-neutral-900">Your Tasks</h2>
        </div>
        <div className="card text-center py-12">
          <svg
            className="animate-spin h-8 w-8 text-primary-600 mx-auto"
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
          <p className="text-neutral-600 mt-4">Loading tasks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-neutral-900">Your Tasks</h2>
        </div>
        <div className="card text-center py-12">
          <div className="text-red-500 mb-2">
            <svg
              className="w-12 h-12 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <p className="text-red-600">{error}</p>
          <button onClick={fetchTasks} className="btn-primary mt-4">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold text-neutral-900">Your Tasks</h2>
          <button 
            onClick={fetchTasks} 
            className="p-1.5 text-neutral-500 hover:text-primary-600 hover:bg-primary-50 rounded-md transition-all flex items-center gap-1.5 text-sm font-medium"
            title="Refresh tasks"
            disabled={isLoading}
          >
            <svg 
              className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
        <FilterTabs
          currentFilter={filter}
          onFilterChange={setFilter}
          counts={counts}
        />
      </div>

      {filteredTasks.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-neutral-400 mb-2">
            <svg
              className="w-12 h-12 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <p className="text-neutral-600">
            {filter === "all"
              ? "No tasks yet"
              : `No ${filter.replace("_", " ")} tasks`}
          </p>
          <p className="text-sm text-neutral-500 mt-1">
            {filter === "all"
              ? "Add a task above to get started"
              : "Try a different filter"}
          </p>
        </div>
      ) : (
        <div className="space-y-3 animate-slide-up">
          {filteredTasks.map((task, index) => (
            <TaskItem
              key={task.id}
              task={task}
              index={index}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          ))}
        </div>
      )}
    </div>
  );
});
