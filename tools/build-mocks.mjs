#!/usr/bin/env node
// Builds mocks/mock-1..3.json from the mock pool: 60 questions each, weighted by skill area, no overlap.
// Deterministic (seeded), so rebuilding gives the same mocks. Part of https://aryantripathi.dev/ai-200
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const course = JSON.parse(fs.readFileSync(path.join(ROOT, 'course.json'), 'utf8'));
const MOCKS = 3;
let seed = 200;
const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

const mocks = Array.from({ length: MOCKS }, () => []);
for (const area of course.skillAreas) {
  const mods = course.paths.filter((p) => p.skillArea === area.n).flatMap((p) => p.modules.map((m) => m.id));
  const queues = mods.map((id) => shuffle(JSON.parse(fs.readFileSync(path.join(ROOT, `content/questions/${id}.json`), 'utf8'))
    .questions.filter((q) => q.pool === 'mock').map((q) => ({ id: q.id, sc: q.scenario }))));
  const need = area.mockTarget * MOCKS;
  if (queues.flat().length < need) throw new Error(`skill area ${area.n}: ${queues.flat().length} mock-pool questions, need ${need}`);
  // deal round-robin across modules so each mock covers every module of the area
  let k = 0, dealt = 0;
  while (dealt < need) {
    for (const q of queues) {
      if (dealt >= need) break;
      const item = q.shift();
      if (!item) continue;
      mocks[k % MOCKS].push(item.id); k++; dealt++;
    }
  }
}
fs.mkdirSync(path.join(ROOT, 'mocks'), { recursive: true });
mocks.forEach((ids, i) => {
  const out = {
    id: `mock-${i + 1}`,
    title: `AI-200 Mock Exam ${i + 1}`,
    minutes: 120,
    passScore: 700,
    note: 'Practice exam written from the Microsoft Learn AI-200T00 course. Not real exam questions. https://aryantripathi.dev/ai-200',
    questions: shuffle(ids),
  };
  fs.writeFileSync(path.join(ROOT, `mocks/mock-${i + 1}.json`), JSON.stringify(out, null, 1) + '\n');
  console.log(`mock-${i + 1}: ${ids.length} questions`);
});
