"use client";

import { useState, useEffect } from "react";
import { todoApi } from "@/services/todo_api";
import { supabase } from "@/services/supabase_client";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Trash2, LogOut, Plus, Loader2, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

export default function Dashboard() {
  const [todos, setTodos] = useState<any[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const router = useRouter();
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setIsLoading(true);
    try {
      const data = await todoApi.list();
      setTodos(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Failed to load todos", error);
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
      });

      // Sign out from Supabase if active
      if (supabase && supabase.auth) {
        await supabase.auth.signOut();
      }

      router.push("/signin");
    } catch (err) {
      console.error("Unexpected sign out error:", err);
      router.push("/signin"); // Force redirect anyway
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
    } catch (error) {
      console.error("Failed to add todo", error);
    } finally {
      setIsAdding(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await todoApi.delete(id);
      setTodos(prev => prev.filter((t) => t.id !== id));
    } catch (error) {
      console.error("Failed to delete todo", error);
    }
  };

  const handleToggle = async (id: string, is_completed: boolean) => {
    setTodos(prev => prev.map((t) => (t.id === id ? { ...t, is_completed } : t)));
    try {
      await todoApi.update(id, { is_completed });
    } catch (error) {
      console.error("Failed to update todo", error);
      // Revert optimization on failure
      await loadTodos();
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-3xl mx-auto space-y-8">
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight">My Tasks</h1>
            <p className="text-muted-foreground">Stay organized and productive.</p>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span className="sr-only">Toggle theme</span>
            </Button>
            <Button variant="outline" size="sm" onClick={handleSignout}>
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </header>

        <Card className="border-none shadow-md bg-card/50 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-xl">Add a new task</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAdd} className="flex gap-3">
              <Input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="Write something here..."
                className="flex-grow bg-background/50"
                disabled={isAdding}
              />
              <Button type="submit" disabled={isAdding || !newTodo.trim()}>
                {isAdding ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="h-4 w-4 mr-1" />
                )}
                Add Task
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="space-y-4">
          {isLoading ? (
            <div className="flex justify-center p-12">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : todos.length === 0 ? (
            <div className="text-center p-12 border-2 border-dashed rounded-xl border-muted">
              <p className="text-muted-foreground">No tasks yet. Add one to get started!</p>
            </div>
          ) : (
            todos.map((todo) => (
              <Card key={todo.id} className="group hover:border-primary/50 transition-colors">
                <CardContent className="p-4 flex items-center gap-4">
                  <Checkbox
                    checked={todo.is_completed}
                    onCheckedChange={(checked) => handleToggle(todo.id, !!checked)}
                  />
                  <span
                    className={`flex-grow text-lg transition-all ${
                      todo.is_completed ? "line-through text-muted-foreground italic" : ""
                    }`}
                  >
                    {todo.title}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(todo.id)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:text-destructive hover:bg-destructive/10"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
