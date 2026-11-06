[R781] NEGATIVE - exact head 1105f54546b2f19d9577b7fad902c908e34f88ee

# [R781] Internal cleared-context review, round R781-1: PR #846 / issue #843

- Head under review: `1105f54546b2f19d9577b7fad902c908e34f88ee`, tree `94be1980e4b837611cb08bc30b0d5dee1b5ecc7f`, eight commits on dev `cc204c6fd2349b543d73f15c97162a2c4434c86e` (the source base and live dev are the same commit).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Each is covered below with the artifact it was judged on.
- Verdict: NEGATIVE, because one MINOR finding is open under `Docs` (F1). The PR body ties its "GATES GREEN" status and its reproduction checkout to the parent commit `4c4c5982`, and at that commit the firmware service-budget gate fails. I found no defect in the tree. Conformance, RTL, Robustness and Tests are clean at this head.
- Prior public review findings on this PR: none. At review time the PR had only the two review-start notices (`[A10]`, R781-1 and R782-1), no review bodies and no finding comments. So nothing had to be resolved or carried forward.

## How the task was reconstructed

1. I read AGENTS.md and CONTRIBUTING.md sections 3 and 6, and the issue #843 body: scope items 1 to 4 and the three acceptance bullets. I read both issue comments (`[A737] TAKEN`, `[A737] REVIEW READY` naming `1105f545`) and the PR #846 body.
2. I read the authority for the maintainer ruling. The FPGA-gPTP issue #100 body, "Maintainer decisions (2026-11-05)" item 5, says the default clockAccuracy is 0x22 and that it is a build parameter so a build with no characterised oscillator can say 0xFE. The #843 body says AX7101 is 0x22 and Arty is 0xFE. The clauses are IEEE 802.1AS-2011 8.6.2.3 a)/b) and 10.5.3.2.3 (grandmasterClockQuality at Announce offset 48), IEEE 1588-2008 7.6.2.5 Table 6 (0x20..0x31 accuracies, 0xFE unknown, the rest reserved or alternate-profile) and IEEE 1722.1-2021 7.2.8.
3. I read the whole diff `cc204c6f..1105f545` (41 paths) and the commit history: eight one-line subjects with no trailers.
4. I read the published executable evidence at `kebag-logic/milan-fpga@3b2b1ef2`, `review-evidence/843-r1`. I fetched it by blob id and checked each blob's hash (`scripts/fetch_evidence.sh`).
5. I ran my own focused runs and four mutants of my own (below).

Disclosure: while searching for the 2026-11-05 maintainer ruling, a keyword search over the FPGA-gPTP #100/#101 comment threads printed some lines from that repository's own review reports on PR #101. That is a different PR in a different repository. I did not use those lines as evidence and did not open the reports. Nothing below depends on them.

## Findings

### F1 - MINOR - Docs - PR #846 body, "Status" line and "How to get into the same state" block - the PR's green status and reproduction point at `4c4c5982`, where the service-budget gate fails

- Authority/evidence:
  - The PR head is `1105f545` (`gh pr view 846`: `headRefOid 1105f54546b2...`).
  - The body's Status reads "GATES GREEN, TWO OPEN DECISIONS -- ... head `4c4c598273904f6c994b75c860e74ac742ae49d2`".
  - Its reproduction block runs `git checkout --detach 4c4c598273904f6c994b75c860e74ac742ae49d2`.
  - At `4c4c5982` the author's own published sweep shard 2 exits 1 (`author/receipts/sweep-4c4c5982/shard-2/results.json`, `"exit_code": 1`). The log `sweep-4c4c5982/shard-2/fw_service_budget.log` shows the cause: `RuntimeError: oracle image changed; rebuild and regenerate the trace fixture`. That failure is why the head commit `1105f545` exists (it regenerates `oracle.json`).
  - The issue's REVIEW READY comment names `1105f545` correctly, and the green receipts are at `1105f545` (`sweep-1105f545/*/complete.json`, all exit 0 after the shard-2 rerun).
  - So the body states a gate verdict against a commit at which that verdict is false, and it sends a cold reviewer to that commit.
  - AGENTS.md section 6, `Docs`: "The PR and Issue contain enough evidence for another cold reviewer."
  - This is a verdict claim bound to the wrong head, not only wording, so I filed it as MINOR rather than RESIDUE.
- Impact: a reviewer or the manager who follows the PR body validates the parent commit and sees `fw_service_budget` fail. The PR's own summary then contradicts the issue's evidence comment about which commit is green.
- Required outcome: the PR body's Status head and its checkout command name `1105f54546b2f19d9577b7fad902c908e34f88ee` (or whatever head is current when it is next edited). Each gate figure the body states must be bound to the commit it was measured at. The physical gPTP suite stays stated as run at `4c4c5982` with the reason already given.
- Verification: `gh pr view 846 --json body,headRefOid` shows the Status head and the checkout command equal to `headRefOid`. That commit's published sweep and `fw_service_budget` receipts exit 0.

### S1 - SUGGESTION - Robustness - `sw/builder/endstation_builder.py:3725` - `gptp.clock_accuracy` is coerced with `int()`, so a malformed YAML value is truncated or crashes instead of getting a named refusal

- Evidence: `receipts/probe_clock_accuracy_types.txt`, through the full `eb.load_config` path at this head:
  - `34.9` is accepted as `0x22` and reaches `--clock-accuracy 0x22`.
  - `'0x22'` (quoted) raises `ValueError` and `null` raises `TypeError`, neither of them `ConfigError`.
  - `-1` is refused, but the message prints `0x-1`.
- Why only a suggestion:
  - This matches the section's existing convention: `_gp_u8` for priority1 and `_gptp_latency_key` also use `int()`.
  - One resolved value feeds both the image and the AVB_INTERFACE descriptor, so wire and descriptor cannot disagree.
  - Every truncated value that is accepted is still a Table 6 value.
- Optional change: refuse `bool`, non-`int` and quoted values with a `ConfigError` naming the key, as `entity.firmware_rev` does at `endstation_builder.py:3774`. Add one float and one string arm to gate 26c's refusals.

### Not findings (checked and recorded)

- `[R-parallel] on #228` appears on added lines in the five configs, `endstation_builder.py` and `test_builder.py`. These are rewraps and moves of existing text: the per-file counts are equal at base and head (`receipts/r_parallel_counts.txt`: 1/1 for each config, 6/6 and 6/6). So they are existing instances tracked by #746, not new RESIDUE. No other reviewer, lane or bench label was added (`receipts/residue_grep.txt`).
- Issue scope item 4, the stricter-readings page. That page comes with PR #842, which is open against dev and is not on dev `cc204c6f`. This PR says so publicly, uses `Relates to #843` instead of `Closes`, and leaves #843 open. The three frozen acceptance bullets do not include item 4. I record it as a pending manager decision (below), not as a defect of this head.
- The stale entity_model_id table at `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:286-292`. It was already stale and is recorded as audit finding D0-053. This PR moves the two AX7101 ids (`receipts/model_ids_base.txt` against `receipts/model_ids_head.txt`: `0x001BC5C1935893E1` to `0x001BC5CD179523AB` and `0x001BC5572467AF35` to `0x001BC5F6CB4A37D1`). The Arty ids are unchanged. No test or tracked artifact pins the AX7101 ids. Dated findings pages that cite the old id are historical records.

## Focus items (1) to (6)

1. Gitlink and ROM digest (`receipts/pin_and_rom.txt`):
   - `gptp-processor` moves `135afd04` to `1616fc8f`, which is FPGA-gPTP `refs/heads/main` on GitHub (`git ls-remote`) and the merge commit of PR #101 (`gh pr view 101`: mergeCommit `1616fc8f`). Its first parent `5184fb36` is PR #99's merge commit.
   - `syn/yosys/rom_digests.tsv` adds one row, `1616fc8f gptp_ucode.hex e83709d9...`, and keeps every older row. My regeneration with the pin's generator default args (the args `ooc.sh` uses) gives `e83709d9...`, equal to the donor's tracked `syn/ooc/work/gptp_ucode.hex`.
2. clockAccuracy per board:
   - `GPTP_ENGINE_CONSUMED = ("priority1", "clock_accuracy")` (`endstation_builder.py:3567`). `gptp_ucode_args()` (`:3705`) passes `--clock-accuracy` from the resolved config, and both the build (`:5983`) and the milan_dp leg generator use it.
   - The pin is relaxed only for that one field. `clock_accuracy` left `gptp_engine_pins()` and gate 1b's refused set. priority2, clockClass, variance and the three log intervals are still refused on divergence (`_gp_pinned`).
   - Values outside Table 6 are refused (`:3577`, `:3717`), and an omitted key resolves to 0xFE.
   - Resolved values (`receipts/model_ids_head.txt`, `receipts/gptp_ucode_args.txt`): both AX7101 configs 0x22, all three Arty configs 0xFE.
   - Gate 26c and the two legs pass at head. Each value is on the wire: `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A, expected clockAccuracy 0x22` in `gptp`, and `0xF8FE436A ... 0xFE` in `gptp-lat`, both 212/212 (`receipts/runs/H-milan_dp-gptp*.log`).
   - The comments that issue item 1 names (`:3561`, `:4153`, `:4165-4168`) no longer say "consumes only" or "announces this field from a constant".
3. OUR_CQ: `tb/verilator/gptp_shadow/Makefile:13` and `tb/verilator/gptp_plane/Makefile:11` read `CQ_C` from the generator that builds the image and pass it as `OUR_CQ_TB`. `sim_main.cpp` refuses to build without it (`#error`). Each harness now grades the plane's own grandmaster Announce clockQuality: shadow 326/326 and plane 31/31 at head.
4. Service-budget oracle (`receipts/receipts_oracle_vs_published.txt`, `receipts/service_rows_dev_vs_head.txt`):
   - All three rows of `oracle.json` at head carry, field for field, the raw log, log digest, rows, budget findings, heartbeat, liveness and media of the published `service-budget-4c4c5982` receipts. Each digest is self-consistent.
   - The dev re-measure receipt has the same rows, heartbeat and liveness as the head, so the timing drift is dev's. Budget findings are equal everywhere. Only the media digest differs from dev, because the descriptor now carries 0x22.
   - The receipts are `gen_oracle.py`'s inputs, and `gen_oracle.py` refuses a trace it did not grade. So the file was regenerated, not hand-edited.
   - `make -C tb/verilator/fw_service_budget` at head: 14 + 55 checks, 0 failures.
5. Docs inventory: `python3 scripts/docs_inventory.py --check` at head gives `OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)`, rc 0. The diagram and PNG-manifest changes are only the pin label.
6. Area and timing record:
   - The published route receipts (`author/receipts/route-dev`, `route-head`; head routed at `8210abaa`) give dev 51,994 LUT / 54,101 FF / 15,841 slices / 13 DSP / WNS +0.236 / WHS +0.036, and head 52,695 / 54,288 / 15,846 / 15 / +0.018 / +0.015. That is +701 LUT, +187 FF, 4 of 15,850 slices free and +2 DSP. The slow-corner WNS of +0.018 ns is below the +0.03 ns floor at Slow_0C and Slow_85C. Both routes are complete with 0 routing errors.
   - `pp_resource_gate.py` at the head gives `RESULT: MATERIAL REGRESSION` on LUT (+683 over the 52,012 record, tolerance 500), DSP (+2, tolerance 0) and the WNS floor.
   - CHANGELOG.md:102, SUBMODULES.md:439 and AREA_BUDGET.md:151-154 state exactly these figures and this refusal, and say only the shipping directive was routed and the decision is open on #843.
   - The routed image is the builder's 0x22 AX7101 image: receipt `5a1d6d19...` equals my regeneration.
   - No commit after `8210abaa` touches a bitstream input: `git diff --stat 8210abaa..HEAD` lists docs, the oracle and a test only.
   - The "worst path is the SoC's SDRAM controller" sentence comes from a transcription in the published `author/HANDOFF.md`. The raw timing report is published only by sha256 (`route-head/large-files.sha256`).
   - I judge the timing gate as the manager's, as instructed.

## Reviewer runs at this head

All runs are on byte copies of this clone under the packet's scratch directory, with Verilator 5.050 (`receipts/tool_identity.txt`), at 2 jobs per build. Logs are in `receipts/runs/`.

| Run | Result |
|---|---|
| `make -C tb/verilator/milan_dp gptp` | rc 0, 212/212, `[CA]` 0x22 in 4 DUT Announces |
| `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 212/212, `[CA]` 0xFE in 4 DUT Announces |
| `make -C tb/verilator/gptp_shadow run` | rc 0, 326/326 |
| `make -C tb/verilator/gptp_plane run` | rc 0, 31/31 |
| `test_builder.py --gates test_rom_clock_contract,test_baremetal_profile_contract,test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board` | rc 0, `ALL GATES PASS` (subset of 4 of 108); gate 1b prints "gPTP ROM changes with station MAC, priority1 and clockAccuracy" |
| `make -C tb/verilator/fw_service_budget` | rc 0, 14 + 55 checks |
| `scripts/docs_inventory.py --check` | rc 0 |
| `git diff --check cc204c6f HEAD` | rc 0 |
| `scripts/check_em_dash.py --base cc204c6f` | NOT RUN: the pinned renderer lock is not installed here, and installing it was out of bounds. The author's receipt at this head (`final-gates-1105f545/em_dash.rc`) is rc 0 |

Reviewer mutants (patches in `receipts/mutants/`). Each one fails, and fails on the check it targets:

| Mutant | Planted change | Caught by |
|---|---|---|
| m1 | AX7101 1x1 config states 0x21, a valid Table 6 value | `gptp` leg: `FAIL [CA] every DUT Announce carries the config's clockAccuracy got 4` (wire 0xF821436A); gate 26b: `ax7101_1x1_tdm8: gptp.clock_accuracy 0x21, the board's decided value is 0x22` |
| m2 | builder always passes `--clock-accuracy 0x22` | `gptp-lat` leg: `FAIL [CA] ... got 4` (wire 0xF822436A, expected 0xFE); gate 26c: `arty_current passes --clock-accuracy 0x22, its board decided 0xFE` |
| m3 | gptp_shadow image built with `--clock-accuracy 0xFE` | `FAIL as master: every Announce carries this image's clockQuality`, 325/326 |
| m4 | gptp_plane image built with `--clock-accuracy 0xFE` | `FAIL grandmaster Announce carries this image's clockQuality got f8fe436a exp f822436a`, 30/31 |

Clone integrity after the probes (`receipts/clone_integrity.txt`):
- HEAD is `1105f545`.
- The worktree and index are clean, with no ignored residue (the `__pycache__` directories my imports created were removed).
- Index equals the HEAD tree. 1,467 tracked blobs were re-hashed from disk: 0 mismatches and 0 mode mismatches. No assume-unchanged or skip-worktree bits are set.
- The gitlinks are `gptp-processor 1616fc8f`, `protocol-processor a9e84b66`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77` and `third_party/verilog-axis 48ff7a7e`, each mode 160000 stage 0 and checked out at its pin.

## Lens results

```text
[R781] PASS Conformance - sw/builder/endstation_builder.py:3567,3577,3705-3733,4233,5983; configs/endstation_{ax7101_1x1_tdm8,ax7101_8x8}.yaml (0x22), configs/endstation_arty_{current,4x4,8ch}.yaml (0xFE); tb/verilator/milan_dp/sim_gptp.cpp:2066-2086 - per-board clockAccuracy against 802.1AS-2011 8.6.2.3 a)/b), the 2026-11-05 maintainer ruling (FPGA-gPTP #100 item 5) and #843 item 1; Table 6 range (1588-2008 7.6.2.5); Announce grandmasterClockQuality offset 48 / frame octets 62..65 (10.5.3.2.3); AVB_INTERFACE bytes 86..96 (1722.1-2021 7.2.8, gate 26b); the three acceptance bullets met with exact-head runs; item 4 is an open manager decision, not a head defect
[R781] PASS RTL - gptp-processor gitlink 135afd04..1616fc8f (receipts/pin_and_rom.txt): KL_gptp_engine.sv and KL_gptp_rx_parser.sv module headers byte-identical, gptp_ucpu_pkg.sv unchanged, so no parent port/parameter/ROM-geometry change; hdl/ unchanged in the parent; syn/yosys/rom_digests.tsv row equals my regeneration and the donor image; the routed image equals the builder's 0x22 image; the route's +701 LUT / +2 DSP / 4 free slices / +0.018 ns are the engine's #100 growth (upstream scope), recorded and left to the manager's timing gate
[R781] PASS Robustness - endstation_builder.py:3717-3733 and gate 26c refusals (0x00,0x1F,0x32,0x7F,0x80,0xFD,0xFF refused; 0x20,0x31 accepted; omitted key gives 0xFE); receipts/probe_clock_accuracy_types.txt; gen_gptp_leg_ucode.py option-set refusal; #error guards in sim_gptp.cpp and both harnesses; empty $(shell) OUR_CQ fails the compile - malformed, boundary, default and feature paths; only S1 (SUGGESTION) open
[R781] PASS Tests - sw/builder/test_builder.py:17976 (gate 1b arm), :26480 (26b), :26612-26693 (26c); sim_gptp.cpp [CA]; gptp_shadow/sim_main.cpp:1450-1469; gptp_plane/sim_main.cpp:526-545; test_clock_contract.py:138-146 - four reviewer mutants (m1..m4) each fail their target check at this head; the head runs are green (table above); the tests read the wire octet, not the builder's argv alone
[R781] MINOR Docs - PR #846 body Status and reproduction block - see F1; the tree docs (CHANGELOG.md:102, docs/reference/SUBMODULES.md:439, docs/design/AREA_BUDGET.md:151-154, docs/ENDSTATION_BUILDER.md:1067 row 31a, milan_dp/README.md:91-92, GPTP_PLANE/TIME_SYNC/guides donor links at 1616fc8f, DOCUMENTATION_AUDIT.md regenerated) were checked against the receipts and the code and found accurate
```

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | builder consume/refuse paths, five configs, sim_gptp `[CA]`, gate 26b/26c, issue #843 acceptance, FPGA-gPTP #100 ruling, 802.1AS 8.6.2.3 / 10.5.3.2.3, 1588 Table 6, 1722.1 7.2.8 | R781-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| RTL | CLEAN | gitlink and upstream hdl/ headers, rom_digests.tsv, routed image hash, route receipts (dev and `8210abaa`, no bitstream input changed since) | R781-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Robustness | CLEAN (S1 suggestion only) | `_gptp_clock_accuracy_key`, type probe, gate 26c refusals, leg/harness guards | R781-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Tests | CLEAN | gates 1b/26b/26c/ROM clock contract, milan_dp gptp/gptp-lat, gptp_shadow, gptp_plane, fw_service_budget, mutants m1..m4 | R781-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Docs | UNCLEAN (F1 MINOR) | PR #846 body; CHANGELOG, SUBMODULES, AREA_BUDGET, ENDSTATION_BUILDER row 31a, milan_dp README, donor links, diagrams, DOCUMENTATION_AUDIT | R781-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |

## Real limits

- No manager source bank runs at this head, and I neither claim nor infer one. I did not run the full parent sweep or the builder, Yosys, PP or gPTP banks. Sweep, behave, firmware self-test and the docs-workflow results are the author's published receipts at `1105f545`, which I read but did not re-execute.
- I did not route Vivado. The area and timing figures are the author's published receipts. The worst-path attribution comes from a transcription; the raw `alinx_ax7101_timing.rpt` is published only as a hash.
- The em-dash gate was not run here (renderer lock absent).
- The physical gPTP suite evidence is at `4c4c5982`, not at this head; those two commits differ only in the oracle.
- Physical calibration was NOT RUN. Nothing here measures the AX7101 oscillator, so the 0x22 claim rests on the maintainer's ruling. Field skips are not hardware proof.
- The hosted contexts on `1105f545` were partly complete at the time I looked (`receipts/hosted_checks.txt`): the docs, elaborate and rtl-fast/rtl-full jobs listed there were mostly passing. Verilator shards 1 to 18, Yosys shards, `rtl-fast`, `docs-check` and `elaborate` were pending. `Physical gPTP` was skipped, as it runs only nightly or manually. That is not a verdict.

## Pending manager duties

- Route F1 to the executor and re-review the corrected PR body.
- Make the owner decision on the route: the resource-gate refusal (LUT, DSP, WNS floor) and the best-of-3 directive rule (#818). Only the shipping directive was routed.
- Decide issue #843 item 4 against PR #842's landing order. The issue cannot close while item 4 is open.
- Do the hosted and act acceptance at the exact head, and the current-dev candidate merge validation (builder and native banks) at the merge turn.
- Confirm whether any upstream FPGA-gPTP review items addressed to the parent re-pin belong in #843's scope. #843 lists none. I did not read those items' content.
- Carry the existing `[R-parallel]` source-comment instances under #746.

R781-1 FINISHED
