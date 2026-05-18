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

  const handleAdded = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className={styles.root}>
      {/* ── Header ── */}
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <div className={styles.brand}>
            <a href="/" className={styles.logo} aria-label="EquityGauge — go to home">
              <span className={styles.logoMark}>▲</span>
              EquityGauge
            </a>
            <span className={styles.subtitle}>P/E Ratio Tracker</span>
          </div>
          <div className={styles.headerMeta}>
            {!loading && !error && (
              <span className={styles.companyCount}>
                {data?.companies?.length ?? 0} companies tracked
              </span>
            )}
          </div>
        </div>
      </header>

      {error && (
        <div className={styles.errorBanner} role="alert">
          <span className={styles.errorIcon} aria-hidden="true">⚠</span>
          <span>Backend nedostupný — {error}</span>
        </div>
      )}

      {/* ── Body ── */}
      <div className={styles.dashboard}>
        {/* Sidebar */}
        <aside className={styles.sidebar} aria-label="Add company panel">
          <div className={styles.sidebarHeader}>
            <h2 className={styles.sidebarTitle}>Add Company</h2>
            <p className={styles.sidebarHint}>
              Enter a ticker symbol to begin tracking its P/E ratio.
            </p>
          </div>
          <AddCompanyForm onAdded={handleAdded} />
        </aside>

        {/* Main content */}
        <main className={styles.content} aria-label="Watchlist">
          <div className={styles.contentHeader}>
            <h1 className={styles.contentTitle}>Watchlist</h1>
            <span className={styles.refreshBadge} aria-live="polite">
              {refreshKey > 0 && `Updated ${refreshKey}×`}
            </span>
          </div>
          <WatchlistTable refreshKey={refreshKey} />
        </main>
      </div>
    </div>
  );
}