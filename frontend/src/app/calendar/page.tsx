'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/auth-provider';
import { useRouter } from 'next/navigation';

export default function CalendarPage() {
  const { session } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!session) {
      router.push('/new-auth/signin');
    }
  }, [session, router]);

  if (!session) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <p className="text-lg text-muted-foreground">Redirecting to sign in...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Calendar</h1>
      <p className="text-lg text-muted-foreground">Calendar functionality coming soon!</p>
    </div>
  );
}