// Entry program for make.fun news-image-20261119 (Node 22, standard
// library only, no network, no dependencies).
//
// The finished newspaper page lives beside this file as entry.png.
// Grading runs this program twice in a fresh container; each run
// copies the same bundled bytes to the output file, so the two runs
// hand back a byte-identical /output/entry.png by construction.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetPath = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePath, targetPath);

// A copy that silently lost bytes would fail the image gate, so the
// written file must be exactly the source's size before we go on.
const expected = statSync(sourcePath).size;
const written = statSync(targetPath).size;
if (written !== expected) {
  throw new Error(`copy incomplete: wrote ${written} of ${expected} bytes`);
}

// The gate tells PNG from JPEG by magic bytes and refuses anything
// else: PNG starts 89 50 4E 47, JPEG starts FF D8 FF. If the bundled
// file were corrupt, failing loudly here beats shipping it.
const head = readFileSync(targetPath).subarray(0, 4);
const isPng =
  head[0] === 0x89 && head[1] === 0x50 && head[2] === 0x4e && head[3] === 0x47;
const isJpeg = head[0] === 0xff && head[1] === 0xd8 && head[2] === 0xff;
if (!isPng && !isJpeg) {
  throw new Error("copied file is neither PNG nor JPEG");
}

console.log(`entry.png: ${written} bytes, ${isPng ? "PNG" : "JPEG"}`);
