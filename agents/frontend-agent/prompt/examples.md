# Few-Shot Examples

## Example 1 — Simple data card

**Input:**
> Create a React component that shows a single company's P/E ratio as a card. Props: ticker, name, pe (number or null).

**Output:**
```jsx
import styles from "./PeCard.module.css";

export default function PeCard({ ticker, name, pe }) {
  const peClass = pe === null ? "muted" : pe > 30 ? "warning" : pe < 15 ? "success" : "neutral";

  return (
    <div className={styles.card}>
      <span className={styles.ticker}>{ticker}</span>
      <span className={styles.name}>{name}</span>
      <span className={`${styles.pe} ${styles[peClass]}`}>
        {pe !== null ? pe.toFixed(2) : "N/A"}
      </span>
    </div>
  );
}
```

---

## Example 2 — Fetch + list

**Input:**
> Component that fetches all companies from GET /companies and renders a list of tickers. Show loading and error states.

**Output:**
```jsx
import { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function CompanyList() {
  const [tickers, setTickers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/companies`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => setTickers(data.companies))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (error) return <p style={{ color: "var(--color-danger)" }}>Error: {error}</p>;

  return (
    <ul>
      {tickers.map((t) => (
        <li key={t} style={{ fontFamily: "'JetBrains Mono', monospace" }}>{t}</li>
      ))}
    </ul>
  );
}
```

---

## Example 3 — Form with POST

**Input:**
> Add company form. Fields: ticker, name, currency (required). Exchange, sector, industry (optional). Posts to POST /companies. Show success/error feedback.

**Output:**
```jsx
import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const INITIAL = { ticker: "", name: "", currency: "", exchange: "", sector: "", industry: "", watchlist: true };

export default function AddCompanyForm({ onAdded }) {
  const [form, setForm] = useState(INITIAL);
  const [status, setStatus] = useState(null); // { type: "success"|"error", message }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    try {
      const res = await fetch(`${API_BASE}/companies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus({ type: "error", message: data.message });
        return;
      }
      setStatus({ type: "success", message: data.message });
      setForm(INITIAL);
      onAdded?.();
    } catch {
      setStatus({ type: "error", message: "Network error" });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {status && (
        <p style={{ color: status.type === "success" ? "var(--color-success)" : "var(--color-danger)" }}>
          {status.message}
        </p>
      )}
      <input name="ticker" value={form.ticker} onChange={handleChange} placeholder="Ticker *" required />
      <input name="name" value={form.name} onChange={handleChange} placeholder="Company name *" required />
      <input name="currency" value={form.currency} onChange={handleChange} placeholder="Currency *" required />
      <input name="exchange" value={form.exchange} onChange={handleChange} placeholder="Exchange" />
      <input name="sector" value={form.sector} onChange={handleChange} placeholder="Sector" />
      <input name="industry" value={form.industry} onChange={handleChange} placeholder="Industry" />
      <button type="submit">Add Company</button>
    </form>
  );
}
```
