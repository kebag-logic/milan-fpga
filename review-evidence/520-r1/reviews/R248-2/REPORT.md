[R248] POSITIVE - exact head d253f86e410e301d146d4bd4e74d027f00cfb462

Round R248-2: external, cleared-context independent review of issue #520 / PR #522.

| item | value |
|---|---|
| exact head | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| tree | `ab5c567780993d405d0954092361396492cf49be` |
| parent (R248-1 head) | `28e350b99ac240a750326b762c6d029f0653362c` |
| source base | `483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| review start | https://github.com/kebag-logic/milan-fpga/pull/522#issuecomment-5789751042 |
| lenses applied at this head | Conformance, RTL, Robustness, Tests, Docs (all five) |
| open BLOCKER / MAJOR / MINOR | none |
| SUGGESTION | 1 (S1, Tests; does not affect coverage) |

## 1. Reconstruction

I read these in order: AGENTS.md, CONTRIBUTING.md (sections 2, 3 and 6.1), and
docs/README.md. Then the #520 issue body, with its frozen acceptance criteria
1-5 and settled scope, and the manager's assignment and evidence comments. Then
REQUIREMENTS.md REQ-VER-02/04 and the result-cache contract in
docs/testing/CI_WORKFLOWS.md. Then
`git diff 483a133e..d253f86e`, the two-commit history, and finally the public
evidence: the correction packet `correction-a187/` and the hosted check runs
for this head. Prior public review findings were read only after this
verdict line and the ledger in section 5 were written; their disposition is
section 6.

## 2. The delta and which lens scopes it touches

`git diff 28e350b9 d253f86e` changes exactly two files, +13/-12
(`receipts/delta_28e350b9_d253f86e.diff`, `receipts/delta_scope_blobs.txt`).
The other five files the PR touches are blob-identical to the parent:
`run.sh`, `result_cache.py`, `cache_selftest.py`, `rom_cache_selftest.py` and
`CI_WORKFLOWS.md`. Nothing under `hdl/`, `tb/`, `sw/` or any submodule moves.

- `.github/workflows/rtl.yml:538-542` is **comment-only**. I proved this three
  ways, against both the parent and the PR base, in
  `receipts/rtl_yml_comment_only_*.txt`:
  - the `yaml.safe_load` results are equal;
  - the 530 non-comment lines are byte-identical;
  - all 9 changed lines are YAML comments, and none of the 32 parsed `run`
    bodies contains the new text.

  Every reader of `rtl.yml` sees the same data. `ci_events.py` parses with
  `yaml.safe_load` (`scripts/ci_events.py:1382`). The `measure_fail_fast.py`
  waivers are keyed on exact line text, not line numbers
  (`scripts/measure_fail_fast.py:470-481`). `ci_scope.py` classifies by path.
  `act_ci.py` maps workflow names. No document cites `rtl.yml` by line number.
  `ci_events --check` and `--selftest` pass (1513 contract items, 1150 arms),
  as do `measure_fail_fast --check`/`--selftest` and `ci_scope --selftest`.
- `syn/yosys/README.md:24-31`: the Contents block.

Per-lens delta touch:

| lens | does the delta touch its scope? | re-applied here? |
|---|---|---|
| Conformance | No executable artifact. rtl.yml is comment-only and README is prose. | yes, in full |
| RTL | No. No HDL, pin, synthesis program or inventory change. | yes, in full |
| Robustness | No. The refusal/ordering code (run.sh, result_cache.py) is blob-identical. | yes, in full |
| Tests | Only a comment in the CI wiring file; the parsed workflow is identical. | yes, in full |
| Docs | Yes: README Contents and the rtl.yml comment. | yes, in full |

All five were re-applied at this head, so no lens relies on coverage banked at
`28e350b9`.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

```text
[R248] SUGGESTION Tests - syn/yosys/rom_cache_selftest.py:212-214 - empty-image arm cannot tell run.sh's existing refusal from the digest helper's
Requirement/evidence: #520 acceptance 3 says missing/empty images "retain their
  specific refusal". The cached empty arm expects the substring
  "generated ROM is empty:". result_cache.py's own refusal
  (result_cache.py:105, printed at :264) also contains that substring. Probe
  M4 moves the digest ahead of run.sh's nonempty check
  (receipts/probe_M4_empty_arm.txt). Under it, the cached empty arm still
  passes on "result_cache: ROM bundle refused: generated ROM is empty:
  ltn_rom.hex" together with "generated ROM bundle could not be digested". At
  the reviewed head the same arm shows run.sh's own "Yosys: generated ROM is
  empty: ..." line.
Impact: none at this head. The bank as a whole still detects M4, because the
  missing-image arm's OSError text lacks the substring (probe M4 fails at
  invalid-ltn_rom.hex-missing-True). One arm is weaker than its label.
Suggested change (optional): anchor the expectation on "Yosys: generated ROM
  is empty:", or assert that "could not be digested" is absent.
Verification: rerun probe M4. The cached empty arm itself should then fail.
```

## 4. Lens results at the exact head

```text
[R248] PASS Docs - syn/yosys/README.md:24-31, .github/workflows/rtl.yml:538-542 - R248-1 F1 resolved; separator switch preserves every anchor, label and description meaning
[R248] PASS Conformance - syn/yosys/run.sh:503-514,434-449; syn/yosys/result_cache.py:52-57,95-116,163-170; receipts/pp_shadow_probe.json; receipts/cache_selftest_head.* - acceptance 1-4 re-evidenced at this head; the motivating top reproduces the issue's stale-evidence numbers and their repair
[R248] PASS RTL - receipts/delta_scope_blobs.txt; receipts/bank_static/28_inventory_base_eq.*; syn/yosys/run.sh:545-560 - no HDL, pin or synthesis-program change; 54-top inventory identical to base; cell extraction untouched
[R248] PASS Robustness - syn/yosys/run.sh:489-514,566-579; syn/yosys/result_cache.py:112-116,154-177; receipts/mutation_probes.jsonl (M4, M5, M8); rom cache arms invalid-* and entry-* - refusals, ordering, malformed/legacy records, seed-only and cache-disabled paths
[R248] PASS Tests - syn/yosys/result_cache.py:386-463; syn/yosys/rom_cache_selftest.py; syn/yosys/cache_selftest.py; .github/workflows/rtl-fast.yml:224; receipts/mutation_probes.jsonl - 7/7 defect-bearing mutants detected; original controls carried forward unweakened
```

### Docs

- **F1 is resolved at both locations.** `README.md:27` now reads: "`--cache DIR`
  skips a top only when every input its key binds matches a verified PASS entry
  (#350), the generated ROM bundle (#520) included". It names the key
  definition, the three ROM images and the schema-2 migration, and all of them
  are in the section it links: the key at `README.md:98-103`, the images and
  framing at `:105-120`, schema 2 at `:122-125`.
- `rtl.yml:538-541` now states the same skip condition and points to
  "The result cache" in `syn/yosys/README.md`. That heading exists
  (`README.md:90`) and defines the key.
- A tree-wide search finds no remaining statement that the pre-#520 input list
  is enough for a skip. `CI_WORKFLOWS.md:223-226` and `:245-257`, the `run.sh`
  usage text (`:43-48`) and the `result_cache.py` docstring (`:10-15`) all
  name the ROM bundle. `run.sh:406-408` describes only the tool half of the
  key, which is accurate.
- **The separator switch changed no meaning**
  (`receipts/contents_meaning_28e350b9_d253f86e.txt`, from
  `scripts/contents_meaning.py`). All 8 entries keep their labels and anchors
  byte-identical, and every anchor resolves to a heading on the page. All 8
  separators are now `--`, and U+2014 appears outside a label nowhere.
- Seven of the eight descriptions keep an identical word sequence; only
  punctuation moved. I read each one by hand. Paired dashes became parentheses
  (Tooling). Single dashes became a colon (Tooling, Runtime levers, Notes,
  ooc.sh) or a sentence break (How it works). No referent or claim changes.
- Only "The result cache" entry changed words, and that change is F1's fix.
  The Tooling entry's `v0.0.12` still matches the CI pin (`rtl.yml:529`).
- **Route.** Taking the page-wide separator switch is what CONTRIBUTING.md:550-555
  prescribes. The only U+2014 left in the block is the `ooc.sh` label that the
  generator copies from a base heading, which is the provenance exemption
  (CONTRIBUTING.md:503-509).
  - `check_em_dash --base 483a133e`: 0 findings over 57 added lines, 1 label
    exempt.
  - `check_em_dash --base 28e350b9`: 0 findings over 8 lines.
  - `gen_toc --check` passes, so the block is byte-identical to the
    generator's render.
- **Gates.** These pass at this head (`receipts/bank_static/`):
  - `gen_toc --check`/`--verify-anchors`/`--selftest`;
  - `docs_check` and its self-test;
  - `check_doc_style` and its self-test;
  - `check_em_dash --selftest`;
  - `check_hygiene --check`/`--selftest`;
  - `check_doc_paths`, `check_feature_status`;
  - `git diff --check` over both ranges.
- **Author packet.** The published delta patch in `correction-a187/` has
  sha256 `28f84379...`, byte-identical to `git diff 28e350b9 d253f86e`. Both
  commit messages are one line with no trailers.

### Conformance

- **Acceptance 1.** Cold then warm at the same source and tools: identical
  cells, and verified hits. This holds for the real-gate `cdc_pulse` arms and
  for `full-cold`/`full-warm` and `elaborate-cold`/`elaborate-warm` on two tops
  (`receipts/cache_selftest_head.*`: 54 driver runs plus 5 original arms, exit
  0, 53 s). The motivating top also holds (`receipts/pp_shadow_probe.json`,
  exit 0): `KL_pp_shadow` ran cold live at 1,141,365 cells, and warm hit
  1,141,365 in 3.8 s.
- **Acceptance 2.** Changing only generated bytes (`ucode.hex` replaced after a
  successful real generator run; the generator is untouched):
  - the former entry misses;
  - the live result is 1,122,602, equal to the uncached run on the same
    change;
  - between the compared identities only `rom_sha256` differs;
  - lookup identity equals store identity.

  These are the issue's own figures, reproduced independently. Every image and
  both modes are covered: each of the three images, in full and elaborate
  modes, misses on the per-head state and on the read-only seed
  (`*-per-head`, `*-seed-only`), and `differences == {"rom_sha256"}` is
  asserted per top.
- **Acceptance 3.** For each image, the arms cover failed, empty and missing
  output, cached and uncached. That is 18 arms, all exit 2 with their existing
  message, and none looks up or stores. Order independence and filename/content
  binding are covered by the unit fixed-oracle arms (`result_cache.py:386-432`).
- **Acceptance 4.** Six forms of old or invalid entry all run live:
  `entry-old-key`, `-old-schema`, `-missing`, `-malformed`, `-mismatch` and
  `-duplicate`. The original forged-cells and seed controls and the unit
  hit-rule arms are carried forward. `receipts/removed_lines_selftests.txt`
  shows the diff removes no assertion.
- **Acceptance 5.** The commands this round is allowed to run all pass. The
  full local, act, hosted and exact-candidate bar, and the merge sequence,
  belong to the manager (section 8).
- **Scope held.** There is no generator, pin, program, inventory
  (`INVENTORY-IDENTICAL tops=54`), structural-check, workflow-behaviour or
  ratchet change.

### RTL

The PR changes no HDL, no submodule gitlink and no synthesis program. The
`program_key` lines (`run.sh:545-560`) and the `stat -json` extraction are
outside every hunk. `run.sh --list` at head equals the base's (54 tops).
Integrity checks put the three required submodules at their pins (verilog-axis
`48ff7a7e`, protocol-processor `424c688f`, gptp-processor `c1b61743`). The RTL
lens here is the synthesis gate's evidence path, and it is unchanged except
for the ROM binding.

### Robustness

The ROM digest is taken only after all three generators succeed and the
existing `[ -s ]` checks pass (`run.sh:494-514`). It is taken only when a cache
is in use, so the uncached gate runs no new command. The uncached invalid-*
arms keep their exact messages. The digest refuses an empty or missing image
(`result_cache.py:103-105`, exit 2 through `run.sh:511-513`).

By reading `result_cache.py:112-116,228` and `run.sh:441-451,566-579`, a
malformed or empty `--rom-sha256` fails argparse with exit 2. Lookup then
counts as refused and the top runs live, and store is declined with a note.
The unit arm rejects six malformed digest forms (`result_cache.py:427-432`).

Probes (`scripts/mutation_probe.py`, each in its own disposable copy):

- M4, the digest taken before the nonempty checks: detected.
- M5, the hit rule ignoring the recorded ROM field: detected.
- M8, the digest missing on seed-only runs: detected.

The legacy and invalid entry forms run live in the real gate. Repeated runs
are idempotent: warm hits, and store keeps an existing entry.

### Tests

The shipping controls catch every mutant that carries a behavioural defect
(`receipts/mutation_probes.jsonl`, `scratch/` logs not published):

| probe | models | unit | real gate |
|---|---|---|---|
| M1 | pre-#520 defect: constant ROM identity | pass | **FAIL**: changed `ltn_rom.hex` served stale hits for both tops |
| M2 | store and lookup keyed differently | pass | **FAIL**: warm did not hit |
| M3 | bundle omits `ucode.hex` | **FAIL** | (stops at unit) |
| M4 | digest before nonempty checks | pass | **FAIL**: missing-image refusal text (see S1) |
| M5 | hit rule skips `rom_sha256` | **FAIL** | (stops at unit) |
| M6 | schema string left at 1 | pass | pass: not detected, and not a defect. The key canonical text already gains the `rom_sha256` line, so genuine schema-1 entries sit at other keys and miss, and relocated ones lack the field and refuse. Schema 2 is verified by reading `result_cache.py:52`. |
| M7 | no length framing | **FAIL** | (stops at unit) |
| M8 | digest missing on seed-only runs | pass | **FAIL**: seed-only did not hit |

`rtl-fast.yml:224` runs `cache_selftest.py`, so the ROM controls ride the
fast workflow. `result_cache.py --selftest` passes, as does `yosys_tally.py
--selftest`, `check_py_idiom` and `check_sh_idiom`.

## 5. Reviewer-owned completion ledger

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #520 acceptance 1-5 and scope; `run.sh:434-514`; `result_cache.py`; real-gate cache self-test; `KL_pp_shadow` probe; inventory diff | R248-2 | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| RTL | CLEAN | delta/PR path list (no HDL/pin change); `run.sh:545-560` programs; `--list` inventory base vs head; submodule gitlinks | R248-2 | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| Robustness | CLEAN | `run.sh:489-514,566-579`; `result_cache.py:95-116,154-177`; probes M4/M5/M8; 18 generation-refusal and 6 entry-refusal real-gate arms | R248-2 | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| Tests | CLEAN (S1 is a SUGGESTION) | `result_cache.py` self-test arms; `cache_selftest.py`; `rom_cache_selftest.py`; `rtl-fast.yml:224`; 8 mutation probes; rtl.yml reader self-tests | R248-2 | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| Docs | CLEAN | `syn/yosys/README.md` (Contents :24-31, cache section :90-172); `rtl.yml:538-542`; `CI_WORKFLOWS.md:221-257`; `run.sh` usage; tree-wide stale-key search; docs gates | R248-2 | `d253f86e410e301d146d4bd4e74d027f00cfb462` |

## 6. Prior public findings at this head

I read these only after sections 1-5 were written. Sources: PR #522 comments
5789594327 (R248-1) and 5782558633 (R247-1). The PR has no review objects.

| finding | round, severity, lens | disposition at `d253f86e` | evidence |
|---|---|---|---|
| F1: two cache-key summaries state the pre-#520 key as enough for a skip | R248-1, MINOR, Docs | **RESOLVED** | Section 4 Docs: `README.md:27` and `rtl.yml:538-541` both name the ROM bundle and point to the key definition. The verification that F1 names passes: `gen_toc --check`, `docs_check`, and `check_em_dash --base 483a133e` (the merge base). Because rtl.yml is touched, the `ci_events` contract checks were run too. The hosted/act rtl-full gates on the new head are manager-owned (section 8). |
| SG1: message-less asserts; a non-AssertionError escapes `run_arms` | R248-1, SUGGESTION, Tests | **RETAINED** (optional) | Artifacts unchanged since `28e350b9` (`rom_cache_selftest.py:125,171,195,199,228`; `cache_selftest.py:132-138`). The gate still fails closed. |
| SG2: no control pins the schema advance | R248-1, SUGGESTION, Tests | **RETAINED** (optional) | Reproduced independently as probe M6. Behaviour-neutral; `SCHEMA` is `/2` at `result_cache.py:52`. |
| SG3: rtl-fast step comment lists only the original four cache arms | R248-1, SUGGESTION, Docs | **RETAINED** (optional) | `rtl-fast.yml:219-222` is unchanged since `28e350b9`. The comment is incomplete but not false, so it does not block Docs coverage. |
| (none) | R247-1, POSITIVE, no findings or suggestions | nothing to resolve | - |

S1 in section 3 is new to the record. It is distinct from SG1 and SG2: it
concerns the discriminating power of one expected-text match, not assert
messages or the schema string.

The out-of-scope notes R248-1 listed remain as they were: README prose quoting
48 tops against the 54-top inventory (`README.md:93-94,159-160`), the Yosys
techlib data directory outside the key, and forgery inside a writable tier by
design. The delta does not touch them. They are not findings against #520.

## 7. Real limits of this round

- **Local tools differ from CI.** Real-gate runs used Yosys 0.66 (distribution
  build) and sv2v v0.0.13. CI pins sv2v v0.0.12 and a CI-built Yosys 0.66.
  Cell counts here are compared only with one another at the same host and
  tools, never with CI figures. The `KL_pp_shadow` numbers happen to equal the
  issue's published figures.
- **Cell-effect coverage is partial.** The real cell-effect probe covered
  `KL_pp_shadow` with a changed `ucode.hex`, in full mode. The other images'
  cell effects rest on the binding controls (all three images, both modes) and
  on the shared digest path. I did not re-measure them on ROM-dependent tops.
- **No banks, act or Docker.** I ran no full parent/PP/gPTP/Yosys/builder
  bank, no act and no Docker. Probes ran only in disposable copies under
  `scratch/`. The candidate `act_ci.py --selftest` was not run on the host.
  Scoped Verilator 5.050 was identity-checked (it reports `Verilator 5.050
  2026-07-01 rev v5.050`) and not needed, since the PR changes no HDL.
- **Author control C1 not reproduced.** `check_em_dash.py` judges only
  committed HEAD, and this round makes no commits. The route rests on
  CONTRIBUTING.md:550-555; the author's control logs are corroboration only.
- **Hosted evidence is a partial snapshot.** Taken at 2026-09-23T06:03:08Z
  (`receipts/check_runs_d253f86e_final.*`):
  - 18 exact-head jobs had concluded `success`;
  - `Verilator shard 4/5` was still in progress;
  - `Physical gPTP (nightly and manual)` was skipped;
  - the `verilator-suites` and `yosys-portability` aggregate contexts were not
    yet emitted.

  Hosted Yosys shard 0 (merge `2dd2b2e` of this head into `483a133e`) restored
  a branch-lineage result cache and published `milan_datapath` from it: 1 hit,
  0 refusals (`receipts/hosted_yosys_shard0_d253f86e.log`). I make no claim
  about the aggregates or about hosted/act acceptance.
- **Manager banks not seen.** The manager's full source static/builder and
  native banks for this head were still running. I have not seen them and do
  not infer their results.
- **This is source review only.** The source base is `483a133e`; live dev is
  `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d`. I did not build or validate the
  current-dev merge candidate.
- **No hardware evidence.** Physical calibration was NOT RUN. Field skips and
  the skipped physical job are not hardware proof.

## 8. Pending manager duties

- Publish this report and its manifest-listed receipts.
- Accept the exact-head hosted required contexts for `d253f86e`, including the
  emitted `verilator-suites` and `yosys-portability` aggregates.
- Run the trusted act replica from a clean live-dev worktree for this head.
- Complete the full source static/builder and native banks at this head.
- Confirm the second positive review. Lane-internal R247-1 was POSITIVE at
  `28e350b9`. Whether its coverage carries to `d253f86e` (a Docs and
  comment-only delta) or needs re-review is for the internal lane to decide
  under AGENTS.md section 7.
- Validate the current-dev candidate (this head merged into live dev
  `776bc77d`) with the full local bar.
- Merge only with explicit maintainer authorization.
- Run canonical post-merge containment, then move the issue to Closed/Done.
- Keep the shared Yosys result seed disabled until this lane clears, as the
  issue decides.

## Integrity

- **Clone left byte-exact at the reviewed head.** Before and after this round
  (`receipts/integrity_before.txt`, `receipts/integrity_after.txt`):
  - HEAD and tree equal the published ids;
  - the index equals HEAD;
  - all 852 tracked blobs re-hash to their HEAD ids with matching modes;
  - there are no assume-unchanged or skip-worktree flags;
  - the status is clean, with no untracked or ignored paths;
  - `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` are
    single stage-0 gitlinks, checked out clean at their pins.
- **Bytecode caches removed.** Focused runs wrote Python bytecode caches
  (ignored paths) into the clone. They held `.pyc` files only and were removed.
- **No GitHub write.** This round made none: no comment, review, label or
  metadata.
- **Publication set.** Only `REPORT.md` and the files listed in
  `MANIFEST.sha256` are publishable. Absolute host paths in them are replaced
  by `<clone>`, `<packet>`, `<shared-tmp>` and `$HOME` placeholders.

R248-2 FINISHED
