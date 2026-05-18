import { useState, useEffect, useCallback } from "react";
import styles from "./WatchlistTable.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const COLUMNS = ["Ticker", "Name", "Sector", "P/E Ratio", ""];

function getPeClass(pe) {
  if (pe === null || pe === undefined) return styles.peMuted;
  if (pe < 15) return styles.peSuccess;
  if (pe <= 30) return styles.peNeutral;
  return styles.peWarning;
}

function formatPe(pe) {
  if (pe === null || pe === undefined) return "N/A";
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(pe);
}

function SkeletonRow() {
  return (
    <tr className={styles.skeletonRow} aria-hidden="true">
      {COLUMNS.map((_, i) => (
        <td key={i} className={styles.skeletonCell}>
          <span className={styles.shimmer} />
        </td>
      ))}
    </tr>
  );
}

function ErrorBanner({ message, onDismiss }) {
  return (
    <div className={styles.errorBanner} role="alert">
      <span className={styles.errorIcon} aria-hidden="true">⚠</span>
      <span className={styles.errorMessage}>{message}</span>
      <button
        className={styles.errorDismiss}
        onClick={onDismiss}
        aria-label="Dismiss error"
      >
        ✕
      </button>
    </div>
  );
}

export default function WatchlistTable() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingTickers, setDeletingTickers] = useState(new Set());

  const fetchPe = useCallback(async (ticker) => {
    try {
      const res = await fetch(`${API_BASE}/companies/${ticker}/pe`);
      if (res.status === 404) return null;
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return data.pe ?? null;
    } catch {
      return null;
    }
  }, []);

  const loadWatchlist = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/companies`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const tickers = data.companies ?? [];

      const initialRows = tickers.map((ticker) => ({
        ticker,
        name: null,
        sector: null,
        pe: undefined,
      }));
      setRows(initialRows);
      setLoading(false);

      const peResults = await Promise.all(
        tickers.map(async (ticker) => {
          const pe = await fetchPe(ticker);
          return { ticker, pe };
        })
      );

      setRows((prev) =>
        prev.map((row) => {
          const found = peResults.find((r) => r.ticker === row.ticker);
          return found ? { ...row, pe: found.pe } : row;
        })
      );
    } catch (e) {
      setError(e.message || "Failed to load watchlist");
      setLoading(false);
    }
  }, [fetchPe]);

  useEffect(() => {
    loadWatchlist();
  }, [loadWatchlist]);

  const handleDelete = async (ticker) => {
    setDeletingTickers((prev) => new Set(prev).add(ticker));
    try {
      const res = await fetch(`${API_BASE}/companies/${ticker}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setRows((prev) => prev.filter((row) => row.ticker !== ticker));
    } catch (e) {
      setError(`Failed to delete ${ticker}: ${e.message}`);
    } finally {
      setDeletingTickers((prev) => {
        const next = new Set(prev);
        next.delete(ticker);
        return next;
      });
    }
  };

  const skeletonCount = 5;

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h2 className={styles.title}>Watchlist</h2>
        <span className={styles.count}>
          {!loading && `${rows.length} ${rows.length === 1 ? "company" : "companies"}`}
        </span>
      </div>

      {error && (
        <ErrorBanner message={error} onDismiss={() => setError(null)} />
      )}

      <div className={styles.tableWrapper}>
        <table className={styles.table} aria-label="Watchlist table">
          <thead>
            <tr>
              {COLUMNS.map((col) => (
                <th key={col} className={styles.th} scope="col">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading
              ? Array.from({ length: skeletonCount }).map((_, i) => (
                  <SkeletonRow key={i} />
                ))
              : rows.length === 0
              ? (
                <tr>
                  <td colSpan={COLUMNS.length} className={styles.emptyState}>
                    <span className={styles.emptyIcon} aria-hidden="true">📋</span>
                    <span className={styles.emptyText}>No companies in watchlist</span>
                  </td>
                </tr>
              )
              : rows.map((row) => {
                  const isDeleting = deletingTickers.has(row.ticker);
                  const peLoading = row.pe === undefined;
                  return (
                    <tr
                      key={row.ticker}
                      className={`${styles.row} ${isDeleting ? styles.rowDeleting : ""}`}
                    >
                      <td className={styles.tdTicker}>
                        <span className={styles.ticker}>{row.ticker}</span>
                      </td>
                      <td className={styles.td}>
                        {row.name ?? (
                          <span className={styles.muted}>—</span>
                        )}
                      </td>
                      <td className={styles.td}>
                        {row.sector ?? (
                          <span className={styles.muted}>—</span>
                        )}
                      </td>
                      <td className={styles.td}>
                        {peLoading ? (
                          <span className={styles.shimmerInline} aria-label="Loading P/E" />
                        ) : (
                          <span className={`${styles.pe} ${getPeClass(row.pe)}`}>
                            {formatPe(row.pe)}
                          </span>
                        )}
                      </td>
                      <td className={styles.tdAction}>
                        <button
                          className={styles.deleteBtn}
                          onClick={() => handleDelete(row.ticker)}
                          disabled={isDeleting}
                          aria-label={`Delete ${row.ticker}`}
                        >
                          {isDeleting ? (
                            <span className={styles.deletingSpinner} aria-hidden="true" />
                          ) : (
                            "Delete"
                          )}
                        </button>
                      </td>
                    </tr>
                  );
                })}
          </tbody>
        </table>
      </div>
    </div>
  );
}