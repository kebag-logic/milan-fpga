[R439] POSITIVE - exact head 420b778a52e4f4bcc8040c13bbc4bef9bc94ada0

# R439-2 - external independent review of PR #636 (issue #635), round 2

- **Head under review:** `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0`, tree `845371799bcdb235cfe12ad4db2aeaf5fcafb61d`. It is five one-line commits over the round-1 head `3370c6cbd5e4b096167c19ca709556a40207e538`. Source base and live `dev`: `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- **Verdict: POSITIVE.**
  - Every round-1 finding of this reviewer is closed at this head: F1 (MINOR), F2 to F4 (RESIDUE) and S1 (SUGGESTION).
  - There is no new BLOCKER, MAJOR or MINOR. There is one new RESIDUE (N1, PR-body wording).
  - All five lenses are covered clean at this head.
- **Scope reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - The #635 body (frozen acceptance 1 to 5).
  - The #635 comments: assignment 5958619779, TAKEN 5958652460 and REVIEW READY 5962152491; round-2 assignment 5962734738, TAKEN 5962752104 and REVIEW READY 5963295768.
  - The PR body, including its Round 2 section.
  - The author's round-2 packet at archive `37ccf808`: `review-evidence/635-r1/author-r2/HANDOFF.md` (blob `65f615e1`) and `PR-BODY.md` (blob `942c508c`). `PR-BODY.md` is byte-equal to the live PR body except for a final newline.
  - `git diff cdf49d1a..420b778a` and `git diff 3370c6cb..420b778a`.
  - Processor sources at `b2db3a97` and `631eeb34`, and processor PR #140's public body.
- **Delta scope** (`receipts/delta_scope.txt`):
  - Exactly four files change between `3370c6cb` and `420b778a`: `CHANGELOG.md` (+5/-1), `docs/reference/REGISTER_MAP.md` (1 line), `docs/reference/SUBMODULES.md` (+3/-2) and `hdl/milan/KL_pp_shadow.sv` (1 comment line).
  - No gitlink moves; `protocol-processor` stays at `631eeb34`.
  - Each commit message is one line with no trailer.

## Round-1 findings, judged at this head under their original severity

| Round-1 finding | Severity | Status at `420b778a` | Evidence |
|---|---|---|---|
| F1: C5a's NOT_IMPLEMENTED echo for a non-AEM command whose response memory fails is not recorded | MINOR (Docs, Conformance) | **CLOSED** | `CHANGELOG.md:47-49` and `docs/reference/SUBMODULES.md:115`, checked against the processor below (claim 1) |
| F2: deadline-answer summary broader than the behaviour | RESIDUE (Docs) | **CLOSED** | `CHANGELOG.md:44-45` carry the exact fix's words as two bullets. The style gate caps a sentence at 10 words, which forces the split; `check_doc_style.py` passes at this head. See claim 2 below |
| F3: bare `#80` in `KL_pp_shadow.sv:1099` | RESIDUE (Docs, RTL) | **CLOSED** | `hdl/milan/KL_pp_shadow.sv:1099` now reads exactly the proposed text. The change is comment-only: the preprocessed, comment-stripped module is byte-identical before and after (`receipts/shadow_preprocessed.sha256`) |
| F4: scoreboard kill tie-offs paired with the hazard row | RESIDUE (Docs) | **CLOSED** | `docs/reference/SUBMODULES.md:114` and `:116` carry the two exact cells |
| S1: `ADP_IDX0[15:0]` description predates C3's fallback | SUGGESTION (Docs) | **TAKEN, correct** | `docs/reference/REGISTER_MAP.md:1016`. The added "and again after a D3 roll-back" was checked (claim 3 below) |

## Claim checks against the processor

### Claim 1 (F1)

**The claim:** a non-AEM command whose response memory fails answers NOT_IMPLEMENTED with the command echoed. GET_MILAN_INFO is such a command, and at `b2db3a97` it answered ENTITY_MISBEHAVING. PR #140 cites Milan v1.2 Section 5.4.3.3, Table 5.19.

**Result: true** (`receipts/claim_sources.txt`).

- **At `b2db3a97`:** in `KL_aecp_engine.sv:3549-3585`, both fail arms (A_ALLOC and A_WR) set `ST_ENTITY_MISBEHAVING_C` for every message type.
- **At `631eeb34`:**
  - `KL_aecp_engine.sv:1751-1753` defines `st_echo_w` as "not (AEM bucket and message_type 0)".
  - Under it, `:3771-3776` and `:3801-3806` override the status to `ST_NOT_IMPLEMENTED_C`, set `echo_r`, and size the frame to the echo.
- **Provenance:** both commits (`9f0299a`, `a2d2a24`) enter `main` through merge `03c842a`, which is PR #140. PR #140's public body cites "Milan v1.2 §5.4.3.3 Table 5.19".
- **Executed:** at `631eeb34`, `tb/pp_top --deadline-only` gives 64 checks and 0 failures (`receipts/pp_focused/deadline_only.log`). Its DL8 section grades GET_MILAN_INFO under four faults: a read error, a write error, a tied-off memory, and a command padded to 540 bytes.
- **Mutant m1:**
  - It gates off both `st_echo_w` fail branches, which rebuilds the `b2db3a97` arm.
  - It fails all four DL8 checks with "status 10, 60 bytes", which is ENTITY_MISBEHAVING (`receipts/pp_mutants/m1_fail_aem_status.*`).
  - So the old-pin answer the changelog names is the one the processor gave, and the bench detects its return.

### Claim 2 (F2)

**The claim:** past the deadline, the answer is ENTITY_MISBEHAVING unless a refusal was already chosen. A command that had already changed state answers for itself.

**Result: true.**

- `KL_aecp_engine.sv:1722-1738` at `631eeb34` says E_DLKILL "answers the best current status through E_FAILSAFE (a SUCCESS not yet built becomes ENTITY_MISBEHAVING), unless the program has already produced an effect: then it ends with its own answer".
- This matches processor `docs/guides/operator.md:56`.
- The DL section that grades this behaviour passed (claim 1 above).

### Claim 3 (S1 and the added clause)

**The claim:** `ADP_IDX0[15:0]` is the index the ADPDU carries until a SET_CONFIGURATION or a D3 restore writes the configuration row. It is carried again after a D3 roll-back.

**Result: true.**

- **The fallback:** `protocol_processor_top.sv:1862` selects `adp_cur_cfg_w = aecp_cur_cfg_v_w ? aecp_cur_config_o : current_cfg_i`.
- **The valid flag** (`KL_aecp_engine.sv:1610` and `:1918-1926`):
  - A write of the configuration row sets it. That write is the µCPU's SET_CONFIGURATION or the D3 writer's restore of record 0x00.
  - `store_rst_n_w = rst_n && !d3_rb_rst_w` clears it, so a D3 roll-back clears it.
- **The parent binding:** the parent drives `current_cfg_i` from `ADP_IDX0[15:0]` (`milan_csr.sv:2831`, `milan_datapath.sv:7611`).
- **Executed:** `tb/pp_top --adp-only` gives 55 checks and 0 failures. Its AD6 is the roll-back arm: configuration 0 is applied, pass 1 rolls it back, and the first ENTITY_AVAILABLE carries `current_cfg_i`.
- **Mutant m2:**
  - It resets the flag on `rst_n` only, so the roll-back no longer clears it.
  - It fails AD6 twice, including "first ENTITY_AVAILABLE carries the image default 1 ... got 0" (`receipts/pp_mutants/m2_rb_keeps_cfg.*`).
  - So the roll-back clause is both true and graded.

### The F3 qualifier

The processor places this ruling on its own issue #80:

- `docs/architecture/01_overview.md:187` reads "manager ruling, processor #80".
- `docs/guides/hdl-engineer.md:64` reads "the ruling on issue #80".

The qualified comment names that issue correctly.

## Findings

### N1 - RESIDUE - Docs - PR #636 body, "Status" section - the Status line still names the round-1 head

- **Evidence:** the PR body's `## Status` line reads "GREEN locally -- ... head `3370c6cbd5e4b096167c19ca709556a40207e538`". The current head and its gates appear only under `## Round 2`.
- **Impact:** this is wording only.
  - The figures are true for the head they name.
  - No measurement, verdict, test, code or clause claim changes.
  - A cold reader who stops at Status may take the old head for the current one.
- **Exact fix:**
  - Start the Status line with "Round 1 (head `3370c6cb`):".
  - Add one line: "Current head `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0`: see [Round 2](#round-2) for its gates."
- **Verification:** read the PR body after the edit.

There is no other finding. The CHANGELOG line "GET_MILAN_INFO is one; at `b2db3a97` it answered ENTITY_MISBEHAVING." is accurate as written.

## Executed evidence (this round)

| Receipt | Command | Result |
|---|---|---|
| `receipts/doc_gates/*` (`scripts/doc_gates.sh`) | `docs_check.py`; `check_doc_style.py` and its `--selftest`; `check_submodule_docs.py` and its `--selftest`; `submodule_boundaries.gen.py --check`; `check_doc_paths.py`; `check_hygiene.py`; `check_sv_idiom.py`; `check_port_contracts.py`; `check_feature_status.py --self-test`; `DOC_MAP.gen.py --check` | all rc 0 |
| `receipts/doc_gates/em_dash*.log` | `check_em_dash.py --base cdf49d1a` and `--base 3370c6cb`. The pinned renderer was installed `--require-hashes` into a private scratch environment | rc 0. 0 findings over 69 added lines (base `cdf49d1a`) and over 9 (base `3370c6cb`); arms 339/339 |
| `receipts/behave.log` | `behave --no-capture -f plain` in `tests/`; the suite reads `REGISTER_MAP.md` | rc 0; 404 scenarios, 1968 steps |
| `receipts/pp_focused/*` (`scripts/pp_focused.sh`) | processor `tb/pp_top` `gsi-build` at `631eeb34`, in a scratch export, with Verilator 5.050; then `--adp-only` and `--deadline-only` | rc 0; AD 55/0, DL 64/0 |
| `receipts/pp_mutants/*` (`scripts/pp_mutants.sh`) | m1 (2 edits) and m2 (1 edit), each in its own scratch export | each rc 1, as required. m1: 4 DL8 failures. m2: 2 AD6 failures |
| `receipts/shadow_preprocessed.sha256` | `verilator -E -P` on `KL_pp_shadow.sv` at `3370c6cb` and at `420b778a` | both sha256 `5a2f3988...0c02` (identical) |
| `receipts/claim_sources.txt` (`scripts/claim_sources.sh`) | processor source lines at both pins, PR #140 ancestry, parent binding | as cited above |
| `receipts/delta_scope.txt` | log, name-status, gitlink diff and full delta for `3370c6cb..420b778a` | 4 files, no gitlink change |
| `receipts/hosted_check_runs.tsv` | check runs on the head at 2026-10-03T00:06:20Z | 13 success. `Physical gPTP` is skipped: a nightly/manual context, not executed. Still in progress at the snapshot: `docs-check`, `elaborate`, Verilator shards 0, 1, 2 and 4. The manager owns hosted acceptance |
| `receipts/restore_verify.txt` | head, tree, index tree, porcelain status, submodule gitlinks and checkouts, after all probes | exact head and tree; index tree `84537179`; clean; gitlinks `631eeb34`, `5dce647a`, `efeb541a`, `48ff7a7e` |

- **Verilator identity:** `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` reports "Verilator 5.050 2026-07-01 rev v5.050".
- **Isolation:** all probes ran in disposable exports under `scratch/`. The review clone was never modified.

## Lens coverage

[R439] PASS Conformance - `CHANGELOG.md:43-49`, `docs/reference/SUBMODULES.md:114-116`, `docs/reference/REGISTER_MAP.md:1016` at `420b778a` - each claim was checked against:
- processor `KL_aecp_engine.sv` at `b2db3a97` and at `631eeb34`;
- `protocol_processor_top.sv:1852-1862`;
- PR #140's citation of Milan v1.2 5.4.3.3, Table 5.19.

Each claim was also executed through DL8 and AD6 and their mutants. Acceptance 5 is now met for the C5a response-memory arm. The delta does not touch acceptance 1 to 4: no gitlink, record or generated file changes.

[R439] PASS RTL - `hdl/milan/KL_pp_shadow.sv:1098-1100` at `420b778a` - the only HDL change is inside a `//!` comment.
- The preprocessed module is byte-identical to `3370c6cb`.
- `check_sv_idiom.py` and `check_port_contracts.py` pass.
- The line is 98 columns; the hygiene limit is 100.
- The processor RTL behind the documented claims was read at the pin: the fail arms, `st_echo_w`, `store_rst_n_w` and `dyn_cfg_v_r`.

[R439] PASS Robustness - the processor fault and reset paths that the delta documents, all executed at `631eeb34`:
- response-memory read error, write error, tied-off memory, and oversize echo (DL8);
- the D3 pass-1 roll-back (AD6);
- the parent reset value `ADP_IDX0` = 0 (`milan_csr.sv:2831`).

Each documented behaviour is shown to be the processor's actual behaviour, not an assumption.

[R439] PASS Tests - `receipts/pp_focused`, `receipts/pp_mutants`, `receipts/behave.log` - the delta adds no test, and none is owed, because it is docs plus one comment.
- The processor checks behind the new prose fail on the defect they claim to detect: m1 against DL8, and m2 against AD6.
- The parent's specification suite, which reads `REGISTER_MAP.md`, stays green.

[R439] PASS Docs - `CHANGELOG.md:39-58`, `docs/reference/SUBMODULES.md:109-121`, `docs/reference/REGISTER_MAP.md:1016`, the PR body's Round 2 section, author packet `37ccf808`.
- The texts answering round-1 F1 to F4 and S1 are present.
- The docs and style gates are green.
- The only defect is N1. It is RESIDUE, so it does not leave the lens unclean.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CHANGELOG.md:43-49`; `SUBMODULES.md:114-116`; `REGISTER_MAP.md:1016`; processor `KL_aecp_engine.sv` at both pins; `protocol_processor_top.sv:1852-1862`; PR #140 body; DL8 and AD6 runs | R439-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| RTL | CLEAN | `KL_pp_shadow.sv:1098-1100` (comment-only, preprocessed equality); processor fail arms and roll-back reset at `631eeb34`; `check_sv_idiom.py`, `check_port_contracts.py`, `check_hygiene.py` | R439-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Robustness | CLEAN | DL8 fault arms; AD6 roll-back; `ADP_IDX0` reset value; mutants m1 and m2 | R439-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Tests | CLEAN | `tb/pp_top` AD (55/0) and DL (64/0) at `631eeb34`; m1 and m2 detected; `behave` 404 scenarios | R439-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Docs | CLEAN (N1 RESIDUE carried) | `CHANGELOG.md`; `SUBMODULES.md`; `REGISTER_MAP.md`; PR body; author packet `37ccf808`; the docs, style, em-dash, submodule, path and hygiene gates | R439-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |

This head is the merge candidate's source head. Every lens was re-applied at it, so no coverage rests on an ancestor.

## Concurrent public findings

This section was written after the verdict and ledger above. Only then was the other reviewer's round-1 report (R438-1, PR #636 comment 5962667464) read.

- **R438-1 F1 (MINOR; Docs, Conformance): resolved at this head.** It is the same defect as this reviewer's round-1 F1.
  - Its required outcome is now met: the `631eeb34` CHANGELOG section and the SUBMODULES parent-observable table both carry the response-memory arm, GET_MILAN_INFO, and the `b2db3a97` answer. The optional REGISTER_MAP pointer was not taken.
  - Its verification gates are rc 0 at this head (`receipts/doc_gates`).
  - The text agrees with processor `operator.md:55` and `:326` at `631eeb34`.
- **R438-1 S1 (SUGGESTION; RTL, Docs): resolved at this head.** The bare `#80` now reads "protocol-processor #80" (this reviewer's round-1 F3 text, not R438-1's "processor issue 80"). Both forms remove the ambiguity, and S1 was optional.
- **Other review state:** the PR carries no other review, inline review comment or reviewer finding. Nothing else is owed resolution.

## Real limits

- **Not run this round:**
  - the builder (48), native (5) and candidate banks;
  - act;
  - the full parent, processor, gPTP and Yosys banks;
  - any hardware.
- **No physical proof:** physical calibration is NOT RUN, and the field skips are not hardware proof.
- **Processor bench coverage:** only the AD and DL sections of `tb/pp_top` ran, plus two disposable mutants. Other processor sections were not re-run.
- **Hosted snapshot:** it is a point in time.
  - `docs-check`, `elaborate` and four Verilator shards were still in progress.
  - `Physical gPTP` is a skipped context, not an executed job.
- **Unpublished logs:** the three Verilator build logs carry host toolchain paths, so they are kept out of the published set. Each build's result is published as its `.rc` file and its run log.
- **Em-dash gate:** it needed the pinned Markdown renderer. That was installed `--require-hashes` into a private scratch environment, not as a shared install.

## Pending manager duties

- At the merge turn, run the builder, native and current-dev candidate banks and the act replica. The source base and live `dev` are both `cdf49d1a`.
- Hosted acceptance, including the contexts still in progress at this snapshot.
- Carry N1 (RESIDUE) to the residue checklist, with its exact fix.
- The second positive review and the merge authorization remain the maintainer's.

R439-2 FINISHED
