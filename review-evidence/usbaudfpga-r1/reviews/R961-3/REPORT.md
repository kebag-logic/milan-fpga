[R961] POSITIVE - exact head 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7

# R961-3: internal independent narrow re-review of PR #1024 (issue #1021), round 6

- Exact head `00979246dc22698c0f3a1e4a9796c1a2bcdd03c7`, tree `ef2e4bc77621cf2b6edc98952472239c137ead97` (verified in the clone).
- Previously reviewed head `0f7402ee97d347352b8c3d613033c440ee55986a` (R961-2, comment 7219613979, NEGATIVE on N1 and N2). Delta reviewed: `0f7402ee..00979246`, one commit.
- Scope (narrow, per brief): my round-2 findings N1, N2 and R1, plus the claim that no gateware changed. Code the delta does not touch keeps its R961-2 lens verdict unless the delta changes what it depends on.
- Reconstruction order: AGENTS.md and CONTRIBUTING.md, docs/README.md, issue #1021 scope and frozen criteria (as reconstructed in R961-2), my R961-2 findings, the diff and history, the author packet `c3658705:review-evidence/usbaudfpga-r1/author-r6`, and exact-head hosted check runs. The external comment 7219426750 was read only after my own pass and probes, for prior findings only.
- All five lenses were applied.
- **Verdict: POSITIVE.** N1 and N2 are closed at this head. R1 is RESIDUE: it is retained, and it recurs in the round-6 handoff. One new RESIDUE (R2) and one new suggestion (S6) are recorded. No BLOCKER, MAJOR or MINOR is open.

## Delta and the gateware claim

`receipts/delta-and-tools.txt` (`git diff --raw 0f7402ee 00979246`) lists seven entries, all with mode 100644:

- `docs/design/USB_AUDIO_PATH.md`
- `docs/reference/REGISTER_MAP.md`
- `scripts/register_descriptions.json`
- `tb/verilator/usbaudio/{check.py,epochs_tb.sv,media_tb.sv,transport_mutations.py}`

No entry under `hdl/`, `configs/`, `sw/` or the constraints changed, and no gitlink changed. **The claim of no gateware change is verified.** None of the three N2 defects was fixed in behaviour. Each was closed by adding stimulus and a check, so the RTL that R961-2 judged correct is byte-identical here.

## Prior findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R961-2 N1 MINOR (Docs): register reference contradicted the writable-latency RTL | **Closed** | See "N1 detail" below. |
| R961-2 N2 MINOR (Tests): three ordering defects survived every test | **Closed** | See "N2 detail" below. |
| R961-2 R1 RESIDUE: broken handoff links | **Retained as RESIDUE, and it recurs** | See R1 below. The round-5 correction patch exists, but it is not applied in the published packet. The new round-6 handoff repeats the same broken targets. |
| R961-2 S5 SUGGESTION (Tests): no per-run timeout in the plant harness | Retained, optional | The `transport_mutations.py:5-7` docstring lists "timeouts" as a campaign failure, but the run call at `:305` has no `timeout=`. This was not changed in the delta. |
| R961-1 S1, S2, S3 (also external R962-2 S1 to S3) | Retained, optional | Not touched by the delta. |
| External R962-2 S4 (duplicate reader key) | Outside my narrow scope | It does not affect my lenses at this head. The evidence ratchet passes (`receipts/docs-gates.txt`). |
| External R962-2 R1 RESIDUE (round-5 links) | Same root as my R1 | Merged into R1 below. |

### N1 detail

- **Generated, not hand-edited.** I ran `gen_register_reference.py --check` with the pinned `wavedrom` 2.0.3.post3 on an exported head tree. It reports `register reference: fresh (203 registers, 34 modules, 240 files)` and exits 0 (`receipts/register-reference-check.txt`). The check fails on any byte difference between the page and its regeneration from `scripts/register_descriptions.json`. So the `REGISTER_MAP.md` delta is exactly the generator's output from the corrected prose source.
- **Prose matches the RTL** (prose at `scripts/register_descriptions.json:1608-1635,3282-3291`, rendered at `docs/reference/REGISTER_MAP.md:1046-1080` and near `:3355-3367`):
  - **Applied bits.** Only `[15:0]` apply, at `hdl/milan/milan_datapath.sv:1896-1910` (`lat_ing_r <= s_axi_wdata[15:0]` on the AWREADY write).
  - **Upper bits.** The full word stays readable from the CSR shadow.
  - **Sign of each correction.** Ingress is subtracted at `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:401-403`, and egress is added per `:36-37`.
  - **Reset values.** The words reset to the configured correction when writable and to zero otherwise (`hdl/common/csr/milan_csr.sv:1593-1596,2053-2054`).
  - **GPTP_LAT.** It reads the applied pair and reads zero with the plane off (`milan_csr.sv:2403-2404`).
  - **Arty split values.** The split resets to 1409/100 ns (`configs/endstation_arty_split.yaml:228,258-259`).
- **The required greps hold.** `grep latency_writable docs/reference/REGISTER_MAP.md` finds the option at the 0x540, 0x544 and 0x7F0 entries (lines 1048, 1056, 1058, 1068, 1076, 1078 and 3358).

### N2 detail

**The new stimulus covers both outcomes N2 asked for.**

- **Deferred playback transition** (`tb/verilator/usbaudio/media_tb.sv:82-125`, looped at `:190` over offsets 0-6):
  - **Offsets.** Offsets 0-6 are exactly the deferral window: offset 0 is the coincident grid event and offsets 1-6 are `emit_r != 0` (`KL_usbaudio_media.sv:64,121-132`). Offset 7 is not deferred and stays covered by the existing grid loop.
  - **Stimulus.** The new epoch's frame is at the FIFO head with acknowledgement room.
  - **Retention.** The checks require that the frame is never ready during deferral or on the application cycle, and that no acknowledgement fires before application.
  - **Exercised window.** `MEDIA_DEFERRED_WINDOW_EXERCISED` requires the deferral to have actually happened, so the check cannot pass vacuously.
  - **Playback.** After application, 11 queued frames do not prime, 12 do, and the retained frame is then played bit-exact exactly once with zero gaps.
- **Status record held across capture-epoch application** (`tb/verilator/usbaudio/epochs_tb.sv:74-75,180-200`):
  - **Stimulus.** An old-epoch status record is held after its third word across the capture-state application.
  - **Fence.** While the host-visible epoch is not the new one, a per-cycle fence check requires the capture packetizer to stay disabled.
  - **Old record.** The old record completes unchanged.
  - **Release.** Capture opens only after a record carrying the new epoch completes.

**Executed results.** Every run used the pinned simulator, whose `--version` reports `Verilator 5.050 2026-07-01 rev v5.050`.

| Run | Result | Receipt |
|---|---|---|
| The three new plants (my p7, p8 and p9, edit-identical to R961-2) with clean `epochs` and `media` baselines | Each is CAUGHT by its own named check: `BRIDGE_SNAPSHOT_ACK_BEFORE_CAPTURE`, `MEDIA_DEFERRED_FRAME_RETAINED`, `MEDIA_DEFERRED_ACK_AFTER_APPLY` | `receipts/plants-A1-results.json`, `receipts/plant-detections.txt` |
| Every other plant on the two changed benches (5 bridge and 9 media), each with a clean baseline | 14/14 CAUGHT by name, so the bench edits regressed no existing detection | `receipts/plants-A2-results.json`, `plants-A3-results.json`, `plants-A4-results.json` |
| Default audio regression (`check.py --jobs 4`) | PASS, rc 0. Includes protocol, reference, media, packet, GPIF, levels, epochs, both storage widths and the short duplex (1,000 frames). The default defect subset ran 15 plants, including the three new ones, all CAUGHT with 6 clean baselines. | `receipts/default-regression-summary.txt`, `receipts/default-regression-defects-results.json` |

**Falsification probes** (`scripts/probe_plants.py`, which reuses the shipped harness with my own plants; `receipts/plants-C1-results.json`, `receipts/plant-detections.txt`). Each probe is a different edit with the same effect as one of the guarded failures, and all four were detected:

- **q2:** the status epoch tracks the applied epoch continuously. It is caught by `BRIDGE_SNAPSHOT_ACK_BEFORE_CAPTURE`, the new fence.
- **q3:** the epoch is published on the first status beat instead of the last. It is caught by `BRIDGE_PUBLISHED_ACK_GATE`, an earlier existing check.
- **q4:** the media endpoint consumes the queued frame on the application cycle. It is caught by `MEDIA_DEFERRED_FRAME_RETAINED`, the new check.
- **q6:** the media endpoint does not re-prime on a playback epoch change. It is caught by `MEDIA_PLAYBACK_BITS`, an earlier existing check.

The harness reports q3 and q6 as NOT_CAUGHT and exits rc 1, only because I guessed the detecting check's name wrong. Both were detected by real named checks, as the `run.log` lines in `plant-detections.txt` show.

## Findings (this round)

### R1 RESIDUE: author handoff links point at paths that do not exist (evidence packet only; retained and recurring)

- **Lenses:** Docs (packet navigation only).
- **Artifacts:** `review-evidence/usbaudfpga-r1/author-r6/HANDOFF-r6.md:6,22` and `REVIEW-READY.md:11` at `c3658705`. The round-5 copies `author-r5/HANDOFF-r5.md` and `REVIEW-READY.md` are still uncorrected at `c3658705`.
- **Evidence:**
  - The round-6 files link `receipts/r6/review-response.md` and `receipts/INDEX.md`. The packet has `receipts-r6/review-response.md` and no `INDEX.md`.
  - The prepared `receipts-r6/public-link-correction.patch` fixes only the round-5 pair, and it has not been applied.
  - The receipts themselves are intact: all 107 `author-r6/` entries match `MANIFEST.json` (0 hash mismatches, 0 unlisted, 0 missing, 0 redacted; see `receipts/author-r6-manifest-check.txt`).
- **Why RESIDUE:** this is pure navigation wording in packet prose. It changes no measurement, verdict, test or contract claim.
- **Exact fix:**
  1. In `HANDOFF-r6.md` and `REVIEW-READY.md`, replace `receipts/r6/review-response.md` with `receipts-r6/review-response.md`.
  2. Replace `receipts/INDEX.md` with `../MANIFEST.json`, labelled "evidence manifest".
  3. Apply the prepared round-5 patch.

### R2 RESIDUE: new bench comments state behaviour but cite no issue or requirement ID

- **Lenses:** Docs (source-comment wording only).
- **Artifacts:** `tb/verilator/usbaudio/media_tb.sv:80-81,115` and `tb/verilator/usbaudio/epochs_tb.sv:180,197`.
- **Evidence:** the owner comment rule says source comments state behaviour and reason with issue and requirement IDs. These new comments state behaviour but carry no ID. They do not contain any lane label, round, reviewer ID or comment ID; that check is clean.
- **Exact fix:**
  - Append `(#1021; AUDIO-FPGA.md 9e5ef16 lines 117-120, 166-167)` to the `media_tb.sv:80` comment.
  - Append `(#1021; AUDIO-FPGA.md 9e5ef16 lines 140-142, 173-175)` to the `epochs_tb.sv:180` comment.

### S6 SUGGESTION (Docs): clarify the plant sentence

- **Artifact:** `docs/design/USB_AUDIO_PATH.md:153`, which reads "Three separate defects remove those ordering guards."
- **Suggestion:** say what the defects are and what catches them. For example: "Three planted defects, each removing one of those guards, fail named checks in the default regression."
- **Why it is optional:** the sentence is accurate.

## Other executed evidence

| Run | Result | Receipt |
|---|---|---|
| `docs_check.py` (in the git clone) | 0 findings: 230 md files, 2,043 scrubbed files, self-test 23/23 | `receipts/docs-gates.txt` |
| `docs_inventory.py --check` | OK, `DOCUMENTATION_AUDIT.md` fresh | `receipts/docs-gates.txt` |
| `measure_test_evidence.py --check` | PASS (71 <= 77, 10 <= 10, 0 <= 0, 3 <= 3) | `receipts/docs-gates.txt` |
| Author packet integrity | 107/107 `author-r6` entries match `MANIFEST.json` | `receipts/author-r6-manifest-check.txt` |
| Author source-identity spot check | The before and after sha256 of `USB_AUDIO_PATH.md`, `REGISTER_MAP.md` and `register_descriptions.json` in `source-identity.json` match the git blobs at `0f7402ee` and `00979246` | (re-derivable) |
| Clone integrity after probes | HEAD and tree as stated; index tree equals the head tree; worktree identical to HEAD; `status --porcelain --ignored` is empty; six gitlinks unchanged | `receipts/clone-integrity.txt` |

## Clean-lens evidence

[R961] PASS Conformance - `tb/verilator/usbaudio/media_tb.sv:82-125,190`, `epochs_tb.sv:74-75,180-200`, `scripts/register_descriptions.json:1608-1635,3282-3291` - What I checked:
- the new checks against AUDIO-FPGA.md 9e5ef16: lines 117-120 and 166-167 (flush and prefill before a new playback epoch, no uncounted gap), and lines 140-142 and 173-175 (apply, then acknowledge, then emit capture);
- the regenerated register contract against `milan_csr.sv`, `milan_datapath.sv`, `KL_gptp_shadow.sv` and `endstation_arty_split.yaml`.

No gateware changed, so the R961-2 conformance of the RTL to criteria 1-2 carries forward unchanged. Criterion 3 remains correctly open.

[R961] PASS RTL - `git diff --raw 0f7402ee 00979246` (`receipts/delta-and-tools.txt`) - No entry under `hdl/`, configs, sw, constraints or gitlinks changed. The RTL that R961-2 covered at `0f7402ee`, an ancestor, is byte-identical. The datapath, CSR and shadow RTL that the new register prose describes was read and matches it (N1 detail).

[R961] PASS Robustness - `receipts/plants-C1-results.json`, `media_tb.sv:82-125`, `epochs_tb.sv:180-200` - What I checked:
- a transition at every deferral offset with the next epoch's frame queued;
- prefill below and at the threshold after the transition;
- an old record stalled mid-stream across capture application, then completed and held;
- four reviewer probes (q2, q3, q4, q6), each detected by a named check.

[R961] PASS Tests - `receipts/plants-A1-results.json` to `plants-A4-results.json`, `receipts/default-regression-summary.txt`, `tb/verilator/usbaudio/transport_mutations.py:22-30`, `check.py:55-56` - What I checked:
- the three requested plants are CAUGHT by their own named checks with clean baselines;
- all 14 other plants on the changed benches are still CAUGHT;
- the default regression includes the three new plants and passes;
- the harness requires a clean baseline, a single exact plant site, and the named `CHECK` string, so a build failure counts as BUILD_FAILED and is never counted as caught.

[R961] PASS Docs - `docs/reference/REGISTER_MAP.md:1046-1080,3355-3367`, `receipts/register-reference-check.txt`, `docs/design/USB_AUDIO_PATH.md:149-153`, `receipts/docs-gates.txt` - What I checked:
- the generated page is fresh from its corrected source and matches the RTL;
- the design-document addition matches the benches;
- docs, inventory and evidence gates pass.

R1 and R2 are RESIDUE and S6 is a SUGGESTION; none of them affects coverage.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | AUDIO-FPGA.md 9e5ef16:117-120,140-142,166-167,173-175 against the new checks; register prose against the CSR, datapath and shadow RTL and the Arty split config; no gateware delta | R961-3 | 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7 |
| RTL | CLEAN | `git diff --raw` for the delta (no hdl, config, sw or gitlink entry); latency RTL read for N1 | R961-3 (re-applied to the delta; R961-2 at ancestor 0f7402ee covered the unchanged RTL) | 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7 |
| Robustness | CLEAN | Deferral offsets 0-6 with a queued next-epoch frame; stalled in-flight status across capture application; probes q2, q3, q4, q6 | R961-3 | 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7 |
| Tests | CLEAN | `media_tb.sv`, `epochs_tb.sv`, `transport_mutations.py`, `check.py`; 3 new and 14 existing plants on the changed benches; default regression | R961-3 | 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7 |
| Docs | CLEAN | `REGISTER_MAP.md` plus its generator and prose source, `USB_AUDIO_PATH.md`, docs, inventory and evidence gates; author-r6 packet (R1) | R961-3 | 00979246dc22698c0f3a1e4a9796c1a2bcdd03c7 |

RESIDUE R1 and R2 do not affect coverage; the manager carries them to the residue checklist. S5 and S6 are optional.

## Real limits

- **Narrow round.** The lenses re-applied the delta and the named findings. Content the delta does not touch keeps its R961-2 verdict at `0f7402ee`; that covers the route, the cost, the ALINX identity, the million-frame run and the network identity. None of these was re-run here.
- **What was not run here:** synthesis, implementation, the builder bank, the Yosys bank, the full parent, PP and gPTP banks, and the 44-step docs workflow. For these I rely on the author's round-6 receipts, which are hash-bound by `MANIFEST.json`.
- **The new reprefill check is not independently proven.** `MEDIA_DEFERRED_REPREFILL` was not shown to catch q6 alone, because an earlier existing check caught it first. q6 is detected either way.
- **Hosted evidence at this head has no executed code verdict.**
  - The first failure is `Verilator preflight`, at step "Run the sweep's preflight self-tests once for this head". The runner's process-cleanup control reported "owner-survivor: CLEANUP FAILED: owned descendants remain" (`receipts/hosted-failure-annotations.txt`).
  - The `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability` failures then end at "Require every gate exactly once" because a dependent job failed or was cancelled.
  - Snapshot: 67 cancelled, 15 failure, 11 success, 1 skipped (`receipts/hosted-check-runs.tsv`).
  - The delta touches none of the sweep or preflight scripts.
- **No hardware proof.** Physical calibration and bench loopback (criterion 3) were NOT RUN, and field skips are not hardware proof.
- **Unsigned evidence commit.** The commit `c3658705` carries no GPG signature. Its binding is the packet `MANIFEST.json`, which I verified.

## Pending manager duties

- **No manager source bank.** None exists at this head, and none is claimed or inferred.
- **The merge-turn candidate belongs to the manager.** Its source base is `4df125b8c11f0e1706b3c1e489f3e66a5d856b18` and live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`. Confirm the candidate base before validation, as noted in R961-2.
- **Hosted and local-replica acceptance belong to the manager.** Rerun after the preflight cleanup-control failure.
- **Publish the R1 link corrections:** the round-5 patch plus the round-6 handoff fixes. Carry R1 and R2 to the residue checklist.
- **Bench and calibration remain outstanding:** criterion 3 bench acceptance and physical calibration.

R961-3 FINISHED
