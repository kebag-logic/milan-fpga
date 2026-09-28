[R387] POSITIVE - exact head e8bf5e080e4b7d586d0484427ec2ef4fe9c51744

# R387-1: external review of PR #613 (issues #606 and #608)

- Head under review: `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744`, tree `46521875e09c5e460544fbec061ed7a21d0f8f56`, source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
- Role: external independent reviewer, cleared context, isolated detached clone.
- Scope source: issue #606 body and the lane assignment comment 5865930182 (frozen scope items 1 to 6), the #608 decision comments, and processor PR #129's body (copied as `receipts/processor-pr129-body.md`).
- Authorities read: AGENTS.md, CONTRIBUTING.md sections 3 and 6, docs/README.md, docs/reference/SUBMODULES.md, the processor's 05_acmp_engine.md, 02_interfaces.md, 08_timing.md and 10_srp_engine.md at `c951a9ff`, Milan v1.2 sections 4.2.7.2.2, 5.3.7.5 (Table 5.3) and 5.5.4.1, IEEE 802.1Q-2014 sections 10.7.5.20 and 10.7.6.6 and Table 10-5, and IEEE 1722.1-2021's ACMP status table (TALKER_DEST_MAC_FAIL = 3).
- Prior public review findings on PR #613: none. At the end of this pass the PR carries only the two review-start notices; there are no review bodies and no inline comments. Nothing to resolve or retain.

## Verdict summary

No BLOCKER, MAJOR or MINOR finding. Four SUGGESTIONs, which do not affect lens coverage.

The six assigned judgements:

1. **Pin and records.** The gitlink is exactly `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`: one stage-0 `160000` record, and the checkout is clean at that commit. Regenerating both ROMs at the pin reproduces the two new `rom_digests.tsv` rows byte for byte, and the ledger stays sorted. SUBMODULES.md, the drawio source (a pin-text-only diff), the SVG, the PNG and the manifest are re-recorded. `check_submodule_docs`, `submodule_boundaries.gen.py --check` and `check_diagram_pngs` all return 0. Hosted `rtl-fast`, `yosys-elaboration` and all four Yosys shards already concluded `success` on this exact head.
2. **[H] and [I].** Both match PR #129's reconciliation text, and neither is weakened beyond what that text requires. Details are under Conformance and Tests below.
3. **Evidence row.** The DUT-reader row is byte-identical to the text supplied in PR #129. `measure_test_evidence.py --check` returns 0. Removing the row in memory returns 1 with "1 unexplained DUT-source reader", so the row is necessary.
4. **Regressions.** Both fail at `16be6768` and pass at `c951a9ff`, which I re-ran myself. I also ran each fix in isolation, and each regression fails exactly when its own named fix is absent (see the matrix below).
5. **Capture.** `check_nvm_capture.py` returns 0: census, clocks, both timing arms and receipt agree, and every planted control is detected. No re-measurement is owed under scope item 5.
6. **Issue links.** The PR body says "Relates to #606. Relates to #608.", `closingIssuesReferences` is empty, and no closing keyword is present. The commit is one line with no trailers.

## Regression attribution matrix (re-run by this reviewer)

Each arm uses the exact committed parent bytes (`git archive` of the head) with the processor checked out at the named revision. Each arm runs the `run-crf` recipe unchanged, under pinned Verilator 5.050.

| Processor revision | Contains | `--first-probe-only` (37 checks) | `--crf-stop-only` (31 checks) |
|---|---|---|---|
| `16be6768` (old pin) | neither fix | FAIL, 14 failures: both sources status 3, DA 0, VID 0 | FAIL, 6 failures: registrar LV at deadline+1 ms, licence still open, 4 late frames, stop count 1 not 2, total 2 not 3 |
| `97bd3786` (PR #130 merge) | LeaveAll fix only | FAIL, same 14 failures | PASS 31/31 |
| `8eefb7b9` (PR #129 tip before main merge) | DA retry fix only | PASS 37/37 | FAIL, same 6 failures |
| `c951a9ff` (new pin) | both | PASS 37/37: DA `91e0f0004f32` and `91e0f0004f33`, status 0 | PASS 31/31: stops 0 to 1 to 2 to 3, zero late frames |

The old-pin arms exit with rc 2 from make and rc 1 from the binary. Each run printed its completed `pp_shadow: N checks, M failures` line, so these are completed behavioural assertions, not build failures. Receipts: `receipts/arm-*.txt`, `receipts/arm_summary.txt`, `receipts/logs/*.first-probe.log` and `receipts/logs/*.crf-stop.log`.

## Findings

### S1: SUGGESTION, Docs: no CHANGELOG entry for processor pin `c951a9ff`
- Where: `CHANGELOG.md:11` and `CHANGELOG.md:36`. The newest processor-pin section is still "Unreleased - processor pin 16be6768".
- Evidence: this adoption changes shipped behaviour that is visible on the wire. Every enabled source now acquires its DA in 100 ms rounds, and own-LeaveAll registrar aging moves to transmit acceptance. The pin commits for `16be6768`, `990f9652` and several earlier pins each added a CHANGELOG entry. Precedent is not uniform, though: the `09f9bf38` and `a8f8ce81` pin commits added none. The behaviour itself is recorded in the authoritative pin reference, `docs/reference/SUBMODULES.md:73-81`, and neither the frozen scope nor CONTRIBUTING requires a changelog entry.
- Impact: a reader using the changelog as the product revision record does not see the #606 and #608 behaviour change.
- Suggested outcome: add an "Unreleased - processor pin c951a9ff" entry, either here or with the bench re-measure that follows on the next image.
- Verification: `gen_toc.py --check` and `check_em_dash.py` stay at 0.

### S2: SUGGESTION, Tests: probe-response matching could be tighter
- Where: `tb/verilator/pp_shadow/sim_main.cpp:2013-2018` (`grade_first_probe` keeps the last matching response) and `:1937-1941` ([H] searches every retained frame, not only frames after its own probe; this code predates the PR and is unchanged).
- Evidence: each window injects exactly one probe, so today the result is the same either way.
- Impact: if a future change emits a second or stale CONNECT_TX_RESPONSE, the grade could read a frame other than the reply to the probe under test.
- Suggested outcome: require exactly one response for that source, among frames that egress after the probe.
- Verification: the old-pin arm still fails and the new-pin arm still passes.

### S3: SUGGESTION, Tests: an unknown harness argument silently runs the full suite
- Where: `tb/verilator/pp_shadow/sim_main.cpp:3826-3831`.
- Evidence: a mistyped `SIM_ARGS` (for example `--first-probe`) falls through to the full run, which passes.
- Impact: a replay command with a typo looks like a green focused regression. The damage is limited, because the full `run-crf` leg includes both regressions.
- Suggested outcome: reject any argument that is not recognised.

### S4: SUGGESTION, Docs: clause citation form
- Where: `tb/verilator/pp_shadow/README.md:419` ("Milan 4.2.7.2.2").
- Evidence: CONTRIBUTING section 6 asks for the `(Milan Section N)` form. `docs_check.py` does not enforce this form, and the clause itself is correct (Milan v1.2 section 4.2.7.2.2, "Instantaneous transition from IN to MT").

## Lens results (each applied at the exact head)

[R387] PASS Conformance - `tb/verilator/pp_shadow/sim_main.cpp:1904-1947` ([H]), `:1949-2031` ([I] and `grade_first_probe`), `:2033-2190` (CRF_STOP), processor `05_acmp_engine.md` section 6bis and `10_srp_engine.md` section 6.5 at `c951a9ff`, the PR #129 body, Milan v1.2 sections 4.2.7.2.2, 5.3.7.5 (Table 5.3) and 5.5.4.1, 802.1Q-2014 sections 10.7.5.20 and 10.7.6.6 and Table 10-5, and 1722.1-2021's status table.

- **[H]** still observes an accepted request, its refusal (`h_acc > 0`, `h_acc == h_ans`, zero grants), the closed DA gate, the status-3 PROBE_TX response and continuing command service (KLPP side port, RX counter +1). It waits `100*PP_MS_CYCLES + N*(1024+64)` clocks, which is one T-ACMP-DA-RETRY round plus the sweep, and it no longer requires a probe-caused request within 4000 cycles. That matches the reconciliation exactly.
- **[I]** pairs each response with the source index of its accepted request, using the new read-only `pp_maap_req_src_w` probe. This pairing is sound because the shim's `req_ready_o = ~rsp_valid_o` means a new request is never accepted in the same cycle as a response. [I] counts per-source grants from a snapshot taken before `MAAP_CTRL` enable, requires exactly one base-plus-index grant per source, and then requires the first probe to succeed. No third-probe wording remains in the tree (repository-wide search).
- **ACMP retry.** Milan Table 5.3 has MAAP allocate a DA for each Stream Output. Milan 5.5.4.1 step 3 and 1722.1 status 3 make the pre-acquisition refusal honest. Automatic per-source acquisition from the parent's claimed block adds no wire traffic.
- **LeaveAll.** 802.1Q-2014 section 10.7.6.6 and Table 10-5 generate rLA! against the registrars at the sLA transmit action (tx! in Active), not at leavealltimer! expiry. Moving the aging to transmit acceptance therefore conforms. Milan 4.2.7.2.2 (IN / rLv! gives MT) is the transition the #608 regression relies on, and the LV + rLv behaviour is left unchanged, as the #608 decision says.
- The first-probe response is also checked for SID `{station MAC, uid}`, DA base+index and VID 2 (Milan 4.2.7.2.1 Class A default).
- All six assigned criteria are met, as summarised above.

[R387] PASS RTL - `protocol-processor` gitlink `c951a9ff` (`git diff 16be6768 c951a9ff -- hdl`: only `hdl/acmp/KL_acmp_talker.sv` and `hdl/srp/{KL_srp_top,KL_srp_encoder,KL_srp_talker_fsm,KL_srp_listener_fsm}.sv` change; `hdl/top`, `hdl/maap`, `hdl/common`, `hdl/packet_engine`, `hdl/adp` and `hdl/aecp` are unchanged), `hdl/milan/KL_pp_maap_shim.sv:175-223`, and `tb/verilator/pp_shadow/recovery_probes.vlt`.

- No parent `hdl/` file changes. The processor's top-level ports and parameters are unchanged, so the parent integration contract (`KL_pp_shadow`, the one-cycle shim) holds.
- The retry timebase `now_ms_w` is generated inside `protocol_processor_top`, which meets the integrator's running-timebase requirement.
- The processor is a single clock domain, so no CDC is introduced.
- `.vlt` adds only `public_flat_rd` observation of four signals, and only in this testbench.
- `check_port_contracts.py` and `pp_srcs.py --check` return 0.
- The timer index (`CAD_LA_MSRP_C = 3`) and the registrar encoding (`R_IN_C = 1`, source 1 at `reg_r[3:2]`) that the harness reads were checked against `KL_srp_top.sv:245-250` and `KL_srp_talker_fsm.sv:200-201,376`.
- Hosted `yosys-elaboration` and Yosys shards 0 to 3 concluded `success` on this head.

[R387] PASS Robustness - `receipts/withdrawal_latency.txt`, `receipts/logs/lat-*.log`, `receipts/logs/new-c951a9ff.crflic.log`, `sim_main.cpp:2102-2190`.

- The harness compresses protocol time to 100 clocks per ms while one CRF PDU is 49,152 clocks. I therefore measured the real stop latency. In all three phases the licence is off 409 clocks after the pre-injection mark, and that count includes the 400-clock injection tail. The one-PDU bound is met by a wide margin and does not depend on any millisecond timer.
- At the old pin, the expiry-window licence never drops.
- The regression covers reset before the sequence, repeated start/stop (three withdrawals, counted 1, 2, 3, with no duplicate stop across a 2 s hold), the timer-expiry race anchored to the real `cad_dl_r[3]` deadline plus 1 ms, and the pre-acquisition refusal path ([H]).
- One consumer that depends on the changed behaviour, milan_dp `crflic` (first PROBE_TX refused, then licence), passes 415/415 at the new pin.

[R387] PASS Tests - `receipts/arm_summary.txt` (the 2x2 matrix above), `receipts/mutants.txt`, `receipts/logs/mut-*.log`, `receipts/logs/new-c951a9ff.{full-crf,run-base,run-vid73,run-pending}.log`, and `receipts/gate-measure_test_evidence*.log`.

- Each regression fails for the defect it names and for no other: the first-probe arm fails only without the PR #129 change, and the CRF arm fails only without the PR #130 change.
- Three planted parent defects, each in a disposable copy:
  - The shim drops `+ source` from the DA. [I] fails on source 1's grant and its first-probe DA (2 failures).
  - STREAM_STOP is not incremented. 7 failures.
  - The CRF framer ignores the licence. The late-frame check fails in all three phases, which shows it is independent of the licence-bit check.
- All four default legs pass at the new pin: 635 + 595 + 595 + 295 = 2,120 checks, 0 failures, matching the author's count.
- The evidence-table negative control fails without the row.
- Weaker spots are filed as S2 and S3.

[R387] PASS Docs - `tb/verilator/pp_shadow/README.md` (contents entry, H/I table rows, the new "Processor recovery regressions" section), `docs/reference/SUBMODULES.md:25,64,73-81`, `docs/diagrams/submodule_boundaries.{drawio,svg,png}` and `PNG_MANIFEST.json`, `CHANGELOG.md`, and the PR #613 body.

- The README states the retry-round allowance, the pairing rule, grants from enable, the first-probe rule and the CRF_STOP procedure. It also states the limit "ordering and a cycle bound, not physical latency" and the focused replay commands. I re-ran those commands and they behave as described. The stale third-probe note is removed.
- The following gates return 0: `docs_check.py`, `gen_toc.py --check` (114 pages), `check_em_dash.py --base 54ce8773` (0 findings over 70 added lines), `check_submodule_docs.py`, `submodule_boundaries.gen.py --check` and `check_diagram_pngs.py`.
- The PR body carries the old and new-pin evidence and the relate-only links.
- Non-blocking items are filed as S1 and S4.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | pp_shadow [H]/[I]/CRF_STOP source; PR #129 reconciliation; processor 05/10 docs at `c951a9ff`; Milan v1.2 4.2.7.2.2, Table 5.3, 5.5.4.1; 802.1Q-2014 10.7.6.6/Table 10-5; 1722.1-2021 ACMP status | R387-1 | `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744` |
| RTL | CLEAN | processor hdl diff `16be6768..c951a9ff`; unchanged top/maap ports; `KL_pp_maap_shim.sv`; `recovery_probes.vlt`; port-contract and source-list gates; hosted Yosys at head | R387-1 | `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744` |
| Robustness | CLEAN | withdrawal latency probe; expiry-race anchor; repeated stop/start and hold; milan_dp crflic at new pin | R387-1 | `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744` |
| Tests | CLEAN (S2, S3 optional) | 2x2 attribution matrix; 3 planted parent defects; four pp_shadow legs (2,120 checks); evidence-row negative control | R387-1 | `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744` |
| Docs | CLEAN (S1, S4 optional) | pp_shadow README; SUBMODULES.md; boundary diagram set and manifest; CHANGELOG; PR body; docs/TOC/em-dash/diagram gates | R387-1 | `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744` |

## Real limits

- **Tool path.** The assigned Verilator path, `<data>/tmp/372-manager-candidate1/pinned-tool-bin/verilator`, does not exist. I used a scratch wrapper that execs the same pinned install that every other `pinned-tool-bin/verilator` wrapper on this host targets (one install root, `verilator --version` = `Verilator 5.050 2026-07-01 rev v5.050`; `verilator_bin` sha256 `44898b22...bbfdd`; see `receipts/verilator_identity.txt`). `scripts/verilator-j8` changes only `--build -j 0` to `-j 8`, to respect the parallel-job cap.
- **Gate invocation.** The first gate batch ran with `python -I`. That hid the scripts' sibling imports and the renderer lock, so `check_nvm_capture`, `check_diagram_pngs`, `check_em_dash` and `gen_toc` failed at import time (`receipts/gates_summary.txt`). Rerun normally with the configured Markdown environment, all of them return 0 (`receipts/gates_summary_rerun.txt`).
- **Scope of runs.** I did not run the full parent, processor, gPTP, Yosys or builder banks; the manager's banks cover those. My runs were focused: the pp_shadow legs, milan_dp `crflic`, and the record, documentation and evidence gates.
- **Hosted checks.** Snapshot at 2026-09-28T09:01Z (`receipts/hosted_checks_snapshot.tsv`). `rtl-fast`, `yosys-elaboration`, Yosys shards 0 to 3, Verilator shards 0 and 3, `verilator-lint`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate` concluded `success`. Verilator shards 1, 2 and 4, `docs-check` and `elaborate` were still in progress. "Physical gPTP (nightly and manual)" was skipped, which is not a pass.
- **Physical evidence.** Physical calibration was NOT RUN, and no hardware was touched. All timing here is simulation cycles with compressed protocol milliseconds, not bench latency.
- **Merge base.** This review covers the source base `54ce8773` only. The merge candidate against live dev `0eff6d2e` has not been reviewed.

## Pending manager duties

- Accept the remaining hosted contexts on this exact head, and run the local act replica per CI_WORKFLOWS.
- Build and validate the current-dev merge candidate (base `54ce8773`, live dev `0eff6d2e`), then carry out post-merge containment.
- Obtain the internal lane review. Merge only with explicit maintainer authorization.
- Keep #606 and #608 open for the bench re-measure on the next image: #606 item 3 (first bind and long hold against 1 s) and #608 item 3 (100/100 stops within one PDU, with STREAM_STOP counted).

## Clone integrity after probes

HEAD, index tree and head tree are all `46521875e09c5e460544fbec061ed7a21d0f8f56`. `git status` is empty. There are no assume-unchanged or skip-worktree flags. All 943 tracked non-gitlink blobs hash to their index ids (897 with mode 100644, 46 with mode 100755), and `git diff-files` is clean. The gitlinks are `protocol-processor` `c951a9ff`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e` and `external` `efeb541a` (not initialised, unchanged), and the processor checkout is clean at `c951a9ff`. All probes ran in disposable copies under `scratch/`. See `receipts/clone_integrity.txt`.

## Reproduction

From the packet root, with `PINNED_VERILATOR` pointing at a Verilator 5.050 wrapper:

```sh
scripts/arm.sh <clone> new-c951a9ff c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 scratch scripts/verilator-j8 crf-stop
scripts/arm.sh <clone> old-16be6768 16be6768f710e79450aace277abacd6c2c3336e5 scratch scripts/verilator-j8 crf-stop
scripts/arm.sh <clone> only608-97bd3786 97bd3786 scratch scripts/verilator-j8 crf-stop
scripts/arm.sh <clone> only606-8eefb7b 8eefb7b scratch scripts/verilator-j8 crf-stop
scripts/mutant.sh scratch/new-c951a9ff scratch scripts/verilator-j8 <name> <file> '<sed-expr>' <--first-probe-only|--crf-stop-only>
python3 scripts/latency_probe.py <copy>/tb/verilator/pp_shadow/sim_main.cpp
(cd <clone> && python3 <packet>/scripts/evidence_norow_control.py)
```

R387-1 FINISHED
