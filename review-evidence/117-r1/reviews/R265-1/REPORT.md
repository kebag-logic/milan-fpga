[R265] NEGATIVE - exact head 0abf147f726721f4a323ee6a32095a02363fe2dc

Round R265-1, external independent review of issue #117 / PR #531.

- Head `0abf147f726721f4a323ee6a32095a02363fe2dc`, tree `512ce39d485d9af8a8b3d411d6395c511d223135`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The diff is three Markdown files: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (new), `docs/design/GM_LOSS_RECOVERY.md` and `docs/findings/README.md`.
- Public evidence commit: `160debeba11231e2fd38fde26c01c467039603ba` (branch `117-review-evidence`, `review-evidence/117-r1`).
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.

## Verdict summary

The bench evidence itself is sound. I re-derived it with my own decoders from the published pcaps, console transcripts, controller logs and power-strip logs:

- identity gate;
- step 2 cadence and turnaround;
- the six-cycle step 3 table: recovery 0.425 to 1.601 s against the 5 s bound;
- publication and `tu` correlation;
- step 5 parity and the Milan-downgrade FAIL;
- bench restoration.

All of it agrees with the page to within about 0.01 s. The packet's own analysis tools also regenerate their published outputs byte for byte.

The head is still not mergeable, for these reasons:

- **Required gate red (F1).** The page's own wording fails the repository's bare-metal-only gate (REQ-VER-04, MUST), so the required `docs-check` context is red at this exact head.
- **Factual slips (F2).** Five statements disagree with the raw artifacts.
- **Stale row (F3).** One acceptance-table row is stale against the page's own step 3 evidence.
- **Untracked follow-ups (F4).** The follow-up issues the page says are needed are neither filed nor linked.

## Findings

### R265-F1 BLOCKER - Conformance, Docs, Tests - docs/findings/117_GPTP_SILICON_EVIDENCE.md:125, :149, :401 - The page fails the bare-metal-only gate, so the required `docs-check` context is red at this head

- **Authority:**
  - `REQUIREMENTS.md:222-224`, REQ-VER-04 (MUST): "... the repository-wide bare-metal-only gate are green with zero policy findings".
  - `CONTRIBUTING.md:55-58`: `docs-check` is one of the seven required `dev` contexts.
  - `.github/workflows/docs.yml:168-171` runs `scripts/check_baremetal_only.py --check`.
  - AGENTS.md section 7: required gates must pass.
- **Evidence:**
  - Hosted `docs` run 35874614091, job 107227198488, at `0abf147f`: `baremetal-only: FAIL (3 finding(s))`. The three findings:
    - `:125` "kernel" (class R);
    - `:149` "host capture" (class S);
    - `:401` "software gPTP owner" (class R).
  - Reproduced locally (`receipts/baremetal_only_by_rev.txt`): base `ede8d48e` 0 findings, rc 0; `c3eb95fa` 2 findings; `0abf147f` 3 findings, rc 1. The failures are introduced by this PR.
  - The lane's published gate records (`bench-a200/gates-c3eb95fa.txt`, `bench-a202/gates-0abf147f.txt`) run five documentation gates and omit this one. They therefore do not cover the workflow behind the `docs-check` context.
  - The hosted job stopped at this step, so the later doc-relevant steps never ran on hosted. I ran them locally and all pass (`receipts/doc_gates.txt`).
- **Impact:**
  - The `dev` merge bar cannot be met.
  - Merging would put a MUST-requirement violation on `dev` and turn `docs-check` red for every later `dev` push.
- **Required outcome:**
  - The page states the same facts without the prohibited terms, so the gate reports zero findings. The gate, its term table and its exemptions stay unchanged.
  - The lane's gate record covers the documentation workflow the context runs.
- **Verification:**
  - `python3 scripts/check_baremetal_only.py --check` rc 0 at the new head.
  - Hosted `docs-check` succeeds on that exact head.
  - `scripts/doc_gates.sh` all rc 0.

### R265-F2 MINOR - Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:45, :125, :305, :320, :474 - Five factual statements disagree with the published raw artifacts

- **Authority:**
  - AGENTS.md section 2: a cold reviewer must be able to reconstruct the task from GitHub and the repository.
  - Issue #117 acceptance box 5: findings include raw artifacts and methodology.
  - The page itself (":36 Every row states what was measured").
- **Evidence:** each item below states the claim, then what the raw artifacts show.
  1. **`:125` host-only records.**
     - Claim: "(76 in Run A, none elsewhere)".
     - Artifacts: the step 3 tap captures carry 38, 0, 38, 45, 0 and 37 host-only records (cycles 1 to 6), and the final 14:13 capture carries 18 (`receipts/probe_details.txt`, `receipts/misc_checks.txt`).
     - The packet's own `bench/cycle{1,3,4,6}/analysis.txt` reports "host-generated excluded 38/38/45/37".
  2. **`:305` holdover duration.**
     - Claim: "`CLKV_STAT` bit 3 (holdover) for 0.3 s".
     - Artifacts: the holdover bit reads set in 3, 3, 5, 3, 4 and 4 consecutive 0.1 s samples (cycles 1 to 6). Cycle 3 shows it from 1.08 to 1.48 s.
     - This is consistent with the RTL's 0.25 to 0.5 s window (`hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:116-122`), but not with a flat 0.3 s.
  3. **`:320` dark-window start.**
     - Claim: "nothing in either direction from 1.03 to 1.71 s".
     - Artifacts: in cycle 2 the DUT sent a Pdelay_Req at 1.75 s (and MSRP at 1.55 s) before the tap went silent (`receipts/probe_details.txt`).
  4. **`:474` binding census.**
     - Claim: "matches the one before them for all 18 states read".
     - Artifacts: the DUT's Stream Output 1 GET_TX_STATE `stream_dest_mac` changed from `00:00:00:00:00:00` (`bench/census-start.jsonl`) to `91:e0:f0:00:8d:6f` (`bench/final/census-final.jsonl`). The connection count is 0 in both (`receipts/census_a200.txt`).
  5. **`:45` daemon check.**
     - Claim: "no daemon on any bench host".
     - Artifacts: `bench/hosts-clock-and-daemons.txt` checked two hosts, the controller host and the capture server, as `:239` itself says.
- **Impact:**
  - None of these changes a PASS result.
  - A reader who re-decodes the published packet finds the durable record contradicted, and cannot tell a transcription slip from a data problem.
- **Required outcome:** each statement matches the raw artifacts, or is scoped to what was measured.
- **Verification:** `scripts/run_all.sh` receipts agree with the corrected text.

### R265-F3 MINOR - Conformance, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:41 - The "reaches asCapable NOT RUN" row is stale against the page's own step 3 evidence

- **Authority:**
  - Issue #117 acceptance box 1 ("reaches and retains asCapable").
  - The task brief: NOT RUN rows must be honest.
  - AGENTS.md section 4: acceptance criteria are judged against the evidence.
- **Evidence:**
  - The row's reason is "the transition happened after the 12:35 UTC power cycle, before these windows opened". That was true of the step 2 windows only.
  - The same page records six asCapable 0-to-1 transitions in step 3 (`:418`, `CLKV_STAT[16]` at 38.78 to 39.91 s). My re-derivation puts them 1.0 to 1.6 s after the switch's first frame on the DUT link, with Pdelay at the step 2 cadence (`receipts/step3.txt`).
  - Commit `0abf147f` updated the box 2 and box 3 rows for step 3, but left this row unchanged.
- **Impact:** the per-box table is what the box decision is read from. As written, it gives a reason the page itself contradicts.
- **Required outcome:** the row either cites the step 3 re-acquisitions with the criterion applied, or keeps NOT RUN with a reason that explains why they do not count.
- **Verification:** the `:41` row and `:418` agree.

### R265-F4 MINOR - Docs, Robustness - docs/findings/117_GPTP_SILICON_EVIDENCE.md:448-449, :458-461, :53, :443 - The follow-up issues the page says are needed are neither filed nor linked

- **Authority:**
  - AGENTS.md section 4: newly discovered work becomes another public Issue.
  - AGENTS.md section 2: public reconstruction.
  - The page itself: "Items 1 to 6 each need their own issue", and "Items 8 to 10 concern the DUT and each need their own issue".
- **Evidence:**
  - `#530` covers items 1 to 3.
  - `#529` covers the step 5 Milan-downgrade FAIL.
  - Issues created on or after 2026-09-23 are only #527, #529, #530 and #532 (`receipts/issue_search_created_2026-09-23.tsv`), so items 4 to 6 and 8 to 10 have no issue.
  - The page links neither #529 (from the FAIL row `:53` or `:443`) nor #530 (from items 1 to 3). It mentions #530 once, at `:363`.
  - Items 8 to 10 are DUT behaviours on the link-loss path that belong to the Robustness lens:
    - LINK_UP and LINK_DOWN did not move over seven outages;
    - Stream Output counters restart at each STREAM_START;
    - there was no ADP advertisement of the DUT's own grandmaster identity.
  - Item 4 is also called "documented design" at `:454`, which contradicts "needs its own issue".
  - The PR description says the observations "are filed as #529 and #530", which does not hold for items 4 to 6 or 8 to 10.
- **Impact:** after merge, these link-loss behaviours would exist only in prose, with no owner.
- **Required outcome:**
  - Every item the page says needs an issue has one, or the page records a disposition for it.
  - The page links #529 and #530 at the items they cover.
- **Verification:** the issue links resolve, and an issue search matches the page.

### R265-S1 SUGGESTION - Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:501-588 - Point the raw-artifact tables at the public mirror

- The page names only the private packets.
- The public mirror (`117-review-evidence` at `160debeb`) exists, and its `MANIFEST.json` maps original to published hashes for the 11 redacted files. One of the listed hashes (attempt 1 lock log, `909699f5...`) is for a file published only in redacted form.
- A pointer would make every listed hash resolvable by a cold reader.

### R265-S2 SUGGESTION - Tests, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:168-170 - State the per-cycle clock-fit quality, not only the residual

- The packet's `analysis.txt` shows these fits:

  | Cycle | Windows kept | Slope |
  |---|---|---|
  | 1 | 10 of 28 | +95.8 ppm |
  | 2 | 7 of 21 | -26.2 ppm |
  | 3 | 13 of 20 | within +/-2.3 ppm |
  | 4 | 21 of 22 | within +/-2.3 ppm |
  | 5 | 20 of 22 | within +/-2.3 ppm |
  | 6 | 21 of 21 | within +/-2.3 ppm |

- The page states only "residual at most 2.0 ms". Cycle 3 is actually 2.017 ms.
- My independent fit, with no outlier rejection, reproduces every table entry within 0.01 s, so no verdict depends on this.

## Lens coverage (this round)

- **Conformance.** Examined issue #117's acceptance and the owner decisions (comments 5561827955, 5565246390, 5789767491 and 5795898094), `REQUIREMENTS.md` REQ-PTP-05..09 and REQ-VER-04/05, `docs/design/GM_LOSS_RECOVERY.md:88-118`, and the result table against the raw data.
  - The bound matches the owner decision: start and end points, 3 + 0.375 + 1.625 = 5 s, Milan intervals.
  - Recovery is 0.425 to 1.601 s in 6 of 6 cycles, and 1.82 to 2.60 s even when counted from the switch's first frame.
  - Loss edges are consistent with the receipt timeouts:
    - sync loss 0.40 to 0.46 s after the last Sync;
    - GM change 3.01 to 3.07 s after the last Announce;
    - asCapable clear 5.01 to 5.09 s after the last Pdelay response.
  - Cadence is within 30 %; turnaround is at most 11,009 ns against 15 ms; peer delay is 380 to 391 ns against 800 ns.
  - The NOT RUN and FAIL rows for Hive, behave, latency, audio, the peer's recovery and Milan compatibility are honest.
  - UNCLEAN under F1 and F3.
- **RTL.** `[R265] PASS RTL - git diff --raw ede8d48e..0abf147f; docs/reference/REGISTER_MAP.md rows 0x720/0x750/0x764/0x774/0x77C/0x780/0x7E4/0x7E8/0x7EC/0x7F0; hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:116-122,244-247; receipts/aem_regen_ede8d48e.txt - checked no HDL, firmware, constraint, config or gitlink change, and checked the page's CSR decodes against the register map and RTL`
  - Decodes checked: `CLKV_STAT` bits 0/1/3/16, `CRFT_CTRL` `0x3002E3`, `GPTP_LAT` 656/219 ns and `ASP_CMD` generation/count.
  - Image identity:
    - The AEM regenerated from `ede8d48e` source is 7,352 B, CRC32 `93742dd2`, SHA-256 `9b077636...`. That equals the on-board AEM CRC and the cited artifact.
    - The QSPI payload CRC `02036e95` equals the asl row and no other seed or the replaced image.
    - The ROM CRC `f6afa4ec` differs from `f6b31625`'s `9c8769a1`.
  - Measured holdover (0.3 to 0.5 s) meets the RTL contract of 0.25 to 0.5 s. F2 item 2 is a transcription item, not an RTL defect.
  - CLEAN.
- **Robustness.** Examined the failure and cleanup paths:
  - attempt 1: the guard switched OUT4 back on after 5.95 s, and the attempt was excluded;
  - the power-strip before, during and after reads;
  - unbind on signal in cycles 4 to 6 (unbound at 109.8 s);
  - A202 census start and end identical except the live propagation delay;
  - 0 kernel drops in all 19 captures;
  - `RST_EPOCH` 1 throughout, and the largest console gap 0.113 s;
  - one stream restart per return, with the peer relocked at 44.80, 43.15 and 44.64 s.
  - UNCLEAN under F4.
- **Tests.** Examined:
  - evidence manifests: 236 entries, 11 redacted and consistent (`receipts/evidence_manifest_verify.txt`);
  - every page hash mapped to a packet file (`receipts/doc_hash_map.txt`). The grader hash equals the `ede8d48e` blob, and the peer firmware-field hash was recomputed;
  - the packet tools regenerate all 6 `analysis.txt`/`analysis.json`, `summary.txt`, the Run A wire summary and the Pdelay output byte for byte (`receipts/packet_analysis_rerun.txt`);
  - my independent decoders reproduce steps 2 to 5 (`receipts/step2.txt`, `steady.txt`, `step3.txt`, `step3_ctl.txt`, `phc_steps.txt`).
  - UNCLEAN under F1.
- **Docs.** Examined:
  - `docs_check`, doc style, TOC check/selftest/anchors, em-dash, doc paths, archive, feature status, DOC_MAP and solution docs: all rc 0 (`receipts/doc_gates.txt`);
  - 33 fragment and relative links all resolve (`receipts/anchors.txt`);
  - the index row and the recovery-bound section.
  - UNCLEAN under F1, F2, F3 and F4.

## Independent re-derivation (page claim versus raw artifacts)

| Area | Page | Re-derived | Receipt |
|---|---|---|---|
| Identity | ROM `f6afa4ec`, QSPI `02036e95`, AEM `93742dd2`, VERSION `00020060`, grader 10/10 | same at 12:41 and 13:44; grader PASS 10/10 in all four logs | steady.txt, misc_checks.txt |
| Sync | 4,556 intervals, mean 124.99-125.02, min 100.6, max 149.4 ms | 4,556; means 124.995-125.017; 100.622 / 149.383; all within 30 % | step2.txt |
| Announce / Pdelay_Req | 565 / 564 / 566 intervals; max 1010.6 / 1029.6 ms; DUT 1000.002 ms | 565 / 564 / 566; 1010.612 / 1029.584; 1000.002 | step2.txt |
| Pdelay exchanges | 568/568 and 570/570; DUT 10,984-11,009 ns; switch outliers 18.33, 18.36 ms | same; 18.330, 18.359 ms | step2.txt |
| asCapable retention | 116 samples all good; 60/60 AS_CAPABLE | 116/116; 60/60 | steady.txt |
| Peer delay | 380-391 ns, median 385; AECP 381-391 | same | steady.txt |
| CRF Run B | 34,061 PDUs, all `tu=0`, bursts 19.67/18.45/15.00/15.00 s | same; sequence continuous; `CRFT_COUNT` `0x850D` | step2.txt, steady.txt |
| Step 3 table | recovery 0.51, 0.52, 1.51, 0.43, 1.46, 1.60 s | 0.508, 0.514, 1.507, 0.425, 1.462, 1.601 s; every other column within 0.01 s | step3.txt |
| Step 3 controller | peer table, GM_CHANGED +2 per cycle, relock times, 0x0040 flag | same | step3_ctl.txt |
| Observation 7 | PHC steps equal the on-to-on interval within 0.04 s | +0.036 s worst | phc_steps.txt |
| Step 5 | probe parity; DUT IEEE17221 only, with the 5.3.8.10 complaint | identical transcripts modulo entity ID; same log lines | misc_checks.txt |
| Bench state | censuses match | A202 identical (live pdelay only); A200 differs in one dest MAC (F2 item 4) | census_a202.txt, census_a200.txt |

## Prior public review findings

There are none on PR #531 at this head. It has no reviews and no review comments; the only comments are the two "review started" notices. The concurrent internal round was not read.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | #117 acceptance and owner decisions; REQUIREMENTS REQ-PTP-05..09, REQ-VER-04/05; GM_LOSS_RECOVERY.md:88-118; result table vs step2/step3 receipts | R265-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| RTL | CLEAN | diff --raw (docs only, gitlinks unchanged); REGISTER_MAP rows; KL_ptp_clock_validity.sv:116-122,244-247; AEM regenerated from ede8d48e; CRC identity table | R265-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Robustness | UNCLEAN (F4) | attempt 1 guard records; power-strip reads; unbind on signal; censuses; capture drop logs; RST_EPOCH; console gaps; stream restart per return | R265-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Tests | UNCLEAN (F1) | evidence manifests; page hash map; packet analysis rerun byte-identical; independent decoders for steps 2 to 5 | R265-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |
| Docs | UNCLEAN (F1, F2, F3, F4) | doc gate set; anchors and links; findings page, index row, recovery-bound section | R265-1 | 0abf147f726721f4a323ee6a32095a02363fe2dc |

## Real limits

- No bench, JTAG, console or power-strip access. Every conclusion comes from the public evidence commit and the public issue and PR comments.
- **Build artifacts are not public.** The bitstream, `bios.bin`, `csr.csv` and `flashboot_layout.json` could not be checked.
  - I could regenerate only the AEM.
  - Bitstream identity rests on the CRC32 readback against the build-ready table. CRC32 is not a SHA-256, and the running configuration was not read over JTAG, as the page says.
  - The `bios.bin` and `csr.csv` hashes, and the la_avdecc library and probe binary hashes, have no public backing artifact.
- The 11 redacted packet files were checked for manifest consistency only.
- The tap-to-host timebase is a fit. Two independent fits agree within about 0.01 s, and the worst margin to the bound is 3.4 s.
- Physical calibration and latency are NOT RUN, and audio continuity is deferred. Skipped hosted contexts and field skips are not hardware proof.
- **Hosted contexts at this head.**
  - Executed: `docs-check` (failure), `rtl-fast`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `bdd-conformance` and `full-ci-gate` (success).
  - Skipped by the docs-only path: `verilator-suites`, `yosys-portability` and their shards.
  - The manager owns hosted and act acceptance. The source static/builder and native bank results the manager cites are not in the published evidence tree, so I could not inspect them.
- I ran no full bank, Verilator, Yosys, act, Docker or builder bank. The only builder use was one AX7101 configuration generation plus AEM packing, in a disposable clone.
- The review clone was restored and verified: HEAD and tree exact, index equal to HEAD, 865 tracked blobs byte- and mode-identical, four gitlinks unchanged, no untracked or ignored files (`receipts/restore_verify.txt`).

## Pending manager duties

- Correct F1 to F4 at a new head, then republish the gate record including the full documentation workflow, and re-review at that head.
- File or disposition the issues for observation items 4 to 6 and 8 to 10 (F4).
- Build and validate the final current-`dev` merge candidate: source base `ede8d48e`, live `dev` `07d85dac` at brief time. Then check containment, and obtain two independent positive reviews with a reviewer-accepted ledger.
- **Evidence-mirror hygiene, outside this PR's tree.** The public `117-review-evidence` mirror still carries bench-identifying material that CONTRIBUTING section 6 keeps out of committed repository text:
  - host names in the clock-offset records;
  - capture interface names in the capture logs and watcher arguments;
  - the reference peer's ENTITY descriptor strings, including its serial number;
  - controller-derived identifiers.

  The PR head itself passes the scrub. Decide whether the mirror needs further redaction.

## Receipts

- `scripts/run_all.sh <clone at head> <workdir>` fetches the evidence commit and regenerates most receipts.
- The separate scripts `aem_regen.sh`, `doc_gates.sh`, `misc_checks.py` and `restore_verify.py` produce the receipts named after them.
- `receipts/hosted_*` are read-only extracts of the hosted check list and the failing job log.
- Every published file is listed in `MANIFEST.sha256`.

R265-1 FINISHED
