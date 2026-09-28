[R386] POSITIVE - exact head e8bf5e080e4b7d586d0484427ec2ef4fe9c51744

Round R386-1, internal cleared-context review of PR #613 for issues #606 and #608.
Head `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744`, tree `46521875e09c5e460544fbec061ed7a21d0f8f56`, source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five are clean.
Open findings: none at MINOR or above. Three SUGGESTIONs (S1 to S3) are listed below.

## Reconstruction

- Contract: AGENTS.md sections 3 to 8 and CONTRIBUTING.md 2.1 to 3.
- Scope: the #606 assignment (issue comment 5865930182), the #606 and #608 analysis comments (5860869610, 5860869482), and the #608 decision reading acceptance 3 as "within one PDU period of a withdrawal that reaches an IN registrar".
- Authority: processor PR #129 body (reconciliation for [H] and [I], and the disposition text), processor architecture 02 section 8, 05 section 6bis, 08 (T-ACMP-DA-RETRY) and 10 section 6.5 (sLA and the Milan registrar deviation) at `c951a9ff`.
- Reviewed the diff `54ce8773..e8bf5e08` (12 files, one commit) and the processor diff `16be6768..c951a9ff`.
- Evidence: the executor's REVIEW READY comment (5866525479) and the public packet `review-evidence/606-608-r1` at `55aaa21f` (final-results.json, old-pin-provenance.json, final-old-crf.log).
- Prior public findings on this PR: none. After my own pass, the PR has 0 reviews, 0 review comments, and only the two review-start markers. Nothing to resolve or retain.

## Assignment items

1. **Pin and records.** The gitlink is exactly `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` (mode 160000, stage 0), and it contains `97bd3786` (PR #130). Records verified:
   - SUBMODULES.md table and history are updated.
   - drawio, svg and png are updated. The rendered PNG reads `pin c951a9ff0cb5`.
   - PNG_MANIFEST source and raster hashes verify (`check_diagram_pngs.py` rc 0).
   - `rom_digests.tsv` gains two rows. They equal the sha256 of `ltn_rom.hex` and `ucode.hex` generated at the new pin (receipt 21). The ledger stays sorted, and all other pins' rows are retained.
   - `check_submodule_docs`, `submodule_boundaries.gen.py --check`, `pp_srcs --check --selftest`, `check_rtl_source_lists`, `check_port_contracts`, `check_cpp_idiom` and `docs_check` all return rc 0 (receipts 30-*).
2. **[H] and [I] match the PR #129 text.**
   - [H] waits `100*PP_MS_CYCLES + N*(1024+64)`, which is one T-ACMP-DA-RETRY round plus the sweep. It requires an accepted request, all answers refused, a shut DA gate, the PROBE_TX reaching the processor, side-port service, and status 3 on the wire. It no longer requires a probe-caused request within 4000 cycles, which the processor change requires.
   - [I] pairs each response with its accepted request's `pp_maap_req_src_w`. It counts per-source grants from before `MAAP_CTRL` enable, so grants during ANNOUNCE polling count, and each source must receive exactly one grant equal to base plus index. The third-probe wording is gone from code and README.
   - Neither check is weakened beyond what the processor contract requires.
3. **Disposition row.** The `retry_mutants.py` row equals the PR #129 text byte for byte after string concatenation. `measure_test_evidence --check` returns rc 0. With the row removed in scratch it returns rc 1 and reports `retry_mutants.py: UNEXPLAINED` (receipt 31).
4. **Both regressions re-run by me with identical committed parent sources.**

   | Arm | Old pin `16be6768` | New pin `c951a9ff` |
   |---|---|---|
   | `run-crf SIM_ARGS=--first-probe-only` | 37 checks, 14 failures. No auto-acquisition, and both first probes return status 3 with DA 0. make rc 2 | 37 checks, 0 failures. Status 0, SID, DA base+s and VID 2, with no probe-caused grant |
   | `run-crf SIM_ARGS=--crf-stop-only` | 31 checks, 6 failures. The registrar reads LV (2) at deadline+1 ms, the licence stays open, 4 late frames, and STREAM_STOP is missed. make rc 2 | 31 checks, 0 failures. Three withdrawals, each stopping within one PDU, count 0 to 3 |

   All four legs at the new pin pass: 595 + 595 + 635 + 295 = 2,120 checks, 0 failures (receipt 20). These numbers match the executor's claims and the published old-pin log.
5. **Capture check.** `check_nvm_capture.py` returns rc 0: census, clocks, both timing arms and the receipt agree, and every planted control is detected (receipt 30).
6. **Issue linkage.** The PR body says "Relates to #606. Relates to #608." `closingIssuesReferences` is empty, and neither the body nor the one-line commit message (no trailers) has a closing keyword.

## Protocol judgement

- **IEEE 802.1Q LeaveAll (Table 10-5, sLA action).** The rLA! applied to the participant's own registrars belongs to the sLA transmit action, not to leavealltimer! expiry. Aging IN to LV at expiry, as `16be6768` did, opened a window in which a Listener Lv found LV. Milan 4.2.7.2.2 (the Δ13 rule, IN to MT on rLv outside the LeaveAll cycle) was therefore bypassed, and the stream ran on the 5 s Milan LeaveTime. That matches the three bench non-stops.
- **The fix at `c951a9ff`.**
  - It keeps IN until preparation acceptance; my run reads registrar 1 at deadline+1 ms.
  - It still transmits the own LeaveAll. A scratch probe shows an MRPDU with LeaveAllEvent=1 egressing at about 10,203 ms against the 10,001 ms deadline (receipt 42).
  - LV + rLv semantics are unchanged.
- **IEEE 1722 Annex B MAAP.** The shim still grants only while KL_maap is in ANNOUNCE and the index is inside the count. ALLOC_DA retries are internal and cause no MAAP wire traffic.
- **IEEE 1722.1 ACMP.** Status 3 (TALKER_DEST_MAC_FAILED) is still returned honestly before acquisition. After acquisition, the first CONNECT_TX (PROBE_TX) response carries status 0, the stream_id, stream_dest_address (offset 54) and stream_vlan_id (offset 66), as the harness checks.

## Findings

S1 - SUGGESTION - Tests - `tb/verilator/pp_shadow/sim_main.cpp:1988-1996` - source 1's acquisition is sampled after source 0's probe, not at the bound
- Authority/evidence: the README says the bound "adds 1,088 clocks per enabled source", and processor 05 section 6bis promises every eligible source within one retry period plus the sweep. Receipt 41 shows `addr_valid` rising at cycle 166,110 and the bound (12,176) ending at about 179,650. Source 1 is checked only at 188,059. Scratch mutant M3b retries source 1 only every other round (receipts 56 and 57). It grants source 1 at 180,013, beyond the bound, and the arm still passes 37/0.
- Impact: at parent level, a one-round fairness or latency regression for a higher-index source is invisible. The #606 defect itself, a refused startup allocation that is never retried, is still caught (old pin: 14 failures).
- Suggested outcome: sample every source's grant count at the bound, before any probe.
- Verification: M3b fails the arm.

S2 - SUGGESTION - Docs - `CHANGELOG.md:11,36` - no product changelog entry for processor `c951a9ff`
- Authority/evidence: the three previous processor pin adoptions (#560, #569, #591) each added an "Unreleased - processor pin" entry. The processor documents the retry as a "consumer-visible timing change". No written rule requires the entry, and SUBMODULES.md carries the pin and the behaviour bullets.
- Impact: the changelog's newest processor entry still names `16be6768`.
- Suggested outcome: add an entry here, or with the bench re-measure.
- Verification: `docs_check.py` rc 0.

S3 - SUGGESTION - Tests - `tb/verilator/pp_shadow/sim_main.cpp:2129-2184` - the expiry-window phase does not itself assert that the own LeaveAll is still transmitted
- Authority/evidence: #608 item 3 says "without weakening ... LeaveAll recovery". The phase proves IN is retained at deadline+1 ms. It would also pass if the own LeaveAll never fired. My scratch probe shows the MRPDU egressing (receipt 42), and the processor suite carries the dedicated mutants.
- Suggested outcome: optionally assert that one own MSRP LeaveAll MRPDU egresses after the deadline.
- Verification: a no-own-LeaveAll processor mutant fails the arm.

## Clean-lens results

[R386] PASS Conformance - `protocol-processor` gitlink `c951a9ff`, `sim_main.cpp` groups H, I and CRF_STOP, processor 10 section 6.5 and 05 section 6bis, receipts 10-13 and 42 - all six assignment items and #606/#608 acceptance items 2 to 4 for simulation are met. The CRF stop applies to a withdrawal reaching IN, per the #608 decision. The processor behaviour agrees with 802.1Q Table 10-5 sLA, Milan 4.2.7.2.2, 1722 Annex B and 1722.1 ACMP status and field offsets.

[R386] PASS RTL - `protocol-processor/hdl/acmp/KL_acmp_talker.sv` diff `16be6768..c951a9ff`, `hdl/milan/KL_pp_maap_shim.sv:191-221`, `hdl/milan/milan_datapath.sv:3079-3084,3191-3218,5351`, receipt 20 - the parent RTL is unchanged. The `protocol_processor_top` ports and parameters are unchanged; the new ports are internal to the SRP encoder, and the `-Wall` build with no `-Wno` is clean. The retry round is wrap-safe (`now_ms - t0 >= 100`). The picker rotates. BACKOFF and DA_OK sources never allocate. A killed grant is released, not installed. The probes `cad_dl_r[3]` (CAD_LA_MSRP_C), `reg_r[1]` (1=IN, 2=LV) and `stop_r[1]` (CRF context N_STREAMS) read the intended signals.

[R386] PASS Robustness - `sim_main.cpp` observe() pairing (lines 247-286), `drain_maap_response`, `crf_withdraw_and_grade`, `grade_crf_stop_regression` reset path, receipts 12, 20, 51 and 53 - unpaired and out-of-range responses fail. RELEASE acknowledgements (ok=0) are neither grants nor refusals. A stuck response fails within four clocks. The CRF group resets the DUT and harness state and passes inside the full run-crf leg. The withdrawal bound counts injection time. The 2 s hold checks for duplicate stops. `--crf-stop-only` on a one-output build fails closed. Reset during the expiry window and reconnect are both exercised.

[R386] PASS Tests - `sim_main.cpp`, `Makefile:112,161`, `recovery_probes.vlt`, receipts 10-13 and 50-57 - both regressions fail at the old pin for the named defects (14 and 6 failures) and pass at the new pin. Parent-RTL mutant M1 (every source gets base+0) is killed by [I] (2 failures). Mutant M2 (CRF stop never counted) is killed (7 failures). The four legs total 2,120 checks with 0 failures. Probes are read-only; nothing is forced. S1 and S3 are optional strengthenings.

[R386] PASS Docs - `docs/reference/SUBMODULES.md:25,64-81`, `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json`, `tb/verilator/pp_shadow/README.md:21,134-135,386-442`, receipts 30 and 32 - the pin authority, diagram and README all agree with the head. The stale third-probe note is removed. The replay commands work as written. Remaining `16be6768` mentions (SAVED_STATE_*, `measurements.json`, the ROM ledger) are dated provenance or historical rows, not current-pin claims. S2 is optional.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlink; H, I and CRF_STOP groups; processor 05/08/10 and PR #129/#130 contract; IEEE 802.1Q Table 10-5, Milan 4.2.7.2.2, 1722 Annex B, 1722.1 ACMP; receipts 10-13, 42 | R386-1 | e8bf5e080e4b7d586d0484427ec2ef4fe9c51744 |
| RTL | CLEAN | KL_acmp_talker and SRP diffs at the new pin, KL_pp_maap_shim, milan_datapath talker-diag and CRF licence wiring, probe targets; receipt 20 | R386-1 | e8bf5e080e4b7d586d0484427ec2ef4fe9c51744 |
| Robustness | CLEAN | harness pairing, drain, withdrawal and reset paths; fail-closed argument handling; receipts 12, 20, 51, 53 | R386-1 | e8bf5e080e4b7d586d0484427ec2ef4fe9c51744 |
| Tests | CLEAN (S1, S3 optional) | old/new-pin arms, four-leg run, mutants M1, M2, M3 and M3b, disposition negative control; receipts 10-13, 20, 31, 50-57 | R386-1 | e8bf5e080e4b7d586d0484427ec2ef4fe9c51744 |
| Docs | CLEAN (S2 optional) | SUBMODULES.md, diagram trio and manifest, pp_shadow README, CHANGELOG, stale-pin census; receipts 30, 32 | R386-1 | e8bf5e080e4b7d586d0484427ec2ef4fe9c51744 |

## Limits

- **Tool path.** The assigned Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a wrapper that runs the same pinned binary as the byte-identical manager wrappers (sha256 `905795b9...`). It reports `Verilator 5.050 2026-07-01 rev v5.050` (receipt 00). The build parallelism was capped at 8 (`scripts/verilator-j8.sh`).
- **Not run:** Yosys, the builder bank, xvlog, the full parent, processor and gPTP banks, act, and hardware. I rely on the manager's and executor's public evidence for those.
- **Hosted checks** at this head were partly pending when snapshotted: 14 pass, 5 pending, 1 skipping (receipt 60). The skipped context is not execution evidence.
- **Simulation scope.** Protocol time is compressed to 100 clocks per millisecond. The simulations prove ordering and cycle bounds, not physical latency. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Old-pin arms ran in scratch clones.** The parent sources there were identical to this head, and only the processor checkout was moved.
- **Receipts** had the local toolchain root and home directory redacted (receipt 99).
- **Review clone integrity (receipt 90).** It was never modified. After the probes it was verified at HEAD and tree, with index and worktree clean, gitlinks at their pins, and submodules clean.

## Pending manager duties

- Hosted exact-head acceptance of `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check` and `elaborate`, and the act replica.
- The external review round.
- Candidate-merge validation against live dev `0eff6d2e`, since the source base is `54ce8773`.
- Post-merge containment.
- The bench re-measure for #606 item 3 and #608 item 3 on the next image. Both issues stay open.
- Deciding S1 to S3.

R386-1 FINISHED
