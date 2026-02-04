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
      credentials: "include", // This allows cookies to be sent/received
      body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.detail || error.message || `Failed to sign up: ${res.status} ${res.statusText}`);
    }

    return await res.json();
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error(`Network error: Unable to connect to the server at ${API_URL}. Please check if the backend server is running.`);
    }
    // Re-throw error to be handled by caller
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
      credentials: "include", // This allows cookies to be sent/received
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.detail || error.message || `Failed to sign in: ${res.status} ${res.statusText}`);
    }

    return await res.json();
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error(`Network error: Unable to connect to the server at ${API_URL}. Please check if the backend server is running.`);
    }
    // Re-throw error to be handled by caller
    throw error;
  }
}
