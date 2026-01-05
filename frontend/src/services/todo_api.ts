const API_BASE = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/api/v1/todos";

function getCookies(): string {
    if (typeof document === 'undefined') return '';
    return document.cookie;
}

export const todoApi = {
    list: async () => {
        const res = await fetch(API_BASE, {
            headers: {
                "Accept": "application/json",
            },
            credentials: "include"
        });
        if (!res.ok) throw new Error("Failed to fetch todos");
        return res.json();
    },
    create: async (title: string) => {
        const res = await fetch(API_BASE + `?title=${encodeURIComponent(title)}`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
            },
            credentials: "include"
        });
        if (!res.ok) throw new Error("Failed to create todo");
        return res.json();
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
