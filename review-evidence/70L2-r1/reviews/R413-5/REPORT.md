[R413] POSITIVE - exact head b3ae17233eb9dd5934255f4018da7d45a159b5ac

Round R413-5, external independent review of issue #70 / PR #623 (#70 lane 2), tree `02d9741fb9f57d81c758ae42adea26ed9694f647`, source base `79c36963660c10e4c1c11a744fb5bff41a552b8b`. The round-5 assignment is #70 comment 5911775903. It covers two commits on round-4 head `5b4a47e9`: `ae203a01` (item 1, texts) and `b3ae1723` (item 2, controls). No firmware, RTL, bitstream or processor change.

Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR is open. All five lenses are covered clean at this exact head. I reconstructed the round from public state in the required order:

1. AGENTS.md and CONTRIBUTING.md sections 3 and 6.
2. docs/README.md.
3. The #70 body, scope record 5880276193, the lane-2 assignment 5888775832, rulings 5894183475, 5906400668 and 5909983141, and the round-5 assignment 5911775903.
4. `BAREMETAL_FIRMWARE.md`, `REGISTER_MAP.md` and `SAVED_STATE_MATERIALIZATION.md`.
5. The diff `79c36963..b3ae1723` and its history.
6. The author-r5 packet in the evidence tree `851e5aa7`.

I read the prior public review findings only after my own pass and my own mutants.

## Item 1 (`ae203a01`): the limit stated as the callee class, with no count

What I checked at this head:

- **Rule comment**, `sw/builder/test_builder.py:1653-1674`. It states the class ("a called function that writes through any pointer carrying no relocation on the static's bytes is not seen, since a call's arguments are recorded and not judged"). It calls it the standing callee limit and gives shapes "include, and are not limited to": a literal address, another object's address carried outside that object, and a run-time pointer (CSR or NVM read, callee's return, frame address plus run-time offset).
- **Docstring**, `:6920-6932`. Same class, same examples.
- **Printed closing line**, `:17233-17237`. Same class, "whatever the pointer's origin", same examples.
- **`docs/integration/BAREMETAL_FIRMWARE.md:973-1007`**, headed "What the pins do not see". Same class, "examples and not a complete list". It cross-references the census's standing callee limit, which I read at `:808-821` (first entry, "A store made inside a CALLED function"), so the reference is accurate.
- **Refusal row**, `:1651`. Same class, plus the unit's own stores the resolver places at a number or on another static. It says "examples, not a complete list".
- **CHANGELOG.md:66-67**.
- **PR body**, round-5 item 1. The round-4 section keeps its history and points forward to round 5.

No text counts the limits:

- A search of `sw`, `docs` (history excluded), `CHANGELOG.md` and `README.md` for "two limits", "outside the two", "second limit", "two writes" and "two addresses" finds nothing in gate-1b context. The only hits are unrelated sentences at `BAREMETAL_FIRMWARE.md:166,1970`, `REGISTER_MAP.md:919`, `MILAN_V12_ROADMAP.md:446`, `ENDSTATION_BUILDER.md:732` and `test_builder.py:1206,5480,11988`.
- The PR body has no such phrase either.

I wrote my own versions of the probes the assignment names (`scripts/limit_probes.py`). Each was planted as the first statement of `nvm_boot()` in the shipping firmware of a byte copy. I then ran gate 1b through its verdict controls (`scripts/plant_stop.py` and `scripts/run_profile_contract.py`).

These are accepted with `kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]`, and each matches the class's words:

| Probe | Shape | Matching words |
|---|---|---|
| `L1_csr_pointer` | `sscanf()` handed `(char *)(uintptr_t)milan_read(MILAN_PP_STAT)` (R412-4 `csr_pointer_sscanf`) | "a CSR or NVM read" |
| `L2_frame_runtime` | a frame buffer plus a CSR-read offset (R412-4 `stack_runtime_sscanf`) | "a frame address plus a run-time offset" |
| `L3_callee_return` | `strtoul()`'s return | "a callee's return" |
| `L4_literal` | a literal address | "a literal address" |
| `L5_before_overrun` | `"%s"` overrunning a 4-byte static declared before the verdict (R412-3 `pre_overrun_sscanf`) | "another object's address carried outside that object", named example |
| `L6_nbr_runtime` | `&neighbour + k`, `k` a CSR read (R412-3 `nbr_runtime_sscanf`) | same, named example |
| `L7_unit_literal` | this unit's own store through a literal address | refusal row: a store "the resolver places at a number" |

The contrasting unit-made stores are refused by rule 1b as unplaceable, as the page says ("A store through an offset known only at run time is refused by rule 1b"):

- `L8_unit_csr_pointer`
- `L9_unit_frame_rt`
- `L10_unit_callee_ret`
- `L11_unit_stack_far`

Receipts: `receipts/probes/p_*.log`, `receipts/summary.tsv`.

## Item 2 (`b3ae1723`): breaks on bytes +2 and +3

- **Controls.** `test_builder.py:14649-14662` plants three breaks: a static just after the verdict, one `int` back, plus 1, 2 or 3 bytes, handed to `sscanf()`.
- **Premise check.** `:14746-14771` reads the image's relocation targets directly, independent of `rv32_image_references()`. It requires `nvm_boot()`'s references on the verdict to be exactly `[offset]`.
- **Unmutated head.** `kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]` (`receipts/stop_none.log`).
- **Refusal at +2 and +3.** Planted directly into the shipping firmware, both are refused naming only "the linked image forms the full address of aem_loaded's storage (... %lo on an addi ...)", the escape pin (`receipts/probes/p_I2_interior_b2.log`, `p_I3_interior_b3.log`).

My own mutants (`scripts/census_mutants.py`, `scripts/run_mutants.sh`) change `rv32_image_references()`'s one range test at `:2147`, or the extent at `verdict_image_pins()`. The rest of the gate is unchanged, and it runs up to the stop point placed after the verdict controls:

| Mutant | Narrowing | Result at this head | Killed by |
|---|---|---|---|
| P1 (= R412-3 M9) | first byte only | KILLED | +1 break |
| P2 (= R413-4 N1, N4) | `[low, low+2)` | KILLED | +2 break |
| P3 (= R413-4 N2) | `[low, low+3)` | KILLED | +3 break |
| S1 (= R413-4 N3) | skip first byte | KILLED | shipping firmware, write pin ("stores in place from nowhere") |
| X0 | drop byte +0 | KILLED | shipping firmware, write pin |
| X1, X2, X3 | drop byte +1, +2, +3 | KILLED | the break on that byte |
| O1 | byte +1 only | KILLED | shipping firmware |
| EV | even bytes only | KILLED | +1 break |
| H1, H2, H3 | verdict extent 1, 2, 3 bytes | KILLED | +1, +2, +3 break |

Necessity, meaning a control can fail for the defect it claims to detect:

| Mutant | Change | Result | Meaning |
|---|---|---|---|
| NO2_X2 | +2 break removed, byte +2 dropped | SURVIVES (16/16) | only the +2 break kills X2 |
| NO3_X3 | +3 break removed, byte +3 dropped | SURVIVES | +3 break needed |
| NO3_P3 | +3 break removed, first three bytes only | SURVIVES | +3 break needed |

Premise mutants move a break's offset. Each is refused before grading, naming the bytes reached:

| Mutant | Offset moved | Bytes reached |
|---|---|---|
| B2TO4 | +2 break onto the neighbour | `[]` |
| B3TO1 | +3 break onto +1 | `[1]` |
| B3TO0 | +3 break onto +0 | `[0]` |

The texts describe what the controls measure:

- **`BAREMETAL_FIRMWARE.md:1035-1046`**, the comment at `test_builder.py:14612-14621` and the closing line at `:17224-17232`. Each claim is measured above:
  - "a census that stops reading any of those three bytes no longer refuses the break on it": X1-X3.
  - "the first byte is where milan_init()'s one store lands, so a census that stops reading it refuses the shipping firmware itself": X0, S1.
  - "nvm_boot() must place them on that break's byte and no other": B2TO4, B3TO1, B3TO0.
- **The history sentence** ("one reading only the first byte passed all fourteen of round 3, and ones reading only the first two or the first three bytes passed all fifteen of round 4") matches the public R412-3 F2 and R413-4 F1 evidence.
- **Search.** No "four-byte range", "measures the census" or stale break count remains in `sw`, `docs` or `CHANGELOG.md`. The page says "seventeen breaks" (`:1011`) and its table lists seventeen (`:1013-1028`).

## Other lenses at this head

- **Scope.** Round 5 touches only `CHANGELOG.md`, `BAREMETAL_FIRMWARE.md` and `test_builder.py`. `git diff 0a80abcb..b3ae1723 -- sw/firmware hdl protocol-processor tb` is empty, and `git diff 597dba85..b3ae1723 -- sw/firmware hdl protocol-processor` is empty.
- **RTL.** I read the PR's RTL diff myself:
  - `A_PP_STAT` at `hdl/common/csr/milan_csr.sv:2234-2243` packs exactly 32 bits: tag [31:24], reserved [23], `restore_cause` [22:21], `rs_cause` [20:18], `rb` [17], `closed` [16], then the pre-existing [15:0].
  - That packing equals `REGISTER_MAP.md:2317`.
  - The port widths equal `protocol_processor_top.sv:479-491` at pin `b2db3a97`.
  - `KL_pp_shadow` passes the four new outputs and `d3_unflushed_o` straight through. `nvm_pend_w` drops `aecp_dyn_dirty_o` as the comment and snapshot-ownership docs state.
  - `milan_datapath.sv` wires them to the CSR.
  - The timing parameters are left to the processor's `CLK_HZ_P` derivation, as ruled.
- **Firmware.** `nvm_restore_ended()` (`milan_baremetal.c:1364`) ends the wait on done or CLOSED. The persistence-disabled path runs the walk blind (`:1469`). The AEM-first order is at `:1675-1677`.
- **Firmware host gate.** `test_nvm_firmware.py --self-test`, which includes `test_boot_walk.py` and its two planted defects, exits rc 0 at this head (`receipts/nvm_firmware_selftest.log`).
- **Docs gates.** Seven Markdown gates in a private venv built from the hash-pinned `tools/markdown/requirements.txt`, each rc 0 (`receipts/docs_gates.log`): `docs_check`, `check_em_dash --base 79c36963`, `check_doc_style`, `check_doc_paths`, `check_archive`, `gen_toc --verify-anchors` and `gen_toc --check`.

## Lens results

```text
[R413] PASS Conformance - sw/builder/test_builder.py:1653-1674,6920-6932,17224-17237; docs/integration/BAREMETAL_FIRMWARE.md:973-1046,1651; CHANGELOG.md:66-67; PR #623 body round 5 - assignment 5911775903 items 1 and 2 checked clause by clause: class stated with shapes as examples and no count; +2/+3 breaks planted, premise exact, escape-only refusal; N1/N2/N4/M9 killed, head passes with the slot kept (receipts/stop_none.log, receipts/mutants/*, receipts/probes/*)
[R413] PASS RTL - hdl/common/csr/milan_csr.sv:2234-2243; hdl/milan/KL_pp_shadow.sv (diff 79c36963..b3ae1723); hdl/milan/milan_datapath.sv; protocol-processor/hdl/top/protocol_processor_top.sv:479-516 at b2db3a97 - PP_STAT 32-bit packing and field positions equal REGISTER_MAP.md:2317, port widths match the processor, and nothing in hdl/firmware/tb/processor changed since 0a80abcb (git diff empty)
[R413] PASS Robustness - receipts/probes/p_L1..L11,I2,I3; receipts/mutants/m_B2TO4,B3TO1,B3TO0 - every stated-limit shape accepted exactly as documented; unit-made run-time/far-stack stores refused by rule 1b; layout drift of any interior break refused before grading with the bytes reached named; compiler-absent arm unchanged (author-r5 builder-absent.log, "FULL BUILDER ABSENT PASS")
[R413] PASS Tests - sw/builder/test_builder.py:2147,14649-14771; receipts/mutants/*.log, receipts/summary.tsv - 13 census/extent narrowings all killed by the control the text names; 3 necessity pairs survive only with that control removed; 3 premise mutants refused; test_nvm_firmware.py --self-test rc 0 (receipts/nvm_firmware_selftest.log)
[R413] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:808-821,973-1046,1651; CHANGELOG.md:66-67; test_builder.py comments/closing line; PR body - every claim about what the controls measure reproduced by a mutant above; no stale count or "four-byte range" text; seven Markdown gates rc 0 (receipts/docs_gates.log)
```

## Findings

None open.

These were considered and not raised:

- **The "What the pins do not see" bullets also mention this unit's own stores.** A store through a literal is placed at a number. One at an offset placed on the neighbour is taken not to leave it. These are true statements carried from round 4. The page's preceding paragraph (`:966-971`) states the standing model they come from, and the refusal row states them explicitly. The class sentence itself is the callee class, as ruled.
- **The refusal row lists "a number or another static".** The prose also lists "a range, the stack". The row does not claim completeness. My far-stack probe (`L11`) is refused by rule 1b, which is stricter than the prose, so no reader is misled toward acceptance.
- **The docs claim that a census dropping the first byte "refuses the shipping firmware"** was measured (X0, S1, O1). The refusal names the write pin.

## Disposition of prior public review findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R412-4 F1 (MINOR; Conformance, Robustness, Tests, Docs): texts count two limits, a run-time pointer is a third | RESOLVED as ruled (5911775903). All six places state the callee class with shapes as examples and no count. `csr_pointer_sscanf` and `stack_runtime_sscanf` equivalents are accepted and match "a CSR or NVM read" and "a frame address plus a run-time offset" | Item 1 above; `receipts/probes/p_L1*,p_L2*` |
| R413-4 F1 (MINOR; Tests, Docs): interior break measures byte +1 only, described as the four-byte range | RESOLVED via option (a). N1, N2, N4 (my P2, P3) are killed by the +2 and +3 breaks. N3 (S1) is killed by the shipping firmware. M9 (P1) is killed by +1. The texts now state what is measured | Item 2 above; `receipts/mutants/*` |
| R412-3 F1 and F2 (MINOR) | Resolved at round 4 and still resolved. `nbr_runtime`/`pre_overrun` shapes are accepted and named in the limit (L6, L5). The range is now measured on every byte (X0-X3) | same |
| R412-1/2 and R413-1/2 findings | Resolved at earlier rounds (R413-3 POSITIVE at `0a80abcb`). Nothing in their scope moved since, except the gate-1b texts and controls judged above | `git diff 0a80abcb..b3ae1723` stat |
| R413-1 S2 (SUGGESTION): sweep receipt lacks a source-head field | Optional; retained with the manager, as before | none |
| #70 record 5904331147 (section 5.3 change 3; persistence-disabled PHY link) | Open work recorded for the next persistence lane, outside lane 2's scope | #70 5904331147 |

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5911775903 items 1-2 against `test_builder.py:1653-1674,6920-6932,14612-14771,17224-17237`, `BAREMETAL_FIRMWARE.md:973-1046,1651`, `CHANGELOG.md:66-67`, PR body; the stop run, 19 mutants and 13 probes | R413-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| RTL | CLEAN | `milan_csr.sv:2234-2243` packing vs `REGISTER_MAP.md:2317`, `KL_pp_shadow.sv` and `milan_datapath.sv` diff, processor ports at `b2db3a97`; RTL/firmware/tb scope unchanged since `0a80abcb` | R413-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Robustness | CLEAN | Probes L1-L11, I2, I3; premise mutants B2TO4, B3TO1, B3TO0; compiler-absent arm (author-r5 `builder-absent.log`) | R413-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Tests | CLEAN | 13 range/extent mutants killed, 3 necessity pairs, 3 premise mutants, `stop_none.log`, `nvm_firmware_selftest.log` | R413-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Docs | CLEAN | `BAREMETAL_FIRMWARE.md:808-821,973-1046,1651`, CHANGELOG, PR body, test_builder texts; 7 Markdown gates rc 0 | R413-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |

## Real limits of this review

- **Full profile contract not run to completion.** The whole `test_baremetal_profile_contract()` did not finish inside this session's 600 s foreground bound (`receipts/head_full_profile_contract.log`, rc 124). My gate-1b evidence comes from the same code stopped right after the verdict controls: an exception is raised just before the store-class mutants.
- **Builder bank not run.** I did not run the builder bank (disallowed). The closing-line text, "ALL GATES PASS EXCEPT 1 NOT RUN" and "FULL BUILDER ABSENT PASS" come from the published author-r5 receipts `gates-b3ae1723/builder-present.log` and `builder-absent.log`.
- **Scoped Verilator absent.** The scoped Verilator path `$DATA/tmp/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host, so no Verilator run was made. This round changes no RTL. My RTL lens rests on reading the RTL.
- **Compiler used.** `$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc`, Buildroot 2026.05 GCC 14.3.0, `riscv32-linux-gcc.br_real` sha256 `f87d55b7...2937c`.
- **Hosted checks, not accepted by this review.** Snapshot at `receipts/hosted_checks_snapshot.tsv`, 2026-09-30T14:41Z:
  - `rtl-fast`, lint, elaborate, docs, Yosys 4/4 and Verilator shards 0, 2 and 3 were success.
  - Verilator shards 1 and 4 were still in progress.
  - "Physical gPTP" was skipped, which is not hardware evidence.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Candidate build.** Source validation at this head is distinct from the current-dev candidate (live dev `ccdd07b5`), which the manager builds at the merge turn.

## Pending manager duties

- Hosted exact-head acceptance, including Verilator shards 1/5 and 4/5.
- The act replica.
- The current-dev candidate merge result and its validation.
- Post-merge containment.
- The second independent positive review (R412-5).
- The #495 entry widened to the callee class, as the ruling states.
- The open #70 items in 5904331147.
- Maintainer merge authorization.

## Clone integrity

At start and end the clone is at `b3ae1723` with tree `02d9741f`, and the index sha256 is identical (`0ece9d9b...4765`). `git status --porcelain=v2 --ignored` is empty. All 972 tracked non-gitlink entries hash to their index blob with matching mode. The four gitlinks are unchanged (`protocol-processor` `b2db3a97`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a` uninitialised as at start). All probes and mutants ran on byte copies under `scratch/`, which were deleted. Receipts: `receipts/clone_integrity_start.log`, `receipts/clone_integrity_end.log`.

R413-5 FINISHED
