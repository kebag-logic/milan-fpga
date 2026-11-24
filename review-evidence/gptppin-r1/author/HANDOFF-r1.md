# HANDOFF r1 — [A835] #994 gPTP pin 1213ac5b

**Status (11:05 CET 2026-11-24): REVIEW READY at `bbfdb674`.** ETA: done. Nothing running; no unit left; scratch 16 GB.
Branch `994-gptp-pin-1213ac5b`, 4 local commits on `300da99b` (PR base `dev-soft-core`), not pushed (the manager pushes).
PR body: `PR-BODY.md`. Evidence summary: `REVIEW-READY.md`. Receipts: `receipts/INDEX.md` (85 files, 1.1 MB, none over 200 KB).

## Commits (on 300da99b)
- `973f2f20` gitlink 1616fc8f -> 1213ac5b (the routed commit).
- `39e9c9d2` pin sites: pin row, engine-guide permalinks, both diagrams by generator, gptp_ucode.hex ledger row.
- `8c5a51e1` behaviour docs (GPTP_PLANE, GM_LOSS_RECOVERY, STRICTER_READINGS), SUBMODULES #994 record, CHANGELOG.
- `bbfdb674` the docs style gate's ten-word sentences (18 findings at `8c5a51e1`, 0 at `bbfdb674`). Markdown only.
- Only Markdown changes after `973f2f20`, so the route, sweep and leg evidence at the earlier heads covers the final tree.

## Routes (release recipe, split image, one interface; at 973f2f20; 2 at once via vivado-slot.sh; 8 threads each)
| Image | Directive | WNS / WHS worst | LUT | FF | Slice | BRAM | DSP |
|---|---|---|---:|---:|---:|---:|---:|
| 8x8/1if base 300da99b | EPPO | +0.105 / +0.036 | 46,621 | 53,338 | 15,570 | 98.5 | 13 |
| 8x8/1if | EPPO (first, meets) | +0.066 / +0.036 | 46,246 (−375) | 53,381 (+43) | 15,622 (+52) | 98.5 | 13 |
| 1x1/1if base 300da99b | ETO | +0.384 / +0.036 | 32,680 | 42,805 | 14,297 | 80.5 | 13 |
| 1x1/1if | EPPO (misses, +0.007; base +0.019 missed too) | | 32,555 | 42,803 | 13,598 | 80.5 | 13 |
| 1x1/1if | ETO (selected, best of 3) | +0.170 / +0.024 | 32,639 (−41) | 42,805 (0) | 14,147 (−150) | 80.5 | 13 |
| 1x1/1if | ASL | +0.072 / +0.024 | 32,633 | 42,803 | 14,142 | 80.5 | 13 |
- #818 floor met by both selected images at every corner; 0 failing endpoints; image identity PASS x4.
- The owner-accepted +455 LUT at 8x8/1if does not appear on this base (−375). Nothing beyond +500; no floor miss -> no STOP.
- 1x1's Fast WHS +0.024 meets #818 (WHS >= 0). It misses only #870's lane-specific WHS >= +0.030 ruling, which is not this
  issue's gate. Worst setup paths: KL_mbx read data (8x8), SoC bus bridge to UART FIFO (1x1); worst hold is chan_map_render.
  None is in the gPTP plane.

## Gates
- Full sweep at `8c5a51e1`, 4 shards: 65 suites, 2,715,829 checks, 0 in-suite failures. 64 PASS in the sweep. `mbx` failed
  only in its dma-mutants harness, because this harness lacked the CI's MAKEFLAGS `--no-print-directory`. Re-run alone with
  that flag it passes: 523,212 checks, 0 failures. Shard 2 was OOM-killed once at a 12 GB cap (capture_coherence, peak
  16.9 GB) and then passed whole at 24 GB.
- tsn_fuzz with TSN_GEN_ROOT (field campaigns): 897 checks, rc 0. gPTP 675 pass and AAF/AVTP 164 pass, both equal to the
  tracked TEST_RESULTS.md; only the timestamps move, so nothing is committed.
- milan_dp gptp 212/212 ([CA] 0x22) and gptp-lat 212/212 ([CA] 0xFE); milan_dp_gptp physical PASS, 205 checks
  (9,301 s wall under load, run with an 18,000 s cap).
- plat_ledger PASS (0 findings). The 24 firmware image digests are identical to 300da99b's -> the firmware gate is not owed.
- Builder legs 0/1 rc 0 (dev's two NOT RUN), union 113 gates exactly once; both legs pass again in the docs run at bbfdb674.
- Docs workflow at bbfdb674: 56 rc 0, 24 SKIP, 3 environment (the RV32 SDK install-verify has no provenance receipt, as on
  the bases).
- Lint, Yosys elaborate and open synth (gPTP plane tops and milan_datapath), ooc_selftest, split-cdc: all rc 0 at bbfdb674.

## For the manager
- Push `994-gptp-pin-1213ac5b` and open the PR against `dev-soft-core` with PR-BODY.md, after the train (#988) lands and you
  have merged dev-soft-core into the branch.
- Follow-up worth an Issue (not done here, out of scope): adopt a +-100 ppm takeover phase into the parent regression. This is
  FPGA-gPTP R905-1-S3, retained for the parent owner.
- The resource gate's endpoints (the all-fabric route-1x1 and the two OOC endpoints) were not re-measured. The issue names
  the release images.

REVIEW READY bbfdb6746d585e490508783dc8a88c79fbab02c0
