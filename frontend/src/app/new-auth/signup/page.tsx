"use client";

import { useState } from "react";
import { signupUser } from "@/services/auth_client";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Loader2, Eye, EyeOff } from "lucide-react";
import { useAuth } from "@/components/auth-provider";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { setSession } = useAuth();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const result = await signupUser({ name, email, password });
      // Update the session manually to reflect the login state
      const sessionData = {
        user: { name, email, id: result.user_id },
        timestamp: Date.now()
      };
      setSession(sessionData);

      router.push("/dashboard"); // redirect on success
    } catch (err: any) {
      // Handle network errors and API errors differently
      if (err instanceof TypeError && err.message.includes('fetch')) {
        alert("Network error: Unable to connect to the server. Please check if the backend server is running.");
      } else {
        alert(err.message || "An unexpected error occurred during signup");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-background via-background to-muted/20 p-4">
      <Card className="w-full max-w-md shadow-lg border bg-card/50 backdrop-blur-sm">
        <CardHeader className="space-y-1">
          <CardTitle className="text-3xl font-bold tracking-tight text-center">
            Create an account
          </CardTitle>
          <CardDescription className="text-center text-muted-foreground">
            Enter your details below to create your account
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSignup} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                disabled={isLoading}
                className="bg-background border-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
                className="bg-background border-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  minLength={6}
                  className="bg-background border-input pr-10"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              <p className="text-xs text-muted-foreground">Password must be at least 6 characters</p>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Sign Up
            </Button>
          </form>
        </CardContent>

        <CardFooter className="flex flex-col gap-2">
          <div className="text-sm text-center text-muted-foreground">
            Already have an account?{" "}
            <Link
              href="/new-auth/signin"
              className="text-primary hover:underline font-medium"
            >
              Sign In
            </Link>
          </div>
          <div className="text-xs text-center text-muted-foreground mt-2">
            <Link
              href="/"
              className="hover:underline"
            >
              ← Back to home
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}