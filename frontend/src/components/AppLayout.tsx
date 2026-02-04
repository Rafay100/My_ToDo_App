'use client';

import { useState, useEffect } from 'react';
import { Moon, Sun, Menu, X, MessageSquare, ListTodo, Settings, Bell, Search, Plus, Filter, Calendar, Tag, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTheme } from 'next-themes';
import { cn } from '@/lib/utils';

interface AppLayoutProps {
  children: React.ReactNode;
  sidebarContent?: React.ReactNode;
  rightPanelContent?: React.ReactNode;
}

export default function AppLayout({ children, sidebarContent, rightPanelContent }: AppLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isRightPanelOpen, setIsRightPanelOpen] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { theme, setTheme } = useTheme();

  // Close panels on mobile screens (client-side only)
  useEffect(() => {
    const checkScreenSize = () => {
      if (typeof window !== 'undefined' && window.innerWidth < 768) {
        setIsSidebarOpen(false);
        setIsRightPanelOpen(false);
      } else {
        setIsSidebarOpen(true);
        setIsRightPanelOpen(true);
      }
    };

    // Check on mount
    checkScreenSize();

    // Add resize listener
    window.addEventListener('resize', checkScreenSize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', checkScreenSize);
    };
  }, []);

  // Close panels on mobile screens
  useEffect(() => {
    if (typeof window !== 'undefined' && window.innerWidth < 768) {
      setIsSidebarOpen(false);
      setIsRightPanelOpen(false);
    }
  }, []);

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Mobile menu button */}
      <div className="md:hidden fixed top-4 left-4 z-50">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="bg-background/80 backdrop-blur-sm"
        >
          {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </Button>
      </div>

      {/* Left Sidebar */}
      {(isSidebarOpen || isMobileMenuOpen) && (
        <>
          {/* Overlay for mobile */}
          {isMobileMenuOpen && (
            <div
              className="fixed inset-0 z-40 bg-black/50 md:hidden"
              onClick={() => setIsMobileMenuOpen(false)}
            />
          )}

          <aside
            className={cn(
              "fixed md:relative z-40 h-full bg-background border-r transition-all duration-300 ease-in-out",
              "w-64",
              isMobileMenuOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
            )}
          >
            <div className="flex flex-col h-full">
              {/* Sidebar Header */}
              <div className="p-4 border-b">
                <div className="flex items-center justify-between">
                  <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
                    TaskFlow AI
                  </h1>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="md:hidden"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <X className="h-5 w-5" />
                  </Button>
                </div>
              </div>

              {/* Navigation */}
              <nav className="flex-1 p-2">
                <ul className="space-y-1">
                  <li>
                    <Button
                      variant="ghost"
                      className="w-full justify-start gap-3 px-3 py-2 rounded-lg"
                    >
                      <MessageSquare className="h-4 w-4" />
                      <span>AI Chat</span>
                    </Button>
                  </li>
                  <li>
                    <Button
                      variant="ghost"
                      className="w-full justify-start gap-3 px-3 py-2 rounded-lg"
                    >
                      <ListTodo className="h-4 w-4" />
                      <span>Tasks</span>
                    </Button>
                  </li>
                  <li>
                    <Button
                      variant="ghost"
                      className="w-full justify-start gap-3 px-3 py-2 rounded-lg"
                    >
                      <Calendar className="h-4 w-4" />
                      <span>Calendar</span>
                    </Button>
                  </li>
                  <li>
                    <Button
                      variant="ghost"
                      className="w-full justify-start gap-3 px-3 py-2 rounded-lg"
                    >
                      <Tag className="h-4 w-4" />
                      <span>Tags</span>
                    </Button>
                  </li>
                </ul>

                {/* Recent Conversations */}
                <div className="mt-6">
                  <h3 className="px-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Recent Conversations
                  </h3>
                  <ul className="mt-2 space-y-1">
                    {[1, 2, 3].map((item) => (
                      <li key={item}>
                        <Button
                          variant="ghost"
                          className="w-full justify-start gap-3 px-3 py-2 rounded-lg text-left"
                        >
                          <MessageSquare className="h-3 w-3 text-muted-foreground" />
                          <span className="truncate">Conversation {item}</span>
                        </Button>
                      </li>
                    ))}
                  </ul>
                </div>
              </nav>

              {/* Sidebar Footer */}
              <div className="p-3 border-t">
                <div className="flex items-center justify-between">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-2"
                    onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                  >
                    {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                    <span>Theme</span>
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Settings className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </aside>
        </>
      )}

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navigation Bar */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-30">
          <div className="flex items-center justify-between p-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                className="md:hidden"
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              >
                <Menu className="h-5 w-5" />
              </Button>

              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search tasks, conversations..."
                  className="pl-10 pr-4 py-2 bg-muted rounded-lg w-64 focus:outline-none focus:ring-2 focus:ring-primary/20"
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Filter className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon">
                <Bell className="h-5 w-5" />
              </Button>
              <Button variant="secondary" size="sm" className="gap-2">
                <Plus className="h-4 w-4" />
                New Task
              </Button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="flex-1 overflow-auto relative">
          <div className="h-full">
            {children}
          </div>
        </div>
      </main>

      {/* Right Panel */}
      {rightPanelContent && isRightPanelOpen && (
        <aside className="hidden md:block w-80 bg-background border-l">
          <div className="flex flex-col h-full">
            <div className="p-4 border-b flex items-center justify-between">
              <h2 className="font-semibold">Task Details</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsRightPanelOpen(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex-1 overflow-auto p-4">
              {rightPanelContent}
            </div>
          </div>
        </aside>
      )}

      {/* Right Panel Toggle Button (Desktop only) */}
      {rightPanelContent && (
        <Button
          variant="outline"
          size="icon"
          className="hidden md:flex fixed top-1/2 right-0 rounded-l-none rounded-r-full border-l-0 -translate-y-1/2 z-30"
          onClick={() => setIsRightPanelOpen(!isRightPanelOpen)}
        >
          {isRightPanelOpen ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      )}
    </div>
  );
}

