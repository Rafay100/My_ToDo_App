"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

type AuthContextType = {
    session: any;
    setSession: (value: any) => void;
    clearSession: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [session, setSessionState] = useState<any>(null);

    const setSession = (value: any) => {
        setSessionState(value);
        if (value) {
            localStorage.setItem("session", JSON.stringify(value));
        } else {
            localStorage.removeItem("session");
        }
    };

    const clearSession = () => {
        setSessionState(null);
        localStorage.removeItem("session");
    };

    useEffect(() => {
        const storedSession = localStorage.getItem("session");
        if (storedSession) {
            try {
                setSessionState(JSON.parse(storedSession));
            } catch (e) {
                console.error("Error parsing session from localStorage:", e);
                localStorage.removeItem("session");
            }
        }
    }, []);

    return (
        <AuthContext.Provider value={{ session, setSession, clearSession }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) {
        throw new Error("useAuth must be used inside AuthProvider");
    }
    return ctx;
};
