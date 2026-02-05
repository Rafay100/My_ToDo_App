'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/auth-provider';
import { useRouter } from 'next/navigation';
import EnhancedChatInterface from '@/components/EnhancedChatInterface';

export default function ChatPage() {
  const { session } = useAuth();
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    if (!session) {
      router.push('/new-auth/signin');
    } else {
      // Extract user ID from session
      setUserId(session.user?.id || null);
    }
  }, [session, router]);

  if (!session || !userId) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <p className="text-lg text-muted-foreground">Redirecting to sign in...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <EnhancedChatInterface userId={userId} />
    </div>
  );
}