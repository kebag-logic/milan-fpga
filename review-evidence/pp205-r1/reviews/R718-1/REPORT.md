[R718] POSITIVE - exact head 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f

# R718-1: external independent review of processor PR #207 (issue #205)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #207, issue #205
- Exact head `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f`, tree `317c13456cdceac6cdcda6e7b40992c40e300b5f` (verified in the isolated clone)
- Base: processor main `097a79875f20c27f0a5987a193c165c5086f3cf5`. Reviewed delta: `git diff 097a7987..7bad3943` (6 files, +135/−28; receipt `receipts/diff.patch`)
- Commits: `c7250d6` (the change) and `7bad394` (the talker README re-measure, README only)
- Role: external reviewer, cleared context. All execution ran in disposable copies under the packet's scratch area. The reviewed clone was never written; its integrity check is at the end.

## Verdict

POSITIVE. A GET_TX_STATE_COMMAND whose `talker_unique_id` is out of range or names a disabled source is now answered TALKER_UNKNOWN_ID with the command's `listener_entity_id` and `listener_unique_id`. Every other field of that response follows Milan v1.2 Table 5.46. The success response keeps Table 5.47's zero listener fields. No other ACMP response changed. The new cases fail on the base RTL, and every new mutant arm is killed. The docs and design comments are current. The parent consumer receipts are complete with rc 0, and I re-ran both idiom checkers with rc 0. There is no top-level port, parameter or register-map change.

I have one open item, a SUGGESTION (F1). It does not affect the verdict. There are no BLOCKER, MAJOR, MINOR or RESIDUE findings.

## Prior public review findings

At the time of this review, PR #207 had no review findings: no PR reviews, no inline review comments, and only two review-start notices (R717-1 and R718-1). Issue #205 has the assignment, TAKEN and REVIEW READY comments. No manager evidence comment is posted yet. So there is nothing to resolve or retain.

## Assignment checks (1)–(7)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | TALKER_UNKNOWN_ID for an unknown `talker_unique_id` echoes `listener_entity_id` and `listener_unique_id`; every other field follows Table 5.46 | MET | `hdl/acmp/KL_acmp_talker.sv:1632-1638`: the unknown arm sets the status and `pdu_leid_r`/`pdu_luid_r`. `:805-810`: the RX-slot fetch now also runs for `MT_GTX_ST_C && !uid_valid_w`. `:1580-1586`: the controller ID, talker ID (`own_entity_id_i`, which equals the command's because `talker_cmd_w` requires `target_eid == own_entity_id_i`), talker unique ID, sequence ID and message type (cmd\|1) are echoed. connection_count, flags and the stream fields are left at 0, which Table 5.46 allows because it marks them "Undefined". Talker suite at head: 1561/1561 PASS (`receipts/talker_head.log`). Full-top wire probe: byte-exact 70-byte frame (`receipts/wire_probe_head.log`) |
| 2 | The success response keeps Table 5.47's values | MET | `:1623-1631`: SUCCESS sets the listener fields to 0 explicitly; RF is live, and SID, DA and VLAN are as before. B2 (`tb/acmp_talker/sim_main.cpp:557`) sends L1/7 and expects 0/0. The wire probe's source-0 GET_TX_STATE gives status 0 with listener fields 0 |
| 3 | No other ACMP response's echo behaviour changed (PROBE_TX, DISCONNECT_TX, GET_TX_CONNECTION) | MET | The diff touches only the `MT_GTX_ST_C` arm and one `needs_pdu_w` term that is gated on `MT_GTX_ST_C`. The PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION arms are byte-identical to base. The wire probe at base and head gives byte-identical frames for PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION unknown-ID. Only GET_TX_STATE differs: base answers listener bytes 0, head echoes them (`receipts/wire_probe_base.log`, `receipts/wire_probe_head.log`). pp_top at head: 10753/10753 PASS (`receipts/pp_top_head.log`) |
| 4 | The new talker cases fail on the base, and the new mutant arm is killed by the driver | MET | Head testbench on base RTL (`097a7987` `KL_acmp_talker.sv`): rc 2, `1561 checks: 1557 PASS, 4 FAIL`, exactly C2 and H3 listener_eid/listener_uid answered 0 (`receipts/talker_newtb_on_base_rtl.log`). `acmp_mutants.py --only` on the three `TX_STATE_ECHO` arms: 3/3 KILLED by their named checks with 4/4/2 failing checks, golden PASS (`receipts/new_arms/`). The full ACMP campaign at head gives 101/101 KILLED and 8 goldens PASS, identical to the author's receipt row by row (`receipts/acmp_full.log`) |
| 5 | Design comments and docs no longer describe the old behaviour | MET | Each comment the issue cited at `ed211803` (`:24`, `:671`, `:1246-1247`) is rewritten at head (`:21-30`, `:800-804`, `:1553-1558`). A repo-wide search for GET_TX_STATE/listener-zeroing wording finds only success-scoped statements. The F05.11 leaves (`docs/architecture/05_acmp_engine.md:420-421`), the new paragraph (`:431-438`), REQ-ACMP-008 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:405`), the talker README (`:22-28`, `:245-248`, `:367-392`) and the driver docstring are all current |
| 6 | Parent consumer gate (with the #202 wiring patch), including `check_cpp_idiom.py` and `check_py_idiom.py`, passed | MET (author receipts; partial independent re-run) | Published receipts (`review-evidence/pp205-r1/author/receipts/parent/`): scratch parent `876a55b9` = dev `97aab1d0` + gitlink `7bad3943` + patch sha256 `ff5068d2…1275` (70,091 bytes, recorded identical to the commit). All 17 steps exit 0, `runner.rc` 0, suite tally 16,534 checks, 0 failures. I re-ran both idiom checkers on a scratch parent at dev `97aab1d0` with this head as the gitlink and gPTP at its pin, without the #202 patch: both rc 0 (`receipts/parent_cpp_idiom_head.log`, `receipts/parent_py_idiom_head.log`). My cpp count is 348 units against the author's 349, the one file the patch adds |
| 7 | No top-level port, parameter or register-map change | MET | Only 6 files change, and no `hdl/top`, `hdl/common`, `syn` or `scripts` file is touched. The `KL_acmp_talker` module header (parameters and ports, 182 lines) is byte-identical between base and head |

## Findings

### F1: SUGGESTION. GET_TX_STATE decides "fetch or not" one clock before it decides the status, from the live `cfg_src_en_i`

- **Lenses:** RTL, Robustness
- **Location:** `hdl/acmp/KL_acmp_talker.sv:787-788` (`uid_valid_w` reads `cfg_src_en_i[tsrc_w]` combinationally), `:805-810` and `:1128` (fetch decided at `S_TXN_REC`), `:1621-1638` (status decided at `S_TXN_ACT`), `:1115-1116` (PDU registers cleared at dispatch)
- **Evidence:** I put a disposable probe in a scratch copy of the talker suite (`scripts/race_probe.py`, `receipts/race_probe_head.log`). It sends GET_TX_STATE for enabled source 2 with listener fields `F1E2D3C4B5A69788`/`8C17` and clears that source's enable bit k clocks after the consume edge:
  - k=0: TALKER_UNKNOWN_ID with the echo.
  - k=1: TALKER_UNKNOWN_ID with listener fields **0/0**. The source was valid when the fetch was skipped and invalid when the status was composed.
  - k=2 and k=3: SUCCESS with 0/0.

  The graded suite still passes 1561/1561 with the probe inserted.
- **Authority:** Milan v1.2 5.5.4.3 step 1 and Table 5.46. The same window exists before this change on the PROBE_TX interface-mismatch path, which does not fetch: `:806-807`.
- **Impact:** Very low. The window is one clock and only opens while the integrator changes a talker-source enable. `docs/guides/integrator.md:259-261` and `docs/architecture/02_interfaces.md:116-118` make that group quasi-static (set before `entity_enable_i`), which puts the window outside the documented operating envelope. However, the suite's phase H and the #202 text exercise and describe a run-time disable.
- **Suggested outcome (optional, not required for merge):** take the GET_TX_STATE validity once. For example, register `uid_valid_w` at `S_TXN_REC` and compose from the registered value, or fetch for every GET_TX_STATE. Either keeps the Table 5.46 echo exact in the window. Any follow-up could also cover the PROBE_TX path.
- **Verification:** with the change, the same probe shows TALKER_UNKNOWN_ID with the echo, or SUCCESS with 0/0, for every k.

### Considered and not raised

- **Clause citation.** The issue and the assignment cite IEEE 1722.1-2021 8.2.4, which is the ACMP *Listener* state machine. The delta cites 8.2.5.3 / Figure 8-4 (ACMP Talker state machine, GET STATE: `response = rcvdCmdResp; error = TALKER_UNKNOWN_ID`) and `txResponse` 8.2.5.2.3. I checked both against the standard's text, and the delta's citation is the correct one. The PR body explains the difference.
- **Comment rule.** I scanned every added comment line in `.sv`, `.cpp` and `.py`. None carries a bench lane label, lane name, review round, reviewer ID or issue-comment ID. The only label-shaped token, "(C2 and H3 grade the echo)" at `tb/acmp_talker/sim_main.cpp:556`, names this suite's own case IDs, the same IDs its check strings use. That is the suite's existing idiom, for example "B3's state again" at `:603` on base, so it is not RESIDUE.
- **`// idle values only: every response below sets its listener fields`** (`:1569`). This is true: every arm that sets `resp_valid_o` sets both listener fields. The only arm that leaves them at the default, a PROBE_TX interface mismatch, sends no response.
- **Stale data.** The new fetch path cannot echo bytes from a previous command. The PDU registers are cleared at every dispatch (`:1115-1117`), and bytes past the slot length read as 0 (`:1137-1139`). My plant that removes the clearing survives the graded suite, but the clearing is pre-existing and outside this delta.

## Lens evidence

### Conformance

- I extracted Milan v1.2 5.5.4.3 and Tables 5.40, 5.44, 5.46, 5.47 and 5.48 from the specification text. In Tables 5.40, 5.44 and 5.46, `listener_entity_id` and `listener_unique_id` are "Same value as in the … COMMAND message", and connection_count, the three flags and the stream fields are "Undefined". Table 5.47 gives `listener_entity_id` 00:00:00:00:00:00:00:00 and `listener_unique_id` 0.
- In IEEE 1722.1-2021 8.2.5.3, Figure 8-4, the GET STATE invalid branch is `response = rcvdCmdResp; error = TALKER_UNKNOWN_ID`. `txResponse` (8.2.5.2.3) "sets the ACMPDU fields to the values from the response parameter".
- The RTL matches all of these. Wire-level confirmation is in `receipts/wire_probe_head.log`: `fc 05 10 2c` gives msg 5 and status 2 (TALKER_UNKNOWN_ID), and listener bytes 42..49 `f1 e2 d3 c4 b5 a6 97 88` and 52..53 `8c 17` are echoed.
- REQ-ACMP-008 now states both responses and is tagged from B2, C2 and H3. `make check` (reqtags and matrix) gives rc 0.

### RTL

- I read the delta and its full context: the walker FSM `:1087-1165`, the response compose `:1552-1649`, the RX-slot face `:1716-1719`, and the top latch `hdl/top/protocol_processor_top.sv:3376-3418`, which passes every talker response field to the 56-byte ACMPDU unchanged.
- The talker lint at head is clean (`receipts/talker_lint_head.log`), and `scripts/lint_hdl.sh` gives rc 0 (`receipts/lint_hdl_head.log`).
- The interface is unchanged (check 7). The fetch adds the existing 13-clock RX read to the refusal only. A successful GET_TX_STATE still goes from `S_TXN_REC` straight to `S_TXN_ACT`.
- Open: F1 (SUGGESTION).

### Robustness

- I ran 11 disposable plants of my own on the talker (`scripts/probe_mutants.py`, `receipts/own_probes.json`, `receipts/own_probes/`). The `control_unmodified` row is the unplanted control, and it PASSES 1561/1561 (the driver labels it "SURVIVED").
- KILLED, each failing exactly 2 checks:
  - eid-only echo
  - uid-only echo
  - eid byte rotation
  - uid byte swap
  - refusal also echoing the command's flags
  - refusal reporting the declared Stream ID
  - fetch only for an out-of-range ID, which leaves a disabled source unfetched. H3 is the case that kills this one.
- SURVIVED as expected-equivalent: the success arm's explicit zeros removed, or replaced by the unfetched PDU registers. Both are equivalent because success never fetches and the registers are cleared at dispatch. The new explicit zeros make the success arm independent of that invariant.
- SURVIVED, pre-existing and outside the delta: dispatch clearing removed.
- The race probe is under F1.

### Tests

- Talker suite: 1545 → 1561 checks. The +16 are H3's consume check, pop check and 14 field checks. C2 now carries distinct listener values `F1E2D3C4B5A69788`/`8C17` in place of L1/2 with an expected 0, and every byte is distinct, so a lane swap is caught. H3 is new. B2 now carries REQ-ACMP-008.
- Head testbench on base RTL: exactly the 4 listener-field checks fail.
- New arms: 3/3 KILLED at 4, 4 and 2.
- Full ACMP campaign: 101/101 KILLED, 8 goldens PASS (`receipts/acmp_full.log`, run 08:26:58Z–08:58:22Z, `--jobs 4`).
- Talker retry campaign at head: PASS, with 62 killed, 7 equivalence controls and 1 performance control. Baseline and restored are each 1561/1561. `no_command_ready` fails 782 and `no_get_tx_state_response` fails 144. All 62 killed rows and the performance row match the README table (`receipts/retry_full.log`, `receipts/retry/`, `receipts/retry_table_vs_run.txt`).
- pp_top (all seven builds): 10753/10753 PASS.
- `make check`: rc 0.
- Test gap, not raised: pp_top has no TALKER_UNKNOWN_ID case for any talker command. The PR states this. My scratch-only wire probe through the full top closes the question for this review, but it is not a committed test.

### Docs

- The F05.11 leaves and the new paragraph in 05, REQ-ACMP-008, the talker README case list, the check count, the #205 section (arm table and measured counts) and the retry re-measure note all agree with what I measured at this head.
- The README figures (1561 checks, 4 base failures, arm counts 4/4/2, retry 782/144, baseline and restored 1561) are reproduced above.
- The PR body's line map and its gate tables match the receipts and my runs. The PR body notes the issue's 8.2.4 citation correctly.
- No stale description of the old behaviour remains (check 5).

## Commands run (exact head unless stated; pinned simulator 5.050, wrapper sha256 `905795b9…e92f`, `--version` "Verilator 5.050 2026-07-01 rev v5.050")

| Run | rc / result | Receipt |
|---|---|---|
| `make -C tb/acmp_talker run` (head) | 0, 1561/1561 PASS | `receipts/talker_head.log` |
| `make -C tb/acmp_talker lint` (head) | 0 | `receipts/talker_lint_head.log` |
| `make -C tb/acmp_talker run` (base `097a7987`) | 0, 1545/1545 PASS | `receipts/talker_base.log` |
| head testbench + base `KL_acmp_talker.sv` | 2, 1557 PASS 4 FAIL (C2 and H3 listener fields) | `receipts/talker_newtb_on_base_rtl.log` |
| `acmp_mutants.py --only` the three TX_STATE_ECHO arms `--jobs 3` | 0, 3/3 KILLED, golden PASS | `receipts/new_arms.log`, `receipts/new_arms/` |
| `acmp_mutants.py` full campaign `--jobs 4` | 0, 101/101 KILLED, goldens PASS | `receipts/acmp_full.log`, `receipts/acmp_full/` |
| `retry_mutants.py --jobs 6` | 0, 62 killed / 7 equivalent / 1 performance | `receipts/retry_full.log`, `receipts/retry/` |
| `make -C tb/pp_top -j8` (seven builds) | 0, 10753/10753 PASS | `receipts/pp_top_head.log` |
| `make check` | 0 | `receipts/make_check_head.log` |
| `scripts/lint_hdl.sh` | 0 | `receipts/lint_hdl_head.log` |
| reviewer fault plants (11) | see Robustness | `receipts/own_probes.json`, `receipts/own_probes/` |
| reviewer race probe | 0 (graded suite unchanged); k=1 shows F1 | `receipts/race_probe_head.log` |
| reviewer wire probe, pp_top `--acmp-only`, head | 0, 63 checks 0 failures; four refusals byte-exact | `receipts/wire_probe_head.log` |
| reviewer wire probe, base | 1, only GET_TX_STATE unknown-ID differs (listener bytes 0) | `receipts/wire_probe_base.log` |
| first wire-probe attempt (head and base) | superseded: the probe expected status 1, but TALKER_UNKNOWN_ID is 2. Kept for the record; apart from that byte, it shows the same result | `receipts/wire_probe_*_status1_attempt.*` |
| parent `check_cpp_idiom.py` and `check_py_idiom.py` (dev `97aab1d0` + gitlink `7bad3943`, no #202 patch) | 0 and 0 | `receipts/parent_*_idiom_head.*` |
| hosted check runs at the exact head (read 08:59:00Z) | docs-gates ×2 and portability ×2 completed success; suites ×2 **in progress**, not concluded | `receipts/hosted_check_runs.tsv` |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.5.4.1–5.5.4.4 and Tables 5.40/5.44/5.46/5.47/5.48; IEEE 1722.1-2021 8.2.5.2.3 and 8.2.5.3 (Figure 8-4); RTL compose `:1580-1646`; REQ-ACMP-008 row; wire probe base vs head | R718-1 | 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f |
| RTL | CLEAN (F1 SUGGESTION open, non-blocking) | `hdl/acmp/KL_acmp_talker.sv` delta and context `:21-30`, `:787-810`, `:1087-1165`, `:1552-1649`, `:1716-1719`; the top's response latch `:3370-3418`; module header diff; lint and lint_hdl | R718-1 | 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f |
| Robustness | CLEAN (F1 SUGGESTION open, non-blocking) | 11 fault plants; race probe k=0..3; stale-data and truncated-PDU paths; slot-free timing | R718-1 | 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f |
| Tests | CLEAN | `tb/acmp_talker/sim_main.cpp` B2/C2/H3; head testbench on base RTL; TX_STATE_ECHO arms; full ACMP campaign; retry campaign vs README table; pp_top seven builds; `make check`; author receipts `review-evidence/pp205-r1` at `d96469cc` | R718-1 | 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f |
| Docs | CLEAN | `docs/architecture/05_acmp_engine.md:404-438`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:405`; `tb/acmp_talker/README.md:5-28, 239-248, 279-315, 367-392`; `tb/pp_top/acmp_mutants.py` docstring; design comments; repo-wide stale-wording search; comment-rule scan; PR body vs receipts | R718-1 | 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f |

## Real limits

- **No manager source bank** runs at this head, and none is claimed. Source-head execution evidence is the author's published receipts plus my own focused runs listed above. I did not run full parent, processor, gPTP, Yosys or builder banks.
- **Parent consumer gate:** I did not re-run it. Check 6 rests on the author's published receipts (17/17 rc 0). My independent re-run covers only the two idiom checkers, without the #202 wiring patch, because the patch bytes were not in my scope.
- **Hosted CI at the exact head:** the two `suites` runs were still in progress when read. Only docs-gates and portability had concluded (success). The manager owns hosted and act acceptance.
- **Not hardware proof:** physical calibration was NOT RUN, and field skips are not hardware proof. The release-image observation (`ed211803`) is reproduced only in simulation, by the base wire probe. No hardware was used.
- **Reviewer probes are not committed tests:** the wire probe and race probe ran in scratch copies only.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, from source base `097a7987` against live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, with the #202 wiring patch until the sixth pin adoption lands. Publish those receipts on the PR. That candidate is distinct from this source-head review.
- Confirm that the hosted `suites` runs at `7bad3943` conclude successfully.
- Decide whether F1 (SUGGESTION) becomes a follow-up issue.
- Collect the second independent review (R717-1) before merge.

## Reviewed-clone integrity after probes

- No probe touched the reviewed clone; every probe used separate scratch copies.
- Final check (`receipts/reviewed_clone_integrity.txt`):
  - HEAD `7bad3943…`, tree `317c1345…`
  - `git status --porcelain --ignored`: 0 lines
  - index equals the HEAD tree (mode, blob and path)
  - 720 working-tree blobs re-hashed, 0 mismatches
  - the processor tree has no gitlinks
- The parent's `protocol-processor` gitlink exists only in my disposable scratch parent, set to `7bad3943`.

R718-1 FINISHED
