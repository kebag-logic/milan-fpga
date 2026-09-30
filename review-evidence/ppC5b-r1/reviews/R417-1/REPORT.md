[R417] NEGATIVE - exact head 54c1e2b11c90e7063fc5882b15ddea5e4335d411

# R417-1: external independent review of PR #138 (lane C5b, AECP dispatch and response)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #138, assignment issue #76 comment 5906184962.
- Exact head: `54c1e2b11c90e7063fc5882b15ddea5e4335d411`, tree `f90877d2037fda973553b0ef1b75f29a7e0a6365`.
- Base: `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff`. Eight commits: b5fd772, b87007b, 692ad8f, 13a001f, 9c3cdb7, 596ab8e, 344daec, 54c1e2b.
- Round: R417-1. Public start notice: PR #138 comment 5915630914.
- The PR closes #50, #53, #74, #76 and #82.

## Verdict

**NEGATIVE.** Two MINOR findings are open, so the RTL, Robustness, Tests and Docs lenses are unclean.

The five issues' own acceptance lists are all met at this head. The conformance reading of every controller-visible change is correct. All 33 processor suites pass, and so do all processor entry points I ran. The author's mutation campaign reproduces arm for arm: 29 of 29 KILLED on their named checks, control PASS, rc 0.

The two findings are both in code this PR adds:

- **F1.** The new 561-byte line floor admits lines at which a whole GET_AUDIO_MAP page is written past the response-buffer reservation the documents give the integrator.
- **F2.** SET_CONTROL's out-of-range `BAD_ARGUMENTS` body changed. The change is not graded, and the PR's parent-visible list does not name it.

Neither finding affects the parent's shipping shape (`PP_DESC_LINE_BYTES_P` = 576; the behaviour in F2 is conformant). Both are small to close.

## Reconstruction (order followed)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` (checked the tree). The contribution rules I found are:
   - `docs/README.md`: single-source rules, spec-citation rules, and the rule that `make check` must pass;
   - `README.md` "Building and checking": `run_suites.sh`, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`.
2. **Scope.** Issue bodies #76, #74, #53, #50 and #82 (frozen acceptance lists), and the assignment comment 5906184962. That comment includes the STOP rule, the parent-visible list duty and the gates.
3. **Linked authorities.**
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md`: GAP-01, GAP-08, REQ-AEM-001/-014/-020, REQ-FWX-001, REQ-MDL-001..011.
   - Architecture 01 F01.5, 03 §7/§7.1, 06 §3/§6.1/§6.5/§6.8/§8, and 07 §3.
   - Integrator guide, parameter and reservation tables.
   - Clauses cited: IEEE 1722.1-2021 §7.2.3/.6/.32, §7.4.21.1/.23.1/.25.1, §7.4.44, Table 7-141, §9.3.5.3.3; Milan v1.2 §5.4.1, §5.4.2.13/.15/.17/.26.
4. **Diff.** `git diff 0451d83d..54c1e2b` (50 files, +2404/−149) and each commit. I read all of it: the RTL/µcode, `tb/pp_top/sim_main.cpp` (A5b, M9, section AX), `tb/ucpu`, `aecp_mutants.py` with all 29 patches, `check_m9_opcodes.py`, `check_upc_map.py`, `run_suites.sh` and every document hunk.
5. **Public executable evidence.** kebag-logic/milan-fpga@d10fd5d8 `review-evidence/ppC5b-r1`. Hashes were verified against its `MANIFEST.json` (see `receipts/00-environment.txt`). The files are the author's HANDOFF, PR body, parent adaptation patch, suite receipt, AECP and D3 mutant receipts, and parent-gate receipt at dev `ec0cc0c1`.
   - That directory holds no manager bank receipts.
   - No manager evidence comments are on the issue or the PR beyond the review-start notices.
6. **Prior public review findings on PR #138.** None: no review objects, no review comments, and only the two start notices. None are carried in or out.

## Findings

### F1 [MINOR]: the 561-byte line floor admits a GET_AUDIO_MAP page written past the documented response-buffer reservation

- **Lenses:** RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_engine.sv:918` (floor check on the rounded `RESP_BUF_C`);
  - `hdl/aecp/KL_aecp_engine.sv:1671` (`RESP_D8_CAP_BYTES_P = RESP_BUF_C`);
  - `hdl/aecp/KL_aecp_engine.sv:900` (`RESP_BUF_C = (16 + LINE_BYTES_P)` rounded up to 16);
  - `hdl/aecp/KL_aecp_ucpu.sv:276-282` (`append_cap_w`, `append_skip_w`);
  - `docs/guides/integrator.md:86` ("At least 561") against `docs/guides/integrator.md:214` (reserve `16 + DESC_LINE_BYTES_P` bytes);
  - `docs/architecture/07_memory_maps.md:309`, `docs/architecture/03_packet_engine.md:299`, and `hdl/top/protocol_processor_top.sv:165` (same `16 + LINE` reservation);
  - `docs/architecture/06_aecp_engine.md:107` (the 561 floor).
- **Authority.** The integrator contract says the processor writes only `16 + DESC_LINE_BYTES_P` bytes at `RESP_BASE_P`, and that "Nothing else may write here" applies to that region alone (integrator guide, 07 §3.3.2, the top's `RESP_BASE_P` banner). The parent restates it as "a SECOND window, 16 + PP_DESC_LINE_BYTES_P bytes wide ... an overlap here is silent corruption" (milan-fpga `hdl/milan/milan_datapath.sv`, dev ccdd07b5, lines 335-340).
- **Evidence.**
  - The new floor refuses a line only when the **rounded** buffer is below 592. The new D8 `APPEND` fills up to that rounded buffer. For a line of 561 to 575 bytes the processor therefore writes up to byte 591, past the `16 + LINE` bytes the integrator was told to reserve.
  - Before this PR no response wrote past `16 + LINE`: the largest READ_DESCRIPTOR is `16 + LINE`, and `APPEND` stopped at 524.
  - Probe B (`probe_line561.py`, raw log `receipts/probes/probeB-line561-aecp-dispatch.log`) binds `DESC_LINE_BYTES_P` to 561 in a scratch copy of the wrap. It shrinks AX's single 576-byte configuration-1 descriptor to 536 bytes so the image is legal at that line, and records every strobed response-memory write.
  - Result: elaboration passes; A5b+M9 697/0 and AX 189/0; after PG the highest byte offset written is **591**, against a documented reservation of offsets 0..576 (16 + 561 = 577 bytes). That is a 15-byte write outside the reservation.
  - No bench check notices. The bench's response-memory model silently drops writes beyond its 592-byte array and never checks writes against the `16 + LINE` bound.
- **Impact.** Latent memory corruption, for an integrator who uses the newly documented minimum or any line from 561 to 575. It reaches up to 15 bytes of whatever the integrator placed after the reservation. The parent (576) is not affected.
- **Required outcome (either one):**
  - make the floor and the D8 cap agree with the documented reservation: refuse `16 + LINE_BYTES_P < 24 + 8·GAMAP_PAGE_MAX_C` (a floor of 576), or cap D8 at `16 + LINE_BYTES_P`; or
  - change the documented reservation everywhere (integrator guide, 07 §3.3.2, 03 §7.1, the top banner) to the rounded buffer size and state the new floor consistently.

  Add a check or fixture that response writes stay within the documented reservation at a non-default line.
- **Verification.** Probe B, or an equivalent in-tree fixture:
  - at the new minimum line, the highest response-buffer byte written by a maximal GET_AUDIO_MAP page is below the documented reservation; or
  - elaboration refuses that line.

### F2 [MINOR]: SET_CONTROL's out-of-range BAD_ARGUMENTS body changed; the change is ungraded and missing from the parent-visible list

- **Lenses:** Tests, Docs.
- **Where:**
  - `hdl/aecp/ucode/gen_ucode.py:1818-1819`: the out-of-range arm now branches to the shared tail `SCTRL_EMIT`. It no longer goes to the zero-bodied `E_BADARG1`.
  - `docs/architecture/06_aecp_engine.md:737`: "The same shared tail answers SET_CONTROL's out-of-range `BAD_ARGUMENTS` with the value in force".
  - `tb/pp_top/sim_main.cpp:7187-7198` (W13) checks only status and cdl, and only while IDENTIFY is 0.
  - The PR body's "Parent-visible" section lists only "The locked refusals now carry the value in force".
- **Authority.** IEEE 1722.1-2021 §7.4.25.1 ("the response always contains the current value ... the old value if it fails"). The head behaviour is conformant, so the Conformance lens is clean for this item.
- **Evidence.** Probe A (`probe_sctrl_badarg.py`; raw logs `receipts/probes/probeA-*.log`):
  - **(a)** A mutant that restores the base's zero body for this arm only leaves the **full default `tb/pp_top` run green: 8290 checks, 0 failures**, AX 189/0.
  - **(b)** One added check was run at the head and on the mutant. The holder sets IDENTIFY to 255, then SET_CONTROL(128) must answer BAD_ARGUMENTS carrying 255, byte-exact.
    - At the head it passes (AX 191/0).
    - On the mutant it fails: "status 7, cdl 17, body byte 0".
  - No other bench exercises SET_CONTROL (searched `tb/*`).
- **Impact.** A controller-visible response body changed without a grading arm. A regression back to the zero body would pass every suite. The pin-adoption lane is not told about this change, although it is told about the adjacent locked-refusal change.
- **Required outcome:**
  - a `tb/pp_top` arm that grades SET_CONTROL's out-of-range BAD_ARGUMENTS byte-exact while IDENTIFY holds a non-zero value, with the zero-body mutation recorded red;
  - the PR's parent-visible list names the change.
- **Verification.** The added arm passes at the head. A patch in the style of `aecp_mutations/` that branches the arm to `E_BADARG1` is KILLED on it. The PR body lists the change.

### S1 [SUGGESTION]: M9 gate self-test count in the docstrings

`scripts/check_m9_opcodes.py:24` and `:80` say the self-test has "three" failing fixtures. The code has four that must fail, plus the parse check: six in all, as the PR body says. Suggest correcting the text. No behaviour impact.

### S2 [SUGGESTION]: the D3-restore half of the READ_DESCRIPTOR current-value claim is not graded end to end

06 §6.1, 07 §3.3 and the parent-visible list say READ_DESCRIPTOR carries a row "a SET or the D3 restore" wrote. AX RD grades only SET-written rows.

The restore path uses the same `RGN_DYNV` valid bit. The dynamic-state and D3 benches grade that bit (for example the D3 `RPL_rate`/`RPL_clks`/`RPL_fmti` arms in the author's D3 receipt). So I rate this a suggestion, not a defect: one RD read after a restore that loads a saved rate would pin the claim.

## Per-issue acceptance (each issue's own list)

| Issue | Acceptance | Result at head | Evidence |
|---|---|---|---|
| #76 GAP-01 | 1. kOpcodes checked against every `OP_*_C` incl. the seven | met | `check_m9_opcodes.py`: PASS, 30 opcodes; selftest 6/6. Engine dispatch uses only `OP_*_C` constants (no literal opcode compare found). `receipts/01-pregates.log` |
| | 2. guard removed from each of the seven turns M9 red, recorded in README | met | seven `m9-guard-*` arms KILLED on `M9: mt=4 word XXXX` (9,9,9,7,7,7,7 failures), matching `tb/pp_top/README.md` |
| | 3. 03 §7 no longer promises a response-size ROM | met | 03 §7 now names the echo sizing and 06 §8.1/§8.2 |
| | 4. run_suites green | met | all 33 suites rc 0 (run per suite; see limits) |
| #74 REQ-FWX-001 | 1. A5b sends 0x002A, 0x0037-0x0039, 0x0047, 0x0048 and checks the byte-exact echo, cdl and wire length | met | A5b rows; command lengths match IEEE figures (4, 12, 8, 8, 12, 4) |
| | 2. a REBOOT SUCCESS arm turns a check red, recorded | met | `a5b-reboot-success-arm` KILLED (1 failure: the byte-exact echo) |
| #53 REQ-AEM-014 | 1. three foreign SETs under lock, ENTITY_LOCKED at cdl 17/20/20 | met | AX LK1/LK3/LK4 |
| | 2. nothing moved: GET old value, write/mark/notify unchanged; holder served | met | LK1/LK3 effect counters and no unsolicited frame; LK3 GETs; LK6 holder |
| | 3. body decided against Milan, stated in 06 §6.8, byte-exact | met | 06 §6.8; IEEE §7.4.21.1/.23.1/.25.1 value-in-force rule; LK byte-exact. See F2 for the adjacent BAD_ARGUMENTS arm |
| | 4. each CHECK_LOCK → NOP recorded red | met | six `lk-*` arms KILLED (9/1, 9/1, 9/1), plus the base reproduction (5) |
| #50 REQ-AEM-001 | 1. descriptor > 508 B, READ_DESCRIPTOR byte-exact, cdl > 524, via slot 4 | met | OV1/OV2/OV5 (576/536 B) byte-exact through slot 4, freed after; OV3/OV4 standard slot |
| | 2. `txs_oversize_o` forced 0 turns it red, recorded | met | `ov-oversize-never` KILLED (18); top routing tied off (18); `>=` at 576 (4) |
| | 3. page above 62: every record, or limit corrected | met (both) | PG1-PG6 served whole to 71; PG7-PG9 NO_RESOURCES with count 0; PG10 recovers |
| | 4. 06 §3 oversize rule matches GET_AVB_INFO / GET_AS_PATH / GET_AUDIO_MAP | met | 06 §3 per command. GET_AVB_INFO cdl 32 + 4k and GET_AS_PATH ≤ 8 ClockIdentities (cdl 80) re-derived from the IEEE layouts |
| #82 GAP-08 | 1. READ_DESCRIPTOR after each SET carries the GET's value, byte-exact | met | AX RD1 (rate, clock source 0 then 1, STREAM_INPUT 0, STREAM_OUTPUT 1); RD0/RD2 negative space |
| | 2. frame > 576 B, cdl > 524, byte-exact, slot 4 used and freed | met | OV1/OV2/OV5 |
| | 3. lint L1-L9 and Table 7-8 enforced in-repo or re-dispositioned to the consumer | met (re-dispositioned) | 00 §6.6 rows name the consumer's model (Ver "—"); 07 §3.1/§3.2/§3.3 |
| | 4. 07 §3.3 and 03 §7 state the Δ8 ceiling | met | both state the response buffer, cdl 592, 618-byte frame at the default line (see F1 for the reservation wording) |

## Parent-visible changes: conformance and scope judgement

| Change | Conformance | Scope |
|---|---|---|
| GET_AUDIO_MAP pages of 63-71 served whole (above cdl 524; slot 4 from 66); >71 NO_RESOURCES with count 0 | Correct. Milan §5.4.1 permits GET_AUDIO_MAP above cdl 524. At the base, `number_of_mappings` named records the response dropped, a real defect. Milan §5.4.2.26 bounds a subset at 176 but does not require one, and the integrator contract `P-MAP-SUBSET-CH-MAX` = 71 is documented (F01.5). NO_RESOURCES (Table 7-141, 8) with no record claimed is a sound refusal for a face that breaks that contract | Inside the lane: #50 acceptance 3's first option. The parent must adopt it knowingly; it is on the list. Arithmetic re-derived: cdl 24 + 8M > 524 from M = 63; frame 50 + 8M > 576 from M = 66; 24 + 8·71 = 592 |
| READ_DESCRIPTOR of configuration-0 AUDIO_UNIT, CLOCK_DOMAIN, STREAM_INPUT/OUTPUT carries stored current values | Correct. IEEE §7.2.3/§7.2.32/§7.2.6 current fields are what GET_SAMPLING_RATE/GET_CLOCK_SOURCE/GET_STREAM_FORMAT return. Field offsets re-derived from the IEEE layouts: 136, 70, 74; lanes 136..143, 72, 80..87. Unset rows keep the image. The overlay programs keep names coherent (probe C: SET_NAME plus SET_CLOCK_SOURCE on CLOCK_DOMAIN 0, byte-exact, AX 191/0) | Inside the lane: #82 acceptance 1. On the list |
| Locked refusals carry the value in force | Correct per IEEE §7.4.21.1/.23.1/.25.1. Milan adds the refusal and is silent on its body | Inside the lane: #53 acceptance 3. On the list |
| SET_CONTROL out-of-range BAD_ARGUMENTS carries the value in force | Correct, same clause | **Not on the list, and ungraded: F2** |
| `DESC_LINE_BYTES_P` gains a 561-byte elaboration floor | The floor is right for the rounded buffer but inconsistent with the documented reservation: **F1** | Disclosed ("576 is above the new 561-byte floor"). No port, parameter or register is added or removed, but the legal range of an existing top parameter narrows |

On the STOP rule: I found no port, parameter or register change. The behaviour changes are the ones the issues' own acceptance lists require. Each is disclosed except F2's. I read them as in-scope conformance fixes that the pin-adoption lane must adopt knowingly. Whether that satisfies the assignment's STOP wording is the manager's call.

**The author's reading of the parent's 8x8 shape.** Checked in public milan-fpga dev ccdd07b5:

- `hdl/milan/milan_datapath.sv` answers a Stream Port Output with `AMAP_OUT_NMAPS_C = 1` and walks `AMAP_OUT_KEYS_C = N_STREAMS * 8` stream-channel keys. That is one subset of up to 64 stream channels at 8x8, as the author says.
- Whether a single port actually reaches 63 or more mappings depends on cross-stream output mappings: the parent's own comment says "a Stream Output has at most eight audio channels". Either way the page is at most 64, which is below 71, so no parent shape reaches NO_RESOURCES.
- `PP_DESC_LINE_BYTES_P` = 576 (`milan_datapath.sv:330`; the builder packs at 576). That is above the 561 floor, and at 576 the F1 overrun does not occur.
- The parent's input `map_page` is bounded 1..11 (`sw/builder/endstation_builder.py`).

**The nxndv observation.** `tb/verilator/milan_dp/gen_divergent_shape.py` (dev ccdd07b5) is a deliberately divergent verification shape. It gives input row 1 a different format base in the face header, and the image is not rebuilt to match it. So GET_STREAM_FORMAT (face) and READ_DESCRIPTOR (image, while unset) disagreeing there before a SET is a property of that test leg, not of a shipping shape.

- The processor's row-sourced overlay is the right choice: it never reports a value the processor did not store.
- No processor action is needed. I agree with the author's classification.
- The author's parent-gate receipt records the face-sourced cut failing that leg at 344daec and the head passing it. That is author evidence at dev `ec0cc0c1`; I did not run it.

## Lens ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 1722.1-2021 §7.2.3/.6/.32, §7.4.21.1/.23.1/.25.1, §7.4.44 and Table 7-141 status 8; Milan §5.4.1, §5.4.2.13/.15/.17/.26; IEEE figure command lengths for 0x002A/0x0037-0x0039/0x0047/0x0048. Checked against E_SSRATE/E_SCLKS/E_SCTRL, E_GAMAP, E_RDESCAU/CD/SI/SO/SF, A5b rows, 06 §3/§6.1/§6.8 and F01.5 | R417-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| RTL | UNCLEAN (F1) | `KL_aecp_engine.sv`: floor, D8 cap, re-dispatch seam `cdl >= 20 && cfg 0`, µPC constants. `KL_aecp_ucpu.sv`: `append_cap_w`, batch exclusion, COPY_BUF TAIL count incl. the zero-count path; no prior `cnd` use on COPY_BUF/APPEND. `ucpu_pkg.sv`: `GAMAP_PAGE_MAX_C`. `gen_ucode.py`: every changed program. Name-table coherence of the overlays: probe C | R417-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Robustness | UNCLEAN (F1) | Response-buffer write bound at the new floor (probe B: offset 591 against the 577-byte reservation); page cap on the 16-bit count (PG9: 256, low byte 0); locked miss path; too-short descriptor fallbacks; configuration guard | R417-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Tests | UNCLEAN (F1, F2) | All 33 suites rc 0, 1,017,540 checks (pp_top 8,310; ucpu 398). Pre-gates rc 0. `make aecp-dispatch` rc 0 (886/0). `aecp_mutants.py` single full run rc 0: 29/29 KILLED on named checks, control PASS, identical to the author's receipt arm by arm. The driver applies patch files to a scratch copy and reads only logs (all 29 patches touch `hdl/` only, restored between arms). Fixture guards 4/4 in the pp_top run. `test_gen_desc_image.py` 6/6. Probes A/B/C | R417-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |
| Docs | UNCLEAN (F1, F2) | 00 §5/§6.6 rows, 01 F01.5, 03 §7, 06 §3/§6.1/§6.5/§6.8/µISA/F06.14, 07 §3.2/§3.3/§3.4 table, 09 F09.4, integrator guide, `tb/pp_top/README.md` (mutation table matches my counts), `tb/ucpu/README.md`, PR body parent-visible list. `make check` rc 0 and `gen_matrix.py --check` rc 0 | R417-1 | 54c1e2b11c90e7063fc5882b15ddea5e4335d411 |

## Commands run (all in the foreground, all restricted to 8 CPUs)

| Command | rc | Result | Receipt |
|---|---:|---|---|
| `check_upc_map.py`; `check_m9_opcodes.py --selftest`; `check_m9_opcodes.py` | 0/0/0 | 58 constants / 86 entry points; selftest 6/6; 30 opcodes | `receipts/01-pregates.log` |
| `make` in each of the 33 `tb/*` suites (the `run_suites.sh` loop body), via `run_suite_subset.sh` | 0 each | 1,017,540 checks, 0 FAIL | `receipts/02-suites-batch*.txt`, `receipts/suites/` |
| `python3 tb/pp_top/aecp_mutants.py` (all arms, one invocation, TMPDIR in the packet scratch) | 0 | 30/30 (control + 29 KILLED), 398 s | `receipts/03-mutants-full.txt`, `receipts/mutants/full/`, `receipts/03-mutants-compare.txt` |
| same, `--only` three M9 arms (timing trial) | 0 | 4/4 | `receipts/03-mutants-c1.txt`, `receipts/mutants/c1/` |
| `scripts/lint_hdl.sh`; `make check`; `gen_matrix.py --check`; `tb/desc_store/test_gen_desc_image.py` | 0/0/0/0 | lint OK; docs gates OK; matrix OK; 6 tests OK | `receipts/06-entrypoints.txt` |
| `make -C tb/pp_top aecp-dispatch` | 0 | A5b+M9 697/0, AX 189/0 | `receipts/07-aecp-dispatch.log` |
| Probe B `probe_line561.py` | 0 | max write offset 591 at line 561 (F1) | `receipts/04-probe-line561.txt`, `receipts/probes/probeB-*` |
| Probe A `probe_sctrl_badarg.py` (head-check, mutant-check, mutant-suite) | 0/1/0 | head passes the added check; mutant fails only it; mutant passes the full suite (F2) | `receipts/05-*`, `receipts/probes/probeA-*` |
| Probe C `probe_name_and_overlay.py` | 0 | name plus clock-source overlay byte-exact | `receipts/08-probe-name-overlay.txt`, `receipts/probes/probeC-*` |
| `verify_clone.sh` after all probes | 0 | 389 tracked paths re-hashed equal to HEAD blobs, modes equal, index tree = f90877d2, no untracked or ignored entries, 0 gitlinks | `receipts/09-clone-verify.txt` |

Build outputs created in the clone were removed with `git clean -fdX` after I confirmed they were only ignored build outputs: before the run the clone had none.

## Real limits

- **Tool substitution.** The assignment's scoped Verilator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used a byte-identical copy of the sibling manager wrapper instead: all 216 pinned-tool-bin wrappers under `$VALIDATION_STORAGE` share sha256 `905795b9…`, and the wrapper reports Verilator 5.050 rev v5.050. The author ran 5.052.
- **Suite runs.** `run_suites.sh` was not run as one invocation because of the per-command time bound. Its two pre-gates and the same `make` in each suite ran separately. My runner lists the Makefile-less `tb/common` as "MISSING"; `run_suites.sh` skips that directory by design.
- **Campaigns not re-run.** I did not re-run the other processor campaigns: `d3_mutants.py` (author receipt 83/83), `gsi_mutants.py`, `name_wr_mutant.py`, `srp_top`/`adp_engine`/`srp_admission`/`acmp_talker` mutants, `desc_mem_guard/mutate.py`, `nvm_port` figures. I also did not run the Yosys run, the parent consumer set, the donor bank, the builder, or hosted/act. The assignment forbids these, or they are outside this PR's AECP surface. They are author-claimed or manager-owned.
- **Hosted CI.** At the exact head, docs-gates and portability were success in both runs (36745878948, 36745905838). The `suites` job was still in progress in both at review time. I did not judge hosted acceptance.
- **No hardware.** No hardware was used. Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- Donor bank and parent consumer bank at milan-fpga dev ccdd07b5 with the combined #132 + C1 adaptation. The only public parent receipt is the author's, at dev ec0cc0c1.
- The final current-dev candidate at the merge turn: source base 0451d83d, live dev ccdd07b5.
- Hosted/act acceptance, including the two in-progress `suites` jobs.
- The public manager bank receipts that the assignment says passed at this head are not in `review-evidence/ppC5b-r1`@d10fd5d8. Publish or link them.
- Second independent review (R416) and the full completion bar before merge.
- Closure of F1 and F2 in a new round at a new exact head.

R417-1 FINISHED
