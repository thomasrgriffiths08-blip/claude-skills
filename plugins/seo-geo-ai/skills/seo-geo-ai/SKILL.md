---
name: seo-geo-ai
description: One-prompt, multi-agent search overhaul — classic SEO, GEO (generative engine optimization), and AI-search visibility (ChatGPT, Perplexity, Google AI Overviews) in a single run that trains itself on the specific site, audits in parallel, fixes, verifies, and loops until the site comes back clean. Use whenever the user asks to "do SEO", "do the SEO/GEO/AI search thing", optimize a site for Google or rankings, get a site "found", make a site show up in ChatGPT/Perplexity/AI answers, add structured data/schema/llms.txt, improve search visibility for any client site — OR asks to "train", "set up", or "onboard" the SEO agents on a website. Trigger even if they name only ONE of the three (just "seo" is enough) — the skill always covers all three together. Works on static HTML sites and framework apps.
---

# SEO + GEO + AI-Search Overhaul

One prompt in, a finished site out. This skill launches a Workflow (skill invocation = explicit opt-in for multi-agent orchestration) that audits the site across 5 dimensions in parallel, fixes everything found, verifies with a deterministic checker, and repeats until a full audit sweep finds nothing new. Do not do the audit single-handed inline — the whole point is the fan-out and the loop.

`SKILL_DIR` below means this skill's own directory (where this SKILL.md lives).

## Step 1 — The site profile (how the agents get trained)

Every agent in the workflow reads a per-site profile: `SKILL_DIR/profiles/<site-folder-name>.md`. It holds the business identity, the facts bank (the only claims agents may publish), the target queries each page should win, competitors, voice constraints, and a run history. Profiles live in the skill dir — not the site root — so they never get deployed with the site.

**If the profile exists**: read it, use it. It is the source of truth and the user may have hand-edited it — their edits win over anything an agent would infer.

**If it doesn't exist** (first run on this site), build it before the overhaul. Spawn these research agents in parallel (Agent tool, one message — this is the small pre-step, not the Workflow):

1. **Harvester** — read every page of the site, any brief/notes/README in the folder, and check memory for client context. Extract: identity, verifiable facts, framework, page inventory, current voice.
2. **Query researcher** — WebSearch how real people search for this kind of business/site (include the location for local businesses). Collect: primary + secondary queries per page topic, and the question-shaped queries people ask AI engines ("how much does X cost", "who is the best X near Y", "is X worth it").
3. **Competitor researcher** — WebSearch the primary queries, note who actually ranks, what their titles/content do, and what gaps this site can exploit. For a local business, also look up the client's real Google Business Profile listing (exact name/address/phone) so schema can match it.

Synthesize all three into the profile using `SKILL_DIR/references/site-profile-template.md`. Facts bank gets **only verifiable facts** — research fills the queries and competitors sections, never invents business claims.

Then continue straight into the overhaul (one-prompt principle) — **unless** the user only asked to "train"/"set up"/"onboard" the agents, in which case stop after writing the profile and show them a summary so they can edit it before the first real run.

## Step 2 — Snapshot and baseline

- If the target is not a git repo, copy it to the scratchpad (`cp -r <target> <scratchpad>/seo-backup-<name>`) before any agent touches it. If it is a repo, make sure the tree is clean enough to diff.
- Run the checker once for the before-picture:
  `python3 SKILL_DIR/scripts/seo_check.py <target> --json`
  Keep the error/warning counts for the final report.

## Step 3 — Launch the workflow

Pass real values via `args` — `{target, profile, url, maxRounds}` where `profile` is the **full text** of the site profile — and substitute the literal SKILL_DIR path. The script below is complete; adapt only if the situation genuinely demands it.

```js
export const meta = {
  name: 'seo-geo-ai-overhaul',
  description: 'Profile-trained parallel SEO/GEO/AI-search audit, fix, verify — looped until a full sweep comes back clean',
  phases: [
    { title: 'Recon', detail: 'map the site once' },
    { title: 'Audit', detail: 'dimensions + citation test in parallel; new lenses each round' },
    { title: 'Gate', detail: 'refute unfounded findings before anyone edits' },
    { title: 'Fix', detail: 'one fixer per file' },
    { title: 'Verify', detail: 'checker script + breakage review' },
  ],
}

const SKILL = 'SKILL_DIR'  // substitute the absolute skill path
const TARGET = args.target
const PROFILE = args.profile
const URL = args.url || 'https://REPLACE-WITH-DOMAIN'
const MAX_ROUNDS = args.maxRounds || 3

const FINDINGS = {type: 'object', required: ['findings'], properties: {findings: {type: 'array', items: {
  type: 'object', required: ['file', 'issue', 'fix', 'severity'], properties: {
    file: {type: 'string', description: 'path relative to the site root, or "." for site-level'},
    issue: {type: 'string'}, fix: {type: 'string', description: 'exact concrete fix'},
    severity: {enum: ['critical', 'major', 'minor']}}}}}}
const FIXED = {type: 'object', required: ['results'], properties: {results: {type: 'array', items: {
  type: 'object', required: ['id', 'status', 'note'], properties: {
    id: {type: 'number'}, status: {enum: ['applied', 'skipped']},
    note: {type: 'string', description: 'if skipped, name the exact missing fact or decision'}}}}}}
const GATE = {type: 'object', required: ['verdicts'], properties: {verdicts: {type: 'array', items: {
  type: 'object', required: ['id', 'real', 'why'], properties: {
    id: {type: 'number'}, real: {type: 'boolean'}, why: {type: 'string'}}}}}}
const VERIFY = {type: 'object', required: ['passed', 'checkerErrors', 'problems'], properties: {
  passed: {type: 'boolean'}, checkerErrors: {type: 'number'}, problems: {type: 'array', items: {type: 'string'}}}}

const DIMS = ['technical', 'structured-data', 'content', 'geo-ai', 'performance']

// Later rounds must look with DIFFERENT eyes. Re-running the same five checklists
// mostly proves the auditors are consistent — it says nothing about whether the
// site is actually good, so rounds 2+ add lenses the dimensions can't see.
const LENSES = [
  ['competitor-gap', `Compare this site against the competitors named in the profile, page by page. Report only what a competitor does for one of our target queries that this site does not: a question they answer and we don't, proof they show and we don't, specifics where we're vague. Ignore their design.`],
  ['completeness-critic', `Everything below has already been audited and fixed by five specialist auditors. Your job is to find what they all MISSED — a page with no target query assigned, a query in the profile with no page covering it, an entity never named on the site, a claim nobody checked. Be concrete and specific.`],
  ['fresh-eyes', `You have never seen this site. You just searched one of the profile's target queries and landed here. Where does the page fail to convince you, in the first screenful, that it answers your question? Report only fixable content and structure problems.`],
]

const dimBrief = d => `Read ${SKILL}/references/dimension-checklists.md — do ONLY your "${d}" dimension.` +
  (d === 'geo-ai' ? `\nAlso read ${SKILL}/references/geo-playbook.md — it is your spec.` : '')

const auditPrompt = (name, brief, ctx) => `You are the ${name} auditor, round ${ctx.round}.
Site root: ${TARGET}   Deployed URL: ${URL}
${brief}

SITE PROFILE — your training file. Target queries, facts bank, voice and constraints here override generic best practice. Judge every page against ITS assigned queries, not against SEO in the abstract:
${PROFILE}

Site map from recon:\n${ctx.recon}
${ctx.handled.length ? `Already fixed — do NOT re-report unless the fix was applied badly:\n${ctx.handled.join('\n')}` : ''}
${ctx.blocked.length ? `Known blocked, waiting on the owner for facts — do NOT re-report:\n${ctx.blocked.join('\n')}` : ''}
${ctx.notes ? `The verifier flagged these last round — check them:\n${ctx.notes}` : ''}
Scan the actual files. Report only real, concretely fixable findings, each with the exact fix. Respect the profile's "Do not touch" list absolutely. An empty findings array is the correct answer when nothing is left to fix.`

// The outcome test. Ticking every GEO box is worthless if no engine would quote the page,
// so ask directly whether a citable answer exists rather than whether the markup is present.
const citationPrompt = ctx => `You are the AI-citation tester, round ${ctx.round}.
For EVERY question in the profile's "AI-search questions" column, and every primary query:
1. Open the page assigned to that query under ${TARGET} and read ONLY what is on it.
2. Decide: answering that question, with this page as a candidate source, would you cite it? Quote the exact passage you would use.
3. If no passage answers the question on its own — nothing quotable, or it only makes sense with the surrounding page as context — that is a FAILURE.
Report one finding per failed question: file = the page that should win it, issue = the question with no citable answer, fix = the exact section or FAQ entry to add and what it must state, using ONLY facts from the profile's Facts bank. If a needed fact is missing from the bank, say precisely which fact is missing instead of inventing it.
Questions that already have a clean quotable answer produce no finding.
SITE PROFILE:\n${PROFILE}\n\nSite map:\n${ctx.recon}`

// Cheap insurance against a hallucinated finding becoming a bad edit: one batched
// skeptic beats N per-finding skeptics at catching "you're missing a tag you already have".
const gatePrompt = list => `You are the findings gate for the SEO overhaul of ${TARGET}.
Other agents proposed the fixes below. Some will be wrong — auditors claim a tag is missing when it's already there, or call content thin when it's fine.
Open the actual files and check each claim yourself. Mark real=false when the problem is already satisfied, when the claim misreads the file, or when it's a subjective rewrite dressed up as a fix. Mark real=true only for problems you confirmed exist.
${list.map(f => `[id ${f.id}] ${f.file}: ${f.issue} → ${f.fix}`).join('\n')}`

const fixPrompt = (file, list) => `Apply these SEO/GEO fixes to ${file === '.' ? `site-level files in ${TARGET} (robots.txt / sitemap.xml / llms.txt)` : `${TARGET}/${file}`}.

SITE PROFILE — single source of truth. The Facts bank is the ONLY set of claims you may publish; match the Voice section; never touch anything in "Do not touch":
${PROFILE}

Fixes to apply:\n${list.map(f => `[id ${f.id}] [${f.severity}] ${f.issue} → ${f.fix}`).join('\n')}
Rules: change only what the fixes require — do not restyle, rewrite voice, or reformat untouched code. If a fix needs a fact that is not in the Facts bank and not already on the site, mark it skipped and name the missing fact — never invent one. Keep HTML valid.
Return one result per id with its real status. Report applied ONLY for fixes you actually wrote to disk: a fix wrongly marked applied disappears from the run and ships broken.`

phase('Recon')
const recon = await agent(`Map the site at ${TARGET} for an SEO overhaul. List every page file with its purpose, the framework (plain HTML / Next.js / other), and current head-tag state per page (title/description/schema: present or missing). Cross-check the page inventory against the profile's Target queries table and note any page with no assigned query (and any assigned query with no page). Profile:\n${PROFILE}\nReturn a dense factual summary, no advice.`, {schema: {type: 'object', required: ['summary'], properties: {summary: {type: 'string'}}}})

const key = f => `${f.file}::${f.issue.toLowerCase().slice(0, 60)}`
const seen = new Set()        // fixes actually written to disk — safe to stop re-reporting
const blocked = new Map()     // found but unfixable without a fact only the owner has
const fixLog = []
let notes = '', clean = false, lastVerify = null, rounds = 0, nextId = 1
let dirty = DIMS.slice()

for (let round = 1; round <= MAX_ROUNDS && !clean; round++) {
  rounds = round
  const ctx = {round, recon: recon.summary, handled: [...seen], blocked: [...blocked.values()], notes}

  const jobs = dirty.map(d => ({label: `audit:${d}`, src: d, prompt: auditPrompt(d, dimBrief(d), ctx)}))
  jobs.push({label: 'audit:ai-citation', src: 'geo-ai', prompt: citationPrompt(ctx)})
  if (round > 1) for (const [name, brief] of LENSES)
    jobs.push({label: `audit:${name}`, src: name, prompt: auditPrompt(name, brief, ctx)})

  const audits = await parallel(jobs.map(j => () =>
    agent(j.prompt, {label: `${j.label} r${round}`, phase: 'Audit', schema: FINDINGS})
      .then(r => (r ? r.findings.map(f => ({...f, src: j.src})) : []))))

  const uniq = new Map()  // lenses overlap; keep one finding per issue
  for (const f of audits.flat())
    if (!seen.has(key(f)) && !blocked.has(key(f)) && !uniq.has(key(f))) uniq.set(key(f), f)
  let fresh = [...uniq.values()]
  fresh.forEach(f => { f.id = nextId++ })
  log(`round ${round}: ${fresh.length} new findings from ${jobs.length} auditors`)

  // Gate the judgment calls. Technical and performance findings are provable by the
  // checker; content and GEO claims are where a wrong finding turns into a bad edit.
  const judgment = fresh.filter(f => f.src !== 'technical' && f.src !== 'performance')
  if (judgment.length) {
    const g = await agent(gatePrompt(judgment), {label: `gate r${round}`, phase: 'Gate', schema: GATE})
    const rejected = new Set((g ? g.verdicts : []).filter(v => !v.real).map(v => v.id))
    if (rejected.size) log(`gate rejected ${rejected.size} unfounded findings`)
    fresh = fresh.filter(f => !rejected.has(f.id))
  }

  if (fresh.length) {
    const byFile = {}
    for (const f of fresh) (byFile[f.file] = byFile[f.file] || []).push(f)
    const results = await parallel(Object.entries(byFile).map(([file, list]) => () =>
      agent(fixPrompt(file, list), {label: `fix:${file} r${round}`, phase: 'Fix', schema: FIXED})))
    const status = new Map()
    for (const r of results.filter(Boolean)) for (const x of r.results) status.set(x.id, x)
    // Only APPLIED fixes are retired. A skipped fix stays visible as a blocked item
    // instead of vanishing into "already handled" and shipping as a clean site.
    for (const f of fresh) {
      const s = status.get(f.id)
      if (s && s.status === 'applied') { seen.add(key(f)); fixLog.push(`${f.file}: ${f.issue}`) }
      else blocked.set(key(f), `${f.file}: ${f.issue} — NEEDS: ${s ? s.note : 'fixer returned no result'}`)
    }
    dirty = [...new Set(fresh.map(f => f.src).filter(s => DIMS.includes(s)))]
  } else {
    dirty = []
  }

  lastVerify = await agent(`Verify round ${round} of the SEO overhaul of ${TARGET}.
1. Run: python3 ${SKILL}/scripts/seo_check.py ${TARGET} --json
2. Open the files modified this round and check nothing broke: valid HTML, JSON-LD parses, no duplicated head tags, no visible design or layout damage, no placeholder left where a real value used to be.
3. Check the profile constraints held — nothing in "Do not touch" was modified, no claim outside the Facts bank was added:\n${PROFILE}
passed = the checker reports 0 errors AND you found no breakage. List every problem found.`,
    {label: `verify r${round}`, phase: 'Verify', schema: VERIFY})
  notes = lastVerify && lastVerify.problems.length ? lastVerify.problems.join('\n') : ''

  // Clean requires BOTH: nothing new to fix, and the deterministic checker passing.
  // Auditor silence alone only proves the auditors agree with each other.
  clean = fresh.length === 0 && !!lastVerify && lastVerify.passed
  log(`verify r${round}: ${lastVerify && lastVerify.passed ? 'PASS' : 'FAIL'}${clean ? ' — clean sweep' : ''}`)
  if (!clean && dirty.length === 0) dirty = DIMS.slice()  // verifier unhappy: re-sweep everything
}

return {clean, rounds, applied: fixLog, blocked: [...blocked.values()], lastVerify}
```

**How the loop actually converges.** A round ends clean only when the auditors find nothing new *and* the deterministic checker passes — auditor silence on its own just means the auditors agree with each other, which is not the same as a good site. Rounds 2+ bring in three lenses the dimension checklists structurally cannot see (competitor gaps, what everyone missed, first-visitor impression), so a later round is a genuinely new look rather than a replay. Fixes that get skipped for want of a real fact are never marked handled: they land in `blocked` and come back to the user as owner actions, because a fix silently dropped is how a site ships broken while reporting clean.

If `maxRounds` is hit without a clean sweep, say so plainly, list what's still open, and offer to resume with a higher `maxRounds` (the workflow returns a `runId` — resuming re-uses cached agent results rather than starting over).

## Step 4 — Report and remember

After the workflow returns:

1. Run the checker yourself once more for the after-picture.
2. **Append a run entry to the profile's Run history** — date, rounds used, findings fixed (by theme), owner actions still open, any decision made (e.g. "chose AutoRepair schema type"). This is the memory the next run trains on.
3. Write a short plain-English report:
   - **Before → after**: checker errors/warnings baseline vs now.
   - **What changed**: grouped by theme (meta/social, schema, content, GEO files, performance) — a few lines each, not a finding-by-finding dump.
   - **Which target queries now have a citable answer** — the citation test's result is the headline GEO number, far more meaningful than "added llms.txt".
   - **Owner actions**: the workflow's `blocked` list verbatim (each one names the missing fact), plus everything only the user or the client can do — real domain into placeholders, Google Business Profile match, Search Console and Bing Webmaster submission, deploy.
   - **Verdict**: clean sweep or not, rounds used, and where the profile lives so he can edit the training.

Never describe a run as clean when `clean` is false or the blocked list is non-empty — the blocked items are exactly the things a client would notice were missing.

## Hard rules

- **Truth over polish**: no invented reviews, ratings, stats, credentials, or business details — ever. If it's not in the profile's Facts bank or already on the site, it doesn't get published. Fake schema is a penalty risk and a lie to the client.
- **The profile outranks the playbook**: where the profile's voice/constraints conflict with generic best practice, the profile wins. Hand-edits to a profile are law.
- **Design untouched**: this skill edits heads, schema, copy structure, alt text, and site-level files. It does not restyle. (Taste rules live elsewhere and don't get overridden here.)
- **One prompt, no mid-run questions**: gaps become owner actions in the report, not blocking questions.
- Framework apps: metadata goes where the framework wants it (Next.js `metadata` export / `app/sitemap.ts` / `app/robots.ts`), not hand-rolled `<head>` tags; the checker then runs against the built output or `--url`.

## Files

- `profiles/<site-folder-name>.md` — one training profile per site (created on first run; user-editable; grows a run history).
- `references/site-profile-template.md` — the profile structure.
- `scripts/seo_check.py` — deterministic checker (dir or `--url` mode, `--json`). The verify gate.
- `references/dimension-checklists.md` — what each audit dimension covers.
- `references/geo-playbook.md` — the GEO/AI-search spec (llms.txt, AI crawlers, answer-shaped content).
