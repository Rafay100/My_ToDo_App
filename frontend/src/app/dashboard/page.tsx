"use client";

import { useState, useEffect } from "react";
import { todoApi } from "@/services/todo_api";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Trash2,
  LogOut,
  Plus,
  Loader2,
  Moon,
  Sun,
  CheckCircle2,
  Circle,
  Filter,
  Search,
  Calendar,
  Flag,
  Tag,
  Bell,
  Settings,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { useTheme } from "next-themes";
import { useAuth } from "@/components/auth-provider";
import AppLayout from "@/components/AppLayout";
import TaskCard from "@/components/TaskCard";
import { Badge } from "@/components/ui/badge";
import { format, parseISO } from "date-fns";

// Prevent hydration errors by ensuring this component only renders on the client
const ClientOnly = ({ children }: { children: React.ReactNode }) => {
  const [hasMounted, setHasMounted] = useState(false);

  useEffect(() => {
    setHasMounted(true);
  }, []);

  if (!hasMounted) {
    return null;
  }

  return <>{children}</>;
};

export default function Dashboard() {
  const [todos, setTodos] = useState<any[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [selectedTask, setSelectedTask] = useState<any>(null);
  const [filters, setFilters] = useState({
    status: 'all', // all, active, completed
    priority: 'all', // all, low, medium, high, urgent
    sortBy: 'due_date', // due_date, priority, created_at
    search: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const { session, clearSession } = useAuth();

  // Redirect to sign in if not authenticated
  useEffect(() => {
    if (!session) {
      router.push('/new-auth/signin');
    }
  }, [session, router]);

  const completedCount = todos.filter(t => t.is_completed).length;
  const totalCount = todos.length;

  useEffect(() => {
    loadTodos();
  }, []);

  useEffect(() => {
    // When a task is selected, update the right panel content
  }, [selectedTask]);

  const loadTodos = async () => {
    setIsLoading(true);
    try {
      const data = await todoApi.list();
      setTodos(Array.isArray(data) ? data : []);
    } catch {
      setTodos([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignout = async () => {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/signout`, {
        method: "POST",
        credentials: "include",
      });
      // Clear the session from auth context
      clearSession();
      router.push("/signin");
    } catch {
      // Clear the session from auth context
      clearSession();
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
    } finally {
      setIsAdding(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await todoApi.delete(id);
      setTodos(prev => prev.filter(t => t.id !== id));
      if (selectedTask?.id === id) {
        setSelectedTask(null);
      }
    } catch {
      await loadTodos();
    }
  };

  const handleToggle = async (id: string, is_completed: boolean) => {
    setTodos(prev => prev.map(t => (t.id === id ? { ...t, is_completed } : t)));
    try {
      await todoApi.update(id, { is_completed });
    } catch {
      await loadTodos();
    }
  };

  // Filter and sort tasks
  const filteredAndSortedTodos = todos
    .filter(todo => {
      // Apply status filter
      if (filters.status === 'active' && todo.is_completed) return false;
      if (filters.status === 'completed' && !todo.is_completed) return false;

      // Apply priority filter
      if (filters.priority !== 'all' && todo.priority !== filters.priority) return false;

      // Apply search filter
      if (filters.search && !todo.title.toLowerCase().includes(filters.search.toLowerCase())) return false;

      return true;
    })
    .sort((a, b) => {
      // Apply sorting
      switch (filters.sortBy) {
        case 'due_date':
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
        case 'priority':
          const priorityOrder: Record<string, number> = { urgent: 0, high: 1, medium: 2, low: 3 };
          return (priorityOrder[a.priority] || 4) - (priorityOrder[b.priority] || 4);
        case 'created_at':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        default:
          return 0;
      }
    });

  // Sidebar content
  const sidebarContent = (
    <div className="p-4">
      <div className="space-y-6">
        {/* Navigation */}
        <nav className="space-y-1">
          <Button variant="ghost" className="w-full justify-start gap-3 px-3 py-2 rounded-lg">
            <CheckCircle2 className="h-4 w-4" />
            <span>All Tasks</span>
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 px-3 py-2 rounded-lg">
            <Calendar className="h-4 w-4" />
            <span>Upcoming</span>
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 px-3 py-2 rounded-lg">
            <Flag className="h-4 w-4" />
            <span>Priority</span>
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 px-3 py-2 rounded-lg">
            <Tag className="h-4 w-4" />
            <span>Tags</span>
          </Button>
        </nav>

        {/* Stats */}
        <div className="border-t pt-4">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Statistics</h3>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Total</span>
              <span className="font-medium">{totalCount}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Completed</span>
              <span className="font-medium text-green-600">{completedCount}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Remaining</span>
              <span className="font-medium">{totalCount - completedCount}</span>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="border-t pt-4">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Recent Activity</h3>
          <div className="space-y-2 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-3 w-3 text-green-500" />
              <span>Completed meeting prep</span>
            </div>
            <div className="flex items-center gap-2">
              <Plus className="h-3 w-3 text-blue-500" />
              <span>Added grocery list</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-3 w-3 text-purple-500" />
              <span>Scheduled dentist appointment</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Right panel content
  const rightPanelContent = selectedTask ? (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-2">{selectedTask.title}</h3>
        <p className="text-muted-foreground">{selectedTask.description || 'No description provided.'}</p>
      </div>

      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-1">Priority</h4>
          <Badge variant="outline" className="capitalize">
            {selectedTask.priority}
          </Badge>
        </div>

        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-1">Due Date</h4>
          {selectedTask.due_date ? (
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span>{format(parseISO(selectedTask.due_date), 'MMM dd, yyyy')}</span>
            </div>
          ) : (
            <span className="text-muted-foreground italic">No due date</span>
          )}
        </div>

        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-1">Status</h4>
          <Badge variant={selectedTask.is_completed ? "default" : "secondary"}>
            {selectedTask.is_completed ? "Completed" : "Pending"}
          </Badge>
        </div>

        {selectedTask.tags && selectedTask.tags.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-1">Tags</h4>
            <div className="flex flex-wrap gap-1">
              {selectedTask.tags.map((tag: string, index: number) => (
                <Badge key={index} variant="secondary" className="text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
        )}

        <div className="pt-4">
          <Button variant="outline" className="w-full">
            Edit Task
          </Button>
        </div>
      </div>
    </div>
  ) : (
    <div className="flex flex-col items-center justify-center h-full text-center py-8">
      <div className="mb-4 p-3 rounded-full bg-muted">
        <CheckCircle2 className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium mb-1">No Task Selected</h3>
      <p className="text-sm text-muted-foreground">
        Select a task to view details and manage it
      </p>
    </div>
  );

  return (
    <AppLayout sidebarContent={sidebarContent} rightPanelContent={rightPanelContent}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-foreground mb-2">
            My Tasks
          </h1>
          <div className="flex flex-wrap items-center justify-between gap-4">
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

            <div className="flex items-center gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search tasks..."
                  value={filters.search}
                  onChange={(e) => setFilters({...filters, search: e.target.value})}
                  className="pl-10 pr-4 py-2 bg-background border focus:outline-none focus:ring-2 focus:ring-primary/20"
                />
              </div>

              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="gap-2"
              >
                <Filter className="h-4 w-4" />
                Filters
                {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </Button>

              <Button variant="secondary" size="sm" className="gap-2">
                <Plus className="h-4 w-4" />
                New Task
              </Button>
            </div>
          </div>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <Card className="mb-6 border bg-card/50 backdrop-blur-sm">
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium text-muted-foreground mb-1 block">Status</label>
                  <select
                    value={filters.status}
                    onChange={(e) => setFilters({...filters, status: e.target.value})}
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    <option value="all">All</option>
                    <option value="active">Active</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium text-muted-foreground mb-1 block">Priority</label>
                  <select
                    value={filters.priority}
                    onChange={(e) => setFilters({...filters, priority: e.target.value})}
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    <option value="all">All</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium text-muted-foreground mb-1 block">Sort By</label>
                  <select
                    value={filters.sortBy}
                    onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    <option value="due_date">Due Date</option>
                    <option value="priority">Priority</option>
                    <option value="created_at">Created At</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Add Task Card */}
        <Card className="mb-8 border-0 shadow-sm bg-card/30 backdrop-blur-sm hover:shadow-md transition-shadow">
          <CardContent className="pt-6">
            <form onSubmit={handleAdd} className="flex flex-col sm:flex-row gap-3">
              <Input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="What needs to be done?"
                className="flex-grow text-base h-12 px-4 bg-background border-0 focus-visible:ring-2 focus-visible:ring-primary/20 rounded-xl"
                disabled={isAdding}
              />
              <Button
                type="submit"
                disabled={isAdding || !newTodo.trim()}
                className="h-12 px-6 gap-2 font-medium shadow-lg hover:shadow-xl transition-all rounded-xl"
                size="lg"
              >
                {isAdding ? (
                <div className="h-5 w-5 flex items-center justify-center">
                  <Loader2 className="h-4 w-4 animate-spin" />
                </div>
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
        <div className="space-y-4">
          {isLoading ? (
            <Card className="border-0 bg-card/30 backdrop-blur-sm">
              <CardContent className="flex flex-col items-center justify-center py-16 gap-4">
                <div className="h-10 w-10 flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
                <p className="text-sm text-muted-foreground font-medium">Loading your tasks...</p>
              </CardContent>
            </Card>
          ) : filteredAndSortedTodos.length === 0 ? (
            <Card className="border-0 bg-card/30 backdrop-blur-sm">
              <CardContent className="flex flex-col items-center justify-center py-16 gap-4">
                <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                  <CheckCircle2 className="h-8 w-8 text-muted-foreground" />
                </div>
                <div className="text-center space-y-1">
                  <p className="text-lg font-semibold">No tasks found</p>
                  <p className="text-sm text-muted-foreground">
                    {filters.search || filters.status !== 'all' || filters.priority !== 'all'
                      ? 'Try changing your filters'
                      : 'Create your first task to get started'}
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            filteredAndSortedTodos.map(todo => (
              <TaskCard
                key={todo.id}
                task={{
                  id: todo.id,
                  title: todo.title,
                  description: todo.description,
                  isCompleted: todo.is_completed,
                  priority: todo.priority || 'medium',
                  dueDate: todo.due_date,
                  tags: todo.tags || [],
                  isRecurring: todo.is_recurring,
                  createdAt: todo.created_at
                }}
                onToggleComplete={handleToggle}
                onEdit={setSelectedTask}
                onDelete={handleDelete}
              />
            ))
          )}
        </div>

        {/* Footer Stats */}
        {!isLoading && todos.length > 0 && (
          <div className="mt-8 text-center">
            <p className="text-sm text-muted-foreground">
              {completedCount === totalCount && totalCount > 0 ? (
                <span className="font-medium text-primary flex items-center justify-center gap-2">
                  All tasks completed! 🎉
                  <CheckCircle2 className="h-4 w-4" />
                </span>
              ) : (
                `${completedCount} of ${totalCount} tasks completed`
              )}
            </p>
          </div>
        )}
      </div>
    </AppLayout>
  );
}