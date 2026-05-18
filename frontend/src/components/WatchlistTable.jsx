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
          <span className={styles.skeletonBlock} />
        </td>
      ))}
    </tr>
  );
}

export default function WatchlistTable() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingTickers, setDeletingTickers] = useState(new Set());
  const [deleteErrors, setDeleteErrors] = useState({});

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

      const peResults = await Promise.all(tickers.map((t) => fetchPe(t)));
      setRows(
        tickers.map((ticker, i) => ({
          ticker,
          name: null,
          sector: null,
          pe: peResults[i],
        }))
      );
    } catch (e) {
      setError(e.message || "Failed to load watchlist.");
    } finally {
      setLoading(false);
    }
  }, [fetchPe]);

  useEffect(() => {
    loadWatchlist();
  }, [loadWatchlist]);

  const handleDelete = async (ticker) => {
    setDeletingTickers((prev) => new Set(prev).add(ticker));
    setDeleteErrors((prev) => {
      const next = { ...prev };
      delete next[ticker];
      return next;
    });
    try {
      const res = await fetch(`${API_BASE}/companies/${ticker}`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || `HTTP ${res.status}`);
      }
      setRows((prev) => prev.filter((r) => r.ticker !== ticker));
    } catch (e) {
      setDeleteErrors((prev) => ({
        ...prev,
        [ticker]: e.message || "Delete failed.",
      }));
    } finally {
      setDeletingTickers((prev) => {
        const next = new Set(prev);
        next.delete(ticker);
        return next;
      });
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h2 className={styles.title}>Watchlist</h2>
        {!loading && !error && (
          <span className={styles.count} aria-live="polite">
            {rows.length} {rows.length === 1 ? "company" : "companies"}
          </span>
        )}
      </div>

      {error && (
        <div className={styles.errorBanner} role="alert">
          <span className={styles.errorIcon} aria-hidden="true">⚠</span>
          <span className={styles.errorMessage}>{error}</span>
          <button
            className={styles.errorDismiss}
            onClick={() => setError(null)}
            aria-label="Dismiss error"
          >
            ✕
          </button>
        </div>
      )}

      <div className={styles.tableWrapper}>
        <table className={styles.table} aria-label="Equity watchlist">
          <thead>
            <tr>
              {COLUMNS.map((col, i) => (
                <th
                  key={i}
                  className={styles.th}
                  scope="col"
                  aria-label={col || "Actions"}
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <SkeletonRow key={i} />
              ))
            ) : rows.length === 0 ? (
              <tr>
                <td colSpan={COLUMNS.length} className={styles.emptyState}>
                  <span className={styles.emptyIcon} aria-hidden="true">📋</span>
                  <span className={styles.emptyText}>No companies in watchlist</span>
                </td>
              </tr>
            ) : (
              rows.map((row) => (
                <tr key={row.ticker} className={styles.row}>
                  <td className={styles.tdTicker}>
                    <span className={styles.ticker}>{row.ticker}</span>
                  </td>
                  <td className={styles.td}>
                    <span className={styles.name}>
                      {row.name ?? (
                        <span className={styles.naText}>—</span>
                      )}
                    </span>
                  </td>
                  <td className={styles.td}>
                    <span className={row.sector ? styles.sector : styles.naText}>
                      {row.sector ?? "—"}
                    </span>
                  </td>
                  <td className={styles.tdPe}>
                    <span
                      className={`${styles.peValue} ${getPeClass(row.pe)}`}
                      aria-label={`P/E ratio: ${formatPe(row.pe)}`}
                    >
                      {row.pe === undefined ? (
                        <span className={styles.peLoading} aria-hidden="true" />
                      ) : (
                        formatPe(row.pe)
                      )}
                    </span>
                  </td>
                  <td className={styles.tdAction}>
                    {deleteErrors[row.ticker] && (
                      <span className={styles.rowError} role="alert">
                        {deleteErrors[row.ticker]}
                      </span>
                    )}
                    <button
                      className={styles.deleteBtn}
                      onClick={() => handleDelete(row.ticker)}
                      disabled={deletingTickers.has(row.ticker)}
                      aria-label={`Remove ${row.ticker} from watchlist`}
                    >
                      {deletingTickers.has(row.ticker) ? (
                        <span className={styles.spinner} aria-hidden="true" />
                      ) : (
                        "Remove"
                      )}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}