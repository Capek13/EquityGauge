# Frontend Agent — EquityGauge

Generates React components and full pages for the EquityGauge financial dashboard by calling the Anthropic API with a curated system prompt, design guide, and few-shot examples.

## What it does
- Takes a natural-language description of a UI element or page
- Sends it to Claude with project-specific context (API schema, design rules, examples)
- Returns raw JSX + CSS ready to drop into `frontend/src/`

## Usage

```js
import { generateComponent } from "./tools/generate.js";
import { parseCode } from "./tools/parse.js";
import { validate } from "./tools/validate.js";
import { writeOutput } from "./tools/write.js";

const raw = await generateComponent(
  "Company watchlist table showing ticker, name, sector and P/E ratio with a delete button per row",
  "react-component"
);

const { jsx, css } = parseCode(raw);
validate(jsx);
const { jsxPath, cssPath } = writeOutput(jsx, css);
console.log("Written:", jsxPath, cssPath ?? "");
```

Output files are written to `./output/` and named after the component's `export default function` identifier.

## Template types
| Type | When to use |
|------|-------------|
| `react-component` | Reusable UI piece (table, card, modal, form) |
| `landing-page` | Full standalone page (marketing, overview) |
| `dashboard` | Data-heavy page with multiple panels and charts |

## File structure
```
frontend-agent/
├── AGENT.md              ← this file
├── config.json           ← model, API, paths
├── prompt/
│   ├── system.md         ← agent role + API schema + output rules
│   ├── design.md         ← visual language (colors, fonts, spacing)
│   └── examples.md       ← few-shot input→output pairs
├── tools/
│   ├── generate.js       ← Anthropic API call with prompt caching
│   ├── parse.js          ← extracts JSX and CSS from raw response
│   ├── validate.js       ← basic sanity checks on generated code
│   └── write.js          ← writes JSX + CSS to ./output/
├── templates/
│   ├── react-component.jsx  ← reusable component scaffold
│   ├── landing-page.jsx     ← full page scaffold
│   └── dashboard.jsx        ← data-heavy dashboard scaffold
└── output/               ← generated files land here
```

## Config reference (`config.json`)
- `anthropic.model` — Claude model ID
- `anthropic.temperature` — keep low (0.2–0.4) for deterministic code output
- `api.baseUrl` — EquityGauge FastAPI URL (change for production)
