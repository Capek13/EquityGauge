import Anthropic from "@anthropic-ai/sdk";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../config.json"), "utf-8")
);

const client = new Anthropic();

function loadPrompt(relPath) {
  return fs.readFileSync(path.resolve(__dirname, "..", relPath), "utf-8");
}

const TEMPLATE_KEYS = {
  "react-component": "reactComponent",
  "landing-page": "landingPage",
  "dashboard": "dashboard",
};

/**
 * @param {string} userRequest - what component/page to generate
 * @param {"react-component"|"landing-page"|"dashboard"} [templateHint]
 * @returns {Promise<string>} raw LLM response text
 */
export async function generateComponent(userRequest, templateHint = null) {
  const systemPrompt = loadPrompt(config.prompts.system);
  const designGuide = loadPrompt(config.prompts.design);
  const examples = loadPrompt(config.prompts.examples);

  let scaffoldBlock = "";
  const templateKey = TEMPLATE_KEYS[templateHint];
  if (templateKey && config.templates[templateKey]) {
    const templatePath = path.resolve(__dirname, "..", config.templates[templateKey]);
    if (fs.existsSync(templatePath)) {
      const scaffold = fs.readFileSync(templatePath, "utf-8");
      scaffoldBlock = `Use this scaffold as the starting structure:\n\`\`\`jsx\n${scaffold}\n\`\`\`\n\n`;
    }
  }

  const userMessage = `${scaffoldBlock}${userRequest}`;

  const response = await client.messages.create({
    model: config.anthropic.model,
    max_tokens: config.anthropic.max_tokens,
    temperature: config.anthropic.temperature,
    // Prompt caching — only the last system block needs the checkpoint
    system: [
      {
        type: "text",
        text: systemPrompt,
        cache_control: { type: "ephemeral" },
      },
      {
        type: "text",
        text: `## Design Guidelines\n\n${designGuide}`,
        cache_control: { type: "ephemeral" },
      },
      {
        type: "text",
        text: `## Examples\n\n${examples}`,
        cache_control: { type: "ephemeral" },
      },
    ],
    messages: [{ role: "user", content: userMessage }],
  });

  const block = response.content.find((b) => b.type === "text");
  if (!block) throw new Error("No text content in API response");
  return block.text;
}
