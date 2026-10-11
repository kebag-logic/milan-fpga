[R609] NEGATIVE - exact head 9975764846e7e63bccf0b68a5188d5cc7f23f890

External independent review, issue #73 / PR #174, round R609-2. Tree `5e0b23b212b2fb4da5735821694ec43e66421d0f`; source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`. All five lenses were applied. One MINOR remains in the export documentation, making Docs UNCLEAN. Conformance, RTL, Robustness and Tests are CLEAN. The earlier public blocking findings are resolved at this head. One separate wording residue does not affect the verdict.

**Scope and reconstruction**

1. No repository or ancestor AGENTS.md or CONTRIBUTING.md was present. Read the supplied command-wrapper instruction, repository README, HDL README and `docs/README.md`: workflow, consumption contract, documentation authorities and the distinction between documentation gates and executable suites.
2. Read the [issue acceptance](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73), [Mark II re-scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6009640063), and [frozen lane scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6100509798). Required: one AECP command table, generated or gated consumers including F06.14 and engine constants, CI enforcement, and accurate generated/hand-written coverage records. ROMs and the elaborated engine must remain unchanged. Parent firmware implementation is expressly deferred; its input format and path must be named.
3. Examined REQ-VER-002/GAP-11; F06.14 and architecture 06 §§6–8; architecture 09 §§1, 7, 8.10; F03.7 hazard classes; architecture 02's transaction/read-face contracts; and the concrete engine, µCPU, status, classifier, scoreboard and notification consumers. Status authority: the project's transcription of IEEE 1722.1-2021 Table 7-141. Copyrighted specification PDFs were not independently re-audited. Also examined [public parent Rule 12](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/development/CODE_QUALITY.md#rule-12-prefer-idiomatic-python) and the [manager addendum](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6105354276).
4. Reviewed the base-to-head diff and all 16 commit subjects: 27 changed files. The independent pass covered the table, generator, every new gate module, bench, campaign driver, build rules, workflow and changed documents before reconciling prior public findings. Retained: `receipts/exact-head.diff`, `history.txt`, `diff-check.*`.
5. Examined the immutable [published evidence](https://github.com/kebag-logic/milan-fpga/tree/02377d3d836eaca55e1fe6d8843dd0a3c6a3ff76/review-evidence/pp73-r1), PR body, public review findings and [round-two requirements](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6104932386). No private author material, management checkout or separate reviewer report files were opened. Public start: [R609-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6107188934).

Acceptance is narrower than F09.1's original ambition. This review does not require a generated golden model, ACMP transition model, timing-table generator or firmware implementation. Explicit limits for echo-command floors, field values/order, GDI ceilings and unswept outcomes are not counted as proof.

**R609-2-F1 — MINOR — Docs — semantic export fields described as prose-only**

- **Where:** `hdl/aecp/ucode/aecp_commands.json:28`; `docs/architecture/09_verification.md:540`; PR #174, field-reference description. Data begins at `aecp_commands.json:426`; readers are `scripts/aecp_gate/rtl.py:134` and `scripts/aecp_gate/record.py:393`.
- **Authority/evidence:** the frozen scope names this JSON as the parent export; round two requires the docs to describe exactly what the gate holds. The reference classifies the whole `documented` collection as “F06.14 prose only: no consumer reads them as machine semantics.” Six rows actually supply otherwise-unserved legal GET_DYNAMIC_INFO members. `scripts/probe_export_fields.py` changes GET_VIDEO_FORMAT's `gdi`, `rtl`, then `opcode`, regenerating F06.14 each time. All three edits produce semantic `decode:` or `engine:` failures, with no F06.14 mismatch. `receipts/export-fields.log` retains the output.
- **Impact:** a consumer following the reference could discard six GDI membership rows as presentation data or treat edits to them as semantically inert. The gate itself correctly protects the fields; no current RTL malfunction is claimed. This is an incorrect machine-field contract in the exported model, not harmless editorial residue.
- **Required outcome:** remove the blanket prose-only classification. Describe `documented[].opcode`, optional `rtl`, and optional `gdi` as semantic inputs for the unimplemented GDI members; distinguish identity/diagnostic fields from `section`/`cells` rendering data. Make 09 §8.10 and the PR field-reference description agree. No production RTL change is needed.
- **Verification:** the reference identifies the existing readers and six rows accurately; `make aecpcmd` passes; the three controls still fail semantically when planted. Do not imply that dropping the whole collection preserves GDI semantics.

**R609-2-R1 — RESIDUE — Docs — stale publication wording**

- **Artifact:** PR #174, Validation introduction: “All results below are local at those commits; the new commits have not been pushed.”
- **Evidence:** the PR API names the exact reviewed commit as its published head (`receipts/pr-wording.txt`).
- **Impact:** publication-status wording only; no measurement, test, code, generated artifact or conformance claim changes.
- **Exact fix:** replace the sentence with “All results below were run locally at those commits.”
- **Verification:** manager residue checklist confirms the replacement. This does not affect the verdict or add an unclean lens.

**Prior public findings at this head**

Read after the independent diff pass: [first internal public findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6104874774), [first external public findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6104929075). Extracts are in `public/prior-public-findings.json`.

| Prior ID | Disposition | Verification owned by this round |
|---|---|---|
| R608-1-F1: decode/dispatch not held | RESOLVED | Fresh engine observations checked against table and record. q1 redirected SET_CLOCK_SOURCE and q2 decode-on-GET fail by command name; clean/restored sweeps pass. MVU sub-decode and GDI record-length controls also fail by name. Docs distinguish observation from generation. |
| R609-1-F1: variable/echo response sizes and command sizes | RESOLVED | All 31 response-cdl and 31 command-cdl +4 controls fail. Unchanged prior size sweep reports 31 held / 0 free for both columns. Unchanged prior ROM probe has no passing reachable mutation. Direct ROM-walk probes detect edits without depending on digest mismatch. GET_AUDIO_MAP cdl 20 and 28 fail; 24 passes. |
| R608-1-F2: generator-read defects tested only in memory | RESOLVED | Real-file MVU-message and unplaced-entry edits fail by name; optimized interpreter still refuses the entry. File-copy/generator-alone cases execute in the 153-plant self-test. |
| R608-1-F4 / R609-1-F2: missing ROM prerequisite | RESOLVED | For pp_top, ucpu and aecp_cmds, a table-only status-code edit makes `make -q ucode.hex` return 1; regeneration changes `518b900c…` to `97151f6a…`. |
| R608-1-F3 / R609-1-F3: doubled plurals | RESOLVED | `resp_text` emits stored plurals unchanged; generated rows are correct; document gate passes. |
| R609-1-S1: status-code authority | RESOLVED | Fixed Table 7-141 map rejects STREAM_IS_RUNNING 12→13; self-test includes that control. |
| R609-1-S2: documented row missing name | RESOLVED | Schema requires `name`; named self-test plant executes. |
| R608-1-S2 / R609-1-S3: assertion removed under optimization | RESOLVED | Explicit raised error tested under `python3 -O`. |
| R608-1-S1 / R609-1-S4: export field reference | PARTLY RESOLVED | Reference added; incorrect `documented` classification remains as R609-2-F1. |
| Manager Rule 12 addendum | RESOLVED for source review | Focused structure checks pass for 12 gate/campaign files. Published author consumer receipt records unchanged parent Python budgets; no manager source bank inferred. |

No prior blocking finding is silently waived. The new field-reference finding is separate from the resolved decode/size defects.

**Execution and evidence**

Only disposable trees below `scratch/` were used. Foreground orchestration waited for every child. Gate/doc checks, µCPU suite and focused decode campaign ran concurrently. Campaign: `--jobs 4`; make: `-j16`; each compiler build bounded to two workers. The scoped compiler reported required 5.050 identity before use. No broad processor, parent, gPTP, synthesis or builder bank was run by this reviewer.

| Check | Result | Receipt |
|---|---|---|
| Command gate/self-test | 31 commands, 84 entries, 41 rows; 153/153 plants caught by name | `receipts/gate-and-docs.log` |
| Focused docs gates | Links, requirement/module matrices and parameters pass | same |
| µCPU | 437 PASS, 0 FAIL | `receipts/ucpu.log` |
| Decode campaign | Clean/restored: 585760 trials, 176/176 checks; four selected mutants detected by name | `receipts/decode-controls/`, `decode-controls.log` |
| Independent contract probes | 62 size drifts, ROM controls, both wrong map bases, four acceptance file drifts, generator refusals and three incremental rules detected | `receipts/contract-probes.log`, `contract-results.json` |
| Unchanged prior probes | No passing size drift or reachable ROM mutation | `receipts/prior-size-sweep.log`, `prior-rom-size-probe.log` |
| Export metadata | Three purported prose-only fields affect semantic verdicts | `receipts/export-fields.log` |
| Source preservation | 46 production SystemVerilog files identical to base; both ROMs identical | `receipts/production-sv-identity.txt`, `rom-identity.json` |
| Final clone integrity | Exact head/tree; 606 tracked blobs, modes/index agree; detached, clean; zero gitlinks | `receipts/final-integrity.json`, `tracked-blobs.json` |

ROM SHA256 at both base and head:

- `ucode.hex`, 26624 bytes: `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`.
- `ltn_rom.hex`, 6138 bytes: `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`.

Published author receipts supply wider source evidence: existing suite records unchanged, new 176 checks increasing 1029620 to 1029796; documentation/lint/42-top portability passing; synthesis/lint records identical; nine existing campaign pairs unchanged; 14 new decode controls detected. These are **author source receipts**, not reviewer reruns or manager source-bank results. Selected raw receipts/comparisons are in `public/author-r2/`.

All 57 fetched author artifacts match immutable Git blob identities and the outer publication manifest's published SHA256 values. Ten `.meta` files have declared path redactions, so their bytes differ from the inner original-file manifest; the outer manifest records and matches the published bytes. Both checks are retained in `receipts/public-*manifest-check.json`. No unexplained evidence-integrity failure remains.

Hosted snapshot, 2026-10-11 08:44:06 UTC: exact-head [run 38125233898](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38125233898) executed and passed docs-gates and portability. Suites were in progress; new decode controls remained pending. Compiler-build step skipped after a cache hit: not an executed build. No whole-run pass or pending-step success is claimed. See `receipts/hosted-jobs.json`. Hosted acceptance remains manager-owned.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance; REQ-VER-002/GAP-11; 31-command table/status authority; F03.7/F06.14; implementation and explicit scope limits | R609-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| RTL | CLEAN | 46 unchanged sources; ROM bytes; µCPU; wrapper/dispatch handshake; clean/restored sweeps; published portability/equality | R609-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Robustness | CLEAN | Real-file refusals; optimized-interpreter guard; malformed-input self-tests; bounded trials; incremental rules; restoration | R609-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Tests | CLEAN | Stimulus independence; recorded/fresh comparison; ROM walk; 153 plants; four compiled controls; 62 size mutations; prior probes; CI wiring | R609-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Docs | UNCLEAN — R609-2-F1 | docs/README; compliance cells; 06 generated/realization tables; 09 §§1/7/8.10; export reference; suite README; module matrix; PR body | R609-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |

**Real limits and pending manager duties**

The decode sweep covers its stated opcode/length/template population, not every possible engine outcome. The ROM walk grades sizes/statuses/lock/notification, not field values/order. Limits include opcodes above 0x007F, unswept outcomes, command sizes with lower accepted floors, and GDI's 524 ceilings. Neither this review nor software receipts demonstrate physical timing/calibration: **physical calibration NOT RUN; field skips are not hardware proof**.

No manager source bank runs at this exact head. Source base: `2cbed0a987c1e68402658d69459ab7e5aa571adc`; live parent dev for merge: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. The manager still owns the final current-dev merge candidate, builder/native banks, hosted/act acceptance and publication of candidate receipts on the PR. Source-head checks do not replace these duties.

Author consumer receipts show unchanged parent Python budgets with documented evidence-reader dispositions, plus the expected moved-pin documentation failure. Parent adoption owes the new `aecp_cmds/mutants.py` evidence-reader disposition, applicable name-evidence disposition, and updated pin docs/diagrams. Required parent gitlinks must be checked on the merge candidate; this standalone processor clone has no submodules. Firmware-table consumption remains a follow-up.

Portable scripts and raw receipts are listed in `MANIFEST.sha256`, using packet-relative paths. `scratch/` is disposable and excluded. The clone was never mutated; final tracked bytes, modes, index and gitlink inventory match the exact published head. No commits, pushes, GitHub writes, merges, shared installs, hardware runs or author contact were performed.

R609-2 FINISHED
