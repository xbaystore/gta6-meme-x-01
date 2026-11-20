// gta6-meme-x-01 — entry program for the "Post a GTA 6 meme on X" bounty.
//
// What is actually judged in this competition is the X post itself: the meme
// image and its caption living on X. The program therefore has almost nothing
// to compute. Its single job is to carry the canonical POST.json (which holds
// the URL of that post) from the bot directory into the output directory,
// byte-for-byte, so the grader can find and verify it. Keeping the program
// this small is deliberate: there is no logic here that could drift, mangle
// the payload, or fail for environmental reasons.
//
// Revision note: on top of the basic shape check (JSON object, `url` is a
// string), the URL itself is now validated to actually look like an X status
// URL — https scheme, host x.com, and a /<handle>/status/<id> path — so a
// malformed or off-platform link fails loudly here instead of at grading.
//
// Runtime: Node 22, standard library only, no network, no wall clock.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

function fail(message: string): never {
  process.stderr.write(`main: ${message}\n`);
  process.exit(1);
}

// Accept only the canonical shape of a link to a single X post:
//   https://x.com/<handle>/status/<status-id>
// The handle and id segments just have to be present and non-empty; whether
// the post exists is X's business, not this program's (and there is no
// network here to check with anyway).
function assertStatusUrl(rawUrl: string): void {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    fail(`POST.json field \`url\` is not a valid URL: ${rawUrl}`);
  }

  if (parsed.protocol !== "https:") {
    fail(`POST.json field \`url\` must use https: ${rawUrl}`);
  }
  if (parsed.hostname !== "x.com") {
    fail(`POST.json field \`url\` must be on x.com: ${rawUrl}`);
  }

  const segments = parsed.pathname.split("/").filter((s) => s.length > 0);
  if (
    segments.length !== 3 ||
    segments[1] !== "status" ||
    segments[0].length === 0 ||
    segments[2].length === 0
  ) {
    fail(
      `POST.json field \`url\` must look like https://x.com/<handle>/status/<id>: ${rawUrl}`,
    );
  }
}

function main(): void {
  const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

  // The output directory may not exist yet on a fresh grading run.
  try {
    mkdirSync(outputDir, { recursive: true });
  } catch (err) {
    fail(`could not create output directory ${outputDir}: ${String(err)}`);
  }

  const sourcePath = join(botDir, "POST.json");

  let raw: Buffer;
  try {
    raw = readFileSync(sourcePath);
  } catch (err) {
    fail(`could not read ${sourcePath}: ${String(err)}`);
  }

  // Validate the payload before copying: it must be a JSON object whose
  // `url` field is a string holding an X status URL. Anything else means
  // the entry is malformed.
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw.toString("utf8"));
  } catch (err) {
    fail(`POST.json is not valid JSON: ${String(err)}`);
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    fail("POST.json must contain a JSON object");
  }

  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== "string") {
    fail("POST.json field `url` must be a string");
  }
  assertStatusUrl(url);

  // Copy byte-for-byte: write the exact bytes we read, never a re-serialized
  // version, so whitespace and encoding survive untouched.
  const destPath = join(outputDir, "POST.json");
  try {
    writeFileSync(destPath, raw);
  } catch (err) {
    fail(`could not write ${destPath}: ${String(err)}`);
  }

  // Success is silent by contract.
}

main();
