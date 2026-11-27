#!/usr/bin/env node
// List the questions behind an answer-tell error: node tools/tells.mjs lp1m2
// Part of https://aryantripathi.dev/ai-200
import fs from 'node:fs';
const ABS = /\b(always|never|only|all|none|every|must|guarantees?|cannot|impossible|entirely|completely)\b/i;
const m = process.argv[2];
const qs = JSON.parse(fs.readFileSync(new URL(`../content/questions/${m}.json`, import.meta.url))).questions;
for (const q of qs.filter((q) => q.type === 'single')) {
  const L = q.options.map((o) => o.text.length), c = L[q.answer];
  const flags = [];
  if (L.filter((x) => x >= c).length === 1) flags.push('LONGEST');
  if (L.filter((x) => x <= c).length === 1) flags.push('SHORTEST');
  if (!ABS.test(q.options[q.answer].text) && q.options.filter((o, k) => k !== q.answer && ABS.test(o.text)).length >= 2) flags.push('ABS');
  if (flags.length && (process.argv.includes('--all') || flags.includes('ABS'))) {
    console.log(`${q.id} [${flags.join(',')}] ${q.q.slice(0, 90)}`);
    q.options.forEach((o, k) => console.log(`   ${k === q.answer ? '*' : ' '} ${o.text}`));
  }
}
