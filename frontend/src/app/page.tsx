"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../components/auth-provider';
import HomePage from './home-page';

export default function Home() {
  const router = useRouter();
  const { session, clearSession } = useAuth();
  const [validatingSession, setValidatingSession] = useState(false);

  // Validate session with backend before redirecting
  useEffect(() => {
    const validateSession = async () => {
      if (session) {
        setValidatingSession(true);
        try {
          // Make a request to validate the session
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/me`, {
            credentials: "include",
          });

          if (response.ok) {
            // Session is valid, redirect to dashboard
            router.push('/dashboard');
          } else {
            // Session is invalid, clear it and show homepage
            clearSession();
          }
        } catch (error) {
          console.error('Error validating session:', error);
          // If there's an error validating, clear the session and show homepage
          clearSession();
        } finally {
          setValidatingSession(false);
        }
      }
    };

    validateSession();
  }, [session, router, clearSession]);

  // If validating or if there's no session, show the homepage
  if ((session && validatingSession) || !session) {
    return <HomePage />;
  }

  // If there's a valid session, redirect will happen via useEffect
  return null;
}