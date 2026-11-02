import {
    createContext,
    useContext,
    useEffect,
    useState,
  } from "react";

const AuthContext = createContext(null);


export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      async function checkSession() {
        try {
          const response = await fetch("/api/auth/me/", {
            credentials: "include",
          });
  
          if (response.ok) {
            setUser(await response.json());
          }
        } catch (error) {
          console.error("Could not check session:", error);
        } finally {
          setLoading(false);
        }
      }
  
      checkSession();
    }, []);
    
    return (
        <AuthContext.Provider value={{ user, setUser, loading }}>
          {children}
        </AuthContext.Provider>
      );
    }
    
export function useAuth() {
    return useContext(AuthContext);
}