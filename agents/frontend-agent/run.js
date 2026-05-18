import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import { generateComponent } from "./tools/generate.js";
import { parseCode } from "./tools/parse.js";
import { validate } from "./tools/validate.js";
import { writeOutput } from "./tools/write.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND_SRC = path.resolve(__dirname, "../../frontend/src");

async function generate(description, templateHint) {
  console.log(`\nGeneruji: ${description}`);
  const raw = await generateComponent(description, templateHint);
  const { jsx, css } = parseCode(raw);
  validate(jsx);
  const result = writeOutput(jsx, css);
  console.log(`  -> ${result.jsxPath}`);
  if (result.cssPath) console.log(`  -> ${result.cssPath}`);
  return result;
}

async function copyToFrontend() {
  const outDir = path.resolve(__dirname, "output");
  const files = fs.readdirSync(outDir).filter((f) => f !== ".gitkeep");
  if (files.length === 0) return;

  const destDir = path.join(FRONTEND_SRC, "components");
  fs.mkdirSync(destDir, { recursive: true });

  for (const file of files) {
    fs.copyFileSync(path.join(outDir, file), path.join(destDir, file));
    console.log(`  Zkopírováno -> frontend/src/components/${file}`);
  }
}

// ── Co se vygeneruje ────────────────────────────────────────────────────────

await generate(
  "Watchlist table showing all companies from GET /companies. " +
  "For each ticker fetch P/E from GET /companies/{ticker}/pe. " +
  "Columns: ticker (monospace), name, sector, P/E (color-coded: <15 success, 15-30 neutral, >30 warning, N/A muted). " +
  "Each row has a delete button (DELETE /companies/{ticker}) that removes the row on success. " +
  "Show skeleton loading and error banner. Export default function WatchlistTable.",
  "react-component"
);

await generate(
  "Add company form with fields: ticker, name, currency (required), exchange, sector, industry (optional). " +
  "Watchlist checkbox defaults to true. " +
  "On submit POST to /companies. Show success message and reset form on 201. Show error message on 409 or network error. " +
  "Export default function AddCompanyForm with optional onAdded callback prop.",
  "react-component"
);

await generate(
  "Full EquityGauge dashboard page. " +
  "Layout: top header bar with logo 'EquityGauge' and subtitle 'P/E Ratio Tracker'. " +
  "Main area: left sidebar (280px) contains AddCompanyForm, right main area contains WatchlistTable. " +
  "Import both components from './AddCompanyForm' and './WatchlistTable'. " +
  "When onAdded fires on the form, refresh the table by passing a refreshKey prop (increment a counter). " +
  "Export default function App.",
  "dashboard"
);

await generate(
  "Landing page for EquityGauge. " +
  "Header with logo and 'Go to Dashboard' button linking to /dashboard. " +
  "Hero section: headline 'Track P/E Ratios in Real Time', subline explaining the app, CTA button. " +
  "Features section: 3 cards — 'Live Data' (Yahoo Finance), 'Watchlist' (add/remove tickers), 'Visual P/E Scoring' (color-coded). " +
  "Footer with copyright. Export default function LandingPage.",
  "landing-page"
);

// ── Zkopíruj výstupy do frontend/src/components ────────────────────────────

console.log("\nKopíruji do frontend/src/components/ ...");
await copyToFrontend();

console.log("\nHotovo. Dalsi krok: cd frontend && npm install && npm run dev");
