[R416] NEGATIVE - exact head 54c1e2b11c90e7063fc5882b15ddea5e4335d411

# R416-1 internal independent review: PR #138 (lane C5b, AECP dispatch and response)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #138, branch `c5b-aecp-dispatch`
- Exact head: `54c1e2b11c90e7063fc5882b15ddea5e4335d411`, tree `f90877d2037fda973553b0ef1b75f29a7e0a6365`. Base: `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (an ancestor; 8 commits)
- Closes #50, #53, #74, #76 and #82. Assignment: #76 comment 5906184962. Review start: PR #138 comment 5915624225
- Reviewer: [R416], internal, round 1. Cleared context, detached clone, no author contact, no GitHub writes

## Verdict

NEGATIVE. The acceptance list of every closed issue is met at this head, and I verified it independently: my runs, and the 29-arm mutation campaign re-run with every arm KILLED on its named check. Three MINOR findings remain open, and all three come from what the PR itself introduces:

- **F1:** a controller-visible change to SET_CONTROL's BAD_ARGUMENTS body. No test grades it, and it is missing from the parent-visible list.
- **F2:** a new, undocumented ceiling on `DESC_LINE_BYTES_P`. The contract row this PR edited states only a floor.
- **F3:** `git diff --check` fails on the new mutation patch directory, which has no whitespace exemption.

Any one of them leaves its lenses unclean. Tests and Docs are UNCLEAN. Conformance, RTL and Robustness are CLEAN.

## Findings

### F1 - MINOR - SET_CONTROL's out-of-range BAD_ARGUMENTS body changed from zero to the value in force: ungraded, and missing from the parent-visible list

- **Lenses:** Tests, Docs
- **Where:**
  - `hdl/aecp/ucode/gen_ucode.py:1818-1819`: E_SCTRL's out-of-range arm now branches to the shared refusal tail `SCTRL_EMIT`, which emits r6, the IDENTIFY value in force. At the base it branched to `E_BADARG1`, a zero body.
  - `tb/pp_top/sim_main.cpp:7182-7199` (W13): the only out-of-range SET_CONTROL. It checks the status and cdl 17 but never the body byte, and it runs while IDENTIFY is 0, so zero and "value in force" are the same byte there.
  - `docs/architecture/06_aecp_engine.md:736` states the new behaviour.
  - The PR body's "Parent-visible" list names only the locked refusals.
- **Authority:**
  - IEEE 1722.1-2021 §7.4.25.1, "The response always contains the current value ... the old value if it fails". The new behaviour is therefore conformant.
  - Assignment #76/5906184962: "If a new test exposes an RTL defect, fix it in this lane with the clause cited and a failing arm". This fix has no failing arm.
  - Assignment item 6 requires the parent-visible list.
- **Evidence:** reviewer probe `probes/r416-sctrl-badarg-zero-body.patch` restores the base's zero-bodied arm (`BRANCH E_BADARG1`).
  - `--aecp-dispatch-only`: 886 checks, 0 failures.
  - Full default build: 8290 checks, 0 failures.
  - Receipt: `probes/r416-sctrl-badarg-zero-body.result.txt`.
  - The mutant is not equivalent. E_BADARG1 emits `r2 = 0` (`MOVE rd=2 imm=0`), while SCTRL_EMIT emits `r6 = READ_ST RGN_DYN+SEL_IDENT`. The two differ whenever IDENTIFY holds 255.
- **Impact:**
  - A controller that sends SET_CONTROL(IDENTIFY, 128) while identifying now gets 255 back where it used to get 0. That is correct, but the pin-adoption lane is not told about it.
  - A regression back to zero would pass every processor check.
- **Required outcome:**
  1. Add a tb/pp_top arm that sends an out-of-range SET_CONTROL while IDENTIFY holds 255. It must demand byte-exact BAD_ARGUMENTS at cdl 17 carrying 255, and no dynamic-store write, NVM mark or notification.
  2. Record the zero-body revert as a mutant KILLED on that named check, in `aecp_mutations/` + `aecp_mutants.py` + README.
  3. Add "SET_CONTROL's out-of-range BAD_ARGUMENTS now carries the value in force (before: zero)" to the PR's parent-visible list.
- **Verification:** the reviewer probe patch (or the recorded equivalent) is KILLED on the new named check, and the parent-visible list names the change.

### F2 - MINOR - `DESC_LINE_BYTES_P` gains an undocumented ceiling (1008); the edited contract row states only "At least 561"

- **Lens:** Docs
- **Where:**
  - `hdl/aecp/KL_aecp_ucpu.sv:271-274`: new `gen_g_d8_cap` refuses `RESP_D8_CAP_BYTES_P > 1024`.
  - `hdl/aecp/KL_aecp_engine.sv:1671` passes `RESP_BUF_C`, which is round16(16 + line) (`:900`).
  - `docs/guides/integrator.md:86`: the row this PR edited says "At least 561".
  - `hdl/aecp/KL_aecp_desc_store.sv:256-258` already requires a multiple of 8, so 561-567 are refused as well.
  - PR body: "No port, parameter or register of `protocol_processor_top` changes", and only the 561-byte floor is listed as parent-visible.
- **Evidence:** `receipts/line_range_probe.txt` is a lint/elaboration of `protocol_processor_top` with `-GDESC_LINE_BYTES_P=`:

  | Line (bytes) | Base | Head | Head's message |
  |---|---|---|---|
  | 560 | elaborates | refused | the new GET_AUDIO_MAP page guard |
  | 568, 576, 1008 | elaborate | elaborate | |
  | 1016, 1024, 1536 | elaborate | refused | `RESP_D8_CAP_BYTES_P=1040 outside 524..1024 (the 10-bit cursor)`, an internal parameter the integrator never set |

  Base lines above 1008 were already unsafe for a descriptor longer than 1008 bytes, because of the 10-bit response cursor. The refusal is therefore a sound choice, and the defect is only in what is disclosed and documented.
- **Impact:**
  - The legal range of a top-level parameter shrinks on both sides, while the integrator contract states only a floor that is not itself legal.
  - An integrator choosing a larger line gets an elaboration error that names an internal knob.
  - The pin-adoption lane is told "no parameter changes". The parent's 576 is unaffected: I verified the parent passes 576 explicitly (`sw/litex/milan_soc.py` at dev ccdd07b5).
- **Required outcome:**
  1. State the legal range, a multiple of 8 from 568 to 1008, in the integrator guide row and the F01.5 / 07 §3.3.1 line description.
  2. Add the ceiling to the PR's parent-visible list.
  3. Optionally, have the engine refuse an over-large line with a message that names `DESC_LINE_BYTES_P`.
- **Verification:** the docs gates, plus re-running `scripts/lint_focus.sh` with `GOPT=-GDESC_LINE_BYTES_P=1016` and checking that the documented range matches.

### F3 - MINOR - `git diff --check` is rc 2: the new `tb/pp_top/aecp_mutations/*.patch` directory has no whitespace exemption

- **Lens:** Tests (a repository gate of the donor bank)
- **Where:** `.gitattributes` exempts `tb/srp_top/mutations/*.patch` and `tb/adp_engine/mutations/*.patch` (`whitespace=-blank-at-eol,-blank-at-eof`, because unified-diff context keeps a blank line as a single space), but not the new directory. The flagged lines:
  - `lk-prefix-zero-body.patch:153,158,251`
  - `lk-sctrl-miss-lock-nop.patch:18`
  - `ov-top-oversize-dropped.patch:4,10`
  - `rd-so-reads-input-row.patch:5`
- **Evidence:**
  - Reviewer receipt `receipts/diff_check.txt`: `git diff --check 0451d83d..54c1e2b1` rc 2, 7 trailing-whitespace hits, all in those patch files.
  - The manager's donor bank reports the same failure (PR #138 comment 5915872144, "8 of 9 rc 0").
  - I first saw this output during my pass and wrongly dismissed it as inherent to the patch format. The existing exemptions show the repository treats it as a gate.
- **Impact:** a donor-bank gate is red at this head.
- **Required outcome:** add `tb/pp_top/aecp_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof` to `.gitattributes`, as lane C3 did for its patches in commit `e8ec039`. Do not strip the context spaces: the patches must still apply with `git apply --check`.
- **Verification:** `git diff --check 0451d83d <new head>` rc 0, and `aecp_mutants.py` still reports every arm KILLED.

### S1 - SUGGESTION - the "too short for the lane" guards of the READ_DESCRIPTOR overlays are ungraded

- **Lenses:** Robustness, Tests
- **Where:**
  - `hdl/aecp/ucode/gen_ucode.py:1138, 1165, 1200`: the guards themselves.
  - `hdl/aecp/KL_aecp_ucpu.sv:591-593`: the TAIL count `rf[ra] - imm` is a 16-bit subtract, so without the guard a descriptor shorter than the lane end gives a wrapped count.
  - `docs/architecture/06_aecp_engine.md` §6.1 documents the fallback ("served whole from the image").
- **Evidence:** probe `probes/r416-rdesc-short-guards-nop.patch` replaces all three guards with NOP. Both legs stay green (886 and 8290 checks; `probes/r416-rdesc-short-guards-nop.result.txt`).
- **Why a suggestion:** by inspection the guards are correct (`COMPARE`/`BR_STATUS lt`, the same idiom PG proves). They are reachable only with an image that breaks the IEEE fixed part, and that image is the consumer's to lint (07 §3.1).
- **Suggested outcome:** a configuration-0 STREAM (or AUDIO_UNIT) shorter than its lane end, with a set row, is served as its image whole, and the probe is recorded as a KILLED mutant.

### S2 - SUGGESTION - `scripts/check_m9_opcodes.py` robustness and wording

- **Lens:** Tests
- **Where:** `scripts/check_m9_opcodes.py:36` and `:24` / `:80`.
- **What:**
  - `RE_ENGINE` only matches `localparam logic [15:0] OP_*_C = 16'hXXXX;`. An `OP_*_C` written in any other form (decimal, another width) would be silently left out of the comparison. The "parsed nothing" guard catches only an empty parse.
  - The docstrings say "three" failing fixtures, but the selftest has four (missing, extra, duplicate, no initializer).
- **Suggested outcome:** count every `OP_[A-Z0-9_]+_C` localparam, fail when any is unparsed, and fix the count in the docstrings.

## Acceptance, issue by issue

**#76 (GAP-01)**
- **1:** `kOpcodes` is the engine's 30 `OP_*_C`, including 0x0008, 0x000E, 0x0010, 0x0011, 0x002C, 0x002D and 0x004B (`tb/pp_top/sim_main.cpp:2998-3003`; engine `:672-785`). `check_m9_opcodes.py` gates it: plain PASS, selftest 6/6 (`receipts/check_m9_*.txt`), run by `run_suites.sh` before any suite. Met.
- **2:** all seven `m9-guard-*` arms KILLED on `M9: mt=4 word XXXX` (9/9/9/7/7/7/7 failures), recorded in the README. Met.
- **3:** 03 §7 no longer promises a response-size ROM. Met.
- **4:** see Tests below. The suites that consume the changed RTL are green in my runs.

**#74 (REQ-FWX-001)**
- **1:** A5b sends 0x002A, 0x0037, 0x0038, 0x0039, 0x0047 and 0x0048 as outer AEM commands, at the IEEE command lengths (`sim_main.cpp:2126-2138`). Met.
- **2:** `a5b-reboot-success-arm` KILLED on the byte-exact echo check. Met.

**#53 (REQ-AEM-014)**
- **1:** LK1/LK3 send each SET from a second controller under the bench's lock, at cdl 20/20/17. Met.
- **2:** GET reads the old value, and there is no write, mark, notify or unsolicited frame (`foreign()`); LK6 serves the holder. Met.
- **3:** the body is decided against IEEE §7.4.21.1/.23.1/.25.1 (Milan §5.4.2.13/.15/.17 are silent on it), stated in 06 §6.8, and checked byte-exact on unset and set rows. Met.
- **4:** the six CHECK_LOCK→NOP arms (main and miss path) plus the base reproduction are all KILLED. Met.

**#50 (REQ-AEM-001)**
- **1:** OV1 reads a 576-byte descriptor at cdl 592, frame 618, byte-exact, through TX slot 4. Met.
- **2:** `ov-oversize-never` KILLED (18 failures), as is `ov-top-oversize-dropped`. Met.
- **3:** pages of 62-71 are served whole; 72, 176 and 256 answer NO_RESOURCES with count 0; P-MAP-SUBSET-CH-MAX is corrected to 71 in F01.5, 06 §6.5 and 00. Met.
- **4:** 06 §3 now goes command by command. I checked the GET_AVB_INFO cdl 32+4k and GET_AS_PATH cdl 80 arithmetic against IEEE §7.4.40.2/§7.4.41.2. Met.

**#82 (GAP-08)**
- **1:** RD1: READ_DESCRIPTOR equals the GET's value byte-exact after each SET. Met.
- **2:** OV1/OV2/OV5: frame > 576, cdl > 524, byte-exact, slot 4 used and freed. Met.
- **3:** REQ-MDL-001..011 are re-dispositioned to the consumer in 00 §6.6 (Ver "—") and 07 §3.1-3.3. Met.
- **4:** the ceiling is stated in 07 §3.3 and 03 §7. Met.

The PR's statement that #38, #51 and #60 stay open is accurate.

## Lens evidence

### Conformance: CLEAN

**Locked refusals carry the value in force.** This follows IEEE 1722.1-2021 §7.4.21.1, §7.4.23.1 and §7.4.25.1; Milan §5.4.2.13, .15 and .17 add the refusal and are silent on the body.
- Order: lock outranks locate, then the list (06 §6.4).
- A foreign miss answers ENTITY_LOCKED with a zero body. There is no descriptor, so there is no value.
- Response forms: cdl 20/20/17 per Figures 7-46/7-47 and the one-byte IDENTIFY value.

**GET_AUDIO_MAP.**
- Milan §5.4.1 permits a response above cdl 524.
- A subset of at most 71 is inside Milan §5.4.2.26's "≤176" permission.
- NO_RESOURCES is status 8 of Table 7-141, sent in the full response form (cdl 24) with `number_of_mappings` 0. The count no longer names records the response does not carry. At the base it did, against §7.4.44.2.

**READ_DESCRIPTOR overlays.** Offsets checked against IEEE: AUDIO_UNIT `current_sampling_rate` @136 (§7.2.3), CLOCK_DOMAIN `clock_source_index` @70 (§7.2.32), STREAM `current_format` @74 (§7.2.6, the same offset in the Table 7-8 and Annex C layouts). The lane rebuilds keep `sampling_rates_offset`/`count` @140-143 and `formats_offset`/`number_of_formats` @82-85.

**Parent-visible changes.** All three listed wire changes are conformance fixes that the closed issues' acceptance mandates, so they are in the lane's scope, and the parent adopts them knowingly through the list. The unlisted ones are F1 and F2.

**The author's reading of the parent is correct**, checked at dev ccdd07b5 (read-only):
- The parent builds its image at a 576-byte line (`sw/litex/milan_soc.py`: `_img.build(..., 576)`) and places a 16 + 576 = 592-byte response buffer.
- Its 8x8 config (`configs/endstation_ax7101_8x8.yaml`) declares 8 talkers × 8 channels, `map_mode: dynamic`, which is 64 output stream channels. With one source per output stream channel (IEEE 7.2.19), an output page holds at most 64 mappings: at or below 71, above cdl 524 (cdl 536), in a standard slot.
- 576 is above the 568 that is actually the smallest legal line.

**The nxndv observation** (the face's STREAM_INPUT 1 format ≠ the image's `current_format` before any SET) is a parent-side model/face coherence matter under IEEE §7.2.6/§7.4.10. It predates this PR: at the base, READ_DESCRIPTOR already served the image and GET the face. The processor is right not to overlay a value it never stored, so no processor action is needed. I could not observe it myself, because that would need the parent bank; see the pending duties.

### RTL: CLEAN

- **Engine seam** (`KL_aecp_engine.sv:3113-3138`): gated on AEM, AEM_COMMAND, READ_DESCRIPTOR, cdl ≥ 20 and cfg 0. The `desc_ix_r` of READ_DESCRIPTOR (@30) selects the dyn-state row. An out-of-range row reads zero with valid clear (`KL_aecp_dyn_state.sv:254-256`), so the image is served.
- **µCPU:**
  - D8 cap applies only when `cnd[0] && !batch_r`.
  - TAIL count `rf[ra]-imm`; a zero count completes (the stall and request logic gates on `copy_left_r != 0`).
  - Only COMPARE writes `lt_r` (`:646`), so the GAMAP "lt of +5" flag survives the CHECK_ARGs.
  - The 71-record page ends exactly at 592 (`cursor+8 > cap` is false at 584).
  - GET_AUDIO_MAP is not a GDI member (`:1037-1045`), so the batch exception cannot drop its records.
- **Microcode:** µPC offsets checked by hand for E_SSRATE, E_SCLKS and E_SCTRL. `place()` asserts on any overlap, and `check_upc_map.py` passes (58 constants, 86 entry points, page cap 71 in sync).
- **Lint:** `lint_hdl.sh`'s exact command over `KL_aecp_ucpu`, `KL_aecp_engine` and `protocol_processor_top`: 0 warnings (`receipts/lint_focus_head.txt`).
- No port, register, or #57/#81/#84 seam change.

### Robustness: CLEAN

- The page cap handles 256 (the count's low byte is 0) and any count above 71. The ITER count is 8 bits, and the cap bounds it first.
- The lock now runs after harmless reads. A memory-fault DESC_ADDR still meets the lock before NO_SUCH_DESCRIPTOR.
- The `gen_g_gamap_page_fit` and `gen_g_d8_cap` elaboration guards turn a latent silent overrun into a refusal (see F2 for how that is documented).
- One defensive arm is ungraded: S1.

### Tests: UNCLEAN (F1, F3)

- **tb/pp_top:** 8310 checks, 0 failures (8290 default + 20 VID build; `receipts/pp_top_*`). `--aecp-dispatch-only` gives 886, and fixture-guards pass 4 of 4.
- **tb/ucpu:** 398 checks, 0 failures.
- **Author's mutation campaign re-run:** 29 of 29 KILLED on their named checks, controls 3/3 PASS (`receipts/aecp-mutants/campaign_summary.txt`). Failure counts are identical to the author's receipt.
- **The two tb/ucpu README mutations** (D8 ignored, batch exception dropped) reproduce: 2 failures each (`probes/r416-ucpu-d8.result.txt`).
- **name_wr_mutant:** killed; golden and restored PASS.
- **The driver:** `aecp_mutants.py` applies explicit patch files with `git apply` in a temporary copy, reads only logs, and counts a kill only on a completed run with the named check failing. That matches the PR's "no parent disposition needed" claim.
- **Gaps:** F1 (MINOR), F3 (MINOR, the `git diff --check` gate) and S1.

### Docs: UNCLEAN (F1, F2)

- 00, 01, 03, 06, 07, 09 and the integrator guide agree with the RTL on the page cap, the ceiling, the overlays and the locked body.
- Documentation gates on the head tree: links, matrix, params and modmatrix all rc 0 (`receipts/docs_gates_head.txt`). The diff touches no mermaid, WaveDrom or SVG.
- Open: F1 (parent-visible list) and F2 (parameter range).

## Prior public review findings

None exist on PR #138 at this head. After writing the verdict and ledger, I checked the PR's comments and reviews again:
- There are no reviews.
- The comments are the two review-start markers (5915624225 and 5915630914) and one manager evidence comment (5915872144, the donor bank). That comment is evidence, not a review finding. Its failing gate is carried here as F3, with my own receipt.

No prior review finding needs resolving or retaining.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gen_ucode.py E_SSRATE/E_SCLKS/E_SCTRL/E_GAMAP/E_RDESC*; IEEE §7.2.3/.6/.32, §7.4.21.1/.23.1/.25.1, §7.4.44.2, Table 7-141; Milan §5.4.1, §5.4.2.13/.15/.17/.26; parent dev ccdd07b5 `milan_soc.py`, `configs/endstation_ax7101_8x8.yaml`, `avdecc/aem_maps.py` | R416-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| RTL | CLEAN | `KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`, `ucpu_pkg.sv`, `gen_ucode.py`, `KL_aecp_dyn_state.sv` (read path); focused lint; `check_upc_map.py` | R416-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Robustness | CLEAN | page-cap and TAIL arithmetic, lock ordering, elaboration guards, line-range probe; S1 probe | R416-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Tests | UNCLEAN (F1, F3) | tb/pp_top (8310), tb/ucpu (398), fixture-guards, aecp_mutants 29/29, ucpu D8 probes, name_wr_mutant, `check_m9_opcodes` gate + selftest, `git diff --check`, reviewer probes F1/S1 | R416-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Docs | UNCLEAN (F1, F2) | 00, 01 F01.5, 03 §7, 06 §3/§6.1/§6.4/§6.5/§6.8/§8, 07 §3.1-3.3/§3.4, 09 F09.4, integrator guide, tb READMEs, PR body; docs gates | R416-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |

## Real limits

- **Verilator identity.** The named scoped binary `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` did not exist. I used a byte-identical copy of the manager-lane 5.050 wrapper, which resolves to Verilator 5.050 rev v5.050, with `verilator_bin` sha256 44898b22…bfdd (`receipts/tool_identity.txt`). The author used 5.052.
- **Parallelism.** Every Verilator build was capped at `-j 8` by editing the `-j 0` in the Makefile of the exported scratch tree only; nothing else changed.
- **Not run by me:** `run_suites.sh` as a whole and the 31 suites that consume no changed RTL (disallowed as a full bank; only pp_top and ucpu consume the changed files); `d3_mutants.py`; `lint_hdl.sh` in full; `make check`'s `lint`/`wavedrom-check`/`stale` legs; Yosys; the parent consumer set and `milan_dp` (including the nxndv observation).
- **gsi_mutants.py:** started, but it exceeded the foreground bound. I stopped it and deleted its partial output, so it is recorded as NOT RUN.
- **Author evidence.** The author's public receipts were fetched and match the published manifest hashes (`receipts/public_evidence_hashes.txt`). They are the author's, not re-execution.
- **Redaction.** Home-directory prefixes in the build logs were rewritten to `<HOME>`/`<TOOL_ROOT>` before hashing. Nothing else in any receipt was changed.
- No hosted CI context inspected. No hardware. Physical calibration NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Merge-turn candidate at live dev ccdd07b52bbbbfe6be9d8f5317e673a6907c375d with the combined #132 + C1 adaptation, including the donor bank and the parent consumer bank. The author's parent run was at dev ec0cc0c1, not ccdd07b5.
- Hosted/act acceptance.
- `d3_mutants`, `gsi_mutants` and the unchanged suites at this head.
- Route the parent-side nxndv STREAM_INPUT 1 face/image `current_format` disagreement to parent tracking.
- Carry F1 and F2 into the pin-adoption lane's parent-visible record once resolved.
- Post the parent consumer bank result: still running per comment 5915872144.

## Clone integrity after probes

Every probe ran in exported scratch trees; the review clone was never written.
- HEAD, the index `write-tree` and the worktree all equal tree `f90877d2037fda973553b0ef1b75f29a7e0a6365`.
- `git status --porcelain --ignored` is empty.
- On-disk mode bits match all 389 tracked entries.
- The tree has no gitlinks (mode 160000), so no submodule pin applies.
- Receipt: `receipts/clone_integrity.txt`.

R416-1 FINISHED
