[R879] POSITIVE - exact head dd163e41438acb86e0c4d4e76df90f3f91ace1c0

Round R879-3. Cleared-context internal independent review of kebag-logic/milan-fpga PR #960 (issue #665 S13, the flip).
Head `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`, tree `0e7909a8d02c4123c604c4a168a8b0cbfdd94e7e`. This is a delta
re-review from the round-2 head `9413958c` (4 commits) plus every named prior finding at its cause. Source base
`59b09884` (dev-soft-core). Live dev `e275d795` is the manager's merge-turn candidate and is not validated here.

No BLOCKER, MAJOR or MINOR is open. There is one SUGGESTION (R879-3-S1) and four RESIDUE items (R879-3-R1..R4).
All five lenses were applied and are clean at this head.

## Scope and method

Context was read in this order: AGENTS.md and CONTRIBUTING.md (the lens and severity rules); the PR body; the author's
REVIEW READY (#665 issuecomment-7073088228); the flip plan item 6 (issuecomment-6799253003) and plan item 2 of
issuecomment-6716584453; the bench re-check (issuecomment-7063917242); `git diff 9413958c..dd163e41`; then the
published evidence at `c06e28ade922988b601abf8b6e6945bd5c890790` `review-evidence/s13-r1/author-r3` (with author-r1
and author-r2 for binding). The round-2 reviews (R880-2 issuecomment-7072611287, R879-2 issuecomment-7072822982) were
read only after my own pass over the diff and the packet.

The delta (`git diff --name-only 9413958c dd163e41`) is `syn/resmap/soc_sweep.py` and six docs pages:
`docs/ENDSTATION_BUILDER.md`, `docs/fpga/FPGA_DESIGN.md`, `docs/integration/INTEGRATION_GUIDE.md`,
`docs/reference/FR_NFR.md`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md` and `docs/testing/TESTING.md`. The delta
touches nothing under `hdl/`, `sw/`, `configs/`, `constraints/` or `tb/`, and no submodule gitlink
(`receipts/clone-restore.txt`). So the delta changes no product source.

## Check (1): the retained identity finding (R880-1-F2 = R880-2-F1 = R879-2-F1)

All of this was done from the published author-r3 tree alone (`git archive` of `c06e28ad`).

- **Publication integrity** (`receipts/published-manifest-check.txt`):
  - The outer `review-evidence/s13-r1/MANIFEST.json` has 257 author-r3 entries. 0 are missing or mismatched, 0 were
    altered by publication (original == published for every entry), 0 are path-redacted and 0 files are unlisted.
  - The inner `identity/MANIFEST.sha256` lists 230 files, and `sha256sum -c` passes. With the manifest itself, the
    directory holds 231 files.
- **Unmodified replay** (`receipts/replay-r879-3.txt`): `python3 -I tools/replay.py .` exits 0 with
  `== RESULT: ALL CLAIMS HOLD`. Its output is byte-equal to the published `replay-output.txt`, except for that file's
  own header line and the count of listed files (229 then, 230 now, because the output file was added after the run).
- **Thirteen planted-operand controls** (`receipts/rmutants-r879-3.txt`): the unmodified `tools/rmutants.py` passes
  its grader self-check 4 of 4. The unplanted control holds. The plants are caught 13 of 13, each by its own named
  marker, with the RESULT line reached every time.
- **The five re-encoded operands bind to round 2's content.** This is stronger than a content-hash claim: I
  re-encoded each round-3 operand's decompressed content and reproduced the exact round-2 file hash recorded in the
  round-2 manifest and in `binding.json` `reencoded` (`receipts/reencoded-round2-preimages.txt`):
  - `shipping/1x1/dump/{bench,flip}.cells.xz`: xz preset 9 reproduces `d398ea22`/`21d551bd`. Their content hashes are
    `0f115bae`/`ece5a067`, the same values round 1 published in `author-r1/receipts/identity/1x1/checkpoint-dump-diff.txt:4,7`.
  - `groups/8x8-1if/declaring-outputs/aecp-outputs.head.log.gz`: gzip 9 with mtime 0 reproduces `936a668d`.
  - `groups/{1x1,8x8-1if}/declaring-outputs/aecp-outputs.measured.log.gz`: GNU gzip -6 with the FNAME header
    `aecp-outputs.log` reproduces `3ab0f4e3` (mtime 1795194441) and `19259754` (mtime 1795175527). The header
    reconstruction was first validated on an unchanged operand (`groups/1x1/none/aecp.measured.log.gz`).
  - Every other operand is byte-identical between the round-2 and round-3 inner manifests. Only `README.md`,
    `binding.json`, `replay-output.txt`, three tools and the five operands changed, and seven files were added.
- **Independent comparison, my own code** (`tools/indep_compare.py`, `receipts/indep-compare.txt`, exit 0). It does
  not reuse any packet tool.
  - **1x1/1if:**
    - 86,465 cells. Name, REF_NAME, LOC and BEL are all equal, and every non-INIT property is equal.
    - 22 INIT bits differ, in 8 cells. Each is a ROM bank or the CSR defaults ROM (`milan_datapath/csr/sweep_cnt_reg_rep`,
      the VERSION 2 -> 3 bit).
    - All 95,172 net lines are byte-identical.
  - **8x8/1if:**
    - 109,093 cells, all equal.
    - 15 INIT bits differ, in 14 ROM/CSR-defaults cells, and the 111-RAM block RAM dump agrees (15 bits, 14 RAMs).
    - All 119,085 net lines are identical.
  - **The 13 groups:**
    - Every JSON leaf is equal, with none excluded, so no measured figure differs.
    - The raw logs differ in exactly 8 lines: 2 in `aecp` and 2 in `aecp-held` at each point.
    - Each of those lines is reproduced exactly by substituting the firmware_version encoding alone. On WIRE lines that
      is `322e39362e30` -> `332e39362e30` ("2.96.0" -> "3.96.0"); on PASS lines it is the mailbox word
      `2e320000` -> `2e330000`.
    - Every other line is equal, including `aecp-outputs`.
- **Bitstream, ELF and export spot-check** (`cmp -l`, in this report's commands):
  - 1x1: 103 bitstream bytes differ, 77 in the header and 26 in the payload (22 frame bytes plus the 4-byte CRC write).
  - 8x8: 93 bytes differ, 74 header and 19 payload (15 + 4).
  - Each ELF pair differs in 6 bytes, and each `aem_desc.bin` in 1 byte (offset 0x184, `2` -> `3`).
  - `argv.txt`, `aem_desc.json`, `aem_desc.map` and `alinx_ax7101_mem.init` are equal.
  - The bench hashes in `binding.json` (`c7189218`, `c873a0aa`, `7d903412`, `d67fd049`) match the public bench
    re-check comment.
- **Reviewer plants** (`tools/own_plants.py`, `receipts/own-plants-r879-3.txt`): 6 of 6 caught, each by name with the
  RESULT line reached.
  - A WIRE payload byte `0x02` adjacent to the version string changed to `0x03`, and the mailbox word adjacent to the
    version's changed `0x02000000` -> `0x03000000`. Both are reported as NOT ANCHORED, so the anchoring is tight.
  - An operand removed with the manifests left as they were, and one removed with the manifests resealed. Both are
    refused by name, with no traceback.
  - An 8x8 route line dropped.
  - A `binding.json` published prefix altered.

**Conclusion.** Every difference between the bench images and the flip images is one of these: the VERSION word, the
ENTITY firmware_version string, the integrity words computed over them (the descriptor CRC lui/addi pair, AEM SHA-256,
bitstream payload SHA, manifest ELF hash, bitstream CRC write), or named header metadata (the `.bit` design-name
SW_CRC and SW_HDR_SHA256 text, date and time; the `csr.csv` generation timestamp). The bench evidence therefore carries
by identity, and the full CPU-budget re-measure is not required. **R880-2-F1 = R879-2-F1 (= R880-1-F2) is RESOLVED.**

## Checks (2) to (4): the other prior findings and the delta

| Prior finding | Status at dd163e41 | Evidence |
|---|---|---|
| R880-2-F1 = R879-2-F1 (R880-1-F2), MAJOR/MINOR | **RESOLVED** | Check (1) above |
| R880-2-F2, MINOR (PR checkout fetched a non-existent branch) | **RESOLVED** | The PR body reads `git fetch origin dd163e41438acb86e0c4d4e76df90f3f91ace1c0 && git checkout --detach FETCH_HEAD` and then `test "$(git rev-parse HEAD)" = dd163e41...`. In a fresh bare repo the exact-SHA fetch from the public remote gives FETCH_HEAD `dd163e41`, tree `0e7909a8` (`receipts/pr-checkout-check.txt`) |
| R880-2-S1 / R879-2-S3 (rmutants counted any failure; replay crashed on an absent operand) | **IMPLEMENTED** | `rmutants.py:25-28`: CAUGHT needs rc != 0, the RESULT line, and a FAIL line holding the plant's marker. `:151-159`: the unplanted control must hold before any plant is graded. Grader self-check 4 of 4. Absent-operand plants (resealed and unresealed) are refused by name (check (1)) |
| R879-2-S1 (sweep self-test did not exercise prepare/export) | **IMPLEMENTED**, residual gap in R879-3-S1 | `soc_sweep.py:253-305`, `:371`. My mutants B, C, D and F are caught. A and E survive (see S1) |
| R879-2-S2 (raw-log 2->3 anywhere) | **IMPLEMENTED** | Adjacent-byte and adjacent-word plants are caught as NOT ANCHORED. The author's control-log plant is caught |
| R879-2-S4 (`env ={`) | **APPLIED** | `soc_sweep.py:135` reads `env = {` |
| R879-2-S5 (duplicated bench-gate pointer) | **APPLIED** | `MILAN_COMPLIANCE_MATRIX.md:4` no longer repeats the pointer. `:7` keeps it |
| R879-2-R1, R880-2-R1 (stale shipping labels) | **APPLIED** | `ENDSTATION_BUILDER.md:3-4` uses the exact wording. `INTEGRATION_GUIDE.md:3-4` gives the same content in two sentences (style rule). `FR_NFR.md:109` is applied. For the three `KL_maap` lines (`FR_NFR.md:173`, `FPGA_DESIGN.md:313`, `TESTING.md:731`), R880-2-R1's "all-fabric allocator" was taken, with the status column untouched. That wording is correct: `milan_datapath.sv:383-387` builds `KL_maap` only at placement 0. Remaining labels outside these lines are R879-3-R1/R2 |
| R1 as taken (R880-1-R1, R879-R1) | **Stands** | Untouched by the delta |
| R880-1-F1, -F3, -F4; R879-F1, -F2; R879-S1 | **Stand as resolved** | The delta does not touch what they depend on |

**The soc_sweep wiring arm.** `wiring_problems()` patches `subprocess.run` with a builder stand-in and patches
`git_listable` out. It then checks four things:

- `prepare(all-fabric)` returns an argv ending in `--entity-gen-dir`, and asks the builder for `--placement all-fabric`.
- `prepare(split)` refuses, naming the absent image.
- `command_export` asks `prepare()` for the plan's placement, and nothing is written under `soc/` first.
- A refusal of the plan is reported as a named finding (`873a5dc2`).

The head self-test passes. The stand-ins are typed and documented, and `check_py_idiom.py` passes at the head.

**The comment rule.** The delta's added source docstrings cite only `#665`. No lane label, round, reviewer ID or
issue-comment ID appears. `(#665 S13)` at `MILAN_COMPLIANCE_MATRIX.md:4` is pre-existing prose, not a source comment.

## Findings

### R879-3-S1 | SUGGESTION | Tests, Robustness | `syn/resmap/soc_sweep.py:253-305` - the wiring arm cannot tell a hard-coded placement from the plan's, and never accepts a present image through `prepare()`

Evidence: `tools/sweep_mutants.py`, `receipts/sweep-mutants-r879-3.txt`. The control passes and 4 of 7 mutants are
caught. These three survive:

- **A:** `command_export` calls `prepare(work, "all-fabric")` instead of `prepare(work, plan_placement(plan))` (`:134`).
- **E:** `prepare` checks images against the builder output (`out`) instead of the export tree (`:118`).
- **G:** `prepare` skips `git_listable`. This one is stubbed by design, and I make no claim about it.

Impact:

- A is behaviour-equivalent within the configurations the self-test admits, because `:350` already fails the
  self-test unless the plan names all-fabric. So the docstring's "command_export asks prepare() for the plan's
  placement" (`:257`) is only partly distinguished.
- E fails closed: a split plan with a present image would be refused spuriously, never silently priced.
- No run-time defect is present in the code.

Optional outcome:

- Call `command_export` with a copy of the plan whose `soc.placement` names a value other than the recorded one, and
  assert that `prepare()` is asked for that value.
- Add a present-image case: create `work/builder-out/c/x.elf` before `prepare(work, "split")`, and expect an argv rather
  than a refusal.

Verification: mutants A and E fail the self-test, and the control still passes.

### R879-3-R1 | RESIDUE | Docs | `docs/reference/FR_NFR.md:582` - the plane-partitioning row still says the control plane's product owner is "current shipping fabric"

Since this PR the AX7101 builds ship the split. The row is in the descriptive section 4.2 table, not a requirement
row, and changes no status or clause.

Exact fix: replace "one owner per function; current shipping fabric until the firmware qualifies, then Mark II
firmware only (NFR-SCOUT-02)" with "one owner per function; firmware in the split the AX7101 builds ship since #665,
fabric in the all-fabric placement until the full qualification, then Mark II firmware only (NFR-SCOUT-02)".

The manager may route the "switch-over/qualification" phrasing together with the author's open item 1.

### R879-3-R2 | RESIDUE | Docs | `docs/design/AREA_BUDGET.md:537`, `docs/design/MARK_II_AREA_PLAN.md:1900` - "all-fabric shipping" reference labels

Exact fixes:

- `AREA_BUDGET.md:537`: "Retain all-fabric shipping and standalone 1x1/8x8 references independently." becomes "Retain
  the all-fabric and standalone 1x1/8x8 references independently."
- `MARK_II_AREA_PLAN.md:1900`: "Retain the all-fabric shipping endpoint and standalone 1x1/8x8 references." becomes
  "Retain the all-fabric endpoint and standalone 1x1/8x8 references."

The line above, `AREA_BUDGET.md:528`, already says "all-fabric was then the shipping default".

### R879-3-R3 | RESIDUE | Docs | `docs/design/MAILBOX_SPLIT.md:2256`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:214` - "until the flip" becomes false once this PR merges

The PR does not drop the four unread face fields (`sw/mailbox/mailbox.yaml` is unchanged in `59b09884..dd163e41`).
Plan item 2 of issuecomment-6716584453 only defers that drop to the flip; it does not require it in S13. The PR also
does not remove the `f0-f4` recipe.

Exact fixes:

- `MAILBOX_SPLIT.md:2256`: "They stay on the face as firmware-written state until the flip (issuecomment-6716584453,
  item 2)" becomes "They stay on the face as firmware-written state; dropping them is a contract change left past the
  flip (issuecomment-6716584453, item 2)".
- `PP_SHADOW_BASELINE_RECIPE.md:214`: "is kept only until the flip removes it; it is not run." becomes "is kept for
  reference; it is not run."

Manager duty: open a follow-up Issue if the four-field drop is still wanted.

### R879-3-R4 | RESIDUE | Docs | PR #960 body, "Known limitations", third bullet - the identity summary understates what differs

The bullet says the operands "differ only in the firmware string and its CRC". The replay and this review show more:
the VERSION word, the firmware string, the integrity words computed over them, and named build metadata. The PR's own
"How to validate" paragraph already says this correctly.

Exact fix: "a replay showing they differ only in the VERSION word, the firmware string, the integrity words computed
over them and named build metadata (the bitstream header's design-name digests, date and time; the export timestamp)".

## Docs gates at the head

`tools/docs_gates.sh` ran 22 docs-workflow commands concurrently (`receipts/docs-gates-r879-3.txt`). 18 passed
directly:

- `docs_check.py`: 0 findings.
- `check_feature_status.py` and its self-test.
- `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py`, `check_hygiene.py --check`.
- `docs_inventory.py --check`: the audit is fresh.
- `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_todo_ownership.py`.
- The naming, test-evidence and fail-fast ratchets.
- `check_sweep_shape.py --self-test`, `soc_sweep.py --selftest`, `check_submodule_docs.py`, `gen_module_matrix.py --check`.

The 4 rows that need the pinned renderer were rerun in a private venv, installed `--require-hashes` from
`tools/markdown/requirements.txt` plus wavedrom 2.0.3.post3 by its `ci/constraints-ci.txt` hash. All pass:

- `check_em_dash.py --base 59b09884`: 0 findings over 180 added lines.
- `gen_toc.py --check` and `--verify-anchors`: 755 links.
- `gen_register_reference.py --check`: fresh.

`act_ci.py --selftest` and the CI-orchestration rows were not run (not allowed here).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #665 flip plan item 6 (issuecomment-6799253003) against the identity carry. Published packet `c06e28ad` `author-r3/receipts/identity` (`receipts/replay-r879-3.txt`, `indep-compare.txt`, `reencoded-round2-preimages.txt`). Bench hashes against issuecomment-7063917242. PR body recipe (`pr-checkout-check.txt`) | R879-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| RTL | CLEAN | `git diff 9413958c..dd163e41 -- hdl sw configs constraints tb` is empty. Routed cells, placements and nets are equal at both shapes, and the INIT bits are ROM/CSR-defaults only (`indep-compare.txt`). `hdl/milan/milan_datapath.sv:383-387` (KL_maap is all-fabric only). Gitlinks are unchanged (`clone-restore.txt`). Prior RTL verdicts stand for untouched RTL | R879-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Robustness | CLEAN (S1 optional) | `syn/resmap/soc_sweep.py:105-122,132-135,253-305` (`sweep-mutants-r879-3.txt`). Replay absent-operand refusal and anchoring (`own-plants-r879-3.txt`) | R879-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Tests | CLEAN (S1 optional) | `identity/tools/rmutants.py` 13 of 13 by marker, grader 4 of 4 (`rmutants-r879-3.txt`). Reviewer plants 6 of 6. `soc_sweep.py --selftest` PASS. Sweep mutants 4 of 7, survivors analysed in S1 | R879-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Docs | CLEAN (R1-R4 residue) | The 6 delta pages at their changed lines. `FR_NFR.md:109,173,582`. `AREA_BUDGET.md:537`. `MARK_II_AREA_PLAN.md:1900`. `MAILBOX_SPLIT.md:2256`. `PP_SHADOW_BASELINE_RECIPE.md:214`. PR body. Docs gates (`docs-gates-r879-3.txt`) | R879-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |

## Real limits

- No hardware was used. Physical calibration is NOT RUN, and field skips are not hardware proof. The 1x1/1if bench
  re-check's open DUT blocker (#954, GET_TX_STATE REGISTERING_FAILED) is outside this PR, as decided, and is the next
  PR.
- The routed checkpoints themselves are not published (their hashes are in `binding.json`). Cell, net and RAM identity
  is judged on the published dumps the author's `dump.tcl`/`bramdump.tcl` wrote. I do not derive the algorithm behind
  the vendor's SW_CRC/SW_HDR_SHA256 header text.
- The harness-image rebuild identity at `dd163e41` and the flip-image input carries (19/16 files) are the author's
  receipts. I did not rebuild them.
- The builder suite, the suites sweep, the flip check and the timing floor are carried from the author's earlier
  receipts. The round-3 delta touches none of their scope (`receipts/carry-scope-62477be4-dd163e41.txt` lists the
  wider 62477be4..dd163e41 change set reviewed in earlier rounds). I did not rerun them.
- The publication check reproduces the archive rule as stated. If the archive applies other rules, the check should be
  rerun on its output (the author's open item 3).
- Hosted evidence at the exact head was incomplete when I inspected it: 33 success, 1 skipped, and 25 queued or in
  progress (rtl-fast, Verilator and Yosys shards among them). No hosted acceptance is claimed.

## Pending manager and owner duties

- The manager validates the current-dev merge candidate (builder and native banks) at the merge turn, against live dev
  `e275d795`, and owns hosted and local-replica acceptance. No manager source bank was run or inferred at this head.
- The manager carries R879-3-R1..R4 to the residue checklist, and opens a follow-up Issue for the four unread face
  fields if their drop is still wanted (R3).
- Open items 1 and 2 remain: NFR-SCOUT-02's "switch-over" wording is for the owner, and the register-map re-record
  from a split export needs an Issue.
- The merge needs explicit maintainer authorization.

## Packet

This report is `REPORT.md`. Receipts are under `receipts/` and the reviewer's scripts under `tools/`, all listed in
`MANIFEST.sha256`.

- `tools/indep_compare.py`, `tools/reencode_probe.py`, `tools/gz_header_search.py`, `tools/own_plants.py`: each takes
  `<identity-dir>` (and a work dir).
- `tools/sweep_mutants.py <repo>`.
- `tools/docs_gates.sh <repo> <logdir>`.

The review clone was restored after the probes: HEAD `dd163e41`, the index write-tree is `0e7909a8`, 0 index or
worktree differences, no untracked or ignored residue, and the gitlinks are as at the head (`receipts/clone-restore.txt`).

R879-3 FINISHED
