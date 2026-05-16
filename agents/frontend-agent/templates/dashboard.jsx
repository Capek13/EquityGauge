import { useState, useEffect } from "react";
import styles from "./Dashboard.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/companies`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className={styles.skeleton} aria-label="Loading" />;
  if (error) return <p className={styles.error} role="alert">Error: {error}</p>;

  return (
    <div className={styles.dashboard}>
      <aside className={styles.sidebar}>{/* sidebar panels */}</aside>
      <main className={styles.content}>
        {/* main panels */}
      </main>
    </div>
  );
}
