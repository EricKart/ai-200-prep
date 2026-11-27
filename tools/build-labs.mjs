#!/usr/bin/env node
// Fills the command blocks in labs/*/README.md from cmd/bash.sh and cmd/ps.ps1, so the README and the
// scripts can never disagree. In a README, write:
//
//   <!-- step:build -->
//   <!-- /step -->
//
// and this script puts the "# @@ build" step between the markers: a bash block, then PowerShell in a
// collapsed <details>. Run `npm run build:labs` after editing cmd/ files. CI fails if a README is stale.
// Every step must appear in the README exactly once.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const LABS = path.join(ROOT, 'labs');

const steps = (file) => {
  const out = new Map();
  const parts = fs.readFileSync(file, 'utf8').split(/^# @@ (\S+)[ \t]*\n/m);
  for (let i = 1; i < parts.length; i += 2) out.set(parts[i], parts[i + 1].replace(/\s+$/, ''));
  return out;
};

const block = (sh, ps) =>
  ['```bash', sh, '```', '', '<details><summary>PowerShell</summary>', '', '```powershell', ps, '```', '', '</details>'].join('\n');

let problems = 0;
for (const d of fs.readdirSync(LABS, { withFileTypes: true }).filter((e) => e.isDirectory())) {
  const dir = path.join(LABS, d.name);
  const readmeFile = path.join(dir, 'README.md');
  const sh = path.join(dir, 'cmd/bash.sh'), ps = path.join(dir, 'cmd/ps.ps1');
  if (!fs.existsSync(readmeFile) || !fs.existsSync(sh) || !fs.existsSync(ps)) continue;
  const readme = fs.readFileSync(readmeFile, 'utf8');
  if (!readme.includes('<!-- step:')) continue; // guide.html labs (LP8, LP9) keep commands in the guide
  const bash = steps(sh), pwsh = steps(ps);
  const used = new Map();
  const next = readme.replace(/<!-- step:(\S+) -->\n[\s\S]*?<!-- \/step -->/g, (_, name) => {
    used.set(name, (used.get(name) || 0) + 1);
    if (!bash.has(name) || !pwsh.has(name)) { console.error(`labs/${d.name}: README uses unknown step "${name}"`); problems++; return _; }
    return `<!-- step:${name} -->\n${block(bash.get(name), pwsh.get(name))}\n<!-- /step -->`;
  });
  for (const name of bash.keys()) {
    const n = used.get(name) || 0;
    if (n !== 1) { console.error(`labs/${d.name}: step "${name}" appears ${n} times in README.md (needs exactly 1)`); problems++; }
  }
  if (next !== readme) { fs.writeFileSync(readmeFile, next); console.log(`updated labs/${d.name}/README.md`); }
}
if (problems) process.exit(1);
