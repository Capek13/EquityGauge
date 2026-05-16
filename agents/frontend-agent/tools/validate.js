/**
 * Basic sanity checks on generated JSX.
 * Throws on hard failures, warns on soft issues.
 */

const REQUIRED_PATTERNS = [
  { pattern: /export default/, label: "missing default export" },
  { pattern: /return\s*[(<]/, label: "missing JSX return" },
];

const SOFT_WARNINGS = [
  { pattern: /#[0-9a-fA-F]{3,6}(?!\w)/, label: "possible hardcoded color (use CSS variables)" },
  { pattern: /console\.log/, label: "console.log left in output" },
  { pattern: /TODO|FIXME/, label: "unresolved TODO/FIXME" },
];

/**
 * @param {string} jsx
 * @throws {Error} if a required pattern is missing
 */
export function validate(jsx) {
  for (const { pattern, label } of REQUIRED_PATTERNS) {
    if (!pattern.test(jsx)) {
      throw new Error(`Validation failed: ${label}`);
    }
  }

  // Strip comments before soft checks to avoid false positives on commented-out code
  const jsxNoComments = jsx
    .replace(/\/\/.*$/gm, "")
    .replace(/\/\*[\s\S]*?\*\//g, "");

  for (const { pattern, label } of SOFT_WARNINGS) {
    if (pattern.test(jsxNoComments)) {
      console.warn(`[frontend-agent] Warning: ${label}`);
    }
  }
}
