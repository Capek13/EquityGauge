# Design Guidelines — EquityGauge

## Visual identity
EquityGauge is a **professional financial tool**, not a consumer app.
Aesthetic direction: Bloomberg Terminal meets modern SaaS — dark, data-dense, precise.

## Color palette (CSS variables)
```css
:root {
  --color-bg:          #0d1117;   /* page background */
  --color-surface:     #161b22;   /* cards, panels */
  --color-border:      #30363d;   /* dividers, table borders */
  --color-text:        #e6edf3;   /* primary text */
  --color-text-muted:  #8b949e;   /* labels, placeholders */
  --color-accent:      #58a6ff;   /* links, highlights, active states */
  --color-success:     #3fb950;   /* positive P/E, good metrics */
  --color-warning:     #d29922;   /* elevated P/E ratios */
  --color-danger:      #f85149;   /* errors, negative metrics, delete */
  --color-brand:       #1f6feb;   /* primary buttons, logo accent */
}
```

## Typography
- Font family: `'Inter', system-ui, sans-serif` (load from Google Fonts)
- Base size: `14px` (financial dashboards are dense)
- Headings: `font-weight: 600`, no uppercase
- Numbers/tickers: `font-family: 'JetBrains Mono', monospace` — always monospace for alignment
- Muted metadata: `var(--color-text-muted)`, `font-size: 12px`

## Spacing & layout
- Base unit: `8px` — all spacing in multiples of 8
- Max content width: `1280px`, centered
- Cards: `border-radius: 6px`, `border: 1px solid var(--color-border)`
- Table rows: `height: 48px`, hover `background: var(--color-border)`

## Components style rules

### Buttons
- Primary: `background: var(--color-brand)`, white text, `border-radius: 6px`
- Danger: `background: transparent`, `color: var(--color-danger)`, border on hover
- No shadows on buttons — flat design

### Tables
- Header: `background: var(--color-surface)`, `color: var(--color-text-muted)`, `font-size: 11px`, uppercase, `letter-spacing: 0.5px`
- Rows: alternating subtle bg is optional; prefer border-bottom only
- P/E value coloring: `< 15` → success, `15–30` → text, `> 30` → warning, N/A → muted

### Status indicators
- Loading: subtle skeleton shimmer animation (`@keyframes shimmer`)
- Error: red banner with icon, dismissible
- Empty state: centered icon + muted text, no borders

## Navigation patterns
- Logo / brand always `<a href="/">` — never a `<span>`. Add `text-decoration: none` in CSS.
- Header nav links: `<a href="/route">` with `text-decoration: none`, hover `opacity: 0.85`.
- CTA buttons that navigate: `<a href="/route" className={styles.ctaPrimary}>` — styled like a button, not a link.

## Do not use
- Gradients on backgrounds
- Box shadows (except `0 1px 3px rgba(0,0,0,0.4)` for modals)
- Rounded corners > `8px`
- Animations longer than `200ms`
- Bright/saturated colors outside the palette
- `html, body, #root` resets inside `.module.css` files — only in global `index.css`
