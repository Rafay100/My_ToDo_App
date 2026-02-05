const API_BASE = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/api/v1/todos";

export const todoApi = {
    list: async () => {
        const res = await fetch(API_BASE + "/", {
            headers: {
                "Accept": "application/json",
            },
            credentials: "include"
        });
        if (!res.ok) throw new Error("Failed to fetch todos");
        return res.json();
    },
    create: async (title: string) => {
        try {
            const res = await fetch(API_BASE + `/?title=${encodeURIComponent(title)}`, {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                },
                credentials: "include"
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({ message: "Failed to create todo" }));
                // If it's an authentication error (401/403), we should handle it specially
                if (res.status === 401 || res.status === 403) {
                    throw new Error("Authentication failed. Please sign in again.");
                }
                throw new Error(errorData.detail || "Failed to create todo");
            }
            return res.json();
        } catch (error) {
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error("Network error. Please check your connection and try again.");
            }
            throw error;
        }
    },
    delete: async (id: string) => {
        const res = await fetch(`${API_BASE}/${id}`, {
            method: "DELETE",
            credentials: "include"
        });
        if (!res.ok) throw new Error("Failed to delete todo");
    },
    update: async (id: string, updates: any) => {
        const res = await fetch(`${API_BASE}/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify(updates),
            credentials: "include"
        });
        if (!res.ok) throw new Error("Failed to update todo");
        return res.json();
    }
};
