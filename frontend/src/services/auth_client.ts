const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type SignupPayload = {
  name: string;
  email: string;
  password: string;
};

type SigninPayload = {
  email: string;
  password: string;
};

export async function signupUser({ name, email, password }: SignupPayload) {
  try {
    const res = await fetch(`${API_URL}/api/v1/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.message || "Failed to sign up");
    }

    return await res.json();
  } catch (error) {
    console.error("Signup network error:", error);
    throw error;
  }
}

export async function signinUser({ email, password }: SigninPayload) {
  try {
    const res = await fetch(`${API_URL}/api/v1/signin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.message || "Failed to sign in");
    }

    return await res.json();
  } catch (error) {
    console.error("Signin network error:", error);
    throw error;
  }
}
