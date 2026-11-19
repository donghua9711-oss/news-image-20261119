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

// The image gate also fixes the canvas at 1024x1024. A PNG carries
// its dimensions in the IHDR chunk: width and height are big-endian
// uint32s at byte offsets 16 and 20. Verify them here so a wrongly
// sized bundle fails at copy time, not at grading.
if (isPng) {
  const ihdr = readFileSync(targetPath).subarray(16, 24);
  const width = ihdr.readUInt32BE(0);
  const height = ihdr.readUInt32BE(4);
  if (width !== 1024 || height !== 1024) {
    throw new Error(`PNG is ${width}x${height}, expected 1024x1024`);
  }
}

// The gate's other hard limit is the file size: at most 1,048,576
// bytes (1 MiB). The size comparison above only proves the copy is
// complete, not that the bundle is legal, so check the cap itself.
const MAX_BYTES = 1_048_576;
if (written > MAX_BYTES) {
  throw new Error(`entry image is ${written} bytes, over the ${MAX_BYTES} cap`);
}

console.log(`entry.png: ${written} bytes, ${isPng ? "PNG" : "JPEG"}`);
