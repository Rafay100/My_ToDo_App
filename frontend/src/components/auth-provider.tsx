"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

type AuthContextType = {
    session: any;
    // eslint-disable-next-line no-unused-vars
    setSession: (value: any) => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [session, setSession] = useState<any>(null);

    useEffect(() => {
        const storedSession = localStorage.getItem("session");
        if (storedSession) {
            setSession(JSON.parse(storedSession));
        }
    }, []);

    return (
        <AuthContext.Provider value={{ session, setSession }}>
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
