"use client";
import { useState } from "react";

export default function TodoItem({ todo, onToggle, onDelete, onUpdate }: any) {
    const [isEditing, setIsEditing] = useState(false);
    const [title, setTitle] = useState(todo.title);

    const handleUpdate = () => {
        onUpdate(todo.id, { title });
        setIsEditing(false);
    };

    return (
        <li className="flex justify-between items-center bg-gray-50 p-3 border rounded">
            <div className="flex items-center gap-3 flex-grow">
                <input type="checkbox" checked={todo.is_completed} onChange={() => onToggle(todo.id, !todo.is_completed)} />
                {isEditing ? (
                    <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} onBlur={handleUpdate} className="border px-1" autoFocus />
                ) : (
                    <span className={todo.is_completed ? "line-through text-gray-400" : ""} onDoubleClick={() => setIsEditing(true)}>{todo.title}</span>
                )}
            </div>
            <button onClick={() => onDelete(todo.id)} className="text-red-500">Delete</button>
        </li>
    );
}
