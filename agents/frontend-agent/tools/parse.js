/**
 * Extracts JSX and CSS from the raw LLM response.
 * The agent is instructed to return raw code, but sometimes wraps it in fences.
 */

const JSX_FENCE = /```(?:jsx?|tsx?)[ \t]*\n([\s\S]*?)```/g;
const CSS_FENCE = /```css[ \t]*\n([\s\S]*?)```/;

/**
 * @param {string} raw - raw text from generate.js
 * @returns {{ jsx: string, css: string | null }}
 */
export function parseCode(raw) {
  // Collect all JSX/TSX fenced blocks — first is the component, second may be CSS-in-JSX
  const jsxBlocks = [...raw.matchAll(JSX_FENCE)].map((m) => m[1].trim());
  const cssMatch = raw.match(CSS_FENCE);

  const jsx = jsxBlocks.length > 0 ? jsxBlocks[0] : raw.trim();

  // Prefer an explicit CSS fence; fall back to second JSX block if it looks like CSS
  let css = cssMatch ? cssMatch[1].trim() : null;
  if (!css && jsxBlocks.length > 1 && jsxBlocks[1].includes("{")) {
    css = jsxBlocks[1];
  }

  return { jsx, css };
}
