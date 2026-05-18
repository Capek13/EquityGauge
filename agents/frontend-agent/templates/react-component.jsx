import { useState, useEffect, useCallback } from "react";
import styles from "./Component.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function Component() {
  const [rows, setRows]       = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/companies`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const { companies } = await res.json();
      // Show UI immediately with full company objects
      setRows(companies.map((c) => ({ ...c, pe: undefined })));
      setLoading(false);
      // Fetch P/E per row — update cells as they arrive
      companies.forEach(async (c) => {
        try {
          const r = await fetch(`${API_BASE}/companies/${c.ticker}/pe`);
          const pe = r.status === 404 ? null : r.ok ? (await r.json()).pe ?? null : null;
          setRows((prev) => prev.map((row) => row.ticker === c.ticker ? { ...row, pe } : row));
        } catch {
          setRows((prev) => prev.map((row) => row.ticker === c.ticker ? { ...row, pe: null } : row));
        }
      });
    } catch (e) {
      setError(e.message || "Failed to load.");
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <div className={styles.wrapper}>
      {/* Error as inline banner — never replaces the whole UI */}
      {error && (
        <div className={styles.errorBanner} role="alert">
          ⚠ {error}
        </div>
      )}
      {/* content */}
    </div>
  );
}
