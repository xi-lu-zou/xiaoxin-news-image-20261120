// Entry point for the make.fun harness: copies the pre-rendered entry.png
// (built by make_image.py from the day's news) into the output directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(out, { recursive: true });
copyFileSync(join(here, "entry.png"), join(out, "entry.png"));
console.log("entry.png written to", out);
