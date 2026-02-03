/**
 * ChatPage component
 * Main page for the chat interface
 */
import { useState, useEffect } from 'react';
import ChatInterface from '../components/ChatInterface';

export default function ChatPage() {
  const [userId, setUserId] = useState<string>('');

  useEffect(() => {
    // Generate or retrieve user ID
    // In a real app, this would come from authentication
    const storedUserId = localStorage.getItem('todo_user_id');

    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      // Generate a random user ID for demo purposes
      const newUserId = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substr(2, 9);
      localStorage.setItem('todo_user_id', newUserId);
      setUserId(newUserId);
    }
  }, []);

  if (!userId) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI-Powered Todo Assistant</h1>
          <p className="text-gray-600">
            Manage your tasks with natural language commands
          </p>
        </header>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <ChatInterface userId={userId} />
        </div>

        <footer className="mt-8 text-center text-gray-500 text-sm">
          <p>Your conversations are securely stored and processed.</p>
        </footer>
      </div>
    </div>
  );
}