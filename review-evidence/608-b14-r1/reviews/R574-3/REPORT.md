[R574] POSITIVE - exact head 42399611fc2217014024f03f4ba0365fb072688c

# R574-3: internal independent re-review of PR #709 (issue #608, lane B14), round 3

- Head `42399611fc2217014024f03f4ba0365fb072688c`, tree `75729d9482463bbc42eed313026c9cae9442026a`. GitHub reports this as the PR head.
- Scope: the delta `d981b1cc..42399611`. It is one one-line commit that changes only `docs/findings/B14_BENCH_5603C353.md` (+27/-14). The PR body is also in scope.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. The round adds two RESIDUE items and one SUGGESTION.
- The five round-2 findings are resolved at this head: R574-2-F1/F2/F3 and R575-2-F1/F2. Both round-2 residues are applied, and R574-2-S1 is applied.
- Earlier rounds stand. The delta changes no measurement, figure or graded result.

## Reconstruction (public state only)

- I read `AGENTS.md`, `CONTRIBUTING.md` (section 6 and the gate list) and the issue #608 thread.
  - The B14 assignment is 6085135051. The SoC-board ruling is 6094000332.
  - The round-3 assignment is 6096487327. The executor's round-3 REVIEW READY is 6096601088.
- I read the PR #709 body at the head.
- Authorities:
  - Milan v1.2 Tables 5.4 and 5.6 as the repository quotes them;
  - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`, `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv` and `hdl/milan/milan_datapath.sv`;
  - `tests/features/counters_contract_milan.feature` and `docs/reference/REGISTER_MAP.md`.
- Evidence:
  - branch `608-b14-review-evidence`, packet commit `c848925d2e88a98e7f31b663e5dd4f342b765487` (author tree `da8818cbd06f40ae65abdf075ebab2e46a95b56f`);
  - round-2 recompute archive commit `273764dfe9147f6749908358032ef397f785e05c`.
- I did not open other reviewers' archived reports on the evidence branch.
- I made my independent pass over the diff, the code and the archive before reading the round-2 review comments. I then read those comments only to resolve or retain each finding (section "Prior findings at this head").

## Independent checks (receipts in this packet)

### 1. FRAMES observation (`:475-485`) against the head

Receipt: `receipts/frames-citations.txt`.

- **AAF listener.** `KL_avtp_rx_monitor_ctx.sv:318-323` declares the "USER 2026-08-05 FRAMES_RX law": the counter is published coalesced and advances by the interval's frame total.
  - `:627-630` commits `ram_q_r + frx_add_r` for FRAMES_RX. `:1150-1164` accumulates one per accepted frame and saturates at 16 bits.
  - The header `:28-36` says each counter moves "by AT MOST ONE" per interval. The page's statement that the declarations conflict is exact.
  - `milan_datapath.sv:6272` instantiates this module for the STREAM_INPUT block.
- **CRF listener.** `KL_crf_rx.sv:233` declares `pdu_count_o` as "FRAMES_RX: intervals with >= 1 accepted PDU". `:484-486` adds +1 per interval tick.
  - The wiring is `pdu_count_o` → `crf_pducnt_w` (`milan_datapath.sv:5890`) → GET_COUNTERS word 11 (`:3701`).
  - That block answers when the descriptor is STREAM_INPUT and its index is `CRF_SNK_IDX_C = N_STREAMS` (`:1756`, `:3686-3688`). That is STREAM_INPUT 1, as the page says.
- **Talkers.** `KL_talker_diag_ctx.sv:32-39` declares FRAMES_TX as an observation-interval count that advances at 1/s.
  - Both talkers feed it through the muxed PDU feed (`milan_datapath.sv:3281`, `:3300`, `:3667`).
- **Counters feature.**
  - `:194-201` is the Milan-Table-5.6 scenario: FRAMES_RX 1 for 8000 frames is graded "milan-interval".
  - `:393-408` is the Table 5.6 law outline: `FRAMES_RX 240060` over 30 s is graded INFO with the per-frame reading.
  - The page's line ranges are exact.
- **Figures** from archive `soak/summary.json`, `counter_deltas_first_to_last_poll`:
  - DUT `5|0` FRAMES_RX +57,599,387; `5|1` FRAMES_RX +7,200;
  - DUT `6|0` and `6|1` FRAMES_TX +7,200;
  - peer `5|0` +57,599,253 and peer `5|8` +3,599,953;
  - elapsed 7,200.535 s.
  - The peer's inputs 0 and 8 are bound to DUT talker uid 0 (AAF) and uid 1 (CRF) (`round2-recompute/outputs/final_vs_asfound.txt`). The page's peer attribution is correct.
- **Focused simulation** with the pinned simulator at the head (`receipts/rxmon-nx.log`, `receipts/rxmon-nx-run.log`):
  - Identity: Verilator 5.050 rev v5.050; wrapper SHA-256 `905795b9...e92f`.
  - Build: the `tb/verilator/avtp_rxmon` multi-stream bench, with the `verilog-axis` FIFO at the head's gitlink `48ff7a7e`.
  - Result: 118 checks, 0 failures. `[IV1b] FRAMES_RX += the burst's 6 frames (coalesced)` passes.
- **Disposable mutation** (`receipts/mutation-frx-plus1.diff`, `receipts/mutation-frx-plus1.log`):
  - On a scratch copy, the FRAMES_RX commit was changed from `frx_add_r` to `+1`.
  - The same bench reports 6 failures (`[IV0]`, `[IV1b]`, `[M13e2]`, s0/s1 coalesced). The bench separates the two laws, so "declares and implements" is backed by executable evidence.
- **PR body.** The first "Observations for triage" bullet states the same contracts and asserts no departure from a declared contract.

### 2. Every cited record exists

Receipts: `receipts/cited-paths.txt`, `receipts/archive-identity.txt`, `receipts/raw-inputs-check.txt`.

- **Cited paths.** `scripts/cited_paths.py` extracts 63 multi-segment packet paths from the page. All 63 exist in the author tree at `273764df`, including the 12 `round2-recompute/` paths; `NNN` is tested as a cycle glob. Missing: 0.
- **Removed citation.** `item4/summary.json` no longer appears on the page. `item4/short-summary-001-050.json` and `item4/short-summary-051-100.json` exist at `c848925d`.
- **Archive commit contents.** `273764df` descends from `c848925d`. Against its parent, it adds only the 19 `round2-recompute/` files and modifies the top-level `MANIFEST.json`. It changes nothing else under `author/`.
- **Manifest.**
  - `round2-recompute/MANIFEST.sha256` hashes to `65636059407702a12a5f7e09c7d28e3858f16d9ad65f6ce3261cafd4cb6489dc`, the digest the page cites.
  - `sha256sum -c` passes on all 18 entries.
  - The set of files equals the manifest's list, plus the manifest itself.
- **Rerun.** `round2-recompute/scripts/run_all.sh` ran against the author tree I extracted at `c848925d`, without the non-public captures. The rc is 0, and all five outputs are byte-identical (`receipts/round2-rerun.txt`).
- **Independent re-derivation** (`scripts/check_ta_lv.py`, `receipts/ta-lv-independent.txt`):
  - The re-decode's bridge `Lv` equals `item3/cycles.tsv` rounded to 1 us in 101 of 101 cycles, with the largest difference 0.498 us. "To the microsecond the re-decode prints, at most 0.498 us apart" is exact.
  - The DUT's Talker Advertise `Lv` appears in cycles 1, 2 and 42 only: 0.0390, 0.0951 and 0.3184 s after the bridge's `Lv`. It agrees with `dut_ta_lv_in_hold` in all 101 cycles.
- **Raw inputs.** `inputs/raw-inputs.tsv` matches the archived raw index on SHA-256, bytes and path in 103 of 103 rows.
  - The two included snapshots match `raw-index/soak.jsonl` lines 645 and 644 byte for byte, by digest.
- **Recomputed claims.** `final_vs_asfound.txt` gives 15 of 15 equal. `inventory_rows.txt` gives 44 of 44 equal, split 2/18/18/2/4. `slip_ledger.txt` gives 146 duplicates = 73 frames, with a final read of `0x92`. Each matches the page.
- **Privacy.** A scan of the archived `round2-recompute/` finds no MAC address or host name. The only 16-hex values in it are stream formats, the DUT's public entity ID and the DUT's CRF stream ID.

### 3. Gates at the head

Receipt: `receipts/doc-gates.txt`. All gates ran with the pinned Markdown environment, whose requirements hash equals `tools/markdown/requirements.txt`. All rc 0:

- `docs_check.py` (0 findings);
- `check_doc_style.py`;
- `gen_toc.py --check` and `gen_toc.py --verify-anchors` (423 anchors);
- `check_em_dash.py --base 5603c353` (704 added lines, 0 findings) and `--base d981b1cc` (27 lines, 0 findings);
- `check_doc_paths.py` (954 paths);
- `check_baremetal_only.py --check`;
- `git diff --check` against both bases.

Run details:

- The three renderer gates first failed in isolated mode, because the pinned venv resolves `six` from the user site. They were re-run without isolation. Both runs are recorded.
- The PR changes only the page, keeps five one-line commits with no merges, and leaves every submodule gitlink equal to the base.

## Findings

### R574-3-R1 RESIDUE: the manifest sentence says it lists every file, itself included

- Lenses: Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:691`, "`round2-recompute/MANIFEST.sha256` (...) lists every file there."
- Evidence: the manifest lists the 18 other files and not itself (`receipts/archive-identity.txt`).
- Impact: none on any figure or claim.
- Exact fix: "lists every other file there".

### R574-3-R2 RESIDUE: the PR body still speaks of the round-2 archive as future

- Lenses: Docs.
- Where: the PR #709 body.
  - The Evidence paragraph says the records "belong under `review-evidence/608-b14-r1/author/round2-recompute/` ..., added to the archive after `c848925d`".
  - The Round 3 table's R574-2-F2 row says "except the `round2-recompute/` paths, which exist once that folder is archived".
- Evidence: the folder is archived at `273764dfe9147f6749908358032ef397f785e05c`, with the cited manifest digest.
- Impact: none. The digest already pins the content.
- Exact fix:
  - Evidence paragraph: "The round 2 recompute records are archived under `review-evidence/608-b14-r1/author/round2-recompute/` at archive commit `273764df` (`MANIFEST.sha256` `65636059...89dc`)."
  - Round 3 row: "Every packet path the page cites exists at `c848925d`, and the `round2-recompute/` paths at `273764df`."

### R574-3-S1 SUGGESTION: name the round-2 archive commit on the page

- Lenses: Docs.
- Where: `:650` and `:690`.
- Detail: the page identifies the folder by path, by branch and by manifest digest. That pins the content, and the round-3 assignment asked for the path. Adding "archive commit `273764df`" would let a reader open the folder directly, as the page already does for `c848925d`.
- Optional.

## Prior findings at this head

| Finding | Status at `42399611` | Evidence |
|---|---|---|
| R574-2-F1 = R575-2-F1 (FRAMES contracts) | **Resolved.** Every required element is present at `:475-485`. The AAF frame-total law is cited as declared and implemented at `:318-323` and `:627-630`, under the 2026-08-05 ruling. The header conflict (`:28-36`) is stated. The CRF interval reading cites `KL_crf_rx.sv:233` and `milan_datapath.sv:3701`. The feature's INFO grading of a per-frame advance is cited (`:393-408`). The triage question asks about conformance and which declaration governs, with no asserted departure. The PR body bullet matches. Every line range is exact | section 1; `receipts/frames-citations.txt`, `receipts/rxmon-nx.log`, `receipts/mutation-frx-plus1.log` |
| R574-2-F2 (nonexistent `item4/summary.json`) | **Resolved.** The citation is replaced by the two `short-summary-*.json` files, which exist. The cited-path check finds 0 missing | `receipts/cited-paths.txt` |
| R574-2-F3 = R575-2-F2 (unarchived round-2 records) | **Resolved.** The records are archived at `273764df` under `review-evidence/608-b14-r1/author/round2-recompute/`. The manifest digest matches the page. Every cited path resolves. Every output reproduces byte for byte from the archived packet. The 0.5 us claim is restated exactly and reproduced independently. The non-public captures are named by hash and tied to the archived raw index, 103 of 103. My round-2 outcome asked for the archive commit to be named. The round-3 assignment asked for paths, and the page pins the content by digest. Naming the commit is carried as R574-3-R2 and R574-3-S1 | section 2 |
| R574-2-R1 = R575-2-R1 (register-map wording) | Applied (`:512`, "must be rendered "not supported" by software"), matching `REGISTER_MAP.md:482-484` | `receipts/frames-citations.txt` |
| R574-2-S1 (peer FRAMES_RX) | Applied (`:484`); figures verified | section 1 |
| R574-1-F2 to F6, R575-1-F1 to F4, and the round-1 residues | Resolved at `d981b1cc` (R574-2, R575-2). The delta touches none of their lines except the records table rows for items 3, 4 and 8 and the recompute paragraph, which are verified above. They remain resolved | `git diff d981b1cc..42399611` |
| R574-1-S1 = R575-1-S1 (findings index) | Open SUGGESTION, left to the manager | - |

## Lens results (each with the artifact examined at `42399611`)

```text
[R574] PASS Conformance - docs/findings/B14_BENCH_5603C353.md:475-485, :647-702; PR body - FRAMES_TX/FRAMES_RX statements against Milan v1.2 Tables 5.4/5.6 as quoted at KL_avtp_rx_monitor_ctx.sv:28-36 and KL_talker_diag_ctx.sv:32-39; soak/summary.json deltas at c848925d; the round-3 assignment items 1-3; cited records at 273764df (63/63 present)
[R574] PASS RTL - KL_avtp_rx_monitor_ctx.sv:28-36,318-325,627-630,1150-1164; KL_crf_rx.sv:233,484-486; milan_datapath.sv:1756,3686-3688,3701,5890,6272; KL_talker_diag_ctx.sv:32-39 - every cited line and the CRF/AAF serving paths traced; avtp_rxmon NxN bench 118/0 and the +1 mutation caught by 6 checks
[R574] PASS Robustness - round2-recompute/outputs/ta_lv_vs_cycles.txt, inputs/raw-inputs.tsv, inputs/snapshot-*.jsonl at 273764df - the 0.498 us rounding bound (101/101 equal at 1 us), TA Lv presence in all 101 cycles, the 103 raw inputs against the raw index on hash, size and path, the snapshot digests, and the privacy scan of the new archive folder
[R574] PASS Tests - round2-recompute/scripts/run_all.sh rerun from c848925d (rc 0, 5/5 byte-identical); scripts/check_ta_lv.py and scripts/check_raw_inputs.py (independent); tb/verilator/avtp_rxmon sim_main_nx.cpp at the head with the mutation control
[R574] PASS Docs - docs/findings/B14_BENCH_5603C353.md (delta +27/-14) and PR body; documentation gates rc 0 (receipts/doc-gates.txt); RESIDUE R574-3-R1 (:691) and R574-3-R2 (PR body); SUGGESTION R574-3-S1
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:475-485`, `:647-702`; PR body; Tables 5.4/5.6 as quoted in the repository; `soak/summary.json` (`c848925d`); round-3 assignment 6096487327; 63 cited paths at `273764df` | R574-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| RTL | CLEAN | `KL_avtp_rx_monitor_ctx.sv:28-36, 318-325, 627-630, 1150-1164`; `KL_crf_rx.sv:233, 484-486`; `milan_datapath.sv:1756, 3686-3688, 3701, 5890, 6272`; `KL_talker_diag_ctx.sv:32-39`; avtp_rxmon NxN simulation and mutation | R574-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Robustness | CLEAN | `ta_lv_vs_cycles.txt`, `ta_lv_all.txt`, `raw-inputs.tsv`, both snapshots, the privacy scan of `round2-recompute/` | R574-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Tests | CLEAN | `run_all.sh` rerun; `scripts/check_ta_lv.py`, `scripts/check_raw_inputs.py`, `scripts/cited_paths.py`; `tb/verilator/avtp_rxmon/sim_main_nx.cpp` (118/0; mutation 6 failures) | R574-3 | `42399611fc2217014024f03f4ba0365fb072688c` |
| Docs | CLEAN (RESIDUE R1, R2 carried) | the page delta and the full FRAMES and Evidence sections; the PR body; the documentation gates | R574-3 | `42399611fc2217014024f03f4ba0365fb072688c` |

- This round reviewed the delta and the statements it corrects, and covers all five lenses at the exact head.
- The page's unchanged round-1 content, covered by R574-2 at `d981b1cc`, is untouched by this commit except where re-verified above.

## Real limits

- **No bench access.** Physical calibration is NOT RUN. Field skips are not hardware proof. Every bench figure rests on the archived packet and its hash-indexed raw files.
- **Non-public captures.** The 101 item-3 tap captures are not public. I verified their digests against the archived raw index, not their bytes. The re-decode output `ta_lv_all.txt` was not regenerated from captures: only the packet-only half of `run_all.sh` ran.
- **Isolation of the renderer gates.** The three renderer-dependent documentation gates ran without isolated mode, because the pinned environment resolves one dependency from the user site.
- **No source bank.** No manager source bank runs at this head, and none is claimed or inferred. The source-head execution evidence is the author's published gate receipts plus the focused runs here.
- **Conformance ruling.** Whether the coalesced FRAMES_RX law conforms to Table 5.6 is not ruled here. The page leaves it for triage, which is correct.
- **Hosted runs, observed but not accepted** (`receipts/hosted-check-runs.tsv`):
  - success: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `wire-accountability`;
  - skipped by path filter: `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, physical gPTP;
  - `docs-check` was still in progress at the last read.

## Pending manager duties

- Accept the hosted and local-replica evidence at the exact head, including the in-progress `docs-check`.
- At the merge turn, build and validate the current-dev merge candidate (source base `5603c353`, live dev `e8454e27`) and publish its receipts.
- Carry R574-3-R1 and R574-3-R2 to the residue checklist.
- Rule on R574-1-S1 = R575-1-S1 (findings index).
- Add the `KL_avtp_rx_monitor_ctx.sv:28-36` header residue to #495, per the round-3 assignment.
  - The bench's own banner line "[IV1] FRAMES_RX: 6 PDUs, one interval -> +1 (was +6)" (`tb/verilator/avtp_rxmon/sim_main_nx.cpp`) is stale in the same way, while its check asserts +6.
- Merge only with maintainer authorization.

## Clone state after the review

Receipt: `receipts/clone-state.txt`.

- HEAD is `42399611fc2217014024f03f4ba0365fb072688c`, tree `75729d9482463bbc42eed313026c9cae9442026a`.
- The worktree equals the index, and the index equals HEAD.
- All 1,233 tracked non-gitlink blobs re-hash equal, and the index modes, blobs and paths equal the tree.
- The five gitlinks equal the head's: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/lwSRP` `9197193e`, `third_party/verilog-axis` `48ff7a7e`.
- The gate runs created a bytecode cache, which was removed. `git status --porcelain --ignored` is empty.
- The simulations and the mutation ran only on scratch copies.

R574-3 FINISHED
