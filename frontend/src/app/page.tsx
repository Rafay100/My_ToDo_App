"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../components/auth-provider';
import HomePage from './home-page';
import AppLayout from '../components/AppLayout';
import EnhancedChatInterface from '../components/EnhancedChatInterface';

export default function Home() {
  const router = useRouter();
  const { session } = useAuth();

  // If user is authenticated, redirect to dashboard
  useEffect(() => {
    if (session) {
      router.push('/dashboard');
    }
  }, [session, router]);

  // If not authenticated, show the homepage
  if (session) {
    return null; // Will redirect via useEffect
  }

  return <HomePage />;
}