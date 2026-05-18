import styles from "./LandingPage.module.css";

const FEATURES = [
  {
    icon: "⚡",
    title: "Live Data",
    description:
      "P/E ratios and equity metrics scraped directly from Yahoo Finance — always up to date, no stale caches.",
  },
  {
    icon: "★",
    title: "Watchlist",
    description:
      "Add and remove tickers instantly. Build a focused list of the companies that matter to your portfolio.",
  },
  {
    icon: "◈",
    title: "Visual P/E Scoring",
    description:
      "Color-coded P/E indicators let you spot undervalued and overvalued equities at a glance — no spreadsheets needed.",
  },
];

export default function LandingPage() {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <span className={styles.logo} aria-label="EquityGauge home">
          <span className={styles.logoBracket}>[</span>
          EG
          <span className={styles.logoBracket}>]</span>
          <span className={styles.logoWord}>EquityGauge</span>
        </span>

        <nav className={styles.nav} aria-label="Primary navigation">
          <a href="#features" className={styles.navLink}>
            Features
          </a>
          <a href="/dashboard" className={styles.navCta} aria-label="Go to Dashboard">
            Go to Dashboard →
          </a>
        </nav>
      </header>

      <main className={styles.main}>
        <section className={styles.hero} aria-labelledby="hero-heading">
          <div className={styles.heroBadge}>Real-time equity intelligence</div>
          <h2 id="hero-heading" className={styles.heroHeadline}>
            Track P/E Ratios
            <br />
            <span className={styles.heroAccent}>in Real Time</span>
          </h2>
          <p className={styles.heroSub}>
            EquityGauge pulls live price-to-earnings data from Yahoo Finance so
            you can monitor your watchlist, spot valuation outliers, and make
            faster, more informed investment decisions — all in one place.
          </p>
          <div className={styles.heroActions}>
            <a href="/dashboard" className={styles.cta} aria-label="Get started with EquityGauge">
              Get started
            </a>
            <a href="#features" className={styles.ctaGhost}>
              See features
            </a>
          </div>
          <div className={styles.heroMeta} aria-hidden="true">
            <span className={styles.metaPill} style={{ color: "var(--color-success)" }}>
              ● P/E 12.4 — Undervalued
            </span>
            <span className={styles.metaPill} style={{ color: "var(--color-text)" }}>
              ● P/E 22.1 — Fair
            </span>
            <span className={styles.metaPill} style={{ color: "var(--color-warning)" }}>
              ● P/E 38.7 — Elevated
            </span>
          </div>
        </section>

        <section
          id="features"
          className={styles.features}
          aria-labelledby="features-heading"
        >
          <h3 id="features-heading" className={styles.featuresHeading}>
            Everything you need to evaluate equities
          </h3>
          <div className={styles.featureGrid}>
            {FEATURES.map((f) => (
              <article key={f.title} className={styles.featureCard}>
                <div className={styles.featureIcon} aria-hidden="true">
                  {f.icon}
                </div>
                <h4 className={styles.featureTitle}>{f.title}</h4>
                <p className={styles.featureDesc}>{f.description}</p>
              </article>
            ))}
          </div>
        </section>
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <span className={styles.footerLogo}>EquityGauge</span>
          <span className={styles.footerCopy}>
            © {new Date().getFullYear()} EquityGauge. Data sourced from Yahoo
            Finance. Not financial advice.
          </span>
        </div>
      </footer>
    </div>
  );
}