import { useState } from "react";
import { useAuth } from "./AuthProvider";

export default function SignInPage() {
  const { user, setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await signIn(email, password);
      setUser(data.user);
      setPassword("");
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  if (user) {
    return <p>Signed in as {user.email}</p>;
  }

  return (
    <main>
      <h1>Sign in</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input
            type="email"
            autoComplete="username"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>

        <label>
          Password
          <input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>

        {error && (
          <p role="alert" style={{ whiteSpace: "pre-line" }}>
            {error}
          </p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <a href="/sign-up">Create an account</a>
    </main>
  );
}