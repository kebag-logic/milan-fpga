[R427] NEGATIVE - exact head b5e9242e2e1911bb2bac11221527f8965a4ccaef

# R427-1: external review of PR #630 (issue #629, bench lane B6)

- Head under review: `b5e9242e2e1911bb2bac11221527f8965a4ccaef`, tree `06140cbdf91f0722643609b5520ef32c6179854d`, one commit on dev `ea3fb38877842f223afea97e3bd72a10500455c9`.
- Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new, 534 lines) and one row in `docs/findings/README.md`. No RTL, tool, test or configuration file changes.
- Evidence examined: `review-evidence/b6-r1/` at the assigned `c9ada33881b714f2faf2414123c2b16fac240b6a`, and at the live `b6-review-evidence` tip `128bc058af554ce9c1229fd036fe08c25b4250ac`. The PR body cites the live tip. It is a child of `c9ada338` and changes only `MANIFEST.json`.
- Reconstruction order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #629 body, the assignment (#629 comment 5929778646), and the executor's public TAKEN, STOP and REVIEW READY comments. After those came the PR body and template, the diff, the cited RTL and design documents, then the evidence packet.
- Prior public review findings on this PR: none. The PR held only the two review-start comments when this round began. See "Prior findings" at the end.

## Verdict summary

The bench work is sound, and the page's figures all reproduce from the published grades.

- The tool controls reproduce bit-exactly.
- The clock-source and binding record holds in every run.
- The A1 and B CRF PASS verdicts and the A2 FAIL follow from the evidence.

Three MINOR findings stay open, so the overall verdict is NEGATIVE:

- **F1:** two statements on the page contradict the published evidence.
- **F2:** the capture-path rule has two blind spots that the page does not state, even though the PASS verdicts rest on that rule. None of the measured events falls in either blind spot.
- **F3:** the PR body departs from the template.

## Findings

### R427-F1 - MINOR - Docs, Tests - two statements contradict the published evidence

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:138-139`
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:420-422`
- **Evidence (a), the B CRF window start.** The page says the B CRF window runs "from 20 s after the DUT's servo read LOCKED". The run did something else:
  - `runs/bcrf/events.jsonl` records the clock-source set at t = ...054.756, `servo-lock` 6.49 s later, and `window-start` at t = ...075.253.
  - So the window opened 20.50 s after the set and 14.00 s after LOCKED.
  - `tools/run_b6.py` (packet, around lines 513-530) counts `SETTLE_S` from `t_set`, the clock-source set, not from the lock. `HANDOFF.md:92` repeats the page's wording.
- **Evidence (b), the read-time exceptions.** The page says: "One-frame listener events show no read-time rise ... The two exceptions, 2.7 ms and 177 ms, sit next to A2's 13.3 s stall."
  - In `summary/a2/events.csv`, the two exceptions (capture frames 28,121,160 at 2.6798 ms and 28,147,698 at 176.8061 ms) both have cause `DUT beat`.
  - No listener event in any case exceeds 1.007 ms (`receipts/one-frame-read-jumps.txt`).
  - Cases A1 and B CRF have no listener events, so "in every case" holds only for A0, A2 and B INTERNAL.
- **Impact:** a reader who repeats the method would settle B CRF for 6 s longer than the run did, and would read two DUT beat events as listener events. No figure or verdict changes. The corrected (b) statement is in fact stronger than what the page says now.
- **Required outcome:**
  - The page states the B CRF window start as executed (20.5 s after the clock-source set, 14.0 s after LOCKED), or says why the stated rule differs.
  - The read-time sentence identifies the two exceptions as DUT beat repeats, and says listener events reach at most 1.0 ms with no exception, in the cases that have any.
- **Verification:**
  - Re-read against `runs/bcrf/events.jsonl` and `summary/a2/events.csv`.
  - Run `scripts/check_runs.py` and `scripts/check_blocks.py` in this packet.
  - Check `receipts/one-frame-read-jumps.txt`.

### R427-F2 - MINOR - Robustness, Tests, Docs - the capture-path rule's blind spots are not stated

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:151-162`, the attribution rule.
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:448-466`, the Limits.
  - Packet `tools/grade_b6.py:174-187`.
- **Evidence (a), the rise branch.** A cluster is put on the capture path when the read-time rise matches its size within 1 ms + 2 %. For any skip of 48 frames or fewer (1 ms or less), a rise of zero also passes that test. So a listener skip of 2 to 48 frames, with no read stall and no deficit rise, is attributed to the capture path.
  - A disposable probe ran the published grader on a synthetic 60 s run (`scripts/probe_attribution.py`, `receipts/probe-attribution.txt`).
  - Planted listener skips of 2, 12 and 48 frames came out as `capture path`.
  - Planted skips of 60 frames and 1 frame came out as `listener`, which is correct.
  - A planted 108-frame capture loss came out as `capture path`, which is correct.
- **Evidence (b), the unmeasurable-rise branch.** This branch accepts a cluster on a read gap of 11 ms or more in the 63 reads around it. It does not require the 48 n + 12 size, although the page's wording at :158-161 implies a size check only "where the rise is spoiled". In these runs a random event meets that gap test by coincidence with a probability of at least 9 to 28 % per case (`receipts/attribution-exposure.txt`).
- **Exposure in this data: none.**
  - No capture-path cluster in any case lost fewer than 60 frames.
  - All 11 gap-only clusters also have every skip at 48 n + 12.
  - A one-frame event can never join a cluster: `receipts/rule-uniform.txt` shows zero one-frame events attributed to the capture path.
  - So the A1 and B CRF verdicts stand.
  - However, the page answers "could the capture-path attribution hide a listener slip" only through its "refined" rule. Its Limits do not say that this rule would absorb a small multi-frame listener skip. A cold reader cannot tell that from the page, and later lanes reuse the method.
- **Required outcome:** the page states both blind spots together with the measured non-exposure: the smallest capture-path loss was 60 frames in every case, and every gap-only cluster was also 48 n + 12. Alternatively, the rule is tightened and re-applied to every case.
- **Verification:**
  - Compare the page text with `receipts/attribution-exposure.txt` and `receipts/probe-attribution.txt`.
  - If the rule changes, re-grade all five cases and confirm the per-case tables.

### R427-F3 - MINOR - Docs - the PR body departs from the template

- **Where:** the PR #630 body, compared with `.github/PULL_REQUEST_TEMPLATE.md`.
- **Evidence:**
  - The body has no "Contents" section. The template has one, and the sister bench PR #628 carries it.
  - "How to validate" is a bullet list of script names, not the template's command block of exact commands.
  - The stated pass criteria are that every figure traces to the packet and every hash resolves. No command is given for either check, nor for the pinned-environment invocation.
  - CONTRIBUTING section 2 says: "PRs use the template".
- **Impact:** a cold reviewer cannot run the validation as written, and the PR body does not have the shape the template requires.
- **Required outcome:** the PR body carries every template section, and How to validate gives runnable commands with their expected results.
- **Verification:** compare the body's headings and validate block with the template.

### Suggestions (optional; these do not affect coverage)

- **S1 (Tests).**
  - The synthetic controls check the clean floor only against the tool's own floor. A mutant that halves the band power (a 3 dB error) survives them. The other 7 of 8 mutants are killed (`receipts/control-mutants.txt`).
  - The published floor is correct when computed independently: -146.064 dB and -145.993 dB from the exact rounding error, -146.051 dB analytic (`receipts/floor-independent.txt`).
  - Adding an analytic-floor assertion would pin it.
- **S2 (Docs).**
  - :333: add `hdl/ieee1722/crf/KL_crf_tx.sv` (the module header describes the /512 divider of `clk_audio_i`) beside the datapath port comment the page cites.
  - :313: lane B5's record states 16.46 ppm, not 16.4. Link that record, PR #628 or `117_AUDIO_CONTINUITY.md` once merged, wherever the page says "lane B5".
  - :379: "stayed LOCKED through the window" rests on three reads (at 5 s, 315 s and 615 s), a static `SLIP_TDM` and 0 net steps. Saying so would be more precise.
  - Method: say that the board's bridge legs were stopped by PID before the cases and restarted at the end. The page now shows this only as "new process IDs" in Bench as left.
  - :305: the largest comb residual is 1.817 frames, slightly over the stated 1.8.
- **S3 (Docs).** Once filed, link the follow-up Issue or decision for A2's talker disagreement and for the servo's DRP config mismatch bit.

## The questions this round was asked to judge

1. **The tool and its synthetic controls: PASS.**
   - `b6_thdn.py controls` re-run in this packet produced a `controls.json` byte-identical to the published one: SHA-256 `7bbefc71...`, 0 field differences (`receipts/controls-compare.txt`).
   - Clean floor: -146.06 / -145.99 dB, confirmed independently (S1).
   - One drop was found at frame 216,777 and one repeat at frame 289,234, each with size 1.
   - 16 ppm and 1 ppm as resampled tones were fitted at +16.000000 and +1.000000 ppm.
   - 16 ppm and 1 ppm as slips gave 23 and 4 one-frame skips, at spacings of 62,500 and 1,000,000 frames.
   - The tone loop regenerates to the page's hash `566d3dfa...`, with 48,000 unique pairs and 0 silent frames (`receipts/tone-rerun.txt`).
2. **The clock-source record: PASS.** In all five graded runs and the probe (`receipts/check-runs.txt`):
   - A format check preceded every bind.
   - Every set went to the listener, was read back by a separate GET, and equalled the talker's format. No talker format was set.
   - Clock sources were set only on the listener: the peer in A1 and A2, the DUT in B CRF. Each read back equal and was restored to the as-found source, then read back.
   - Every format and map ended as found.
   - The peer's CLOCK_SOURCE descriptors place the A1 source on the input that carries the AAF format, and the A2 source on the input that carries the CRF format (`receipts/peer-clock-sources.txt`).
   - Each window opened at least 20 s after the last bind or set. B CRF is the exception noted in F1.
3. **The case verdicts.** Every table figure reproduces from `summary/<case>/grade.json`, `events.csv` and `blocks.csv`: listener drops and inserts, beat repeats, combs, `SLIP_TDM`, capture events, clusters and frames, reads and stalls, blocks at the floor, offsets, counted and timed ratios, and halves (`receipts/recheck-cases.txt`, `receipts/check-blocks.txt`).
   - **A0 and B INTERNAL** show the mismatch: 519 and 506 one-frame listener drops, with +6.52 and +6.05 ppm counted.
   - **A1 PASS:**
     - 0 listener events and 0 undecodable frames.
     - All 315 one-frame repeats sit on the beat comb, one per tooth. The 7 missing teeth all fall inside capture-path losses, so no listener drop cancelled a beat.
     - Counted -10.631 ppm, which equals the beat; timed -12.19 +-2.44 ppm.
   - **A2 FAIL**, and the diagnosis is supported, not merely consistent:
     - Two independent measurements show the DUT's two talker outputs carrying clocks 10.6 ppm apart. A peer following the CRF tracks McASP0 to -0.068 ppm (2 frames in 616 s). A peer following the AAF tracks McASP0 at -10.63 ppm.
     - The mechanism is consistent with the cited code and design: `KL_crf_tx` stamps the /512 grid of `clk_audio_i` (`milan_datapath.sv:445` and :5756, `KL_crf_tx.sv` header), while the packet grid is the free-running NCO (`TIME_SYNC.md:166-169`).
     - The page's own Limits state that no CRF timestamp was captured on the wire.
   - **B CRF PASS:**
     - Counted 0 net steps in 30,237,600 frames; timed -0.01 +-0.65 ppm.
     - `SLIP_TDM` static (0xc066) through the window.
     - `MCSRV_STAT` 0xffa00034 to 0xffa10034, which decodes per `REGISTER_MAP.md:2082` as state 4 LOCKED, bit 4 DRP config mismatch and trim -96/16 = -6.0 ppm.
     - 0 undecodable frames.
4. **The attribution rules: stated, uniformly applied, and following from the evidence, with the limits in F2.**
   - Every one of the 132 clusters across the five cases re-derives to its published decision under the stated rule (`receipts/rule-uniform.txt`).
   - The grader has no case-specific branch.
   - The page's statements about the refinement check out: 255 of 265 rise-matched skips are 48 n + 12, and the 10 exceptions are classified correctly; there are five stale-replay clusters; the 12-loop 18,626-frame loss has a rise of 12,387.9 ms.
   - Read stalls of up to 13.3 s, and losses that match the stall size, follow from the read-time deficit. Each stale replay hides 1 to 6 frames of real audio.
   - A one-frame listener slip cannot be absorbed into a cluster. Audio the capture path lost hides any event inside it; that is about 2 % of A1's window, and the page states it.
5. **Restore and residuals: acceptable as recorded.**
   - The census matches 43 of 46 entries. The other three are the DUT's propagation delay and two peer talker states that keep a stream ID, destination MAC and VLAN at connection count 0 (`restore/census-compare.txt`).
   - DUT NVM went from 2 to 8 commits, seq 238 to 244, with `dirty=0` at the end (`restore/dut-end.txt`). The saved image therefore matches the live state, whose formats, maps and clock source read back as found.
   - Identity values on the page equal `identity/console-identity.stdout` and `grader-identity.txt` (10/10).

- **Evidence hashes.**
  - Against `MANIFEST.json` at the assigned `c9ada338`, 42 of the page's 54 hashes resolve to `original_sha256` or `RAW-ARTIFACTS.json`. The other 12 are label-masked files whose `original_sha256` there equals the masked hash.
  - At the PR-cited `128bc058` (MANIFEST.json only: "Record the unmasked originals' hashes"), all 54 resolve. All 240 published files re-hash to their `published_sha256` (`receipts/hash-check.txt`).
  - The masked grade tool reproduces the page-cited original hash once its labels are substituted (`receipts/unmask-probe.txt`).
- **Public text.**
  - The page and the index row name no host, peer, switch or instrument. They state no channel map, capture layout, stream count or peer index, and use role labels only.
  - The signal-path wording follows the assignment's own public text and pages already on dev (`451_TDM8_TIMING_SOC_BOARD.md`, `617_DIN_FRAME_COHERENCE_BENCH.md`).
  - The docs gates pass at this head in the pinned Markdown environment (`receipts/docs-gates.txt`): `docs_check`, `check_doc_style`, `check_em_dash --base ea3fb388` and `--selftest`, `gen_toc --check` and `--verify-anchors`, `check_doc_paths`, `check_feature_status --self-test`, and `git diff --check`.
  - The commit message is one line with no trailers.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 body acceptance and assignment 5929778646. Page :20-33, :138-147, :219-229, :250-271, :291-341, :366-389. `runs/*/events.jsonl` (`receipts/check-runs.txt`). `restore/peer-descs.jsonl` (`receipts/peer-clock-sources.txt`). `summary/*` (`receipts/recheck-cases.txt`). `hdl/milan/milan_datapath.sv:445`, :5756. `hdl/ieee1722/crf/KL_crf_tx.sv` header. `docs/design/TIME_SYNC.md:166-169`, :463-478 | R427-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| RTL | CLEAN | Diff name-status (no `hdl/` path). Page register claims against `docs/reference/REGISTER_MAP.md:2082` (`MCSRV_STAT`) and :847 (`CRF_CTRL`). `SLIP_TDM` 0x8D8 against `TIME_SYNC.md:169`. CRF talker clocking at `milan_datapath.sv:445`, :5756-5759. Gitlinks unchanged against base | R427-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Robustness | UNCLEAN (F2) | Packet `tools/grade_b6.py:114-260`. Synthetic attribution probe (`receipts/probe-attribution.txt`). Exposure (`receipts/attribution-exposure.txt`). Stale-replay and loop-folded clusters in `summary/{a1,a2,bcrf}/grade.json`. Undecodable/torn/boundary handling in packet `tools/b6_thdn.py:109-161` | R427-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Tests | UNCLEAN (F1, F2) | Controls re-run, byte-identical (`receipts/controls-compare.txt`). 8 tool mutants (`receipts/control-mutants.txt`). Independent floor (`receipts/floor-independent.txt`). Tone regenerated (`receipts/tone-rerun.txt`). Rule re-derivation (`receipts/rule-uniform.txt`). Run windows (`receipts/check-runs.txt`) | R427-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Docs | UNCLEAN (F1, F2, F3) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (all 534 lines). `docs/findings/README.md:15`. PR #630 body against `.github/PULL_REQUEST_TEMPLATE.md`. Hash table against the evidence (`receipts/hash-check.txt`). Docs gates (`receipts/docs-gates.txt`) | R427-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |

## Real limits of this round

- The raw captures, read-time records and timing samples stay on the bench host. The grades were re-derived and audited from the published summaries, events and blocks, not recomputed from raw audio. The grader's behaviour was probed on synthetic data only.
- `tools/run_b6.py`'s page-cited original hash was not reproduced from its masked copy. It rests on `MANIFEST.json` at `128bc058` and on the packet's own `MANIFEST.sha256`. Its format-check, set-clock and settle logic is outside the masked lines and was read directly.
- No hardware or bench access. Physical calibration was NOT RUN. The rates are on uncalibrated clocks, as the page states.
- No RTL changed, so no simulation ran and the pinned Verilator was not needed. No full banks, act, Docker or hosted-runner actions were run.
- At the snapshot time (`receipts/hosted-checks-b5e9242e.tsv`), the exact-head hosted `rtl-fast`, `full-ci-gate`, `elaborate`, `bdd-conformance`, `wire-accountability`, `changes` and `docs-check-no-git` had executed and succeeded. `docs-check` was still in progress. The Verilator/Yosys shards, `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration` and the physical gPTP job were skipped contexts, which are not evidence.
- After every probe the clone was verified: `HEAD` and index tree equal the head tree, 978 tracked files have equal bytes and modes, there are no assume-unchanged or skip-worktree flags, and all four gitlinks are unchanged (`receipts/clone-integrity.txt`).

## Pending manager duties

- **Evidence archive mask.** In both evidence commits, the published grade tool still spells the capture layout in the code of its channel-identification step. The label mask covered only its docstring. Re-mask and republish it. This is outside the PR diff; this report does not repeat the values.
- **Evidence reference.** The review-start comment points at `c9ada338`, where 12 cited masked files lack their unmasked `original_sha256`. The PR body and the live branch use `128bc058`, where all 54 resolve. Point the record at `128bc058`.
- **Follow-up Issues (AGENTS section 4):**
  - A2's DUT-talker disagreement at INTERNAL: the CRF output runs on the physical grid and the AAF stream on the NCO grid. The executor recorded it as needing an owner decision or a new Issue, and it is not filed.
  - The servo's DRP config mismatch bit read on silicon. This is its first record in `docs/`.
- **Self-test evidence on the PR.** The DoD item is unchecked and the REVIEW READY evidence sits on the Issue.
- **Merge-turn duties:** hosted `docs-check` completion, act acceptance, the current-dev candidate merge build, and the internal review R426.

## Prior findings

When this round started (2026-10-01T13:06:59Z), the PR held no review findings, only the two review-start comments, so no prior finding needs resolving or retaining.

A metadata-only re-check was made after this verdict and ledger were written (`receipts/prior-findings-check.txt`).

- It shows the concurrent internal round R426-1, posted at 13:24:00Z with its own verdict. That round is concurrent, not prior.
- It was not read before this verdict, and this round neither adopts nor answers it.
- The PR head is still `b5e9242e`.

R427-1 FINISHED
