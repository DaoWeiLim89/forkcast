async function getCsrfToken() {
    const response = await fetch("/api/auth/csrf/", {
      credentials: "include",
    });
  
    if (!response.ok) {
      throw new Error("Could not get CSRF token.");
    }
  
    const data = await response.json();
    return data.csrfToken;
  }
  
  async function postAuth(endpoint, body) {
    const csrfToken = await getCsrfToken();
  
    const response = await fetch(`/api/auth/${endpoint}/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(body),
    });
  
    const isJson = response.headers
      .get("content-type")
      ?.includes("application/json");
  
    const data = isJson ? await response.json() : {};
  
    if (!response.ok) {
      const message =
        data.message ||
        Object.entries(data)
          .map(([field, messages]) =>
            `${field}: ${
              Array.isArray(messages) ? messages.join(" ") : String(messages)
            }`
          )
          .join("\n") ||
        "Request failed. Please try again.";
  
      throw new Error(message);
    }
  
    return data;
  }
  
  export function signIn(email, password) {
    return postAuth("sign-in", { email, password });
  }
  
  export function signUp(email, username, password) {
    return postAuth("sign-up", { email, username, password });
  }
  
  export function signOut() {
    return postAuth("sign-out", {});
  }
  
  export async function getCurrentUser() {
    const response = await fetch("/api/auth/me/", {
      credentials: "include",
    });
  
    if (response.status === 401) {
      return null;
    }
  
    if (!response.ok) {
      throw new Error("Could not load current user.");
    }
  
    return response.json();
  }