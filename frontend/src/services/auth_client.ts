// src/services/auth_client.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function signupUser({ name, email, password }: { name: string; email: string; password: string }) {
    const res = await fetch(`${API_URL}/api/v1/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
        credentials: "include",
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message || "Failed to sign up");
    }
    return res.json();
}

export async function signinUser({ email, password }: { email: string; password: string }) {
    const res = await fetch(`${API_URL}/api/v1/signin`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message || "Failed to sign in");
    }
    return res.json();
}
