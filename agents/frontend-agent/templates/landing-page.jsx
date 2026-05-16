import styles from "./LandingPage.module.css";

export default function LandingPage() {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.logo}>EquityGauge</h1>
        <nav className={styles.nav}>{/* nav links */}</nav>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <h2>{/* headline */}</h2>
          <p>{/* subline */}</p>
          <a href="/dashboard" className={styles.cta}>Get started</a>
        </section>
      </main>

      <footer className={styles.footer}>{/* footer */}</footer>
    </div>
  );
}
