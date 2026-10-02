[A503]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Round 2](#round-2)** -- The answers to R438-1 and R439-1, the new head and its gates.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally -- `635-pp-pin-631eeb34` -> `dev`, head `3370c6cbd5e4b096167c19ca709556a40207e538`, twelve commits over dev `cdf49d1a` (still the live `dev` tip at validation).

- The 16 consumer commands: 16 of 16 rc 0 (`pp_shadow` 606/606/646/311 checks; `nvm_cosim` 315 of 315; `milan_dp` 9 RESULT PASS with 6/6 and 6/6 mutant arms; `milan_dp_render` 65 + 152, leg defects 5/5; `test_builder.py` whole, ALL GATES PASS EXCEPT 1 NOT RUN, the board calibration gate).
- `scripts/run_all_suites.sh`: 57 of 57 suites, 2,147,149 checks, 0 failures (4 declared `tsn_fuzz` skips without the tsn-gen oracle). `syn/yosys/run.sh`: 54 of 54 tops.
- The nightly physical gPTP suite (`run_all_suites.sh --physical-gptp`, `VERILATOR_JOBS=4`): 179 checks, 0 failures, 3,983 s (the hosted nightly on dev `cdf49d1a` timed out at 5,400 s with 139 physical checks passing; that predates this branch).
- Every `docs.yml` step and job under GNU Make 4.3, and every `rtl-fast.yml` step: rc 0.
- Not run here: `elaborate.yml` (no LiteX on this host) and the act replica (no PR yet). Hosted contexts follow the push.

## Round 2

Executor `[A509]`, per the round-2 assignment on #635 (comment 5962734738). It answers R438-1 (PR #636 comment 5962667464) and R439-1 (comment 5962728186). Both were NEGATIVE on the same documentation MINOR.

- Head `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0`: five one-line commits over `3370c6cb`, nothing amended.
- The changes are documentation plus one RTL comment line.
- The `protocol-processor` gitlink stays `631eeb34`. No port, parameter, generated file, SoC, CSR, VERSION or firmware changes.

| Commit | Item | Finding | Change |
|---|---|---|---|
| `ce948861` | 1 | R438-1 F1 = R439-1 F1 (MINOR; Docs, Conformance) | `CHANGELOG.md:47-49` and a new C5a row at `docs/reference/SUBMODULES.md:115`. A non-AEM command whose response memory fails answers NOT_IMPLEMENTED with the command echoed. GET_MILAN_INFO is one, and at `b2db3a97` the same fault answered ENTITY_MISBEHAVING. Both records cite processor PR #140 and Milan Table 5.19; the SUBMODULES row also cites Milan v1.2 Section 5.4.3.3 |
| `e19f1484` | 2 | R439-1 F2 (RESIDUE) | `CHANGELOG.md:44-45`: the reviewers' deadline-answer text |
| `987720eb` | 2, 3 | R439-1 F3 = R438-1 S1 | `hdl/milan/KL_pp_shadow.sv:1099`: "manager ruling on protocol-processor #80" (R439-1's text). Comment only; the byte diff is that one line |
| `b8ab4f81` | 2 | R439-1 F4 (RESIDUE) | `docs/reference/SUBMODULES.md:114` and `:116`, the reviewers' two cells. The three scoreboard kill tie-offs now sit on the deadline row, and the hazard row reads "No top port or parameter" |
| `420b778a` | 4 | R439-1 S1 | `docs/reference/REGISTER_MAP.md:1016`: `ADP_IDX0[15:0]` is the index the ADPDU carries while the processor's configuration row is unset (from processor pin `631eeb34`) |

**Two places where the wording differs from the reviewers' exact text:**

- F2. `scripts/check_doc_style.py` holds `CHANGELOG.md` to 10 words per sentence. The reviewers' text is one sentence that the gate counts as 20 words, and the gate rejects it ("sentence has 20 words; maximum is 10"). So its two clauses became two bullets, with the words unchanged: "Its answer is ENTITY_MISBEHAVING unless a refusal was already chosen." and "A command that had already changed state answers for itself."
- R439-1 S1, whose text was offered as optional. The row adds ", and again after a D3 roll-back". A D3 roll-back resets the overlay's valid flag along with the store (`KL_aecp_engine.sv:1610`, `:1912-1920`, `protocol_processor_top.sv:1852-1856` at `631eeb34`), so the ADPDU falls back to `ADP_IDX0` again.

**Not taken:** the optional pointer from the `REGISTER_MAP.md` memory-bridge section. Both F1s call it optional, and item 1 names only the CHANGELOG and SUBMODULES.

**Round-2 validation.** Run at head `420b778a`, with live `dev` still at `cdf49d1a`. Every command exited 0. None was piped, all ran from the lane's physical `/data` path, and the tree was clean before and after.

| Gate | Result |
|---|---|
| The 16 consumer commands (host GNU Make 4.4.1, Verilator 5.050) | 16 of 16 rc 0. `pp_shadow` 606/606/646/311 checks, 0 failures. `nvm_cosim` lint pass, quick 315 of 315. `milan_dp` 9 RESULT PASS (`sim` 235, `notify` 382, `crflic` 416, `nxn` 1,845, `nxndv` 1,847, `nxn8` 3,525, `nxn4c` 1,845, `nolpf` 235, `prune` 33, `ax1x1` 232, `aclk` 191; `gmstep` 104, `gptp` 182, `gptplat` 182), `render_mutants.py` 6/6, `gmstep_mutants.py` 6/6, 1,519 s. `milan_dp_render` 65 + 152 checks, leg defects 5/5. `test_builder.py` whole: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the calibration gate, needs a board build tree), 1,109 s. Port contracts 3,798 ports, undocumented 217/19/111 at the ratchet, 59 without a rationale, all recorded. Naming 96. Test evidence 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3. `docs_check.py` 0 findings. `lint_rtl.py --check` 90 <= 90 |
| For the comment edit | `pp_shadow` (above); `check_rtl_source_lists.py` 107 files, 4 of 4 lists, processor 36/42 tops; `xvlog_gate.py --check` 4 findings == ratchet, 0 in `hdl/`, run alone, 147 s; `lint_rtl.py --check` (above) |
| `docs.yml`, every `docs-check` step plus the `wire-accountability` and `docs-check-no-git` jobs, GNU Make 4.3 first on `PATH` in every step | 46 of 46 rc 0. The added-line em-dash gate in its pull_request form (base `cdf49d1a`): 0 findings over 69 added lines in 4 pages, arms 339/339. Concise documentation: 22 documents OK. `make -C gptp-processor docs` under make 4.3. `test_builder.py --require-rv32`: ALL GATES PASS EXCEPT 2 NOT RUN (gate 11, and gate 1b's `MAKEFLAGS += -e` arm, which make 4.3 does not honour), 1,068 s. Entity shape 219 checks under make 4.3. Contents gate: 127 pages. Cited paths: 877 |
| Also run | `behave` in `tests/`: 404 scenarios (the behave suite reads `REGISTER_MAP.md`). `lint_rtl.py --check --self-test`. `check_nvm_capture.py` PASS (census and firmware digest equal the receipt). `check_submodule_docs.py`, `submodule_boundaries.gen.py --check`. `ooc.sh --record-rom-digests` leaves `rom_digests.tsv` unchanged |

Not re-run in round 2: `scripts/run_all_suites.sh`, `syn/yosys/run.sh` and the physical gPTP suite. The round-2 gate list does not name them, and a comment line and Markdown change no elaborated RTL. Their round-1 results are above.

Deviations from the hosted runner, each recorded in the handoff:

- pyslang 11.0.0 was installed `--require-hashes` into scratch space.
- The Markdown renderer, pyyaml and wavedrom 2.0.3.post3 came from a prepared environment. A `--require-hashes` dry run checked it against `tools/markdown/requirements.txt`.
- sv2v v0.0.12, from the release zip with the workflow's sha256, was put first on `PATH` instead of `/usr/local/bin`.
- The RV32 SDK step was given a fresh `--destination`.
- The act self-test ran from the audited `dev` copy (sha256 `79579e6b...38f8`, equal to `scripts/act_ci.py`).

## Linked Issue / roles

Closes #635
Relates to #629

Executor: `[A503]`
Internal cleared-context reviewer: `[R438]`
External reviewer: `[R439]`

## Description

Adopts protocol-processor `main` `631eeb34` (lanes C2 to C6 and P141), per the assignment on #635. The `protocol-processor` gitlink moves from `b2db3a97` to `631eeb34`, and nothing else in the processor changes. The parent applies the supplied adaptation `parent-adoption-c4c6-ea3fb388.patch` (sha256 `67bcd698...7bd7c`), one commit per concern, and re-records every pin-derived record through its generator.

| Commit | Item | Change |
|---|---|---|
| `14f8c27f` | 1 | `protocol-processor` gitlink `b2db3a97` -> `631eeb34` |
| `c4bf64e2` | 2 | `scripts/measure_test_evidence.py`: `DUT_READER_DISPOSITIONS` entry for `protocol-processor/tb/pp_top/acmp_mutants.py` (C4, processor PR #137) |
| `15933a60` | 2 | `hdl/milan/KL_pp_shadow.sv`: `.EN_IDENTIFY_NOTIF_P (1'b0)` and `.identify_button_i (1'b0)`, each with its `//!` rationale (C6, processor PR #139) |
| `927428d1` | 2 | `scripts/measure_test_evidence.py`: entry for `protocol-processor/tb/pp_top/notify_mutants.py` (C6) |
| `3c68c6b1` | 3 | `syn/yosys/rom_digests.tsv` via `syn/yosys/ooc.sh --record-rom-digests`: `ltn_rom.hex` unchanged, `ucode.hex` `518b900c...37f8` |
| `81a80dd6` | 3 | Boundary diagram via `docs/diagrams/submodule_boundaries.gen.py` |
| `46ed4e91` | 3 | `scripts/port_docs.budget` via `check_port_contracts.py --write-budget`: three scoreboard kill-face tie-offs left the processor top (C5a) |
| `216d6feb` | 3 | `scripts/naming.budget` via `measure_naming.py --write-budget`: identity rows unchanged, count line 96 |
| `eb775875` | 3 | `docs/reference/SUBMODULES.md`: pin row and the seven merged processor lanes |
| `2087ee76` | 5 | `docs/reference/SUBMODULES.md`: what the parent can observe (identify tie-off, C5a deadline and hazard faces, C5b line range, C3, C2, P141) |
| `2ed1f7e4` | 5 | `docs/design/MEDIA_CLOCK_FOLLOWING.md`, "Protocol-processor changes": status landed at `631eeb34` (D3C1 to D3C4) |
| `3370c6cb` | 5 | `CHANGELOG.md`: "Unreleased - processor pin 631eeb34" |

The three patch commits together equal `git apply` of the whole patch on dev `cdf49d1a`, byte for byte (same blobs, same patch-id).

**Saved state (item 4).** `scripts/check_nvm_capture.py` passes unchanged: the census (8x8: 12,634 bytes, 156 records; 1x1 TDM8: 3,218 bytes, 53 records) and the product firmware digest (`a73ecc25...0eb3`) equal the receipt, so the capture is not re-measured. The recorded 8x8 maximum is 13.23 ms, below 24.5 ms.

**Parent-visible list.**

- `protocol_processor_top` gains input `identify_button_i` and parameter `EN_IDENTIFY_NOTIF_P` (default 0, C6). `KL_pp_shadow` ties both to 0. No other top port or parameter changes. The datapath, SoC, CSR map, VERSION (`0x0002_0060`) and firmware are unchanged.
- C5a adds no top port. Its kill face is internal to the processor (`KL_aecp_engine`, `KL_aecp_ucpu`, neither instantiated by the parent). An AECP command past its 100 ms deadline is answered (ENTITY_MISBEHAVING unless a refusal was chosen; NOT_IMPLEMENTED with the command echoed for non-AEM messages). AECP and ACMP work serialize by hazard class.
- C5b: locked `SET_SAMPLING_RATE`, `SET_CLOCK_SOURCE` and `SET_CONTROL` refusals, and `SET_CONTROL`'s out-of-range refusal, carry the value in force; GET_AUDIO_MAP pages of 63 to 71 records are served whole; READ_DESCRIPTOR carries stored current values; `DESC_LINE_BYTES_P` must lie in 576..1008 in steps of 8, and the parent binds 576.
- C3: the ADPDU configuration index follows a SET_CONFIGURATION; the parent image declares one configuration, so the wire is unchanged while `ADP_IDX0` is 0.
- C6 at the parent's setting: an unsolicited SET_STREAM_INFO carries the 84-byte SET body. IDENTIFY_NOTIFICATION stays off.
- C2 acts only with `cfg_maap_internal_i` = 1, which the parent ties to 0. C4 and P141 change no RTL.
- Records: ROM ledger rows for `631eeb34`; the boundary diagram; port-contract inventory 59 unjustified connections (was 62); naming 96 recorded; test-evidence 72 <= 77 with 0 unexplained DUT-source readers.

## Authoritative references

- #635 and its assignment comment; processor PRs #135, #136, #137, #138, #139, #140 and #142, their parent-visible lists.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md`, "Protocol-processor changes" (#629).
- `docs/reference/SUBMODULES.md`; `syn/yosys/README.md` (the ROM digest ledger); CONTRIBUTING.md 2.1 step 7 and 3.
- IEEE 1722.1-2021 7.5.1 and Milan v1.2 5.4.5.4 (IDENTIFY_NOTIFICATION, held off by `EN_IDENTIFY_NOTIF_P` = 0).

## How to get into the same state

```sh
git fetch origin 635-pp-pin-631eeb34
git switch --detach FETCH_HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status   # protocol-processor at 631eeb342ca1e3fa80e734077a56a943aee76ff1, leading space
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/pp_srcs.py --check --selftest
python3 sw/builder/test_builder.py
make -C tb/verilator/pp_shadow -j16
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
make -C tb/verilator/nvm_cosim lint
make -C tb/verilator/nvm_cosim quick
make -C tb/verilator/milan_dp -j16
make -C tb/verilator/milan_dp_render -j16
python3 scripts/lint_rtl.py --check
python3 scripts/check_nvm_capture.py
python3 scripts/check_submodule_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
(cd syn/yosys && ./ooc.sh --record-rom-digests) && git diff --exit-code syn/yosys/rom_digests.tsv
suite_logs=$(mktemp -d); scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
```

Expected result / pass criteria: every command exits 0. `test_builder.py` prints "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the calibration gate, needs a local board build tree). The `rom_digests.tsv` re-record leaves no diff.

## Known limitations / out of scope

- No processor source changes beyond the gitlink, and no parent port, pin, SoC, CSR, VERSION or firmware change beyond the supplied patch.
- `scripts/test_evidence.budget` stays at 77 although the ratchet now reads 72 and can be lowered: the file has no generator and the assignment's record list does not name it. Left for a ruling.
- The `KL_pp_shadow` comment on `current_cfg_i` keeps its wording; processor PR #136's optional rewording ("while no configuration is set or restored") would be an RTL edit beyond the patch.
- The processor PRs' optional compliance-matrix citations (5.4.2.x, 5.4.5, 5.5.2/5.5.3, 5.6.x) are not taken.
- The parent does not mirror processor integrator diagram 21, so there is no parent copy to update; `docs/reference/SUBMODULES.md` records that.
- The saved-state capture is not re-measured: its census and firmware digest are unchanged (`check_nvm_capture.py` passes).
- The identify sequencer stays disabled (`EN_IDENTIFY_NOTIF_P` = 0); no board button exists. It is graded in the processor's simulation only.
- No hardware or bench run.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (1, 2, 3 and 5 by this branch; 4's hosted contexts and the manager's banks are pending)
- [x] New or changed behavior has self-checking tests (the processor's: D3C, NP/ST/RN/ID, DL/HZ/TB and the rest, run by the processor suites; the parent change is a tie-off and records, graded by `pp_shadow`, `milan_dp` and the gates)
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
