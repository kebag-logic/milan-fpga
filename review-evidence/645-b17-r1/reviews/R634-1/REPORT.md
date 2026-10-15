[R634] NEGATIVE - exact head 56d008f68f445156a9bdd81eb32f8d5353cc7a7f

Round R634-1. Internal independent review of PR #741 (issue #645, bench lane B17), from a cleared context.

- Head `56d008f68f445156a9bdd81eb32f8d5353cc7a7f`, tree `341f591136be7d3f5c42cd050bd4b4ebac87658e`.
- Source base and live dev are both `f62602531d415d6c1cae1374a3cc2938faf54049`.
- The diff touches one file, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, adding 301 lines: the Contents entry at :89 and the section at :4612-4910.

## Verdict basis

The verdict is NEGATIVE because one MINOR finding is open: F1, under Docs and Tests. The page states two after-slip figures for "the same hold". Its receipts compute them through the end of the capture, about 41.9 s after the bind, which goes past the 32 s hold and the last poll. Under the owner rule this is not wording-only, because a printed figure changes.

The lane's own result for #645 reproduces from the raw artifacts. That result is:

- ten slips, each +2 dups (one frame), 0.07 to 5.67 s after its bind;
- every slip class (c) under the ruling;
- #645 stays open.

There are also two RESIDUE wording items (F2, F3) and one SUGGESTION (F4).

No prior public review findings existed on PR #741 at this head. Its comments are the two review-start notices for R634-1 and R635-1, and it has no review bodies. So there is nothing to resolve or retain.

## What was reconstructed, and from where

**Authority:**
- `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
- Issue #645's body.
- The ruling after lane B14 (issuecomment-6099627217).
- The B17 assignment (6186729424), the STOP (6186910934) and the resume ruling (6186940255).
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` § Settle recentre (:1060-1188).
- `docs/reference/REGISTER_MAP.md` `SLIP_LB` (:1878) and `RENDER_STAT` (:2017-2064).
- `docs/findings/B14_BENCH_5603C353.md` item 2 (:74-81).
- `hdl/milan/milan_datapath.sv` and `hdl/ieee1722/aaf/KL_chan_map_capture.sv`, both at this head.

**Evidence** comes from the public evidence tree `review-evidence/645-b17-r1` at `35cc1ae4ad6cb5b102b4215f838893b9aa6f23aa`, fetched into a disposable bare repository:
- the raw counter logs `author/cycles/cNN/poll.jsonl` and the events `cNN/events.jsonl`;
- the grades `summary/cNN.json`, plus `summary/cycles.json`, `table.md` and `counter-logs.sha256`;
- the tools with their hashes;
- the controls;
- the identity, identity-resume and restore records.

The author's handoff note in that tree was not read.

The raw tap captures are not published. Every tap-derived figure (delta_ppm, rates, lateness, bursts, priming) is therefore checked against the published grade output `summary/cNN.json`, which lists every peer PDU more than 10 us late, each stream's rate and the priming quantities. It is not checked against the pcaps.

## Checks performed and results

Receipts are under `receipts/`, and the reviewer scripts are at the packet root.

### 1. Identity gate, as found, and restore

Sources: `identity/identity-verdict.txt`, `grader-identity.txt`, `lock-window.txt`, `identity-resume/*`, `restore/*`.

- **Identity gate: PASS, 11 of 11 checks.** Every fact below matches the assignment's expected values and the page at :4652-4659:
  - entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version 2.96.0, serial AX7101-0001;
  - ID `4d494c4e`, VERSION `00020060`;
  - AEM CRC `5ba355eb`;
  - ENTITY and CONFIGURATION byte-equal to QSPI, 312 and 106 bytes;
  - CLOCK_SOURCE 0, 1 and 2 present, 3 answering NO_SUCH_DESCRIPTOR, CLOCK_DOMAIN list 0/1/2, GET_CLOCK_SOURCE 0;
  - UART grader 10 of 10.
- **Lock window** 07:26:41.266Z to 07:26:47.078Z, which is 09:26:41 to 09:26:47 CEST as printed.
- **Resume identity:** PASS over ATDECC, with GET_CLOCK_SOURCE 0. The controller-clock stamp corrected by the measured 1.357 s offset gives 07:39:28.8Z, which matches "09:39:28 CEST".
- **The serial is public.** It is the ROM default and already in the tree: `avdecc/aem_specs.py:44`, `configs/endstation_ax7101_1x1_tdm8.yaml:28`, and earlier B-lane sections. Publishing it is not a hygiene issue.
- **As found** (`restore/dut-start.txt`, 07:27:46Z) matches the page at :4663-4667 and the STOP comment:
  - `SLIP_LB` `0xd0` = 208 dups, 0 skips; `SLIP_TDM` 0;
  - CLOCK_SOURCE 0, servo IDLE;
  - NVM image seq 295, commits ok=61, pend=1.
- **As left** (`restore/dut-end.txt`, 07:57:46Z):
  - `SLIP_LB` `0xe4` = 228;
  - NVM seq 315, commits ok=81, pend=1, VD_OK.
- **Census** (`census-compare.txt`): 45 of 46 entries equal; the one difference is the GET_AVB_INFO propagation delay, `0x17d` vs `0x181`, which is 381 vs 385 ns.
- **Controller and tap cleanup:** the controller-end and controller-cleanup files show no process and the staging removed. Every cycle's `capture-end` reads `remote_equal` true and `removed_from_tap` true.
- **Capture hashes:** all ten names, byte counts and SHA-256 values in the page table (:4890-4899) equal the `capture-end` events (`receipts/comparisons.txt`: PCAP_TABLE_MATCH).

### 2. The 10-cycle table, against the raw counter logs

Script `recompute_b17.py` reads only `poll.jsonl` and `events.jsonl` and writes `receipts/recompute-table.jsonl`. It shows:

- **Polls:** 80 per cycle, none unreadable, all eight words present. Poll spacing is 0.500 to 0.515 s, with one 0.582 s gap in c08.
- **Poll coverage:** first poll -8.01 to -7.99 s from the bind, last poll +31.75 to +31.93 s.
- **Bind times:** each cycle's bind UTC equals the page.
- **Unbind to bind:** 6.012 to 6.032 s.
- **Command results:** every unbind and bind answered status 0 with flags `0x0002`; no bind retry and no finally-rebind occurred; formats were equal, so nothing was set.
- **End state:** every cycle ended with `clk_dut` 0, the peer's clock unchanged, and the DUT bound as found.
- **`SLIP_LB`:** exactly one change per cycle, +2 dups and 0 skips, each in the bound region after the bind.
  - The intervals match the page to the printed precision: 2.560-3.138, 1.091-1.956, 1.072-1.945, 3.103-3.681, 0.066-0.643, 3.569-4.146, 1.060-1.943, 1.175-1.942, 1.045-1.946 and 5.094-5.671 s.
  - The interval widths are 0.577 to 0.901 s.
  - 26.13 to 31.19 s of polls remain after each slip.
  - The counter runs 208 to 228 across the lane, and each cycle's first read equals the previous cycle's last read.
- **Other words:** `SLIP_TDM` 0 throughout; `MCSRV_STAT` state 0 (IDLE) and `AAFM_STAT` 0 in all 800 polls; `RENDER_STAT` rails 11 throughout.
- **Settle boundary:** undefined in every cycle, because no poll read LOCKED. This is B14's definition as cited (`B14_BENCH_5603C353.md:80`).
- **Re-grading:** `ana_b17.py cycle <dir> -` on the raw logs reproduces the published poll sections of all ten `summary/cNN.json` identically. `summ_b17.py` on a copy reproduces `summary/cycles.json`, `table.md` and `counter-logs.sha256` byte-for-byte, and the last of those hashes to `a1d41530…c7848`.
- **Page table:** :4764-4775 is byte-identical to `summary/table.md`.
- **Poller:** `tools/console_poll_b8.py` has SHA-256 `1912837a…67d4f7`, equal to lane B8's published hash (page :1893) and to `ORIGIN-B14`/`ORIGIN-B15`. Its `CMDS` read `0x8e0`(8), `0x8f8`, `0x8d4`(12), `0x738` and `0x748`, which are the eight words the page names. The period is 0.5 s, as the events record (`poll-start period_s 0.5`).

### 3. Classification under the resume ruling

**(a) needs an observable arming term, and none occurs.**
- Every cycle read CLOCK_SOURCE 0 at its start and end and set none.
- The RTL agrees that a bind arms nothing:
  - `settle_arm_w` (`hdl/milan/milan_datapath.sv:6616-6618`) is the OR of three terms: a selected-index change, aligner re-engagement, and an excursion with no recentre pending and not in recovery.
  - The aligner's frame event is the local audio capture (`:6190-6191`, from `aafcap_pv_w`, `:1005`), not the received stream.
  - So a listener bind enters none of the three terms.
- On the observability side, `recentres_o` drives `rsp_recentres_w` (`:6807`, `:6851`) and reaches no CSR. `RENDER_STAT` packs rails, converged, prefill and fill only (`:6810-6812`).

The page's statement that (a) cannot be shown on this image is therefore accurate and not overclaimed.

**(b) needs a rate interval 1/(f_s*|delta_ppm|), recomputed here from the stated delta_ppm.** Script `recompute_tap_b17.py` writes `receipts/recompute-tap.jsonl`. It shows:
- delta_ppm equals peer-aaf minus dut-aaf in every cycle.
- The intervals are 104,167; 34,722; 41,667; 12,255; 104,167; 13,021; 104,167; 69,444; 208,333 and 34,722 s. That is the same figure whether computed from the rounded or the unrounded difference, and it equals the page.
- The expected rate slips per bound window (33.7 to 33.9 s) are at most 0.00276.
- Five cycles have positive delta (a faster peer), where a rate offset would give skips, not dups.
- No slip can be (b), so (c) follows for all ten.
- The page adds two (b) conditions beyond the ruling's text: direction, and at least one expected slip. Both are stated publicly, both only make (b) stricter, and the outcome does not depend on them.
- The re-run controls of `ana_b17.py` pass 17 of 17 (`receipts/controls-rerun.json`, `receipts/comparisons.txt`; it matches the published `controls/b17-ana-controls.json` check for check). They include (b) with a slower peer, (c) with a faster one, and a lone dup at 0.002 ppm.

**The time base holds.** The tap's unbind-to-bind interval equals the host's to within 0.0 to 0.1 ms in every cycle. All streams run +4.9928 to +5.0161 ppm against gPTP, matching the page's "+4.99 to +5.02". The DUT's AAF and CRF rates are equal in every cycle (the A2-a single clock). There are no sequence gaps in any stream.

### 4. PDU lateness against the slips

From the published `late_pdus` lists, with bursts grouped as the lane groups them (over 20 us, under 1 ms apart):

- In 10 of 10 cycles no PDU over 10 us falls between the bind and the slip interval.
- Exactly one burst starts inside each slip interval, and it is the cycle's first burst.
- The in-interval maxima are 24.565 to 29.309 us, matching the page's 24.6 to 29.3.
- There are 11 to 24 bursts per cycle of 3 to 12 PDUs.
- The priming figures match the page: first peer PDU 7.854 to 163.485 ms after the command, phase median 1.405 to 1.450 us, and 99.9th-percentile lateness 4.448 to 6.139 us.
- A later burst exceeds the slipping burst in 9 of 10 cycles (not in c01). This holds even when restricted to the hold.
- **Exception: F1, the window of the after-slip figures.** See below.

### 5. The design reference, and root cause

- **The quote.** `MEDIA_CLOCK_FOLLOWING.md:1187-1188` reads "A bind still primes the ring where its first PDU lands; the next settle recentre centres it." The page (:4824-4826) paraphrases this accurately.
- **The arming terms.** The page's arming list (:4804-4806) matches the "Armed by" row (:1090).
- **No overclaimed root cause.** The mechanism paragraph (:4846-4851) is labelled "a reading of the evidence, not a measurement", and the page states that the ring's fill and margin are not readable. The section claims no root cause, and the verdict rests only on the ruling's classes.
- F3 is a one-word causal attribution elsewhere, recorded as RESIDUE.

### 6. Public hygiene

The 301 added lines were scanned (`scratch/added.txt` was not published; only the method is given here) for:
- IP and MAC addresses, device paths, home and tmp paths, host-like domains and interface names;
- vendor, instrument and tool names, and person names.

The only hits are the four github.com issue links. "SoC board", "controller host", "tap host" and "passive tap on the DUT's link" are neutral role labels already used in earlier public sections. The peer's following of the DUT's CRF is the AVDECC configuration already public on this page (:67, :467). No private names, hosts, instruments, wiring or clock topology were found.

### 7. Docs gates at the head (reviewer re-run, `receipts/gate-*.log` and `.rc`)

| Gate | Result |
|---|---|
| `docs_check.py` | rc 0 |
| `check_doc_style.py` | rc 0 |
| `check_doc_paths.py` | rc 0 |
| `git diff --check f6260253..HEAD` | rc 0 |
| `gen_toc.py --check` | rc 0, with the pinned renderer installed into a disposable venv under `scratch/` |
| `check_em_dash.py --base f6260253` | rc 0 (301 added lines, 0 findings), same venv |
| `check_hygiene.py` | Refused rc 2: it needs initialized submodules, and this clone does not initialize them. Recorded as a limit; the gate is code-quality, not docs. |

All cross-page anchors resolve to existing headings: `B14_BENCH_5603C353.md#item-2-source-switches-645-647`, `MEDIA_CLOCK_FOLLOWING.md#settle-recentre` and `REGISTER_MAP.md#0x8dc-----render-setpoint-state`.

## Findings

### F1 — MINOR — Docs, Tests — after-slip burst figures stated for "the same hold" are computed to the capture's end

**Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4836`, :4840 and :4834, and the PR #741 body's "Bind priming" bullet. The figures are generated by the summary tool's `bursts_after_interval` and `burst_peak_after_interval_us` in `summary/cycles.json`.

**Evidence:**
- **The capture outlasts the hold.** Each capture runs 50 s, and the peer stream on the tap lasts to +41.82 to +41.91 s after the bind. The hold is 32 s, and the last poll ends at +31.75 to +31.93 s.
- **The tool's window is unbounded.** It counts "after" bursts with no upper bound (`summ_b17.py`, `after = [z for z in b if z["s"] > x["s_hi"]]`).
- **The page labels the peak "in the same hold" (:4836).** Its "Largest lateness after the slip, in the same hold | 27.6 to 30.3 us" takes:
  - its maximum from c05's burst at +37.50 s (30.260 us);
  - its minimum from c08's burst at +37.01 s (27.575 us);
  - both after the hold.
  
  Within the 32 s hold (and equally within the last poll) the range is 27.092 to 30.071 us.
- **The burst count "The 10 to 23 bursts after it slipped nothing" (:4840)** counts 2 to 7 bursts per cycle that fall after the last poll. Within the polls the count is 8 to 18.
  - That those later bursts "slipped nothing" is true, but only through the cumulative counter: the next cycle's first `SLIP_LB` read equals the previous cycle's last in all nine transitions, and the end baseline reads 228.
  - The page does not state that basis.
- **The PR body** repeats "The 10 to 23 later bursts, up to 30.3 us, slipped nothing".
- **The same table row (:4834), "per cycle 11 to 24",** is also counted to the capture end, without saying so.
- **Two smaller figure-label imprecisions of the same kind (the timing method):**
  - (i) "`RENDER_STAT` left prefill 0.12 to 0.65 s after each bind and read fill 8 to 14, converged, from then on" (:4793-4794).
    - 0.12 to 0.65 s are the end times of the first polls that read prefill 0, not the exit instants.
    - In c02, c04, c05, c07 and c08 that first poll is also the first after the bind. There the exit is bracketed only by the first peer PDU and that poll's end: for example c05 at (0.008, 0.138] s and c08 at (0.029, 0.249] s.
    - In c02, c04, c05 and c07 that poll read converged 0. "Converged from then on" starts one poll later.
  - (ii) c09's last poll "+31.79" (:4774) is a double rounding of +31.7848 (3 dp, then 2 dp). Rounded once it is +31.78.

**Impact:**
- A reader takes 30.3 us as the largest lateness the bind-primed ring survived inside the observed hold, and 10 to 23 as the number of polled bursts that did not slip it. Both are overstated for the hold.
- This bind-priming record is what the follow-up design round (issue #645, comment 6187595500) cites to derive its reproduction parameters ("a late burst of 20 to 30 us").
- No class, verdict or slip timing changes.

**Required outcome:**
- Either restrict the after-slip figures to the hold or the polled window, or keep the capture-end figures and label their window, adding that the slips-nothing basis beyond the last poll is the next cycle's first poll and the end baseline. Do the same in the PR body.
  - Restricted: 8 to 18 later bursts, peak 27.1 to 30.1 us, and 9 of 10 cycles still have a later, larger burst.
  - Labelled: "to the capture's end, about 41.9 s after the bind".
- State the per-cycle burst count's window.
- State prefill exit and convergence as the poll bound they are, for example "by 0.12 to 0.65 s (the end of the first poll that read prefill 0)", with convergence from the following poll in four cycles.
- Print c09's last poll as +31.78, or round once in the summary tool.

**Verification:** re-run `after_window_b17.py` (this packet) on the evidence tree. The page's after-slip figures must equal the `after_hold_32s` or `after_last_poll` row, or be labelled with the capture-end window. `recompute_b17.py` must give c09's last poll as 31.78 to 2 dp.

### F2 — RESIDUE — Docs — the RTL citation's "the same at `5603c353`" does not hold for the line numbers

**Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4713`.

**Evidence:** the `RENDER_STAT` packing is at `hdl/milan/milan_datapath.sv:6810-6812` at this head. At `5603c353` the same content is at :6797-6799; four later commits touched the file.

**Fix (wording only):** "(`hdl/milan/milan_datapath.sv:6810-6812` at this head, `:6797-6799` at `5603c353`)".

### F3 — RESIDUE — Docs — a causal attribution stated as fact

**Where:** :4841-4842, "The arrival phase is the same in every cycle, because the peer's talker follows the DUT's CRF."

**Evidence:** the phase constancy (1.405 to 1.450 us) and delta_ppm about 0 are measured. That following causes the constancy is an inference that the lane did not test, for example against the peer on its internal source (see the page's own limits at :4871-4873).

**Fix (wording only):** "The arrival phase is the same in every cycle, as expected with the peer's talker following the DUT's CRF."

### F4 — SUGGESTION — Docs — say where the lane packet is published

**Where:** :4644-4646 and :4884-4886.

The page says the manager holds packet `645-b17-a619`, unpublished. It is now public as `review-evidence/645-b17-r1` on branch `645-b17-review-evidence` (commit `35cc1ae4…`, named in the design-round TAKEN comment). Earlier sections on this page added "where the packet is published" for exactly this cold-reader need. This is optional, and it is for the manager to decide when to link.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #645 acceptance, the ruling after B14, the B17 assignment, STOP and resume ruling, against :4632-4642, :4736-4739 and :4796-4820; `recompute_b17.py`/`recompute_tap_b17.py` receipts (one slip per cycle, all (c), interval from stated delta, (a) not observable); identity gate and restore records against :4650-4671 and :4853-4867 | R634-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| RTL | CLEAN | Page RTL and CSR claims against `hdl/milan/milan_datapath.sv:6800-6851` (`RENDER_STAT` packing, `recentres_o` reaching no CSR), `:6585-6650`, `settle_arm_w` at `:6616-6618`, `:6150-6197` and `:1005` (aligner frame source is the local capture); `KL_chan_map_capture.sv` priming and flush notes; `REGISTER_MAP.md:1878` (`SLIP_LB` per fed and primed pair) and stream format `0205022001006000` (4 channels, 2 pairs); no RTL in the diff | R634-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Robustness | CLEAN | Raw polls: unreadable reads (0), bound, unbound and pre-unbind regions, skips half 0, `SLIP_TDM` 0, saturation headroom (208-228 vs 0xFFFF), retry and finally-rebind paths (`cyc_b17.py:300-330`, not taken), tap-to-host mapping (≤0.1 ms), sign-of-delta cases (5 positive and 5 negative), slip at the stream start (c05, 0.066 s), next-cycle counter continuity | R634-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Tests | UNCLEAN (F1) | `ana_b17.py control` re-run 17/17; poll re-grade identical 10/10; `summ_b17.py` byte-identical rebuild; poller hash vs B8; F1: the after-slip window in `summ_b17.py` is unbounded while the page claims the hold | R634-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Docs | UNCLEAN (F1; F2 and F3 are RESIDUE and do not unclean) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:89` and `:4612-4910`, all figures recomputed; anchors; docs gates re-run (rc 0); hygiene scan; PR #741 body | R634-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |

## Real limits

- **No pcaps.** The raw tap captures are not published, so the tap-derived figures were checked against the published grade output, not re-derived from the pcaps. The reviewer did check the grading code (`ana_b17.py`), its controls and their reproducibility.
- **The bench was not run.** Physical calibration was NOT RUN, and nothing here is hardware proof beyond the lane's own records.
- **No full-repository banks.** No manager source bank runs at this head, and none is claimed. `check_hygiene.py` could not run without the submodules.
- **Hosted state at review time** (snapshot in `receipts/hosted-checks-snapshot.tsv`):
  - Executed with success: `rtl-fast`, `changes`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `wire-accountability` and `full-ci-gate`.
  - Still in progress: `docs-check`.
  - Skipped for a docs-only change (skips are not evidence): `verilator-suites`, `yosys-portability`, the shards, and the firmware jobs.
- **The poll's own resolution.** A slip is timed only to its 0.58 to 0.90 s poll interval.

## Pending manager duties

- Carry F2 and F3 to the residue checklist with their exact fixes.
- After F1 is corrected, a new head needs re-review of Docs and Tests, plus Conformance if the bind-priming record's figures change.
- Link the published packet location on the page or PR (F4) if wanted.
- Own the hosted and act acceptance, including the in-progress `docs-check`.
- Build and validate the current-dev merge candidate at the merge turn.
- The second, external review (R635-1) is independent of this one.

## Clone integrity

The clone was left at exact head bytes, verified in `receipts/clone-integrity.txt`:
- HEAD and tree are as above; the work tree and index are clean, with 0 untracked files.
- The page blob is `d6f1db70…`, mode 644.
- The submodule gitlinks are unchanged: gptp-processor `e4869fd0`, protocol-processor `2ad2f845`, third_party/verilog-axis `48ff7a7e`.

No source edit, commit, push or GitHub write was made.

R634-1 FINISHED
