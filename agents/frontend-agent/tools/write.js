import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../config.json"), "utf-8")
);

function deriveComponentName(jsx) {
  const match = jsx.match(/export default function (\w+)/);
  return match ? match[1] : "GeneratedComponent";
}

/**
 * @param {string} jsx
 * @param {string | null} css
 * @returns {{ name: string, jsxPath: string, cssPath: string | null }}
 */
export function writeOutput(jsx, css = null) {
  const outDir = path.resolve(__dirname, "..", config.output.dir);
  fs.mkdirSync(outDir, { recursive: true });

  const name = deriveComponentName(jsx);
  const jsxPath = path.join(outDir, `${name}${config.output.fileExtension}`);
  fs.writeFileSync(jsxPath, jsx, "utf-8");

  let cssPath = null;
  if (css) {
    cssPath = path.join(outDir, `${name}.module.css`);
    fs.writeFileSync(cssPath, css, "utf-8");
  }

  return { name, jsxPath, cssPath };
}
