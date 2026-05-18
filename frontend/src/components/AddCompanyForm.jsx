import { useState, useEffect } from "react";
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
  const [successMessage, setSuccessMessage] = useState(null);

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
    setSuccessMessage(null);

    try {
      const res = await fetch(`${API_BASE}/companies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const responseData = await res.json();
      setData(responseData);

      if (res.status === 201) {
        setSuccessMessage(
          `${form.ticker.toUpperCase()} was successfully added to your watchlist.`
        );
        setForm(INITIAL_FORM);
        onAdded?.();
      } else if (res.status === 409) {
        setError(
          responseData?.message ??
            `${form.ticker.toUpperCase()} already exists in the system.`
        );
      } else {
        setError(responseData?.message ?? `Unexpected error (HTTP ${res.status}).`);
      }
    } catch {
      setError("Network error — could not reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDismissError = () => setError(null);
  const handleDismissSuccess = () => setSuccessMessage(null);

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h2 className={styles.title}>Add Company</h2>
        <p className={styles.subtitle}>
          Track a new equity by adding its ticker and metadata below.
        </p>
      </div>

      {successMessage && (
        <div className={styles.banner} role="status" aria-live="polite">
          <div className={styles.bannerSuccess}>
            <span className={styles.bannerIcon} aria-hidden="true">✓</span>
            <span className={styles.bannerText}>{successMessage}</span>
            <button
              className={styles.bannerDismiss}
              onClick={handleDismissSuccess}
              aria-label="Dismiss success message"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className={styles.banner} role="alert" aria-live="assertive">
          <div className={styles.bannerError}>
            <span className={styles.bannerIcon} aria-hidden="true">⚠</span>
            <span className={styles.bannerText}>{error}</span>
            <button
              className={styles.bannerDismiss}
              onClick={handleDismissError}
              aria-label="Dismiss error message"
            >
              ×
            </button>
          </div>
        </div>
      )}

      <form
        className={styles.form}
        onSubmit={handleSubmit}
        noValidate
        aria-label="Add company form"
      >
        <fieldset className={styles.fieldset} disabled={loading}>
          <legend className={styles.legend}>Required fields</legend>

          <div className={styles.fieldGroup}>
            <div className={styles.field}>
              <label className={styles.label} htmlFor="ticker">
                Ticker <span className={styles.required} aria-hidden="true">*</span>
              </label>
              <input
                className={styles.input}
                id="ticker"
                name="ticker"
                type="text"
                value={form.ticker}
                onChange={handleChange}
                placeholder="e.g. AAPL"
                required
                autoComplete="off"
                spellCheck={false}
                aria-required="true"
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
                type="text"
                value={form.name}
                onChange={handleChange}
                placeholder="e.g. Apple Inc."
                required
                aria-required="true"
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
                type="text"
                value={form.currency}
                onChange={handleChange}
                placeholder="e.g. USD"
                required
                maxLength={3}
                aria-required="true"
              />
            </div>
          </div>
        </fieldset>

        <fieldset className={styles.fieldset} disabled={loading}>
          <legend className={styles.legend}>Optional fields</legend>

          <div className={styles.fieldGroup}>
            <div className={styles.field}>
              <label className={styles.label} htmlFor="exchange">
                Exchange
              </label>
              <input
                className={styles.input}
                id="exchange"
                name="exchange"
                type="text"
                value={form.exchange}
                onChange={handleChange}
                placeholder="e.g. NASDAQ"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="sector">
                Sector
              </label>
              <input
                className={styles.input}
                id="sector"
                name="sector"
                type="text"
                value={form.sector}
                onChange={handleChange}
                placeholder="e.g. Technology"
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="industry">
                Industry
              </label>
              <input
                className={styles.input}
                id="industry"
                name="industry"
                type="text"
                value={form.industry}
                onChange={handleChange}
                placeholder="e.g. Consumer Electronics"
              />
            </div>
          </div>
        </fieldset>

        <div className={styles.formFooter}>
          <label className={styles.checkboxLabel} htmlFor="watchlist">
            <input
              className={styles.checkbox}
              id="watchlist"
              name="watchlist"
              type="checkbox"
              checked={form.watchlist}
              onChange={handleChange}
              disabled={loading}
            />
            <span className={styles.checkboxCustom} aria-hidden="true" />
            <span className={styles.checkboxText}>Add to watchlist</span>
          </label>

          <button
            className={styles.submitButton}
            type="submit"
            disabled={loading}
            aria-busy={loading}
          >
            {loading ? (
              <span className={styles.buttonLoading}>
                <span className={styles.spinner} aria-hidden="true" />
                Adding…
              </span>
            ) : (
              "Add Company"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}