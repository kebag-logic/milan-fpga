[R635] NEGATIVE - exact head 56d008f68f445156a9bdd81eb32f8d5353cc7a7f

# R635-1: external review of PR #741 (issue #645, bench lane B17)

- Head `56d008f68f445156a9bdd81eb32f8d5353cc7a7f`, tree `341f591136be7d3f5c42cd050bd4b4ebac87658e`, base and live dev `f62602531d415d6c1cae1374a3cc2938faf54049`.
- Change: one file, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+301 lines): a Contents entry and the section "Dev 5603c353, 2026-10-15: lane B17".
- The PR has no RTL, firmware, test or gate change.
- Public evidence: `review-evidence/645-b17-r1` at `35cc1ae4ad6cb5b102b4215f838893b9aa6f23aa` (98 files).
- Authorities, read in this order:
  - AGENTS.md and CONTRIBUTING.md.
  - The issue #645 body.
  - The ruling [6099627217](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217), the assignment [6186729424](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186729424), the STOP [6186910934](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186910934) and its answer [6186940255](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255).
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md` "Settle recentre".
  - `docs/reference/REGISTER_MAP.md` (`0x8D4`, `0x8DC`, `0x8E0`, `0x8F8`).
  - `docs/findings/B14_BENCH_5603C353.md` item 2.
  - `hdl/milan/milan_datapath.sv` at this head and at the image revision `5603c353`.
- This is a findings-only record. The DUT and the bench were not touched, and nothing was run on hardware.

**Verdict: NEGATIVE.**
- The record is sound in substance:
  - Every slip and count matches the raw counter logs.
  - All ten slips are class (c) under the ruling.
  - The rate intervals recompute from the stated delta_ppm.
  - The PDU-lateness observation holds in all ten cycles.
  - The design statement is cited accurately, and no root cause is overclaimed.
  - Public hygiene is clean.
- One MINOR keeps `Docs` and `Tests` unclean: two printed figures in the slips table are double-rounded and disagree with the raw counter log (F1).

## Findings

### F1: MINOR, Docs and Tests: two table figures are double-rounded against the raw counter log

**Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4773` (c08) and `:4774` (c09). The same c08 cell is in the PR body's table and in the REVIEW READY comment.

**Evidence:**
- The page's method defines each slip's interval as running "from the start of the poll before it to the end of the poll that saw it".
- Rounded once from the raw logs `cycles/c08/poll.jsonl` and `cycles/c09/poll.jsonl`, against each cycle's `bind-time` event:

| Cycle | Figure | Raw value | Correctly rounded | Printed |
|---|---|---|---|---|
| c08 | Slip interval, lower edge | +1.174981 s | 1.17 | **1.18** |
| c09 | Last poll | +31.784840 s | +31.78 | **+31.79** |

- The other 38 poll figures in the table match.
- The cause: `tools/ana_b17.py` rounds to 3 decimals (1.175, 31.785), and `tools/summ_b17.py` then formats those to 2 decimals.
- No control covers the table's formatting.
- Receipt: `receipts/printed-rounding.txt`, from `scripts/check_printed_rounding.py`.

**Impact:**
- The c08 interval as printed is narrower than the interval the method defines: rounding the lower bound up excludes 1.175 to 1.18 s.
- The c09 poll coverage is overstated by 5 ms.
- The table is presented as the raw log's figures, and these two cells are not.
- No class, count, verdict or other claim changes.

**Required outcome:**
- The c08 row reads `1.17 to 1.94`, on the page and in the PR body's table.
- The c09 row reads `-8.00 to +31.78`.
- Every printed poll figure equals the raw value rounded once. Either derive it from unrounded values or print the grade's 3 decimals.

**Verification:** `python3 -I scripts/check_printed_rounding.py <packet>/author docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` reports `mismatches: 0` at the new head.

### RES-1: RESIDUE, Docs: "converged, from then on" is early by one poll in four cycles

**Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4793-4794`.

**Evidence:**
- In c02, c04, c05 and c07, the first poll after the prefill exit (0.12 to 0.17 s after the bind) read `RENDER_STAT[9]` = 0.
- Converged first read 1 at the next poll, 0.64 to 0.67 s after the bind, and never dropped afterwards.
- Receipt: `receipts/render-converged.txt`.

**Impact:** the wording only. No figure or claim depends on it.

**Exact fix:** replace "read fill 8 to 14, converged, from then on" with "read fill 8 to 14 from then on, and converged from that poll or the next one on".

### RES-2: RESIDUE, Docs and RTL: the line citation reads as the same lines at `5603c353`

**Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4713-4714` reads "(`hdl/milan/milan_datapath.sv:6810-6812`, the same at `5603c353`)".

**Evidence:** at this head, lines 6810-6812 are the `render_status_w` assignment. At `5603c353`, the identical assignment is at lines 6797-6799.

**Impact:** a reader opening lines 6810-6812 at the image revision finds other code.

**Exact fix:** "(`hdl/milan/milan_datapath.sv:6810-6812` at this head; the same assignment at `:6797-6799` in `5603c353`)".

### S1: SUGGESTION, Robustness and Docs: record the DUT-side event about 1.55 s after every ACMP change

- In all ten cycles, the console poll that starts about 1.55 s after the unbind takes 0.27 to 0.43 s instead of about 0.08 s.
- The poll that starts about 1.55 s after the bind does the same.
- This is consistent with firmware activity such as the saved-state commit the page lists as a residual (commits 61 to 81).
- Five of the ten slip intervals contain that poll: c02, c03, c07, c08 and c09. The other five do not: c05's slip precedes it, and c01, c04, c06 and c10 come later.
- So it does not explain the slips. The late-burst coincidence holds in all ten.
- The bracketing stays valid, because each interval spans the previous poll's start to this poll's end.
- Stating it would let the design round exclude it explicitly. Receipt: `receipts/evidence-hashes-and-long-polls.txt`.

### S2: SUGGESTION, Robustness and Tests: characterise c08's extra capture traffic

- c08's capture holds 814,991 frames. The other cycles hold 774,651 to 776,308.
- The c08 file is 91,179,068 B, against about 86.8 MB for the others.
- The three graded streams have the same PDU counts as in the other cycles, so about 38,700 AVTP frames (about 770 per second) on the DUT's link were not graded or described.
- The c08 slip behaves like the others. Naming what the extra frames were would close the question.
- The raw captures are not published.

### S3: SUGGESTION, Tests and Docs: state the delta_ppm resolution

- delta_ppm is the difference of two rates that are each rounded to 4 decimals (`ana_b17.py`), so it carries a rounding error of up to 0.0001 ppm.
- The rate intervals are printed to six figures (for example 208,333 s from +0.0001).
- Either compute delta from unrounded rates or state the resolution.
- The (b) exclusion is unaffected: the interval stays at least 11,574 s against a window of about 34 s.

### S4: SUGGESTION, Docs: point at the published packet

- The page says the packet "the manager holds; this lane did not publish it".
- It has since been published at `review-evidence/645-b17-r1` (`35cc1ae4`).
- A locator at the next head would let a cold reader reach the raw counter logs that the digest binds.

## What was checked

### (1) Identity gate, as-found record and restore

**Identity gate:** `identity/identity-verdict.txt` records 11 of 11 PASS:
- entity_id, name, firmware_version and serial;
- ID/VERSION `4d494c4e`/`00020060`;
- AEM CRC `5ba355eb` over 7,512 B;
- live ENTITY and CONFIGURATION byte-equal to the QSPI bytes, 312 and 106 B;
- clock sources 0 to 2 present and 3 answering NO_SUCH_DESCRIPTOR, with CLOCK_DOMAIN list 0, 1, 2 and current source 0;
- UART grader 10/10;
- ADP.

The lock window is 07:26:41.266Z to 07:26:47.078Z, which is the page's 09:26:41 to 09:26:47 CEST. The resume re-check (`identity-resume/`) shows the four ENTITY facts and GET_CLOCK_SOURCE 0.

**As found:** the census `restore/census-start.jsonl`, `restore/dut-start.txt` and the STOP comment agree with the page:
- The DUT's STREAM_INPUT 0 is bound to the peer's talker with flags `0x0002`, and STREAM_INPUT 1 is unbound.
- The formats are equal, `0205022001006000`: 4 channels, 6 samples at 48 kHz, 125 us per PDU.
- The maps hold 4 and 8 mappings, and the DUT's CLOCK_SOURCE is 0.
- The peer's STREAM_INPUT 0 and 8 are bound (`0x0082`), and its CLOCK_DOMAIN is on source 1.
- `SLIP_LB` reads `0x000000d0` (208 dups, 0 skips) and `SLIP_TDM` reads 0.
- NVM is at seq 295 with 61 commits and pend=1.

**Restore:**
- My own payload-level comparison gives 45 of 46 census entries equal. The other is GET_AVB_INFO propagation delay, `0x17d` to `0x181` (381 to 385 ns).
- At the end, `SLIP_LB` reads `0xe4` (228) and NVM is at seq 315 with 81 commits, VD_OK.
- Every cycle's `cycle-check` reads bound_as_found true, DUT clock 0, peer clock unchanged.
- Every capture shows `remote_equal` and `removed_from_tap` true.
- The raw capture rows on the page match the capture-end events.

### (2) The ten-cycle table against the raw counter logs

My recomputation is independent and stdlib-only: `scripts/recompute_polls.py`, receipt `receipts/recompute_polls.jsonl`.

**Counter log digests:**
- All ten `poll.jsonl` match `summary/counter-logs.sha256`.
- That file's SHA-256 is `a1d41530...7c848`, as the page states.
- The poller's SHA-256 is `1912837a...d4f7`, as the page states and as each cycle's `start` event records.

**Per cycle:**
- 80 polls, `n` contiguous from 0, none unreadable.
- Poll spacing is 0.50 to 0.51 s (0.582 s once, in c08).
- The polls run from -8.01 to -7.99 s up to +31.75 to +31.93 s.
- The unbind is at -6.012 to -6.032 s, every unbind and bind status is 0, and there are no retries.

**SLIP_LB:**
- Exactly one change per cycle: +2 dups, 0 skips.
- None while bound before the unbind, none while unbound, and none in the remaining 26.13 to 31.19 s of each hold.
- The counter went 208 to 228 across the ten cycles, and `SLIP_TDM` read 0 throughout.

**Slip intervals:**
- The intervals are 0.577 to 0.901 s wide, so the page's "0.58 to 0.90 s" holds.
- Every interval and count matches the table, except the two rounding cells in F1.
- The bind times are the `bind-time` instants truncated to the millisecond.
- `MCSRV_STAT[2:0]` read 0 (IDLE) and `AAFM_STAT` read 0 in every poll.
- `RENDER_STAT` exited prefill 0.123 to 0.653 s after the bind, with fill 8 to 14 and rails 11 (RES-1 covers the converged bit).

**Toolchain:**
- The published `summ_b17.py`, run on a scratch copy, regenerates `cycles.json`, `table.md` and `counter-logs.sha256` byte for byte.
- The published `ana_b17.py` regenerates every cycle's poll grade identically.
- The page's table equals `summary/table.md`.
- The receipt is `receipts/regen-and-mutate.txt`.

### (3) Each slip's class under the ruling

**(a):**
- At `5603c353`, `settle_arm_w` (`milan_datapath.sv` lines 6603-6605 there) is a source-index change, aligner re-engagement or an aligner excursion. A bind is not among them.
- `settle_pend_r` and `rsp_recentres_w` are simulation taps only, and `RENDER_STAT` carries no recentre count.
- The register map keeps recentre counters as verification taps (`REGISTER_MAP.md:2064`).
- So "not observable on this image" is correct, and no CLOCK_SOURCE changed in any cycle.

**(b):**
- I recomputed `1/(48000 x |delta_ppm| x 1e-6)` from each stated delta. All ten intervals match: 104,167, 34,722, 41,667, 12,255, 104,167, 13,021, 104,167, 69,444, 208,333 and 34,722 s.
- The bound windows are 33.73 to 33.91 s, so a rate offset gives at most 0.003 slips per cycle.
- delta is the peer's AAF rate less the DUT's AAF rate, both from presentation timestamps.
- The DUT's AAF and CRF agree exactly, and all streams run 4.9928 to 5.0161 ppm against gPTP. The page's "+4.99 to +5.02" holds.
- The tap arrival rates of the two AAF streams agree to 0.001 ppm.

**(c):** all ten slips are (c), so #645 stays open, as the ruling requires.

### (4) PDU lateness against the tap data

I recomputed from the grade output; the raw captures are not published. The script is `scripts/recompute_tap.py`, receipt `receipts/recompute_tap.txt`.

**Per slip:**
- No peer PDU more than 10 us late arrived between the bind and the slip's interval.
- The first burst over 20 us lies inside the interval, at a burst start 0.036 to 0.757 s after the interval's lower edge.
- The largest lateness inside the interval is 24.565 to 29.309 us.
- 10 to 23 bursts follow it, peaking at 27.575 to 30.26 us.
- In nine cycles a later burst peaked above the slipping burst (c01 is the exception).

**Overall ranges:**
- 11 to 24 bursts per cycle, of 3 to 12 PDUs each.
- The first PDU arrived 7.854 to 163.485 ms after the bind.
- The median phase is 1.405 to 1.450 us, and the 99.9th-percentile lateness is 4.448 to 6.139 us.
- The tap and host unbind-to-bind intervals agree within 0.1 ms.
- No graded stream has a sequence gap.

All of these match the page.

### (5) The design reference and root-cause claims

**The design reference:**
- `MEDIA_CLOCK_FOLLOWING.md:1187-1188` reads "A bind still primes the ring where its first PDU lands; the next settle recentre centres it."
- The page paraphrases it accurately and links the section.
- The page's arm terms match the table's "Armed by" row.

**Root cause:** the page does not overclaim one.
- The mechanism paragraph is labelled "consistent with" and "a reading of the evidence, not a measurement".
- The table row states a timing coincidence that holds at poll resolution in all ten cycles.

### (6) Public hygiene

- I scanned the 302 added lines for addresses, MACs, host paths, remote-shell or capture-tool names, interface names, instrument or vendor names, wiring and cable terms, and personal or model names. None are present.
- The role labels are ones dev already uses on this page.
- The serial "AX7101-0001" is the AEM default in repository source (`configs/endstation_ax7101_1x1_tdm8.yaml:28`) and appears on dev pages.

### Gates and controls

**Gates** at the exact head, all rc 0:
- `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_baremetal_only.py --check` and `git diff --check base..head`.
- `gen_toc.py --check`, `gen_toc.py --verify-anchors` and `check_em_dash.py --base f6260253`, run with the pinned Markdown renderer (cmarkgfm 2025.10.22, html5lib 1.1) in a disposable environment.
- The section's internal and cross-page anchors resolve.
- Receipts: `receipts/doc-gates*.txt`, `receipts/verify-anchors.txt` and `receipts/intra-anchors.txt`.

**Controls:**
- The published controls rerun at 17 of 17.
- Five disposable grader mutations are each caught by a named control:
  - classification forced to (c);
  - delta sign flipped;
  - interval opened at this poll's start;
  - a lone slip taken as periodic;
  - lateness threshold raised to 40 us.

**Hashes:**
- Every evidence hash on the page matches the published packet.
- `MANIFEST.json` reports 98 entries and 0 published-hash mismatches.
- One file was redacted on publication: `author/identity-resume/identity-verdict.json`, whose serial was replaced. That explains its `author/MANIFEST.sha256` mismatch.

**Hosted contexts at the exact head:**
- `rtl-fast`, `full-ci-gate`, `docs-check-no-git`, `elaborate`, `bdd-conformance`, `wire-accountability` and `changes` succeeded.
- `docs-check` was in progress when read.
- `verilator-suites`, `yosys-portability`, the firmware and Yosys jobs, and physical gPTP were skipped, as expected for a documentation-only change. They are not executed evidence.

## Prior public review findings

- When this round started, PR #741 had no review, and its only comments were the two review-start notices (R634-1 and R635-1).
- No earlier finding exists to resolve or retain.
- The concurrent internal round was not read.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The ruling, assignment and answer items against the page section (lines 4612-4910): identity verdicts; census as found and at the end; ten `events.jsonl` and `poll.jsonl`; classes and intervals recomputed; verdict "stays open" | R635-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| RTL | CLEAN (RES-2 residue only) | `milan_datapath.sv` `settle_arm_w` and `g_settle_recentre` and `render_status_w` at `5603c353` and at the head; `rsp_recentres_w` as a tap only; `REGISTER_MAP.md` `SLIP_LB` unit (`:1878`), `MCSRV_STAT` encoding (`:2147`), `RENDER_STAT` bits (`0x8DC`); `MEDIA_CLOCK_FOLLOWING.md:1060-1188` | R635-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Robustness | CLEAN (S1 and S2 are suggestions) | Unreadable polls (0); poll spacing; interval bracketing under the long polls; capture completeness (sequence gaps 0; captured against filtered at the capture end, outside the window); host-to-tap mapping (0.1 ms); the slip near the bind in c05; the runner's re-bind on failure and its state checks (`tools/cyc_b17.py`) | R635-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Tests | UNCLEAN (F1) | Controls rerun 17/17; five mutations caught; summaries regenerated byte-identical; `check_printed_rounding.py` finds 2 mismatches | R635-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |
| Docs | UNCLEAN (F1; RES-1 and RES-2 residue) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:92`, `:4612-4910`; the PR body; documentation gates rc 0; anchors; quote accuracy; hygiene scan | R635-1 | `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` |

## Real limits

**Tap figures:**
- The raw tap captures and controller transcripts are not published.
- Tap figures (delta_ppm, rates, lateness, bursts, priming) were checked against the published grade output (`summary/cNN.json`), the published grading tool and its controls. They were not re-derived from the captures.
- The capture hashes are bound only through the page and the events.

**Unverifiable history:** the operator's statements about earlier tool runs cannot be checked from public material. These are the first control run at 15 of 16, and a re-grade that left fields unchanged.

**Not done:**
- No hardware.
- No physical calibration.
- No manager source bank or builder bank at this head.
- None is claimed.

**Hosted evidence:** `docs-check` had not finished when read. The long gates were skipped contexts, not runs.

## Pending manager duties

**Merge:**
- Re-review after F1 is fixed. RES-1 and RES-2 go to the residue checklist.
- Validate the current-dev merge candidate.
- Own the hosted and act acceptance, including `docs-check` at the head.

**Publication:**
- The REVIEW READY comment on #645 carries the same c08 cell; F1's fix applies there too.
- The publication redacted the serial in one evidence file but not in `identity/identity-verdict.txt`. It is repository-public, but the policy should be applied consistently.

## Receipts

Scripts are in `scripts/` and outputs in `receipts/`. All are listed in `MANIFEST.sha256`.

R635-1 FINISHED
