"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { tokenManager } from "@/lib/api";

interface HeaderProps {
  user?: {
    id: number;
    email: string;
    username: string;
  } | null;
}

export function Header({ user: propUser }: HeaderProps) {
  const router = useRouter();
  const { user: contextUser, isAuthenticated } = useAuth();
  const user = propUser || contextUser;

  const handleSignOut = async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      tokenManager.clearAuth();
      router.push("/login");
    }
  };

  return (
    <header className="bg-white border-b border-neutral-200 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link
              href="/"
              className="text-xl font-bold text-primary-600 hover:text-primary-700"
            >
              Todo App
            </Link>
          </div>

          {/* Navigation */}
          <div className="flex items-center gap-4">
            {isAuthenticated && user ? (
              <>
                <div className="hidden sm:flex items-center gap-2 text-sm text-neutral-600">
                  <span>Hi,</span>
                  <span className="font-medium text-neutral-900">
                    {user.username}
                  </span>
                </div>
                <button
                  onClick={handleSignOut}
                  className="btn-secondary text-sm py-1.5"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/login"
                  className="text-neutral-600 hover:text-neutral-900 text-sm font-medium"
                >
                  Sign In
                </Link>
                <Link href="/signup" className="btn-primary text-sm py-1.5">
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
