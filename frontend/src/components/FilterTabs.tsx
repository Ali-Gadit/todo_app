"use client";

import { type FilterOption } from "@/lib/api";

interface FilterTabsProps {
  currentFilter: FilterOption;
  onFilterChange: (filter: FilterOption) => void;
  counts?: {
    all: number;
    pending: number;
    in_progress: number;
    completed: number;
  };
}

export function FilterTabs({
  currentFilter,
  onFilterChange,
  counts,
}: FilterTabsProps) {
  const filters: { value: FilterOption; label: string }[] = [
    { value: "all", label: "All" },
    { value: "pending", label: "Pending" },
    { value: "in_progress", label: "In Progress" },
    { value: "completed", label: "Completed" },
  ];

  return (
    <div className="flex items-center gap-1 p-1 bg-neutral-100 rounded-lg overflow-x-auto">
      {filters.map((filter) => (
        <button
          key={filter.value}
          onClick={() => onFilterChange(filter.value)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-all whitespace-nowrap ${
            currentFilter === filter.value
              ? "bg-white text-neutral-900 shadow-sm"
              : "text-neutral-600 hover:text-neutral-900 hover:bg-neutral-200/50"
          }`}
        >
          {filter.label}
          {counts && counts[filter.value as keyof typeof counts] !== undefined && (
            <span
              className={`ml-2 px-1.5 py-0.5 rounded-full text-xs ${
                currentFilter === filter.value
                  ? "bg-primary-100 text-primary-700"
                  : "bg-neutral-200 text-neutral-600"
              }`}
            >
              {counts[filter.value as keyof typeof counts]}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
