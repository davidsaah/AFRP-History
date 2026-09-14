# AFRP-FTB → AFRP-FamilyTree — cleanup and repo plan
**14 September 2026** · audit of `C:\Users\David\Projects\AFRP-FTB`, plan for `github.com/davidsaah/AFRP-FamilyTree`

---

## Read this first

**The v117 source is not on your computer.** I searched `Projects\`, `Downloads\`, and `Projects\Claude outputs\`. What's there:

| looked for | found |
|---|---|
| `AFRP_Family_Tree_Package_v117.zip` | **no** |
| `AFRP_Portal_Handoff_Bundle.zip` (contains `builder/` = full v117 source) | **no** |
| `Ramallah Family Tree_20260813.ged` (master GED) | **no** |
| `Ramallah_Handoff_20260815.zip` | yes — but it's the *book chapters* handoff, no tree code |
| `AFRP-transfer-package.zip` | yes — but it's *bylaws and portal mockups* |

The v117 release notes say the files were **"delivered in the conversation (no cloud transfer)"** — so they're attachments in the tree-builder chat, never saved to disk.

**What I can recover right now:** `claude/AFRP_Family_Tree_Builder_v117.html` is in this project — 1,326,738 bytes, **19,475 lines**, `APP_VERSION = 'v116.0 (2026-08-15)'`, matching the v117 notes exactly. I opened it: the JavaScript is **unminified and fully readable**, with every engine symbol intact (`rosetteSqueeze` ×15, `polishLayout` ×8, `finalPolish`, `svgScene`, `bookExport`, `setupIO`, `optimizer`, `buildFunStats`). The engine is not lost. Only the *modular TypeScript* packaging, the test suite, the CLI tools and the GED are.

So step 1 is a fork, and it's worth ten minutes of your time before anything else happens.

---

## ⚠ The thing that must be decided before the repo is created

**The master GED holds birth dates for thousands of living relatives.**

The Portal handoff doc already flagged this: *"whether the portal gates living people's birth dates behind login (the book prints them; the web is a different exposure)."* A **public** GitHub repo is a much bigger exposure than either — it's permanent, indexed, cloneable, and git history keeps it even after deletion.

Three options, in the order I'd recommend them:

1. **Make `AFRP-FamilyTree` private.** Simplest, safest. You lose nothing — nobody outside the family needs the source.
2. **Public repo, GED stays out.** `*.ged` in `.gitignore`, the file lives beside the repo, the README says where to get it. Code is shareable, data isn't.
3. **Public repo with a redacted GED** — living individuals stripped or dates suppressed. Most work, and easiest to get subtly wrong.

**If the repo is public and the GED ever gets committed, removing it later means rewriting history and force-pushing** — and any clone made in between keeps it. Decide now, not after.

---

## What's in AFRP-FTB today

A Google AI Studio scaffold, cloned once from `github.com/davidsaah/AFRP-FTB` on 5 September, commit `c06a23f`, authored `David S Saah <dsaah@sig-gis.com>`. No local commits. You've said the AI Studio app is dead — so all of this goes. For the record, here's what it was, because a couple of pieces are worth a second look before they're deleted:

**Broken on arrival**

- `components/PageTabs.tsx` and `components/SettingsPanel.tsx` are **0 bytes** and imported by nothing
- `index.html` links `/index.css` — **the file does not exist**
- `vite.config.ts` inlines `GEMINI_API_KEY` into the client bundle, but there's no `@google/genai` dependency — dead boilerplate, and an API-key leak waiting to happen if anyone ever set it
- d3 loads **twice** — a `<script>` tag *and* an npm import
- an AI Studio `importmap` pointing at `aistudiocdn.com` fights the npm dependencies in `package.json`
- circular import: `App.tsx` ↔ `TreeView.tsx`/`Header.tsx` via `useTheme`
- README is AI Studio boilerplate, pointing at an `ai.studio` URL and a Gemini key you don't need
- no tests, no CI, no LICENSE

**Wrong for the brief**

- the layout is `d3.forceSimulation` — a physics settle that lands differently every run. Your brief needs *"easy to regenerate every tree whenever the GEDCOM file is updated."* Force layouts fight that. **v117 already solved this** — deterministic per-person jitter, `finalPolish`/`polishLayout` with hard no-touch/no-cross guarantees, and a tracked crossings set.
- the GEDCOM parser has **no `CONC`/`CONT` handling** — long notes and names silently truncate
- **no `REFN` handling** — and REFN is the stable ID your book pipeline and John's exports depend on
- no `CHAR`/encoding handling — Arabic names will mangle on an ANSEL or BOM'd file
- `SavedPage` configs are never persisted; only the theme is. The app's whole point evaporates on refresh.

Nothing here is worth carrying forward. v117's parser already handles ANSI/UTF-8/UTF-16, GEDCOM 5.5/5.5.1, REFN and auto-REFN.

---

## The plan

### Phase 0 — recover the source (do this first)

**Route A — find the real package.** In the tree-builder chat (or the portal-handoff chat of 21 August), download:

- `AFRP_Family_Tree_Package_v117.zip` — `builder/` with `src/`, `standalone/`, `tools/`, `tests/`, `dist/`, plus the master GED and the Awwad test GED
- or `AFRP_Portal_Handoff_Bundle.zip` — same `builder/` plus the eight spec docs

Drop either in `Downloads\` and tell me. **This is worth real effort** — it's the difference between inheriting a working pipeline and rebuilding one.

**Route B — reconstruct from the standalone.** If the zips are gone, I split the 19,475-line bundle back into modules along the documented map (`gedcomParser`, `genealogyAnalyzer`, `radialLayout`, `svgScene`, `bookExport`, `registerPages`, `setupIO`, `optimizer`), restore `standalone/build.cjs`, and re-add TypeScript types module by module.

What Route B costs you: the **50-check regression suite** and 18 probes, `regen.cjs` and `makebook.cjs`, and the **master GED**. Those get rebuilt or re-sourced. The engine itself survives intact — it's all readable.

*I'd give Route A a hard try first.*

### Phase 1 — clear the folder

Delete everything except `.git` (kept one more step for the audit trail), then delete `.git` too — you chose fresh history. On Windows I can't `rm` through the bridge, so the dead files move to `_to_delete\` and you empty it.

### Phase 2 — lay out the new repo

```
AFRP-FamilyTree/
├─ README.md               what it is, how to build, how to regenerate the book
├─ LICENSE                 (AFRP-History has one — match it)
├─ .gitignore              node_modules, dist artifacts, *.ged (see the privacy decision)
├─ builder/
│  ├─ src/                 the TypeScript engine
│  ├─ standalone/          build.cjs + template.html → the single-file app
│  ├─ tools/               regen.cjs, makebook.cjs, legend utilities
│  ├─ tests/               regression suite + probes
│  ├─ package.json  tsconfig.json
├─ assets/
│  └─ cover.jpg            ← see note below
├─ data/                   master GED + test GED (or gitignored — privacy decision)
├─ dist/
│  └─ AFRP_Family_Tree_Builder.html
└─ docs/
   ├─ ARCHITECTURE.md      from the portal bundle's 02_Architecture.md
   ├─ DATA_MODEL.md        REFN/clan conventions, the 3-pass clan algorithm
   ├─ LAYOUT.md            tree grammar, pagination ladder, capacity rule
   ├─ DESIGN_LANGUAGE.md   palette, weight scale, typography
   └─ RELEASE_HISTORY.md   v87 → v117, from the project docs
```

**The cover-art note:** the standalone inlines the cover photo as a **401,376-character base64 line**. In a git repo that single line re-diffs on every rebuild. Pull it out to `assets/cover.jpg` and inline it at build time — the repo stays readable and diffs stay small.

### Phase 3 — git

Fresh history, as you chose:

```
git init -b main
git remote add origin https://github.com/davidsaah/AFRP-FamilyTree.git
git add -A
git commit   # one clean initial commit, cleanup already applied
git push -u origin main
```

Two details worth getting right while we're here:

- **Set the author email for this repo** to your personal address — the old commit used `dsaah@sig-gis.com`, which is your work account. `git config user.email` at the repo level.
- **`.gitattributes`** — copy AFRP-History's. Its absence is what produced the CRLF warnings that silently broke that repo's push script in August.

Leave `davidsaah/AFRP-FTB` alone; archive it on GitHub later if you want one obviously-live repo.

### Phase 4 — prove it still works

Before the first push is called done:

1. `node builder/standalone/build.cjs` → rebuilds the single-file HTML
2. Open it, drop a GED in, confirm a tree renders
3. Run the regression suite if Route A got it back
4. Compare the rebuilt HTML against the v117 original — **the same identity check the v117 release used** (743/743 pages pixel-identical). If the rebuild isn't identical, the reconstruction is wrong and we find out now rather than later.

---

## What I need from you

1. **Private or public repo?** — the GED question above. Nothing gets pushed until this is answered.
2. **Route A or B?** — go look for those two zips. Five minutes of searching could save a day of reconstruction.
3. Confirm you want the AI Studio files gone entirely (I'll stage them in `_to_delete\` either way — nothing is destroyed without you emptying that folder).

Once I have 1 and 2, I can do the rest end to end.

---

## Open questions I couldn't settle from here

- Does `github.com/davidsaah/AFRP-FamilyTree` already exist, and is it empty? I can't check without your browser. If it was created with a README, the first push needs `--force` or a pull-rebase.
- `Projects\AFRP-Hub\` has a `tree\` app — is that a third implementation, or a placeholder? Worth knowing before we declare AFRP-FamilyTree the single home for tree code.
- The v117 notes list the master GED as `Ramallah Family Tree_20260813.ged`, but the Portal bundle references it under `builder/`. If John has since sent a newer export (the REFNs for 157 new people), that's the one the repo should carry.
