[R807] NEGATIVE - exact head 936e0a566867aa648fb48e772a26fec99e3619c9

# R807-2: internal cleared-context review of PR #864 (issue #859, part of #665, Mark II split S15), round 4 delta

- **Head:** `936e0a566867aa648fb48e772a26fec99e3619c9`, tree `c8da5b75caa0d7666437e0f4f905f8dd64934a46`, on `dev-soft-core` source base `1d6bf555`.
- **Delta reviewed:** `7aa6ef0c..936e0a56`, five commits and 14 files, against the round 4 ruling (#859 issuecomment-6746289265) and its owners comment (issuecomment-6746307340: tsn-c-stack#31, #865, #866). Code the delta does not touch keeps its R807-1 lens verdict, unless the delta changes what that code depends on.
- **Verdict basis:** one MAJOR is open. It is R807-1-F1 / R808-1-F1, the ACMP owed-release alias, and it is retained at its cause. By the ruling's own plan the alias stays in the tree until the tsn-c-stack pin move and round 5. Every other prior finding is resolved at this head (table in section 3).
- **What this round got right:** the round's own fix is correct, verified and well tested. That is the decode wrap at the window's top, found by the author and fixed in 95ad6f88 with its cross-check in 936e0a56. The ruling's items 2 to 5 are met.
- **Sources:** this review used only public state (issue, PR, published evidence archive `92efa492`, hosted checks) and its own runs and probes.

## 1. Findings

### R807-2-F1 MAJOR - Conformance, RTL, Robustness, Tests - the 32x32 image still builds ACMP at 33 sinks against the pinned 32-bit owed-release mask (R807-1-F1 / R808-1-F1, retained)

- **Where:** `sw/firmware/ctrl/test/ctrl_srp_image.py:77-89` (`acmp_sizing`, which passes `-DACMP_MAX_SINKS=33u`) builds the 32x32 image against the gitlink `third_party/tsn-c-stack` `70936b77dc41981e192438388cd0aced69954f18`:
  - `include/acmp.h:400` keeps `uint32_t release`;
  - `src/acmp.c:816` and `:871` compute `1u << k`;
  - `src/acmp.c:310` (`transmit`) and `:1225` (`acmp_poll`) read `(release >> k) & 1u`.
- **Authority/evidence:**
  - C11 6.5.7p3 makes a shift by 32 undefined.
  - Milan v1.2 5.5: a change notice waits only behind its own owed response.
  - AGENTS.md section 7: a finding moved to another Issue is not resolved while the defect is in the tree.
  - The round 4 ruling, item 1: "this is a donor fix, not a decision to accept it". It also says "S15 does not move the pin" and "S15 round 5 syncs onto that pin. It then runs the R808-1-F8 probe on index 32, rebuilds the 32x32 image, re-runs the 32x32 point, and checks the disassembly".
  - At this head the gitlink is unchanged (`receipts/tree-integrity.txt`).
  - The published disassembly of the measured image `2e47b49e...` shows the alias. `bind_response` has `sll a3,a3,s3` at `0x4a94`; `transmit` has `srl a5,s2,a4` at `0x49d8`; `acmp_poll` has `srl a5,a5,a4` at `0x63f4`. I read each in the archive's `author/a752d/receipts/r4/probes/*.dis`. RV32I takes the low five bits of the count, so sink 32 and sink 0 share one bit.
  - The donor PR kebag-logic/tsn-c-stack#33 is open at `c6013804`, and its receipt `donor/probes/probe-head.log` passes the round 1 mask probe (rc 0). It is not in this tree.
- **What is resolved:**
  - The census row (`docs/design/SHAPE_32X32_CENSUS.md`, Findings, first bullet) and the PR body (Round 4, item 1; Known limitations) now state exactly what the RV32 image does: sinks 0 and 32 share one bit, and each holds the other's notices.
  - They name tsn-c-stack#31 (open) and PR #33 as owners, in place of the closed #653.
  - I checked every cited line at the pin (section 4). The Docs part of the finding is therefore resolved, and Docs is not carried.
- **Impact:**
  - The simulation shape's linked firmware, the image whose costs this PR publishes and S2b grades, still runs undefined behaviour in ACMP's response-before-notice path. For sink 0 and the CRF sink, Milan's rule is broken.
  - No gate in this tree detects it. The build-time refusal and the 33-sink test exist only in the donor.
  - The impact is narrower than in round 1. The documentation is true, the owner is open, and no harness script binds a sink past 1. So no published row reaches the alias, but the image carries it.
- **Required outcome:** the ruling's own path:
  - the pin moves to a tsn-c-stack `main` that carries the donor change, in its own lane;
  - this branch syncs onto it, so the 33-sink build executes no shift by 32 on the owed-release path;
  - then the round 5 items run: the probe on index 32, the rebuilt 32x32 image, the 32x32 point re-run, and the disassembly of `bind_response` and `transmit`.
  - The census row and the PR body are then updated to the fixed state.
- **Verification:** `git ls-files -s third_party/tsn-c-stack` names a commit that contains `src/acmp.c:35`'s build-time refusal and the `acmp_wide` test. The round 1 `acmp_mask_probe.sh` at 33 sinks exits 0 against the pinned stack. The rebuilt 32x32 image's `bind_response`, `transmit` and `acmp_poll` index the release words by `k / 32`. The 32x32 point is re-run on that image.

### R807-2-R1 RESIDUE - the REVIEW READY's open-risk line misdescribes the block decodes

- **Where:** #859 issuecomment-6754805021 (and -6753726718), "Open risks/questions". It says: "the skeleton's block decodes (publication, face, bound-talker) use the same bound form as the rings".
- **Evidence:** they do not.
  - `sw/mailbox/mailbox_skeleton.py:295-297` (bound-talker) and `:345-349` (publication), and the face decode (generated `hdl/milan/mailbox/KL_mbx.sv:288`, `:301-302`), bound an access by `off_w >= AW2_C'(BASE)` and `(rel >> $clog2(STRIDE)) < AW2_C'(MBX_N_IF_C)`, where `rel = off_w - BASE`.
  - No `BASE + size` is cast to `AW2_C` bits, so a block that ends at the window's top decodes in full.
  - The only cast base-plus-size bounds are the event and channel rings (`_ring_decode`, `mailbox_skeleton.py:524-531`), and this round fixed them.
  - The remaining `off_w == AW2_C'(BASE + i * STRIDE + REG)` decodes (`:454`, `:466`, `:471`, `:489`, `:515`) are exact register offsets below the register space, and can never reach the top.
  - The hand-written leaves (`hdl/milan/mailbox/KL_mbx_*.sv`) contain no window-bound arithmetic. The firmware writes `tx_base + 4 * (index & (words - 1))` (`sw/firmware/ctrl/mbx/mbx.c:434`), which stays below `0x8000`.
  - The line is pure wording: it changes no code, test, figure or verdict.
- **Exact fix:** in the next REVIEW READY or PR body, replace the sentence with: "The skeleton's block decodes (publication, face, bound-talker) bound an access by its interface index, `(rel >> $clog2(STRIDE)) < N_IF`, not by a cast `base + size`, so a block that ends at the window's top decodes in full. The event and channel rings were the only cast bounds, and `_ring_decode` now handles the one at the top."

### R807-2-S1 SUGGESTION - Tests, RTL - the decode cross-check proves inclusion, not exclusion

`ring_decode_findings` (`sw/mailbox/gen_mailbox.py:124-143`) checks that each ring's decode holds its first and last word. It does not check that the decode stops at the ring's end.

- **Probe:** `scripts/mutants.sh` mutant MB plants an unbounded decode on every ring. `--check` catches it at the tracked layout (rc 1, drift), but `--variant-shape` on the 32x32 layout and `--selftest` both pass (`receipts/mutants/summary.txt`). So a ring below the top that loses its bound would overlap every span above it, and the variant's cross-check would not see it.
- **Related:** `_ring_decode` (`sw/mailbox/mailbox_skeleton.py:528`) drops the bound when `end == contract.window_bytes`. That equals the `AW2_C`-bit top only while the window is a power of two. Nothing in `_check_contract` (`sw/mailbox/mailbox_model.py:775`) requires that today; the contract's window is `0x8000`.
- **Suggested:** also evaluate the first offset past each ring that ends below the top, which must be outside the decode. Key the unbounded form to `1 << AW2_C` (or refuse a window that is not a power of two). Add an arm with mutant MB.

### R807-2-S2 SUGGESTION - Tests - the generator's gates run in no workflow step

`docs/testing/CI_WORKFLOWS.md:204-207` states that no step runs `gen_mailbox.py --check --crosscheck`. No step runs `--selftest` either.

- The new arms are local only: the wrap arm, the derived-depth arm, the contract-ring refusal and the ACMP adapter's compile against the short layout.
- The 32x32 variant's cross-check and `shape_findings` reach CI only through the firmware self-test's RV32 SRP arm (`sw/firmware/ctrl/test/srp_arms.py:157-161`, which calls `write_shape_variant` and refuses its findings at `:49-52`).
- This gap predates the PR. **Suggested:** an issue to run both generator gates in a fast job.

### R807-2-S3 SUGGESTION - Tests - no self-test arm for the grader's point rings

`grade.tx_rings` and its `rings` argument (`tb/verilator/ctrl_service_budget/grade.py:37-41`, `:217-235`; passed by `run.py:264-269`) are exercised only by the 53-minute 32x32 run. That run shows them working at this head: 17 groups graded, 0 refusals, the owed row's 51 responses read at `0x7000`. But a regression would surface only there.

- `ctrl_service_hooks/hooks.py:587` keeps the contract's rings. That is correct, because that harness takes 1x1 and 8x8 only (`hooks_build.py:37`).
- **Suggested:** a harness self-test arm that grades a synthetic log with transmit records in the 32x32 layout's ACMP ring, and is refused under the contract's rings.

### R807-2-S4 SUGGESTION - Tests - the index-32 probe (R808-1-F8, retained as SUGGESTION)

At this head no harness script touches a stream past entry 0 of either interface (`tb/verilator/ctrl_service_budget/scenario.py`). The ruling schedules the probe on index 32 for round 5, after the pin move; it is the natural closing test for R807-2-F1.

## 2. Ruling items, one by one (round 4, issuecomment-6746289265)

1. **Census row and PR body on the owed-release mask: met.**
   - The census Findings bullet and PR body item 1 state that sinks 0 and 32 share one bit and that each holds the other's notices. They name tsn-c-stack#31 (open) and PR #33 (open, head `c6013804`), and #653 is gone from the census (`grep` finds none).
   - The cited lines at the pin match: `acmp.h:164` `#define ACMP_OWED_MAX 8u`; `:400` `uint32_t release`; `acmp.c:310` in `transmit`, `:816` in `bind_response`, `:871` in `unbind`, and `:1225` in `acmp_poll`.
   - The PR body says `acmp_poll`'s loop is `srl`, and the published disassembly confirms it at `0x63f4`.
   - The defect itself stays in the tree (R807-2-F1), as the ruling plans.
2. **ACMP transmit ring from the census rule: met.**
   - `acmp_tx_words` and `with_tx_ring` (`sw/mailbox/gen_mailbox.py:248-286`), applied in `shape_variant` (`:307-312`), compute 33 x (2 + 18) = 660 words, rounded to the next power of two, 1,024 words. The ring sits at `0x7000`, the lowest free 4 KiB-aligned span, and holds 51 records.
   - The 32x32 variant I generated (`receipts/variant32.log`) defines `MBX_CH_ACMP_TX_BASE 0x7000u` and `MBX_CH_ACMP_TX_WORDS 1024u`. `MBX_RING_AW_C` is 10 in both the variant and the tracked package, so the 1,024-word ring fits the existing ring address width.
   - The form is stated: a ring, because `ACMP_OWED_MAX` is a fixed stack definition. The census section 3 rule matches Milan v1.2 5.5.2.3.
   - Self-test arms: 51 of 33; the contract's ring is refused "holds 12 of the 33"; `shape_findings` refuses a short ring at every build. My mutants confirm it: MC (ring not resized), MF (512 words, 25 of 33) and MG (`shape_findings` off) are each caught; ME (sinks - 1) is equivalent, since it gives the same power of two.
   - `--check --crosscheck`: 0 findings at the head. The tracked mailbox outputs show no diff from `1d6bf555` to the head.
   - #865 (open) owns the receive shortfalls, and the census rows link it. The PR body's "Ring items" lists what is met and what is owed.
   - The 32x32 point was re-run on the resized layout (archive `r4/harness/M32`, `HEAD 936e0a56 DIRTY 0`, image `2e47b49e...`, ring receipt `acmp-tx-ring.txt`).
   - At 1x1 and 8x8 the backlog scripts at this head are byte-identical to round 3's (`receipts/scripts-7aa6ef0c.json` equals `receipts/scripts-936e0a56.json`). At 32x32 the owed row fills the 51-record ring with 51 frames in bursts of 12, 12, 12, 12 and 3 (`receipts/owed32-script.txt`).
3. **Census owners: met.**
   - The AEM ROM's 16-bit store row cites `avdecc/aem_assemble.py:309-320`. Its figures reproduce on this head's builder: `AEM_ROM_BYTES_C` 4,527 / 11,753 / 41,465 (`receipts/builder-*.log`). The TDM8 refusal text (87,545 B + 64 B) is in the archive's `r4/shape/aem_rom_probe.log`, and the TDM32 reason is stated.
   - #866 (open) is linked from five rows: the ROM store, the `aem` slot (`sw/litex/milan_soc.py:140`, the same line at `a9d69c77`), COUNTERS_CHANGED (`sw/mailbox/mailbox.yaml:857-863`), SRP's per-interface declarations, and the second AVB_INTERFACE.
   - The hook harness (`hooks_build.py:37`) and the F5 counters have their reasons in section 5.
   - The guard citation `hdl/milan/milan_datapath.sv:5354-5358` is the channel-map writer's cursor check at this head.
   - Every `path:line` in section 5, which is now labelled as the head's state, matches the head (checked mechanically, each line printed).
4. **Costs: met for what this base can measure.**
   - The PR body's table puts `record.*`, `centisecond` and `rebuild` at image `2e47b49efd92...` beside S2b round 22's projection. I recomputed every projection from the two S2b points, at 2, 16 and 64 streams, and every error (projected less measured); each matches to 0.1 us.
   - Every stated cost equals the archive's cycle count x 1.05, rounded up to 5 us (`r4/costs/parts-32x32.txt`).
   - The instrumented leg's image hash equals the plain leg's.
   - The PR says "Relates to #859" and lists the costs that stay owed.
5. **Residue and suggestions: met.**
   - `sw/builder/endstation_builder.py:201` reads `#: at that shape (#859).`
   - The census reads "AECP's change-notice retries", the harness README's term (`README.md:921`).
   - The section 8 fit is labelled at `41f963d5`, and its image hash equals this head's. The later commits touch only docs, `gen_mailbox.py` and the skeleton, none of them the firmware.
   - Gate 39 shows 3/3 plants red, including `srp.rtl_table`.
   - The `simulation identity` rule has its row, refusal arm and mutant, each passing or caught in `receipts/gates/ctrl-memory.log`.
   - The ACMP adapter arm compiles against the layout and is refused by both static assertions against the one-entry-short layout.

**The decode defect (95ad6f88, 936e0a56): a real defect, correctly fixed.**
- In the pinned simulator, at the 32x32 layout, the old bounded form `off_w < AW2_C'(BASE + 4 * WORDS)` casts `0x8000` to 15 bits as `0x0`. It decodes **0** words of the ring. The new unbounded form decodes exactly 1,024 words, `0x7000..0x7ffc` (`receipts/probe_wrap.log`).
- `off_w = {host_addr_i, 2'b00}` covers exactly the window, so the unbounded form aliases nothing, and `acmp_tx_host_w` is used only as the ring's write enable.
- The generated 32x32 `KL_mbx` lints like the tracked one. The only extra warning is the pre-existing unused `MBX_ENTRY_ORDINAL_C` (`receipts/lint-*.log`).
- The cross-check catches the reverted fix (mutant MA: the variant build has rc 1 and two self-test arms fail). The self-test's plant arm guards the check's own modulo (mutant MD).
- The same bound form left in other blocks is **neither a defect now nor a real latent risk**. The blocks never used that form (R807-2-R1). The only residual weakness is the inclusion-only check (R807-2-S1).

## 3. Prior public findings at this head

| Finding | Severity then | At this head | Evidence |
|---|---|---|---|
| R807-1-F1 / R808-1-F1 | MAJOR | **Retained** as R807-2-F1. The documentation part is resolved. | Section 1 |
| R807-1-F2 / R808-1-F2 | MINOR / MAJOR | Resolved | Item 2 |
| R807-1-F3 / R808-1-F3 | MINOR | Resolved | Item 3 |
| R807-1-F4 | MINOR | Resolved for the measurable costs; the rest are owed on #859 as the ruling records | Item 4 |
| R807-1-R1 / R808-1-F5 | RESIDUE | Resolved, in the ruling's shorter form | `endstation_builder.py:201` |
| R808-1-F6 | RESIDUE | Resolved | Census aecp/srp transmit row |
| R807-1-S1 / R808-1-F4 | SUGGESTION | Done | `SPLIT_CONTROL_MEMORY.md` section 8 |
| R807-1-S2 | SUGGESTION | Done | Gate 39 3/3; `simulation identity` rule |
| R808-1-F7 | SUGGESTION | Done | `gen_mailbox.py --selftest` ACMP adapter arms |
| R808-1-F8 | SUGGESTION | Retained (R807-2-S4), scheduled for round 5 | `scenario.py` |

## 4. Lens results

**Conformance (UNCLEAN, R807-2-F1).**
- `[R807] PASS Conformance` for the rest of the delta:
  - `sw/mailbox/gen_mailbox.py:248-312` against Milan v1.2 5.5.2.3. The ring holds 33 PROBE_TX_COMMANDs of 20 words, the 70-byte frame of 5.5.2.2 with the two-word header.
  - The census rules (section 3) against the issue's "derived from a protocol rate or timer".
  - The cost table against the ruling's item 4 (recomputed).

**RTL (UNCLEAN, R807-2-F1).**
- `[R807] PASS RTL` for the mailbox RTL in the delta:
  - the generated 32x32 `KL_mbx.sv` decode (`off_w` width 15, ring write enable, `wr_addr_i` slice of `$clog2(1024)`, `MBX_RING_AW_C` 10), and the decode probe;
  - lint of the variant and the tracked mailbox with their leaves;
  - the block decodes (R807-2-R1) and the leaves' and firmware's address arithmetic.

**Robustness (UNCLEAN, R807-2-F1).**
- `[R807] PASS Robustness` for the rest:
  - `with_tx_ring` refuses when no aligned span is free and re-runs `_check_contract`;
  - `ring_decode_findings` reports a missing decode;
  - the owed row's burst arithmetic (`scenario.py:801-815`) at room 12, 13, 24 and 51;
  - existing shapes unchanged: tracked outputs show 0 drift, and the 1x1 and 8x8 scripts are identical.
- Equivalent mutant noted: ME.

**Tests (UNCLEAN, R807-2-F1).**
- `[R807] PASS Tests` for the delta's new tests. Each can fail for its defect: mutants MA, MC, MD, MF and MG are caught; gate 39 has 3/3 plants red; the `simulation identity` mutant is caught.
- Not caught: the exclusion gap (R807-2-S1, a SUGGESTION) and the CI wiring (R807-2-S2, a SUGGESTION).

**Docs (CLEAN).**
- `[R807] PASS Docs`, covering:
  - `docs/design/SHAPE_32X32_CENSUS.md` (every section 5 `path:line` checked at the head; the AEM figures reproduced);
  - `docs/design/MAILBOX_SPLIT.md:120-139`;
  - `docs/design/SPLIT_CONTROL_MEMORY.md` section 3 rule row and section 8;
  - `tb/verilator/ctrl_service_budget/README.md:55-60`, and the PR body against the receipts;
  - docs gates: `docs_check.py` 0 findings, `check_doc_paths.py` OK, `gen_toc.py --check` OK, `check_em_dash.py --base 1d6bf555` 0 findings.
- The owner comment rule holds: the delta's added code lines contain no lane label, round, reviewer ID or comment ID. R807-2-R1 is RESIDUE and leaves the lens clean.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R807-2-F1) | `ctrl_srp_image.py:77-89` with the tsn-c-stack pin, `gen_mailbox.py:248-312`, census sections 3 and 5, the PR body's cost table | R807-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| RTL | UNCLEAN (R807-2-F1) | generated 32x32 `KL_mbx.sv` and package, `mailbox_skeleton.py:524-531`, `:295-349`, `receipts/probe_wrap.log`, `receipts/lint-*.log` | R807-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Robustness | UNCLEAN (R807-2-F1) | `with_tx_ring`, `ring_decode_findings`, `scenario.py:801-815`, `receipts/mutants/summary.txt`, `receipts/scripts-*.json` | R807-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Tests | UNCLEAN (R807-2-F1) | `gen_mailbox.py` self-test arms, gate 39, `test_ctrl_memory.py` identity arm and mutant, harness self-test, `receipts/mutants/` | R807-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Docs | CLEAN | census, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md`, harness README, PR body, docs gates | R807-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |

## 6. Executed at this head by this review

All runs were on the clean detached clone at `936e0a56`; logs and return codes are in `receipts/`.

- **Lane gates, all rc 0:**
  - `gen_mailbox.py --check --crosscheck` ("0 finding(s)");
  - `gen_mailbox.py --selftest` (94 arms ok, "0 arm(s) failed");
  - `test_ctrl_memory.py` ("RESULT: PASS");
  - `test_soc_options.py` ("RESULT: PASS");
  - `test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged` ("ALL GATES PASS", gate 39 3/3, gate 41 1/1);
  - `check_py_idiom.py` and `--selftest` (54 of 54);
  - `ctrl_service_budget/run.py --self-test` ("0 failures");
  - the docs gates listed above;
  - `git diff --check 1d6bf555 HEAD`.
- **First runs kept:** test_ctrl_memory, test_soc_options and the em-dash/TOC gates first failed only because the host python lacked `migen` and the Markdown renderer. They were re-run with the host's existing LiteX venv and pinned Markdown venv, with no install.
- **Probes:** the decode probe (pinned simulator 5.050, identity checked by `--version`); variant and tracked lint; seven generator mutants; builder runs at three configs; the 1x1/8x8 script comparison against round 3; the 32x32 owed script.
- **Hosted checks at the exact head (read-only):** 68 success and 1 skipped, the nightly and manual "Physical gPTP" job, which did not execute (`receipts/gh-pr-checks.txt`, `receipts/check-runs-936e0a56.tsv`). Among the successes are `rtl-fast`, the 19 Verilator shards, the 4 Yosys shards, `docs-check` and `elaborate`.
- **Published archive:** `review-evidence/665s15-r1` at `92efa492`: all 1,962 manifest entries match their published SHA-256. 46 entries are path-redacted, and none is unlisted.
- **Tree integrity after every probe:** HEAD, tree `c8da5b75...` (equal to `git write-tree`), clean index and worktree, no untracked file, gitlinks as pinned (`receipts/tree-integrity.txt`).

## 7. Real limits

- **Not run by this review:** the full `test_builder.py --require-rv32` legs, the firmware self-test and mutant drivers, the 65-suite sweep, `bdd-conformance`, and every harness point (the 32x32 run takes 53 minutes). For those, and for the 139 workflow steps, this review relies on the author's published receipts, which I spot-checked: the step table, the M32/M1/M8 heads and image hashes, the cost parts, the disassembly and the donor probe. It also relies on the exact-head hosted contexts.
- **Donor PR:** not reviewed beyond the claim (open at `c6013804`; its probe receipt shows rc 0).
- **No manager source bank** is claimed or inferred. The current-dev merge candidate (live dev `123f57a922bf...`) is not validated here.
- **No hardware:** physical calibration was NOT RUN, and the skipped physical context is not hardware proof.
- **Not graded:** the 32x32 harness point is recorded, not graded, against T_svc.

## 8. Pending manager duties

- Carry R807-2-R1 to the residue checklist.
- Track R807-2-F1 to the tsn-c-stack pin-move lane and to round 5 (ruling item 1).
- Consider issues for R807-2-S1 to S3.
- Validate the current-dev merge candidate, and own hosted and act acceptance at the merge turn.

R807-2 FINISHED
