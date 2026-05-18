# Few-Shot Examples

## Example 1 — Simple data card

**Input:**
> Create a React component that shows a single company's P/E ratio as a card. Props: ticker, name, pe (number or null).

**Output:**
```jsx
import styles from "./PeCard.module.css";

export default function PeCard({ ticker, name, pe }) {
  const peClass = pe === null ? styles.muted : pe > 30 ? styles.warning : pe < 15 ? styles.success : styles.neutral;

  return (
    <div className={styles.card}>
      <span className={styles.ticker}>{ticker}</span>
      <span className={styles.name}>{name}</span>
      <span className={`${styles.pe} ${peClass}`}>
        {pe !== null ? new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(pe) : "N/A"}
      </span>
    </div>
  );
}
```

```css
.card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
}
.ticker { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 600; color: var(--color-text); }
.name   { font-size: 12px; color: var(--color-text-muted); }
.pe     { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 600; }
.success { color: var(--color-success); }
.neutral { color: var(--color-text); }
.warning { color: var(--color-warning); }
.muted   { color: var(--color-text-muted); }
```

---

## Example 2 — Fetch list + progressive P/E loading

**Input:**
> Component that fetches all companies from GET /companies and shows a table. For each company fetch P/E from GET /companies/{ticker}/pe. Show company info immediately, fill in P/E as it loads per row.

**Key rules demonstrated:**
- `GET /companies` returns full objects — use `name`, `sector` directly, no second fetch needed
- Set `loading=false` right after the company list arrives — show the table immediately
- Fetch P/E per ticker independently with `forEach`+`async`, update each row via `setRows` as it resolves
- Error shows as inline banner — never replaces the table

**Output:**
```jsx
import { useState, useEffect, useCallback } from "react";
import styles from "./CompanyTable.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function CompanyTable() {
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

      // Show table immediately with name/sector — pe: undefined means "still loading"
      setRows(companies.map((c) => ({ ...c, pe: undefined })));
      setLoading(false);

      // Fetch P/E per row independently — update each cell as it arrives
      companies.forEach(async (c) => {
        try {
          const peRes = await fetch(`${API_BASE}/companies/${c.ticker}/pe`);
          const pe = peRes.status === 404 ? null : peRes.ok ? (await peRes.json()).pe ?? null : null;
          setRows((prev) => prev.map((r) => r.ticker === c.ticker ? { ...r, pe } : r));
        } catch {
          setRows((prev) => prev.map((r) => r.ticker === c.ticker ? { ...r, pe: null } : r));
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
      {error && (
        <div className={styles.errorBanner} role="alert">
          ⚠ {error}
        </div>
      )}
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.th}>Ticker</th>
            <th className={styles.th}>Name</th>
            <th className={styles.th}>Sector</th>
            <th className={styles.th}>P/E</th>
          </tr>
        </thead>
        <tbody>
          {loading
            ? Array.from({ length: 5 }).map((_, i) => (
                <tr key={i} aria-hidden="true">
                  {[0,1,2,3].map((j) => (
                    <td key={j} className={styles.td}><span className={styles.skeleton} /></td>
                  ))}
                </tr>
              ))
            : rows.map((row) => (
                <tr key={row.ticker} className={styles.row}>
                  <td className={styles.td}><span className={styles.ticker}>{row.ticker}</span></td>
                  <td className={styles.td}>{row.name ?? "—"}</td>
                  <td className={styles.td}><span className={styles.muted}>{row.sector ?? "—"}</span></td>
                  <td className={styles.td}>
                    {row.pe === undefined
                      ? <span className={styles.skeleton} />
                      : <span className={row.pe === null ? styles.muted : row.pe < 15 ? styles.success : row.pe <= 30 ? styles.neutral : styles.warning}>
                          {row.pe === null ? "N/A" : new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(row.pe)}
                        </span>
                    }
                  </td>
                </tr>
              ))
          }
        </tbody>
      </table>
    </div>
  );
}
```

```css
.wrapper { overflow-x: auto; }
.errorBanner {
  padding: 12px 16px;
  margin-bottom: 16px;
  background: color-mix(in srgb, var(--color-danger) 10%, var(--color-surface));
  border: 1px solid var(--color-danger);
  border-radius: 6px;
  color: var(--color-danger);
  font-size: 13px;
}
.table  { width: 100%; border-collapse: collapse; }
.th     { padding: 8px 12px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--color-text-muted); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.td     { padding: 12px; border-bottom: 1px solid var(--color-border); font-size: 14px; color: var(--color-text); }
.row:hover td { background: color-mix(in srgb, var(--color-border) 40%, transparent); }
.ticker { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.muted  { color: var(--color-text-muted); }
.success { color: var(--color-success); font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.neutral { color: var(--color-text);    font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.warning { color: var(--color-warning); font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.skeleton { display: inline-block; width: 64px; height: 14px; border-radius: 3px; background: linear-gradient(90deg, var(--color-surface) 25%, var(--color-border) 50%, var(--color-surface) 75%); background-size: 200% 100%; animation: shimmer 1.4s ease-in-out infinite; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
```

---

## Example 3 — Form with POST

**Input:**
> Add company form. Fields: ticker, name, currency (required). Exchange, sector, industry (optional). Posts to POST /companies. Show success/error feedback.

**Output:**
```jsx
import { useState } from "react";
import styles from "./AddCompanyForm.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const INITIAL = { ticker: "", name: "", currency: "", exchange: "", sector: "", industry: "", watchlist: true };

export default function AddCompanyForm({ onAdded }) {
  const [form, setForm]     = useState(INITIAL);
  const [status, setStatus] = useState(null); // { type: "success"|"error", message }
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/companies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus({ type: "error", message: data.message ?? `HTTP ${res.status}` });
        return;
      }
      setStatus({ type: "success", message: "Company added." });
      setForm(INITIAL);
      onAdded?.();
    } catch {
      setStatus({ type: "error", message: "Network error — is the backend running?" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      {status && (
        <p className={status.type === "success" ? styles.success : styles.error}>
          {status.message}
        </p>
      )}
      <input className={styles.input} name="ticker"   value={form.ticker}   onChange={handleChange} placeholder="Ticker *"       required />
      <input className={styles.input} name="name"     value={form.name}     onChange={handleChange} placeholder="Company name *" required />
      <input className={styles.input} name="currency" value={form.currency} onChange={handleChange} placeholder="Currency *"     required />
      <input className={styles.input} name="exchange" value={form.exchange} onChange={handleChange} placeholder="Exchange" />
      <input className={styles.input} name="sector"   value={form.sector}   onChange={handleChange} placeholder="Sector" />
      <input className={styles.input} name="industry" value={form.industry} onChange={handleChange} placeholder="Industry" />
      <button className={styles.submit} type="submit" disabled={loading}>
        {loading ? "Adding…" : "Add Company"}
      </button>
    </form>
  );
}
```

```css
.form    { display: flex; flex-direction: column; gap: 8px; }
.input   { padding: 8px 10px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: 6px; color: var(--color-text); font-size: 13px; outline: none; }
.input:focus { border-color: var(--color-accent); }
.input::placeholder { color: var(--color-text-muted); }
.submit  { margin-top: 8px; padding: 9px 16px; background: var(--color-brand); color: #fff; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; }
.submit:hover    { opacity: 0.88; }
.submit:disabled { opacity: 0.5; cursor: not-allowed; }
.success { font-size: 13px; color: var(--color-success); }
.error   { font-size: 13px; color: var(--color-danger); }
```
