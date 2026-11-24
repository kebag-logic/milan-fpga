[R913] POSITIVE - exact head 30796098256670c76115610498a3cdad4d8281ba

# R913-3: narrow re-review of milan-fpga PR #992 (Closes #991), `20-lwsrp-pin-d1bb4f4` -> `dev-soft-core`

Head `30796098256670c76115610498a3cdad4d8281ba`, tree `9c57ac8c6108d8ef99d2a1287b2e4456fa1d9d82`. Delta since the
previously reviewed head `ed7df79c6f87a4172c885f268ad67629bd56c4eb`: one manager commit with a one-line message and
no trailers. It changes only `tb/verilator/milan_dp/README.md`, with 4 lines added and 3 removed at `:1406-1410`.
Gitlinks are unchanged (`receipts/delta.txt`). Evidence packet: `review-evidence/lwsrppin-r1/author-r2b` at
`ab1710ee`.

## Summary

All five lenses were applied to the delta, and all five are clean. R913-2-F1 (MINOR, Docs) is **RESOLVED**. The
sentence now claims exactly what the self-test holds. The round-2 txLA! Registrar mutant still passes the
self-test, and the README no longer claims that case.

This round adds no BLOCKER, MAJOR or MINOR. It adds one wording RESIDUE: the PR body was not updated for this
commit (N-R1). It also adds one SUGGESTION (N-S1). Prior residue and suggestions are carried below. R914-2
POSITIVE at `ed7df79c` stands, because nothing that round examined has changed apart from this README sentence.

## Prior findings at this head

| Finding | Status | Evidence at `30796098` |
|---|---|---|
| R913-2-F1 (MINOR, Docs): README `:1406-1408` said the self-test holds "both cases, with the Registrar MT and with it IN" | **RESOLVED** | README `:1407-1409` now reads "holds the txLA! case with the Registrar MT, and the txLAF! case with the Registrar MT and with it IN". Matching against `twin_mrp.py` `selftest()`: `omission-with-room` (`:430-431`) is the txLA! omission, run on `joined` with no rJoinIn (Registrar MT). `omission-from-full` (`:432-434`) is txLAF! with the Registrar MT. `omission-from-full-registrar-in` and `joinin-after-omission-from-full` (`:435-442`) are txLAF! after `rJoinIn!` (Registrar IN). The docstring `:402-410` says the same. The rest of the sentence also holds: "the Lv after the own LeaveAll" is `msrp-`/`mvrp-lv-after-own-leaveall` (`:424-427`), and "the octet counts" are the four octet checks (`:444-454`). The round-2 mutant (Table 10-4 txLA! row `"txLA!": {"IN": "LV"}` at `:98` emptied) still gives `OK (11 checks)` rc 0. Control at this head: `OK (11 checks)` rc 0 (`receipts/txla-registrar-mutant.txt`). That gap is no longer claimed. |
| R913-2-R1 (RESIDUE, Docs): PR body routed-image paragraph gives the wrong reason the route stands | **RETAINED** (carried) | `receipts/pr-body-live.md:96-97` is unchanged ("Round 2's images are byte-identical to `dbba60e6`'s ..."). The exact fix from R913-2 still applies. This head also changes no image input (`receipts/delta.txt`) |
| R913-2-R2 (RESIDUE, Docs): `test_ctrl_firmware.py:80-82` "... own LeaveAll sent as Lv ..." parses ambiguously | **RETAINED** (carried) | Unchanged at `sw/firmware/ctrl/test/test_ctrl_firmware.py:81-82`. Exact fix as R913-2: "... after the board's own LeaveAll is sent as Lv within 240 ms" |
| R913-2-S1 (SUGGESTION): `--selftest` prints `OK (0 checks)` on its failing zero-check exit | open, optional | `twin_mrp.py:465-466` unchanged |
| R913-2-S2 (SUGGESTION, Tests): Table 10-4's txLA! Registrar row has no self-test or capture coverage | open, optional | Still true. The mutant above passes. Since F1 was fixed by scoping the claim rather than by adding a check, the gap is honest but uncovered. The row predates this PR. It belongs in a new Issue or in this lane, as the author chooses |
| R913-1-F1, R914-1-F1 (MINOR) | RESOLVED at `ed7df79c`, still resolved | The delta does not touch `twin_mrp.py`. The control self-test at this head is `OK (11 checks)` |
| R913-1-S1 (SUGGESTION) | TAKEN at `ed7df79c` | Unchanged |
| R914-2 (POSITIVE at `ed7df79c`, no findings) | stands | No file it examined changed except the README sentence reviewed here |

## New findings

### N-R1 - RESIDUE - Docs - PR #992 body ("What changes" table; "Evidence at the head" paragraph `:29`; gate rows `:38-39`, `:50`)

- **Evidence:**
  - The body was last edited at 2026-11-24T05:07:44Z. This head was committed at 05:34:41Z
    (`receipts/twin-input-identity.txt`).
  - The "What changes" table has no row for "State the twin self-test's Registrar cases for each LeaveAll
    omission as it holds them".
  - `:29` "The last two commits change only `twin_mrp.py`, the twin README and a docstring ..." describes the
    `4ad6c164`/`ed7df79c` pair.
  - The rows "at this head" for `make twin`, `make twin-plants` and the 44 `docs.yml` steps were produced at
    `ed7df79c`. The body names no head SHA, so "this head" now reads as `30796098`.
- **Why wording only:** no figure or result changes at this head.
  - No twin or plant input changed. The only changed path is the README, and no bench Makefile, script or source
    file reads it; every README mention there is a comment or citation (`receipts/twin-input-identity.txt`).
  - At exact head, the docs gates that read this page pass on my rerun: `docs_check.py` 0 findings,
    `check_em_dash.py` with the pinned renderer 0 findings over `ed7df79c..HEAD` and over `aa30d77f..HEAD`, and
    `check_baremetal_only.py` 0 findings.
- **Impact:** a cold reader cannot see from the PR alone that this commit exists or which head the gate rows ran
  at.
- **Exact fix:**
  - Add a table row: "State the twin self-test's Registrar cases for each LeaveAll omission as it holds them |
    the twin README only: `twin_mrp.py --selftest` holds the txLA! omission with the Registrar MT and the txLAF!
    omission with the Registrar MT and IN".
  - Change `:29`'s opening to: "The last three commits change only `twin_mrp.py`, the twin README and a docstring
    of `test_ctrl_firmware.py`; the last changes the README only."
  - Change "at this head" in the `make twin`, `make twin-plants` and `docs.yml` rows to "at `ed7df79c` (this head
    changes only the twin README, read by none of them except the docs gates, which pass at this head)".
- **Verification:** reread the body against `git log aa30d77f..30796098` and this packet's receipts.

### N-S1 - SUGGESTION - Docs - `tb/verilator/milan_dp/README.md:1407-1410`

The sentence lists what the self-test holds but leaves out `mt-at-own-leaveall` (`twin_mrp.py:428-429`, "Mt
there is illegal"). The list is not stated as exhaustive, so nothing in it is false. Optional: add "the Mt that no
rLA! allows at a carried value" so that the list matches the 11 checks.

Comment-rule scan of the delta: none of the 4 added lines has a bench lane label, lane name, review round,
reviewer ID, issue-comment ID, tool or model name, or host detail. There is no U+2014 or U+2013 and no trailing
whitespace. The longest added line is 75 columns, against 78 in the surrounding paragraph
(`receipts/residue-scan.txt`).

## Lens results (delta, exact head 30796098)

- `[R913] PASS Conformance` — `tb/verilator/milan_dp/README.md:1392-1410` against IEEE 802.1Q-2022 10.7.5.8,
  10.7.5.9, Table 10-3 and Table 10-4 as encoded at `twin_mrp.py:76-103`; issue #991 acceptance 2 ("docs gates
  pass"; `receipts/issue-991-body.md`).
  - The changed sentence makes a coverage claim only. The txLA!/txLAF! semantics before it (`:1393-1406`) are
    unchanged and match `twin_mrp.py:181-190`.
  - Acceptance 2, docs part: `docs_check` 0 findings, em-dash (pinned renderer) 0 and 0, bare-metal 0, doc-style
    OK (`receipts/docs-check.txt`, `em-dash.txt`, `baremetal-only.txt`, `doc-style.txt`).
  - No other acceptance item depends on this file.
- `[R913] PASS RTL` — `git diff --stat ed7df79c..30796098` (`receipts/delta.txt`): no file under `hdl/`,
  `configs/`, `sw/` or `third_party/` changed, and the six gitlinks are identical. Not applicable beyond confirming
  that. The prior RTL verdict at `ed7df79c` stands by ancestry.
- `[R913] PASS Robustness` — `receipts/delta.txt` and `receipts/txla-registrar-mutant.txt`: no executable path
  changed. The self-test's control result at this head matches `ed7df79c` (`OK (11 checks)`, rc 0), and its
  zero-check guard (`twin_mrp.py:466`) is unchanged. The prior verdict stands.
- `[R913] PASS Tests` — `twin_mrp.py:398-455` and `receipts/txla-registrar-mutant.txt`. No test changed.
  - The README's coverage claim now matches the checks that run. Each case it names has a check that can fail
    for it: R913-1's `txlaf-registrar-kept` mutant was caught at `ed7df79c` by the Registrar-IN pair, and that
    code is unchanged.
  - The one uncovered row, txLA! IN to LV, is no longer claimed (S2 is still open and optional).
- `[R913] PASS Docs` — README `:1404-1410` against `twin_mrp.py:398-455`. The packet `author-r2b` matches its
  `MANIFEST.json` hashes 3 of 3, and its `diff.txt` is byte-identical to `git diff ed7df79c..30796098`
  (`receipts/evidence-packet.txt`).
  - The REVIEW-READY claims are true: README only, no code, test or image change, doc-style OK, `docs_check` 0.
  - My own reruns agree and add em-dash and bare-metal.
  - N-R1 is RESIDUE and N-S1 is a SUGGESTION. Neither leaves the lens unclean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | README.md:1392-1410; twin_mrp.py:76-103, 181-190; issue #991 acceptance 1-2; docs gate receipts | R913-3 | 30796098256670c76115610498a3cdad4d8281ba |
| RTL | CLEAN | delta stat and name-status ed7df79c..30796098; gitlinks at both heads | R913-3 | 30796098256670c76115610498a3cdad4d8281ba |
| Robustness | CLEAN | delta stat; twin_mrp.py:398-466 control run; zero-check guard | R913-3 | 30796098256670c76115610498a3cdad4d8281ba |
| Tests | CLEAN | twin_mrp.py:398-455 checks vs README claim; txLA! Registrar mutant (control and planted) | R913-3 | 30796098256670c76115610498a3cdad4d8281ba |
| Docs | CLEAN (N-R1 RESIDUE, N-S1 and prior S1/S2 SUGGESTION; prior R1/R2 RESIDUE carried) | README.md:1404-1410; twin_mrp.py:399-410 docstring; author-r2b packet vs MANIFEST.json; PR #992 body; docs_check, check_em_dash (pinned), check_baremetal_only, check_doc_style | R913-3 | 30796098256670c76115610498a3cdad4d8281ba |

Each lens is covered at the exact head. Lens scopes untouched by the delta (RTL, Robustness, and Tests' executable
artifacts) also keep their clean coverage from R913-2 and R914-2 at `ed7df79c`. That head is the parent of this
one, and nothing in those scopes has changed since.

## Real limits

- No manager source bank ran at this head, and none is claimed. Source-head execution evidence for unchanged code
  comes from the author's published gate receipts at earlier heads; this delta changes no executable input.
- I ran no `make twin`, `make twin-plants`, firmware, harness, Verilator, Yosys, builder or route at this head. My
  probes were the self-test (control and one planted fault) and the docs gates that read the changed page.
- The em-dash gate ran with the pinned renderer, installed hash-checked from `tools/markdown/requirements.txt`
  into a disposable venv under the packet's unpublished `scratch/`. The shared toolchain was not used.
- `check_doc_style.py` does not cover `tb/verilator/milan_dp/README.md` (not in its DOCUMENTS list), so its OK is
  not evidence for this page. The author's packet cites it, which is true but not specific to the page.
- The `author-r2b` packet is checked against `MANIFEST.json` sha256 values and the git diff. GitHub reports
  `ab1710ee` and `30796098` as unsigned, and I found no detached signature to verify.
- Hosted runs at exact head, read 2026-11-24T05:45:56Z (`receipts/hosted-and-signatures.txt`), are a snapshot,
  not acceptance.
  - Completed success: bdd-conformance, changes, docs-check-no-git, elaborate-gates-2/3, full-ci-gate, Prepare
    pinned Yosys (2), split-cdc, verilator-lint, wire-accountability.
  - Skipped: Physical gPTP (nightly and manual).
  - Still in progress or queued: docs-gates-0..2, the firmware jobs, the Verilator and Yosys shards, and the
    others.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry N-R1, R913-2-R1 and R913-2-R2 to the residue checklist. N-R1 should be fixed in the PR body before merge,
  so the body names this commit and the head its gate rows ran at.
- Own hosted and act acceptance at the exact head, including docs-gates-0..2, which were still running at read
  time.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn and link the
  receipts. Source base `aa30d77f` is the PR's base branch `dev-soft-core` tip. Note that the live `dev` tip is
  `e275d795`; which base the candidate uses is the manager's call.
- Decide whether S2 (txLA! Registrar row coverage) becomes a new Issue.
- Merge only with explicit maintainer authorization.

## Receipts and scripts

All files are listed in `MANIFEST.sha256`.

- `scripts/txla_registrar_mutant.sh`: control and planted txLA! Registrar fault, restored from HEAD on exit.
- `scripts/checkout_integrity.sh`: blob, mode, index, ignored-file and gitlink check after the probes.
- `receipts/`:
  - `delta.txt`, `txla-registrar-mutant.txt`, `docs-check.txt`, `em-dash.txt`, `baremetal-only.txt`,
    `doc-style.txt`, `residue-scan.txt`;
  - `evidence-packet.txt`, `twin-input-identity.txt`, `hosted-and-signatures.txt`;
  - `pr-body-live.md`, `issue-991-body.md`, `review-start-comment.md`;
  - `checkout-integrity.txt`: INTEGRITY OK, 1937 blobs, 0 differing, 0 untracked or ignored entries, six gitlinks
    as recorded.

R913-3 FINISHED
