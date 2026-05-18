import { useState } from "react";
import styles from "./AddCompanyForm.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const INITIAL_FORM = {
  ticker: "",
  name: "",
  currency: "",
  exchange: "",
  sector: "",
  industry: "",
  watchlist: true,
};

export default function AddCompanyForm({ onAdded }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState(INITIAL_FORM);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const res = await fetch(`${API_BASE}/companies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const json = await res.json();

      if (res.status === 201) {
        setData(json.message ?? "Company added successfully.");
        setForm(INITIAL_FORM);
        onAdded?.();
      } else if (res.status === 409) {
        setError(json.message ?? "Ticker already exists.");
      } else {
        setError(json.message ?? `Unexpected error (HTTP ${res.status}).`);
      }
    } catch {
      setError("Network error — could not reach the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <h2 className={styles.heading}>Add Company</h2>

      <form
        className={styles.form}
        onSubmit={handleSubmit}
        noValidate
        aria-label="Add company form"
      >
        {data && (
          <div
            className={styles.banner}
            data-variant="success"
            role="status"
            aria-live="polite"
          >
            <span className={styles.bannerIcon} aria-hidden="true">✓</span>
            {data}
          </div>
        )}

        {error && (
          <div
            className={styles.banner}
            data-variant="error"
            role="alert"
            aria-live="assertive"
          >
            <span className={styles.bannerIcon} aria-hidden="true">✕</span>
            {error}
            <button
              type="button"
              className={styles.bannerDismiss}
              aria-label="Dismiss error"
              onClick={() => setError(null)}
            >
              ×
            </button>
          </div>
        )}

        <div className={styles.grid}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="ticker">
              Ticker <span className={styles.required} aria-hidden="true">*</span>
            </label>
            <input
              className={styles.input}
              id="ticker"
              name="ticker"
              value={form.ticker}
              onChange={handleChange}
              placeholder="e.g. AAPL"
              required
              autoComplete="off"
              spellCheck="false"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="name">
              Company Name <span className={styles.required} aria-hidden="true">*</span>
            </label>
            <input
              className={styles.input}
              id="name"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="e.g. Apple Inc."
              required
              autoComplete="off"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="currency">
              Currency <span className={styles.required} aria-hidden="true">*</span>
            </label>
            <input
              className={styles.input}
              id="currency"
              name="currency"
              value={form.currency}
              onChange={handleChange}
              placeholder="e.g. USD"
              required
              autoComplete="off"
              spellCheck="false"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="exchange">
              Exchange
              <span className={styles.optional}> — optional</span>
            </label>
            <input
              className={styles.input}
              id="exchange"
              name="exchange"
              value={form.exchange}
              onChange={handleChange}
              placeholder="e.g. NASDAQ"
              autoComplete="off"
              spellCheck="false"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="sector">
              Sector
              <span className={styles.optional}> — optional</span>
            </label>
            <input
              className={styles.input}
              id="sector"
              name="sector"
              value={form.sector}
              onChange={handleChange}
              placeholder="e.g. Technology"
              autoComplete="off"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="industry">
              Industry
              <span className={styles.optional}> — optional</span>
            </label>
            <input
              className={styles.input}
              id="industry"
              name="industry"
              value={form.industry}
              onChange={handleChange}
              placeholder="e.g. Consumer Electronics"
              autoComplete="off"
            />
          </div>
        </div>

        <div className={styles.checkboxRow}>
          <input
            className={styles.checkbox}
            type="checkbox"
            id="watchlist"
            name="watchlist"
            checked={form.watchlist}
            onChange={handleChange}
          />
          <label className={styles.checkboxLabel} htmlFor="watchlist">
            Add to watchlist
          </label>
        </div>

        <div className={styles.footer}>
          <p className={styles.requiredNote}>
            <span className={styles.required}>*</span> Required fields
          </p>
          <button
            className={styles.submitButton}
            type="submit"
            disabled={loading}
            aria-busy={loading}
          >
            {loading ? (
              <>
                <span className={styles.spinner} aria-hidden="true" />
                Adding…
              </>
            ) : (
              "Add Company"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}