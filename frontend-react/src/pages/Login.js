import { useState } from "react";
import API from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const res = await API.post("/auth/login", { email, password });
      
      // IMPORTANT: Double check if your backend returns 'token' or 'access_token'
      const token = res.data.token || res.data.access_token; 
      
      if (token) {
        localStorage.setItem("token", token);
        // Using replace ensures they can't click "back" to return to the login form
        window.location.replace("/dashboard"); 
      } else {
        setError("Login failed: No token received from server.");
      }
    } catch (err) {
      console.error("Login Error:", err);
      setError(err.response?.data?.detail || err.response?.data?.message || "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleLogin} style={styles.card}>
        <h2 style={styles.title}>Welcome Back</h2>
        <p style={styles.subtitle}>Please enter your details</p>

        {error && <div style={styles.error}>{error}</div>}

        <div style={styles.inputGroup}>
          <label style={styles.label}>Email</label>
          <input
            required
            type="email"
            value={email} // Controlled component
            placeholder="name@company.com"
            style={styles.input}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Password</label>
          <input
            required
            type="password"
            value={password} // Controlled component
            placeholder="••••••••"
            style={styles.input}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button 
          type="submit" 
          disabled={isLoading} 
          style={isLoading ? {...styles.button, opacity: 0.7, cursor: "not-allowed"} : styles.button}
        >
          {isLoading ? "Signing in..." : "Login"}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: { display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", backgroundColor: "#f4f7f6" },
  card: { padding: "40px", borderRadius: "8px", backgroundColor: "#fff", boxShadow: "0 4px 6px rgba(0,0,0,0.1)", width: "100%", maxWidth: "400px" },
  title: { margin: "0 0 8px 0", textAlign: "center", color: "#333" },
  subtitle: { margin: "0 0 24px 0", textAlign: "center", color: "#666", fontSize: "14px" },
  inputGroup: { marginBottom: "16px", display: "flex", flexDirection: "column", gap: "8px" },
  label: { fontSize: "14px", fontWeight: "bold", color: "#555" },
  input: { padding: "12px", borderRadius: "4px", border: "1px solid #ddd", fontSize: "16px", outlineColor: "#007bff" },
  button: { width: "100%", padding: "12px", backgroundColor: "#007bff", color: "#fff", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "16px", marginTop: "10px", fontWeight: "bold" },
  error: { padding: "10px", backgroundColor: "#fff1f0", border: "1px solid #ffa39e", color: "#cf1322", borderRadius: "4px", marginBottom: "16px", fontSize: "14px", textAlign: "center" }
};