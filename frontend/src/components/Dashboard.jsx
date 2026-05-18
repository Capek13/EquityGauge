import { useState, useEffect } from "react";
import styles from "./Dashboard.module.css";
import AddCompanyForm from "./AddCompanyForm";
import WatchlistTable from "./WatchlistTable";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

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

  const handleAdded = () => setRefreshKey((k) => k + 1);

  if (loading) return <div className={styles.skeleton} aria-label="Loading" />;
  if (error) return <p className={styles.error} role="alert">Error: {error}</p>;

  return (
    <div className={styles.root}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <div className={styles.brand}>
            <span className={styles.logo}>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
                <rect x="1" y="1" width="20" height="20" rx="4" fill="var(--color-brand)" opacity="0.18" />
                <polyline
                  points="3,16 7,10 11,13 15,7 19,4"
                  stroke="var(--color-brand)"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  fill="none"
                />
              </svg>
            </span>
            <span className={styles.logoText}>EquityGauge</span>
          </div>
          <span className={styles.subtitle}>P/E Ratio Tracker</span>
        </div>
      </header>

      <div className={styles.dashboard}>
        <aside className={styles.sidebar} aria-label="Add company panel">
          <div className={styles.sidebarHeader}>
            <h2 className={styles.sidebarTitle}>Add Company</h2>
            <p className={styles.sidebarDesc}>Track a new ticker on your watchlist.</p>
          </div>
          <AddCompanyForm onAdded={handleAdded} />
        </aside>

        <main className={styles.content} aria-label="Watchlist">
          <div className={styles.contentHeader}>
            <h1 className={styles.contentTitle}>Watchlist</h1>
            {data?.companies?.length > 0 && (
              <span className={styles.badge}>{data.companies.length} companies</span>
            )}
          </div>
          <WatchlistTable refreshKey={refreshKey} />
        </main>
      </div>
    </div>
  );
}