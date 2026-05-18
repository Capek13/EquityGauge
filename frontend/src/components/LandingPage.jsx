import styles from "./LandingPage.module.css";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const FEATURES = [
  {
    id: "live-data",
    icon: "⚡",
    title: "Live Data",
    description:
      "P/E ratios and equity metrics scraped directly from Yahoo Finance — always up to date, no stale caches.",
  },
  {
    id: "watchlist",
    icon: "★",
    title: "Watchlist",
    description:
      "Add or remove tickers instantly. Build a focused list of the companies that matter to your portfolio.",
  },
  {
    id: "pe-scoring",
    icon: "◈",
    title: "Visual P/E Scoring",
    description:
      "Color-coded P/E bands at a glance — green for undervalued, amber for elevated, red for caution zones.",
  },
];

export default function LandingPage() {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <span className={styles.logo}>
            <span className={styles.logoBracket}>[</span>
            EquityGauge
            <span className={styles.logoBracket}>]</span>
          </span>

          <nav className={styles.nav} aria-label="Primary navigation">
            <a href="#features" className={styles.navLink}>
              Features
            </a>
            <a
              href="/dashboard"
              className={styles.navCta}
              aria-label="Go to Dashboard"
            >
              Go to Dashboard
            </a>
          </nav>
        </div>
      </header>

      <main className={styles.main}>
        <section className={styles.hero} aria-labelledby="hero-heading">
          <div className={styles.heroBadge}>
            <span className={styles.heroBadgeDot} aria-hidden="true" />
            Live Yahoo Finance data
          </div>

          <h1 id="hero-heading" className={styles.heroHeadline}>
            Track P/E Ratios
            <br />
            <span className={styles.heroAccent}>in Real Time</span>
          </h1>

          <p className={styles.heroSubline}>
            EquityGauge pulls price-to-earnings data straight from Yahoo Finance
            so you can monitor valuations, manage your watchlist, and spot
            over- or under-priced equities — all in one focused dashboard.
          </p>

          <div className={styles.heroActions}>
            <a
              href="/dashboard"
              className={styles.ctaPrimary}
              aria-label="Get started with EquityGauge"
            >
              Get started →
            </a>
            <a href="#features" className={styles.ctaSecondary}>
              See features
            </a>
          </div>

          <div className={styles.heroMeta} aria-hidden="true">
            <span className={styles.heroMetaItem}>
              <span className={styles.heroMetaDot} data-color="success" />
              P/E &lt; 15 — undervalued
            </span>
            <span className={styles.heroMetaItem}>
              <span className={styles.heroMetaDot} data-color="neutral" />
              P/E 15–30 — fair
            </span>
            <span className={styles.heroMetaItem}>
              <span className={styles.heroMetaDot} data-color="warning" />
              P/E &gt; 30 — elevated
            </span>
          </div>
        </section>

        <section
          id="features"
          className={styles.features}
          aria-labelledby="features-heading"
        >
          <h2 id="features-heading" className={styles.featuresHeading}>
            Everything you need to evaluate equities
          </h2>
          <p className={styles.featuresSubheading}>
            Built for investors who want signal, not noise.
          </p>

          <div className={styles.featureGrid}>
            {FEATURES.map((f) => (
              <article key={f.id} className={styles.featureCard}>
                <div className={styles.featureIcon} aria-hidden="true">
                  {f.icon}
                </div>
                <h3 className={styles.featureTitle}>{f.title}</h3>
                <p className={styles.featureDescription}>{f.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className={styles.cta} aria-labelledby="cta-heading">
          <div className={styles.ctaInner}>
            <h2 id="cta-heading" className={styles.ctaHeading}>
              Ready to gauge the market?
            </h2>
            <p className={styles.ctaBody}>
              Open the dashboard and start tracking P/E ratios across your
              watchlist right now — no sign-up required.
            </p>
            <a
              href="/dashboard"
              className={styles.ctaPrimary}
              aria-label="Open the EquityGauge dashboard"
            >
              Open Dashboard →
            </a>
          </div>
        </section>
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <span className={styles.footerLogo}>EquityGauge</span>
          <p className={styles.footerNote}>
            Data sourced from Yahoo Finance. Not financial advice.
          </p>
          <p className={styles.footerCopy}>
            © {new Date().getFullYear()} EquityGauge. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}