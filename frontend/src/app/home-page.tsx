"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../components/auth-provider';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  const router = useRouter();
  const { session } = useAuth();

  useEffect(() => {
    // If user is authenticated, redirect to dashboard
    if (session) {
      router.push('/dashboard');
    }
  }, [session, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center space-y-8 animate-in fade-in duration-500">
          <div className="space-y-4">
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              TaskFlow AI
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The intelligent task manager that understands you. Transform how you organize, prioritize, and accomplish your goals with AI-powered assistance.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              className="px-8 py-6 text-lg rounded-xl"
              onClick={() => router.push('/new-auth/signin')}
            >
              Sign In to Continue
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="px-8 py-6 text-lg rounded-xl"
              onClick={() => router.push('/new-auth/signup')}
            >
              Create Account
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            <div className="bg-muted/50 p-6 rounded-xl border">
              <div className="text-2xl font-bold text-primary mb-2">AI-Powered</div>
              <p className="text-sm text-muted-foreground">Natural language task management with intelligent suggestions</p>
            </div>
            <div className="bg-muted/50 p-6 rounded-xl border">
              <div className="text-2xl font-bold text-primary mb-2">Secure</div>
              <p className="text-sm text-muted-foreground">Enterprise-grade security with end-to-end encryption</p>
            </div>
            <div className="bg-muted/50 p-6 rounded-xl border">
              <div className="text-2xl font-bold text-primary mb-2">Cross-Device</div>
              <p className="text-sm text-muted-foreground">Sync seamlessly across all your devices</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}