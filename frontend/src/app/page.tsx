import { redirect } from "next/navigation";

export default function Home() {
    // Phase II logic: redirect to signup/dashboard
    // In a real app we'd check session here, but standard redirect works for now
    redirect("/signup");
}
