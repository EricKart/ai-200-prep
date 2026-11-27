#!/usr/bin/env node
// AI-200 Prep quality gate. Every rule here must pass before a pull request can merge.
// Usage: node tools/check.mjs [--report] [--only lp1m1]
// Zero dependencies (Node 20+). Part of https://aryantripathi.dev/ai-200
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const REPORT = args.includes('--report');
const ONLY = args.includes('--only') ? args[args.indexOf('--only') + 1] : null;
const errors = [];
const warnings = [];
const err = (where, msg) => errors.push(`${where}: ${msg}`);
const warn = (where, msg) => warnings.push(`${where}: ${msg}`);
const read = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
const exists = (p) => fs.existsSync(path.join(ROOT, p));
const pct = (a, b) => (b ? Math.round((100 * a) / b) : 0);

// Thresholds. Change them only with a reason in the pull request.
const T = {
  scenarioFloor: 0.6,
  longestMax: 0.3, // correct option is the single longest
  shortestMax: 0.35, // correct option is the single shortest
  longestMaxModule: 0.45,
  positionMin: 0.15,
  positionMax: 0.35,
  hintMax: 200,
  dupeJaccard: 0.8,
  mockSize: 60,
  mockMinutes: 120,
  mockSkillTolerance: 2,
  absoluteOnlyInDistractorsMax: 0.1,
};
const BRAND = 'aryantripathi.dev';
const ABSOLUTE = /\b(always|never|only|all|none|every|must|guarantees?|cannot|impossible|entirely|completely)\b/i;

const course = JSON.parse(read('course.json'));
const modules = course.paths.flatMap((p) => p.modules.map((m) => ({ ...m, lp: p.n, skill: p.skillArea })));
const modById = Object.fromEntries(modules.map((m) => [m.id, m]));

// ---------- questions ----------
const all = [];
const byId = new Map();
for (const m of modules) {
  if (ONLY && m.id !== ONLY) continue;
  const f = `content/questions/${m.id}.json`;
  if (!exists(f)) { err(f, 'missing question bank'); continue; }
  let bank;
  try { bank = JSON.parse(read(f)); } catch (e) { err(f, 'invalid JSON: ' + e.message); continue; }
  if (bank.module !== m.id) err(f, `"module" must be "${m.id}"`);
  if (!Array.isArray(bank.questions) || !bank.questions.length) { err(f, 'no questions'); continue; }
  const units = new Map(m.units.map((u) => [u.u, u]));
  bank.questions.forEach((q, i) => {
    const where = `${f} #${i + 1} ${q.id ?? ''}`;
    q._module = m.id; q._skill = m.skill; q._file = f;
    const want = `${m.id}-${String(i + 1).padStart(3, '0')}`;
    if (q.id !== want) err(where, `id must be ${want} (ids are positional; append new questions at the end, never reorder)`);
    if (byId.has(q.id)) err(where, 'duplicate id');
    byId.set(q.id, q);
    all.push(q);
    checkQuestion(q, where, units);
  });
}

function nonEmpty(s) { return typeof s === 'string' && s.trim().length > 0; }

function checkQuestion(q, where, units) {
  const u = units.get(q.unit);
  if (!u) err(where, `unit "${q.unit}" is not a unit of this module`);
  else if (u.exercise) err(where, `unit ${q.unit} is an exercise; cite the content unit the fact comes from`);
  if (!['practice', 'mock'].includes(q.pool)) err(where, 'pool must be "practice" or "mock"');
  if (typeof q.scenario !== 'boolean') err(where, 'scenario must be true or false');
  if (!['easy', 'medium', 'hard'].includes(q.difficulty)) err(where, 'difficulty must be easy, medium or hard');
  if (!nonEmpty(q.q)) err(where, 'empty question text');
  if (!nonEmpty(q.explain)) err(where, 'missing explain');
  if (!nonEmpty(q.hint)) err(where, 'missing hint');
  else {
    if (q.hint.length > T.hintMax) err(where, `hint is ${q.hint.length} chars (max ${T.hintMax})`);
    if (/\b(the answer is|correct answer|correct option)\b/i.test(q.hint)) err(where, 'hint gives the answer away');
  }
  if (!nonEmpty(q.origin)) err(where, 'missing origin');
  if (/<\/?(b|i|em|strong|code|br|p|div|span|a|ul|ol|li|pre|sup|sub|table|tr|td)(\s[^>]*)?\/?>/i.test(JSON.stringify([q.q, q.hint, q.explain]))) err(where, 'HTML tags in text; use Markdown (`code`, **bold**)');
  const hintLeaks = (txt) => {
    const t = (txt || '').toLowerCase().replace(/[`*_]/g, '').trim();
    return t.length >= 6 && q.hint && q.hint.toLowerCase().replace(/[`*_]/g, '').includes(t);
  };
  switch (q.type) {
    case 'single':
    case 'multi': {
      if (!Array.isArray(q.options) || q.options.length < 3 || q.options.length > 6) { err(where, 'needs 3–6 options'); return; }
      const ans = q.type === 'single' ? [q.answer] : q.answer;
      if (q.type === 'single' && !Number.isInteger(q.answer)) err(where, 'single needs an integer answer');
      if (q.type === 'multi' && (!Array.isArray(q.answer) || q.answer.length < 2)) err(where, 'multi needs 2+ answers');
      if (!Array.isArray(ans) || ans.some((a) => !Number.isInteger(a) || a < 0 || a >= q.options.length)) { err(where, 'answer out of range'); return; }
      const texts = new Set();
      q.options.forEach((o, k) => {
        if (!nonEmpty(o.text)) err(where, `option ${k + 1} empty`);
        if (!nonEmpty(o.why)) err(where, `option ${k + 1} has no reason ("why")`);
        const right = ans.includes(k);
        if (right && !/^Correct\b/.test(o.why || '')) err(where, `correct option ${k + 1}: reason must start with "Correct"`);
        if (!right && /^Correct\b/.test(o.why || '')) err(where, `wrong option ${k + 1}: reason starts with "Correct"`);
        const key = (o.text || '').toLowerCase().trim();
        if (texts.has(key)) err(where, `duplicate option "${o.text}"`);
        texts.add(key);
        if (right && hintLeaks(o.text)) err(where, 'hint contains the correct option text');
      });
      if (q.type === 'multi' && !/\((select|choose) (two|three|all)|\bwhich (two|three)\b/i.test(q.q)) warn(where, 'multi question should say how many to select');
      break;
    }
    case 'yesno':
      if (!Array.isArray(q.rows) || q.rows.length < 2) { err(where, 'yesno needs 2+ rows'); return; }
      q.rows.forEach((r, k) => {
        if (!nonEmpty(r.text) || typeof r.answer !== 'boolean' || !nonEmpty(r.why)) err(where, `row ${k + 1} needs text, boolean answer, why`);
      });
      if (q.rows.every((r) => r.answer) || q.rows.every((r) => !r.answer)) warn(where, 'all rows have the same answer');
      break;
    case 'match':
      if (!Array.isArray(q.choices) || q.choices.length < 2) err(where, 'match needs 2+ choices');
      if (!Array.isArray(q.items) || q.items.length < 2) { err(where, 'match needs 2+ items'); return; }
      q.items.forEach((it, k) => {
        if (!nonEmpty(it.text) || !Number.isInteger(it.answer) || it.answer < 0 || it.answer >= q.choices.length || !nonEmpty(it.why)) err(where, `item ${k + 1} needs text, valid answer, why`);
      });
      break;
    case 'order':
      if (!Array.isArray(q.steps) || q.steps.length < 3) err(where, 'order needs 3+ steps (listed in the correct order)');
      else if (new Set(q.steps).size !== q.steps.length) err(where, 'duplicate steps');
      break;
    default:
      err(where, `unknown type "${q.type}"`);
  }
}

// ---------- hints that may give the answer away (warning; reviewed ids are listed in tools/hint-reviewed.json) ----------
{
  const STOP = new Set('that this with from your into they them their have when which what does should only each more than then also used uses using before after about would could there these those where while other some most less same over under like just will very much many need needs make made because azure'.split(' '));
  const toks = (s) => new Set(String(s).toLowerCase().replace(/[`*_]/g, '').match(/[a-z0-9][a-z0-9.\-]{3,}/g) || []);
  const reviewed = exists('tools/hint-reviewed.json') ? new Set(JSON.parse(read('tools/hint-reviewed.json'))) : new Set();
  for (const q of all) {
    if ((q.type !== 'single' && q.type !== 'multi') || reviewed.has(q.id) || !Array.isArray(q.options)) continue;
    const ans = q.type === 'single' ? [q.answer] : q.answer;
    if (!Array.isArray(ans) || ans.some((a) => !q.options[a])) continue;
    const right = new Set(ans.flatMap((a) => [...toks(q.options[a].text)]));
    const other = new Set([...toks(q.q), ...q.options.filter((_, k) => !ans.includes(k)).flatMap((o) => [...toks(o.text)])]);
    const h = toks(q.hint);
    const leak = [...right].filter((w) => !STOP.has(w) && !other.has(w) && h.has(w));
    if (leak.length) warn(`${q._file} ${q.id}`, `hint uses "${leak.join('", "')}", which appears only in the correct option. Point to the concept instead (or add the id to tools/hint-reviewed.json after review)`);
  }
}

// ---------- answer tells & balance ----------
function tells(list, where, longestMax) {
  const singles = list.filter((q) => q.type === 'single' && Array.isArray(q.options));
  if (!singles.length) return {};
  let longest = 0, shortest = 0, absOnlyWrong = 0;
  const pos = new Array(6).fill(0);
  for (const q of singles) {
    const L = q.options.map((o) => (o.text || '').length);
    const c = L[q.answer];
    if (L.filter((x) => x >= c).length === 1) longest++;
    if (L.filter((x) => x <= c).length === 1) shortest++;
    pos[q.answer]++;
    const rightAbs = ABSOLUTE.test(q.options[q.answer].text);
    const wrongAbs = q.options.filter((o, k) => k !== q.answer && ABSOLUTE.test(o.text)).length;
    if (!rightAbs && wrongAbs >= 2) absOnlyWrong++;
  }
  const n = singles.length;
  if (longest / n > longestMax) err(where, `correct option is the single longest in ${pct(longest, n)}% of single-choice questions (max ${pct(longestMax, 1)}%)`);
  if (shortest / n > T.shortestMax) err(where, `correct option is the single shortest in ${pct(shortest, n)}% (max ${pct(T.shortestMax, 1)}%)`);
  if (absOnlyWrong / n > T.absoluteOnlyInDistractorsMax) err(where, `${pct(absOnlyWrong, n)}% of questions have absolute words only in 2+ distractors (max ${pct(T.absoluteOnlyInDistractorsMax, 1)}%)`);
  return { n, longest: pct(longest, n), shortest: pct(shortest, n), pos };
}
function scenario(list, where) {
  const s = list.filter((q) => q.scenario).length;
  if (list.length && s / list.length < T.scenarioFloor) err(where, `scenario ${pct(s, list.length)}% (floor ${pct(T.scenarioFloor, 1)}%)`);
  return pct(s, list.length);
}

const stats = [];
for (const m of modules) {
  const qs = all.filter((q) => q._module === m.id);
  if (!qs.length) continue;
  const where = `content/questions/${m.id}.json`;
  const t = tells(qs, where, T.longestMaxModule);
  const sc = scenario(qs, where);
  for (const pool of ['practice', 'mock']) if (!qs.some((q) => q.pool === pool)) err(where, `no "${pool}" questions`);
  // coverage: every content unit is tested
  for (const u of m.units.filter((u) => !u.exercise)) if (!qs.some((q) => q.unit === u.u)) err(where, `unit ${u.u} "${u.title}" has no question`);
  stats.push({ module: m.id, total: qs.length, practice: qs.filter((q) => q.pool === 'practice').length, mock: qs.filter((q) => q.pool === 'mock').length, hints: qs.filter((q) => nonEmpty(q.hint)).length, scenario: sc, longest: t.longest, shortest: t.shortest });
}
if (!ONLY && all.length) {
  const t = tells(all, 'all questions', T.longestMax);
  scenario(all, 'all questions');
  const n = t.n;
  t.pos.slice(0, 4).forEach((c, k) => {
    if (c / n < T.positionMin || c / n > T.positionMax) err('all questions', `correct answer is option ${'ABCD'[k]} in ${pct(c, n)}% of single-choice questions (allowed ${pct(T.positionMin, 1)}–${pct(T.positionMax, 1)}%)`);
  });
}

// ---------- near-duplicate stems ----------
const toks = (s) => new Set(s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter((w) => w.length > 2));
const allowDupes = exists('tools/allow-dupes.json') ? new Set(JSON.parse(read('tools/allow-dupes.json')).map((p) => p.sort().join('|'))) : new Set();
{
  const stems = all.map((q) => [q.id, toks(q.q + ' ' + (q.options || q.rows || q.items || []).map((o) => o.text || o).join(' '))]);
  for (let i = 0; i < stems.length; i++) for (let j = i + 1; j < stems.length; j++) {
    const [a, A] = stems[i], [b, B] = stems[j];
    let inter = 0; for (const w of A) if (B.has(w)) inter++;
    const jac = inter / (A.size + B.size - inter || 1);
    if (jac >= T.dupeJaccard && !allowDupes.has([a, b].sort().join('|'))) err(`${a} ~ ${b}`, `near-duplicate questions (similarity ${jac.toFixed(2)})`);
  }
}

// ---------- stable ids ----------
if (exists('tools/ids-lock.json') && !ONLY) {
  const lock = JSON.parse(read('tools/ids-lock.json'));
  for (const id of lock) if (!byId.has(id)) err('tools/ids-lock.json', `published id ${id} was removed (learners' saved progress uses it)`);
  try {
    const base = JSON.parse(execSync('git show origin/main:tools/ids-lock.json', { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).toString());
    for (const id of base) if (!lock.includes(id)) err('tools/ids-lock.json', `${id} was removed from the lock file`);
  } catch { /* no remote main yet */ }
}

// ---------- mocks ----------
if (!ONLY) {
  const seen = new Map();
  const mockFiles = exists('mocks') ? fs.readdirSync(path.join(ROOT, 'mocks')).filter((f) => /^mock-\d+\.json$/.test(f)).sort() : [];
  if (mockFiles.length !== 3) err('mocks/', `expected 3 mock exams, found ${mockFiles.length}`);
  for (const f of mockFiles) {
    const where = `mocks/${f}`;
    const mk = JSON.parse(read(where));
    if (mk.minutes !== T.mockMinutes) err(where, `minutes must be ${T.mockMinutes}`);
    if (mk.questions?.length !== T.mockSize) err(where, `needs ${T.mockSize} questions, has ${mk.questions?.length}`);
    const qs = [];
    for (const id of mk.questions || []) {
      const q = byId.get(id);
      if (!q) { err(where, `unknown question ${id}`); continue; }
      if (q.pool !== 'mock') err(where, `${id} is a practice question; mocks use only the mock pool`);
      if (seen.has(id)) err(where, `${id} is also in ${seen.get(id)}`);
      seen.set(id, f); qs.push(q);
    }
    scenario(qs, where);
    for (const s of course.skillAreas) {
      const c = qs.filter((q) => q._skill === s.n).length;
      if (Math.abs(c - s.mockTarget) > T.mockSkillTolerance) err(where, `skill area ${s.n} has ${c} questions (target ${s.mockTarget} ± ${T.mockSkillTolerance})`);
    }
  }
}

// ---------- lessons & cheat sheets ----------
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
for (const m of modules) {
  if (ONLY && m.id !== ONLY) continue;
  const f = `content/lessons/${m.id}.md`;
  if (!exists(f)) { err(f, 'missing lesson'); continue; }
  const text = read(f);
  const h2 = [...text.matchAll(/^## (.+)$/gm)].map((x) => x[1].trim());
  const want = m.units.filter((u) => !u.exercise).map((u) => u.title);
  for (const t of want) if (!h2.some((h) => slug(h) === slug(t))) err(f, `missing "## ${t}" (h2 must equal the Learn unit title)`);
  const order = want.map((t) => h2.findIndex((h) => slug(h) === slug(t))).filter((x) => x >= 0);
  if (order.some((x, i) => i && x < order[i - 1])) err(f, 'unit sections are not in Learn order');
  for (const u of m.units.filter((u) => !u.exercise)) if (!text.includes(u.url)) err(f, `no link to the Learn unit ${u.u} (${u.url})`);
  if (!/^# /m.test(text)) err(f, 'missing the # title');
}
if (!ONLY) for (const p of course.paths) if (!exists(`content/cheatsheets/lp${p.n}.md`)) err(`content/cheatsheets/lp${p.n}.md`, 'missing cheat sheet');

// ---------- every document: brand line, no PII, no secrets ----------
const SKIP = /(^|\/)(node_modules|\.git|dist|\.next)(\/|$)/;
function walk(dir, out = []) {
  for (const e of fs.readdirSync(path.join(ROOT, dir), { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (SKIP.test(p)) continue;
    if (e.isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}
const PII = [
  [/[A-Z0-9._%+-]+@(?!example\.(com|org)|contoso\.com|noreply)[A-Z0-9.-]+\.[A-Z]{2,}/i, 'an email address'],
  [/@lpu\.in\b/i, 'a university email'],
  [/(?<![\dA-Fa-f.])1[12]\d{6}(?![\dA-Fa-f.])/, 'a student roll number'],
  [/(?<![\dA-Fa-f+])(\+91[ -]?)?[6-9]\d{9}(?![\dA-Fa-f])/, 'a phone number'],
  [/(AccountKey|SharedAccessKey|client_secret|api[_-]?key)\s*[=:]\s*["']?[A-Za-z0-9+/]{20,}/i, 'a secret'],
];
const PII_ALLOW = /(<[^>]+>|\$\{?[A-Z_]+\}?|xxxx|\.\.\.)/;
for (const f of walk('.')) {
  const rel = f.replace(/^\.\//, '');
  if (!/\.(md|html|json|sh|ps1|py|mjs|js|ts|yml|yaml|txt|kql|sql)$/.test(rel)) continue;
  if (rel === 'tools/check.mjs') continue;
  const text = read(rel);
  if (/\.(md|html)$/.test(rel) && !rel.startsWith('.github/') && !text.includes(BRAND)) err(rel, `missing the ${BRAND} line`);
  for (const [re, what] of PII) {
    const hit = text.match(re);
    if (hit && !PII_ALLOW.test(hit[0])) err(rel, `looks like ${what}: "${hit[0].slice(0, 40)}"`);
  }
}

// ---------- labs ----------
if (!ONLY && exists('labs')) {
  for (const d of fs.readdirSync(path.join(ROOT, 'labs'), { withFileTypes: true }).filter((e) => e.isDirectory())) {
    const base = `labs/${d.name}`;
    if (!exists(`${base}/README.md`)) { err(base, 'missing README.md'); continue; }
    const readme = read(`${base}/README.md`);
    if (!/^## .*cost/im.test(readme)) err(`${base}/README.md`, 'needs a "## … cost" section');
    if (!/^## .*clean ?up/im.test(readme)) err(`${base}/README.md`, 'needs a "## … clean up" section');
    const steps = (f) => exists(f) ? [...read(f).matchAll(/^# @@ (\S+)\s*$/gm)].map((x) => x[1].trim()) : null;
    const sh = steps(`${base}/cmd/bash.sh`), ps = steps(`${base}/cmd/ps.ps1`);
    if (!sh) err(base, 'missing cmd/bash.sh');
    if (!ps) err(base, 'missing cmd/ps.ps1');
    if (sh && ps && sh.join('|') !== ps.join('|')) err(base, 'bash.sh and ps.ps1 step names differ');
    if (sh && !sh.some((s) => /clean/i.test(s))) err(`${base}/cmd/bash.sh`, 'needs a clean-up step');
  }
}

// ---------- output ----------
if (REPORT && stats.length) {
  console.log('module   total practice mock hints scen% long% short%');
  for (const s of stats) console.log(`${s.module.padEnd(8)} ${String(s.total).padStart(5)} ${String(s.practice).padStart(8)} ${String(s.mock).padStart(4)} ${String(s.hints).padStart(5)} ${String(s.scenario).padStart(5)} ${String(s.longest).padStart(5)} ${String(s.shortest).padStart(6)}`);
  console.log(`total questions: ${all.length}`);
}
for (const w of warnings) console.log('warn  ' + w);
for (const e of errors) console.log('ERROR ' + e);
console.log(`\n${errors.length} errors, ${warnings.length} warnings`);
process.exit(errors.length ? 1 : 0);
