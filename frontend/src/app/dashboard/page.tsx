"use client";

import { useState, useEffect } from "react";
import { todoApi } from "@/services/todo_api";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Trash2, LogOut, Plus, Loader2, Moon, Sun, CheckCircle2, Circle } from "lucide-react";
import { useTheme } from "next-themes";

export default function Dashboard() {
  const [todos, setTodos] = useState<any[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const router = useRouter();
  const { theme, setTheme } = useTheme();

  const completedCount = todos.filter(t => t.is_completed).length;
  const totalCount = todos.length;

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setIsLoading(true);
    try {
      const data = await todoApi.list();
      setTodos(Array.isArray(data) ? data : []);
    } catch {
      // Silently handle error - UI shows empty state
      setTodos([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignout = async () => {
    try {
      // Sign out from our backend
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/signout`, {
        method: "POST",
        credentials: "include",
      });

      router.push("/signin");
    } catch {
      // Force redirect even on error
      router.push("/signin");
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim()) return;
    setIsAdding(true);
    try {
      await todoApi.create(newTodo);
      setNewTodo("");
      await loadTodos();
    } catch {
      // Silently handle error - user can retry
    } finally {
      setIsAdding(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await todoApi.delete(id);
      setTodos(prev => prev.filter((t) => t.id !== id));
    } catch {
      // Silently handle error - optimistic update may fail
    }
  };

  const handleToggle = async (id: string, is_completed: boolean) => {
    setTodos(prev => prev.map((t) => (t.id === id ? { ...t, is_completed } : t)));
    try {
      await todoApi.update(id, { is_completed });
    } catch {
      // Revert optimization on failure
      await loadTodos();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      {/* Navbar */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
              <CheckCircle2 className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-xl bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              TaskFlow
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="rounded-full"
            >
              <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span className="sr-only">Toggle theme</span>
            </Button>
            <Button variant="ghost" size="sm" onClick={handleSignout} className="gap-2">
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Sign Out</span>
            </Button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {/* Header Section */}
        <div className="mb-8 sm:mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mb-3 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
            My Tasks
          </h1>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Circle className="h-4 w-4" />
              <span>{totalCount - completedCount} active</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4" />
              <span>{completedCount} completed</span>
            </div>
          </div>
        </div>

        {/* Add Task Card */}
        <Card className="mb-8 border-2 shadow-xl bg-card/50 backdrop-blur-sm hover:shadow-2xl transition-shadow">
          <CardContent className="pt-6">
            <form onSubmit={handleAdd} className="flex flex-col sm:flex-row gap-3">
              <Input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="What needs to be done?"
                className="flex-grow text-base h-12 px-4 bg-background border-2 focus-visible:ring-2 focus-visible:ring-primary/20"
                disabled={isAdding}
              />
              <Button
                type="submit"
                disabled={isAdding || !newTodo.trim()}
                className="h-12 px-6 gap-2 font-medium shadow-lg hover:shadow-xl transition-all"
                size="lg"
              >
                {isAdding ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Plus className="h-5 w-5" />
                )}
                <span className="hidden sm:inline">Add Task</span>
                <span className="sm:hidden">Add</span>
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Tasks List */}
        <div className="space-y-3">
          {isLoading ? (
            <Card className="border-2">
              <CardContent className="flex flex-col items-center justify-center py-16 gap-4">
                <Loader2 className="h-10 w-10 animate-spin text-primary" />
                <p className="text-sm text-muted-foreground font-medium">Loading your tasks...</p>
              </CardContent>
            </Card>
          ) : todos.length === 0 ? (
            <Card className="border-2 border-dashed bg-muted/20">
              <CardContent className="flex flex-col items-center justify-center py-16 gap-4">
                <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                  <CheckCircle2 className="h-8 w-8 text-muted-foreground" />
                </div>
                <div className="text-center space-y-1">
                  <p className="text-lg font-semibold">No tasks yet</p>
                  <p className="text-sm text-muted-foreground">Create your first task to get started</p>
                </div>
              </CardContent>
            </Card>
          ) : (
            todos.map((todo) => (
              <Card
                key={todo.id}
                className="group border-2 hover:border-primary/50 hover:shadow-lg transition-all bg-card/50 backdrop-blur-sm"
              >
                <CardContent className="p-5 flex items-center gap-4">
                  <Checkbox
                    checked={todo.is_completed}
                    onCheckedChange={(checked) => handleToggle(todo.id, !!checked)}
                    className="h-5 w-5 rounded-full border-2"
                  />
                  <span
                    className={`flex-grow text-base sm:text-lg font-medium transition-all select-none ${
                      todo.is_completed
                        ? "line-through text-muted-foreground/70"
                        : "text-foreground"
                    }`}
                  >
                    {todo.title}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(todo.id)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:text-destructive hover:bg-destructive/10 rounded-full h-9 w-9"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Footer Stats */}
        {!isLoading && todos.length > 0 && (
          <div className="mt-8 text-center">
            <p className="text-sm text-muted-foreground">
              {completedCount === totalCount ? (
                <span className="font-medium text-primary">All tasks completed! 🎉</span>
              ) : (
                `${completedCount} of ${totalCount} tasks completed`
              )}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
