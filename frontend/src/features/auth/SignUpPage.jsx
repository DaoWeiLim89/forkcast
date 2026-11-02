import {useState} from "react";
import { signUp } from "./api";

export default function SignUpPage() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);
  
    async function handleSubmit(event) {
      event.preventDefault();
      setError("");
      setLoading(true);
      
      try {
        await signUp(email, username, password);
        setPassword("");
        setSuccess(true);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }
    
    if (success) {
        return (
          <main>
            <h1>Account created!</h1>
            <a href="/sign-in">Continue to sign in</a>
          </main>
        );
      }
      
      return (
        <main>
          <h1>Sign up</h1>
      
          <form onSubmit={handleSubmit}>
            <label>
              Email
              <input
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>
      
            <label>
              Username
              <input
                type="text"
                autoComplete="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
              />
            </label>
      
            <label>
              Password
              <input
                type="password"
                autoComplete="new-password"
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
              {loading ? "Creating account..." : "Sign up"}
            </button>
          </form>
        </main>
      );
}