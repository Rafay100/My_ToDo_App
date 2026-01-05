"use client";
import { Component, ReactNode } from "react";

export class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4">
          <h2 className="text-xl font-bold mb-4">Something went wrong.</h2>
          <button onClick={() => window.location.reload()} className="bg-blue-500 text-white px-4 py-2 rounded">
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export function EmptyState() {
  return (
    <div className="text-center py-10">
      <p className="text-gray-500">No todos found. Start by adding one above!</p>
    </div>
  );
}
