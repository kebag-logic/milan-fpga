[R422] NEGATIVE - exact head c39312b4871c8cc3ca604eb7c57f4b0b45d914e0

Round R422-2. Internal independent review of PR #627 (Refs #451, bench lane B4, the timing item), tree `d9b3febc6f776dce41435775941fe960f1e1b6f1`, on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. The round-2 commit `c39312b4` changes one file, `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`, over the round-1 head `35a60c8d`. All five lenses were applied at this head.

The round-1 findings are fixed. R422-1 F1, R422-1 F2 with R423-1 S1, and R423-1 F1 are resolved, and the suggestions were taken. The FSYNC verdict claims only what the evidence carries. The one-bit-offset wording matches an independent probe. Every measurement table is byte-identical to round 1, and the docs gates return rc 0.

One MINOR finding is open, so Docs is not clean and the verdict is NEGATIVE. It comes from my own round-1 suggestion S2. The new figure "58.7 s before the unbind" subtracts timestamps taken on two different host clocks. On one clock the interval is 60.0 s. That is a one-line fix and changes no measured figure or verdict.

## Reconstruction

These are the authorities, read in this order:

- AGENTS.md; CONTRIBUTING.md sections 2, 3 and 6; docs/README.
- The #451 issue body, the SoC-board amendment 5729936674 and the owner decisions 5916029287 and 5924157808.
- The B4 assignment 5924192573, the STOP 5924930868, the ruling 5924950994 and the round-2 assignment 5925185587, whose items 1 to 4 are the frozen scope of this round.
- The A469 TAKEN 5925194601 and REVIEW READY 5925296626.
- `docs/litex/CLOCK_DOMAINS.md` Audio variants; `hdl/ieee1722/aaf/KL_tdm_capture_master.sv`; `hdl/milan/milan_datapath.sv`.
- `git diff e4b771f9..c39312b4`, the round-2 diff `35a60c8d..c39312b4`, and the commit history.
- The public evidence at `5a756676:review-evidence/b4-r1`: `author/` and `author-r2/`.
- The PR #627 body and its exact-head check runs.

I read the round-1 review reports (`reviews/R422-1`, `reviews/R423-1`) only after my own pass over the diff, the probe and the receipts below.

## Findings

### R422-2 F1: MINOR (Docs): `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:349-350`, "58.7 s before the unbind" mixes two host clocks

- **Authority/evidence.** The figure subtracts the talker's `end` record from the orchestrator's `unbind` event: 1790828976.783 minus 1790828918.128 (author-r2 `HANDOFF.md:38`). Those two stamps come from different hosts:
  - `tools/run_timing.py:54-55` stamps `events.jsonl` with the orchestrating host's `time.time()`.
  - `tools/aaf_talker.py:40` and `tools/avdecc_ro.py:53-54` stamp `controller-logs.txt` and `ctl-*.jsonl` with the controller host's `time.time()`. Both run over ssh (`run_timing.py:64-74,96-101`).
  - The controller recorded each command 1.36 to 1.38 s *after* the orchestrator logged that command's return. So the two clocks differ by at least 1.38 s (`receipts/talker_unbind_interval.json`: bind 1.378, map-add 1.359, map-remove 1.382, unbind 1.384, map-final 1.384).
  - On the controller clock alone, the talker ends at 1790828918.128 and the unbind runs at 1790828978.166. That is 60.04 s. Any single-clock reading gives at least 59.87 s.
  - The figure is my own: round-1 suggestion R422-1 S2 proposed 58.7 s from this cross-clock subtraction. The executor took it as written. I correct it here.
- **Impact.** A durable findings page states an exact interval that its own packet contradicts. The narrative still holds: the talker ended first, because the stalled capture held the console. No measured figure or verdict depends on the number. This is the same class as R422-1 F1, a wrong precise figure on the page.
- **Required outcome.** The interval at `:350` is one the packet supports on a single clock. Two examples: "60.0 s, on the controller host's clock", or "about 60 s". The PR body's R422-1 S2 line should match.
- **Verification.** Re-run `scripts/talker_unbind_interval.py` on the packet's `runs/timing-long`. Compare the page line, then re-run the docs gates.

Why only Docs:

- No acceptance criterion or verdict of the #451 timing item rests on this sentence, so it is not Conformance.
- It is not an executable test or test evidence, so it is not Tests.
- The ordering claim it supports, that the talker ended before the unbind, holds, so it is not Robustness.

### R422-2 S1: SUGGESTION (Docs): the PR #627 body, "Verdicts" table, FSYNC row

The row reads "fs 47,997.947 Hz on the SoC board's clock", with "-32.1 ppm against the plan". It makes no accuracy claim, so it is not wrong. The page's own verdict cell (`:36`) is sharper: it says "uncalibrated", and it attributes the -32.1 ppm as the DUT oscillator's error relative to the SoC board's clock. The PR body could mirror that cell. This is optional, since the body is not committed text.

## Prior public findings, resolved or retained at this head

| Finding | State at `c39312b4` | Evidence |
|---|---|---|
| R422-1 F1 (MINOR), recording size | RESOLVED | `:115-117` reads "967.7 MB at the full 630 s". 630 x 48,000 x 32 B = 967,680,000 B, and 921.6 MB was 600 s (`receipts/rederive_fs.json`) |
| R422-1 F2 (MINOR) and R423-1 S1 (SUGGESTION), FSYNC verdict | RESOLVED | See below |
| R423-1 F1 (MINOR), one-bit-offset sentence | RESOLVED | See below |
| R422-1 S1, "every identity value" | TAKEN | `:61` |
| R422-1 S2, talker end before unbind | TAKEN, but the figure I proposed was wrong | Retained as R422-2 F1 above |
| R423-1 S2, data delay from `dsp_a` | TAKEN | See below |
| R423-1 S3, root shell and credential | TAKEN | See below |

R422-1 F2 and R423-1 S1, the FSYNC verdict:

- The verdict cell (`:36`) reads "47,997.947 Hz on the SoC board's uncalibrated clock". Its evidence: -42.8 ppm against 48 kHz; -10.64 ppm is the plan; the remaining -32.1 ppm is the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified; +-0.12 ppm granularity.
- The fs bullet (`:315-320`) says the same, and it says the measurement cannot resolve the plan's -10.64 ppm.
- The Frequencies paragraph (`:244-250`) replaces "the sum of both boards' clock errors" with the signed relative error. The sign is right: measured fs is about plan x (1 + e_DUT - e_SoC).
- "Accuracy", "within the", "sum of both" and "every class" appear nowhere in the page or the index row.
- The arithmetic re-derives: -42.763, -10.639 and -32.124 ppm, and the plan plus the relative error equals the total (`receipts/rederive_fs.json`).

R423-1 F1, the one-bit-offset sentence:

- `:303-314` now names the checks each direction trips, and `:153-161` (Framing) is consistent with it.
- My own probe, `scripts/probe_bit_offset.py`, builds a continuous serial line whose ordinals cross bit 15 and wrap at 0xffff. It runs each case through the packet's decoder (SHA-256 `cfb7121b...`, equal to the packet manifest). Receipt: `receipts/probe_bit_offset.json`.
- **Data one bit early:** 0 torn frames, 0 low-byte words and 0 zero words.
  - Channels 0 to 2 read tags 2t or 2t+1.
  - Channel 3 reads 8, or 9 (invalid).
  - Channels 4 to 7 are invalid in every frame.
  - Every ordinal step is +2.
- **Data one bit late:** every frame is torn, and 256 low-byte words appear (every odd frame). Zero words stay at 0.
  - Channel 0 reads tag 0 and is invalid in every frame.
  - The other channels read the wrong tags.
  - No ordinal step survives.
- That is exactly the page's wording, including "Only the zero-word count stays clean".

R423-1 S2, the data delay:

- `:154-157` and `:303-305` say the one bit of delay is the McASP driver's mapping of `dsp_a`, not a register readback.
- That matches the B4 assignment, which forbade register writes and devmem on any peripheral and allowed only read-only interfaces.

R423-1 S3, the root shell and credential:

- `:15-18` and `:97-99` add the `id` check and "no credential was typed or stored".
- `soc/r2-shell-check.log` shows `uid=0(root)` from `id; tty`, and the STOP comment 5924930868 states "No credential was typed or stored."

## Per-lens results, with evidence

[R422] PASS Conformance - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:15-18,36,61,97-99,115-117,153-161,244-250,303-320` at c39312b4, against round-2 assignment 5925185587 items 1-4, B4 assignment 5924192573, ruling 5924950994, #451 recipe item; `receipts/rederive_fs.json`, `receipts/probe_bit_offset.json`, `receipts/table_identity.txt` - What I checked:

- Every assignment item is met. F1, F2 and R423-F1 are resolved and the four suggestions were taken, as tabled above.
- No verdict says "48 kHz within the SoC board's clock accuracy".
- The framing PASS, fs 47,997.947 Hz, BCLK inferred as 256 x fs, the 475.6 s length row and the #626 limits are unchanged.
- The 11 measurement tables are byte-identical to `35a60c8d`. The only table line that changed is the FSYNC verdict row the assignment names.
- The PR body carries `Refs #451` and no closing keyword. Its issue references are #451 and #626 only.
- The commit subject is one line, with no trailers.

[R422] PASS RTL - `hdl/ieee1722/aaf/KL_tdm_capture_master.sv:46-62,138-146`, `hdl/milan/milan_datapath.sv:1008-1013,1053-1058`, `docs/litex/CLOCK_DOMAINS.md:110-135` at c39312b4, against the page's `:153-161,244-260` - The diff touches no RTL and no gitlink. `git diff --raw e4b771f9..c39312b4` lists two `.md` files. I checked the page's RTL premises:

- BCLK = SLOTS_P x WORD_BITS_P x fs.
- FSYNC is a one-BCLK pulse.
- `DATA_DELAY_P = 1'b1` on both shipping instantiations, which is the `dsp_a` shape.
- Plan A gives `audio = 24,575,738.529 Hz`, so 47,999.489 Hz is -10.64 ppm.
- TDM8 has no idle bit clocks.

All of these are consistent with the page.

[R422] PASS Robustness - `author/soc/r2-shell-check.log`, `author/runs/timing-long/{events.jsonl,controller-logs.txt,ctl-*.jsonl,soc-capture.log}`, `author/tools/run_timing.py` at packet 5a756676, against the page's `:15-18,97-99,264-299,343-351` at c39312b4 - The round-2 text changes three robustness-relevant statements, and each holds:

- The root shell check is a read (`id`, `tty`).
- The talker ended before the unbind, because the stalled capture held the console until its deadline. That ordering is confirmed on one clock (60.04 s). The magnitude is R422-2 F1, filed under Docs.
- The truncated-capture and no-loss statements are unchanged: 95 RUNNING samples on one trigger, the window ending 0.24 s before the event.

[R422] PASS Tests - `scripts/probe_bit_offset.py` with the packet's `tools/decode_capture.py` (sha256 cfb7121b589fe231e139012646fe567b76022e694e08d3bb89d8a7481bda2568), `scripts/rederive_fs.py` over `runs/timing-long/soc-capture.log`, `scripts/page_hashes.py` at packet 5a756676 - The PR adds no executable test. The evidence it rests on can fail, and it re-derives:

- **Decoder.** It trips on both one-bit offsets, in exactly the checks the page names, and passes the aligned case (`receipts/probe_bit_offset.json`).
- **fs.** An independent parser gives 47,997.9474 Hz (first to last) and 47,997.9464 Hz (least squares) over 22,677,480 frames in 472.468 s. The uptime cross-check gives 47,997.714 Hz, the one-step bound is 0.353 ppm, and `SLIP_TDM` gives 10.628 ppm (`receipts/rederive_fs.json`).
- **Hashes.** All 11 page evidence-file rows equal the packet in bytes and SHA-256 (`receipts/page_hashes.txt`). The raw capture is off-packet; see Real limits.

[R422] UNCLEAN Docs - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (all 393 lines) and `docs/findings/README.md:12` at c39312b4; `receipts/gates/gates-summary.txt` - R422-2 F1 is open. The rest of the Docs lens is clean:

- **Gates.** All rc 0 at the exact head, with the hash-locked renderer (cmarkgfm 2025.10.22, html5lib 1.1):
  - `docs_check.py`: 0 findings, scrub self-test 23/23.
  - `check_doc_style.py`.
  - `gen_toc.py --check` and `--verify-anchors`.
  - `check_em_dash.py --base e4b771f9`: 0 over 393 added lines. With `--base 35a60c8d`, also 0.
  - `check_doc_paths.py`: 861 paths.
  - `ci_scope.py --selftest`.
  - `check_feature_status.py --self-test`.
  - `git diff --check` against both bases.
- **Bare-metal gate.** `check_baremetal_only.py --check` first returned rc 2 in my renderer environment, which lacks pyyaml. With pyyaml 6.0.3 it returned rc 0: 0 findings over 951 files. That was a reviewer-environment fault, not a tree fault. CI installs pyyaml for this gate (`.github/workflows/docs.yml:45`).
- **Privacy.** The 47 added lines name no private host, path, serial, peer or instrument, and no wiring, pin or instrument topology. The page's AM62x mentions are the quoted recipe item and are unchanged since round 1.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:15-18,36,61,97-99,115-117,153-161,244-250,303-320` against 5925185587 items 1-4, 5924192573, 5924950994, #451 item; fs re-derivation; offset probe; table identity; PR body references | R422-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| RTL | CLEAN | `KL_tdm_capture_master.sv:46-62,138-146`; `milan_datapath.sv:1008-1013,1053-1058`; `CLOCK_DOMAINS.md:110-135`; diff raw (no RTL, no gitlink) | R422-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Robustness | CLEAN | `r2-shell-check.log`; `events.jsonl`, `controller-logs.txt`, `ctl-*.jsonl`, `soc-capture.log`, `run_timing.py` against page `:15-18,97-99,264-299,343-351` | R422-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Tests | CLEAN | Packet decoder under `probe_bit_offset.py`; `rederive_fs.py`; `page_hashes.py` (11/11 equal) | R422-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Docs | UNCLEAN (R422-2 F1) | Page (393 lines) and index row; docs gates at head (all rc 0); privacy scan of added lines | R422-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |

Every lens examined the findings page. So a fix for F1 un-covers all five lenses under AGENTS section 7, and they must be covered again at the new head. If the fix changes only `:350` and the PR body, a confirmation that nothing else changed would cover it.

## Out-of-scope observation (not a finding on this PR)

`hdl/ieee1722/aaf/KL_tdm_capture.sv:46-48,78-79` labels `DATA_DELAY_P = 0` as "DSP mode A" and 1 as "DSP mode B". `KL_tdm_capture_master.sv:57-59,144` labels 0 as DSP B, as does ASoC, where `dsp_a` is the one-bit delay. The page relies on the master, and its wording matches it. The slave's comment predates this PR. It may deserve its own Issue; that is the manager's call.

## Real limits

- The 730,595,328 B raw capture is held off the packet, so I did not re-decode it. The decode figures come from the packet's `decode.json`, whose SHA-256 equals the page's row, and from round 1's consistency checks.
- The data delay is shown from the DT format, the driver's `dsp_a` mapping and the bit-exact decode. No McASP register was read.
- I had no bench, instrument or hardware access. Physical calibration was NOT RUN, and nothing here is pin-level proof. FSYNC width, edges, levels and absolute ppm remain with #626.
- I ran no full parent, PP, gPTP, Yosys or builder bank. The diff is docs-only, and no simulation was run.
- **Clone integrity.** My gates created a bytecode cache (`scripts/__pycache__`, 9 ignored files). I removed it. After that:
  - HEAD, tree and index tree are `c39312b4` / `d9b3febc`.
  - Status, including ignored and untracked files, is empty, and both diff checks are quiet.
  - No index flags are set.
  - Both PR files hash to their tree blobs, mode 100644.
  - The four gitlinks equal the tree. The three required submodules are at their pins; `external` stays uninitialised by design (`receipts/clone_integrity.txt`).

## Pending manager duties

- **Hosted snapshot** (`receipts/hosted_check_runs.tsv`). Executed and successful: `rtl-fast`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate`. `docs-check` was still in progress. `verilator-suites`, `yosys-portability` and their shards were skipped contexts, the docs-only no-op path, not executed evidence. Hosted and act acceptance stays with the manager.
- Candidate-merge validation against the live dev tip at the merge turn (source base and live dev both `e4b771f9` at review time).
- The second independent review at this head or its successor.
- After R422-2 F1 is fixed, a re-review at the new head covering all five lenses.
- Owner items carried by the PR:
  - re-attaching the SoC board's USB function on the bench host;
  - whether the 1,016 unexplained whole-frame discontinuity clusters get their own Issue;
  - whether the slave capture's DSP-mode comment does;
  - closing #451's timing item once the page is clean, with #626 holding the oscilloscope version.

R422-2 FINISHED
