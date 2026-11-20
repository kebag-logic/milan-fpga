[R865] POSITIVE - exact head 15168e14a1fe709b9ab5336acd6daf54e4d6e0a4

Round R865-6, cleared-context internal review of PR #945 (the flip train; issues #665, #871, #894, #917, #919, #920,
#923, #924, #925, #927, #929, #930, #936, #943, #946, #951). Exact head `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4`,
tree `8f6df0edb6b1592d3e1eb6cace389a0cf1f58cae`; source base `cb96336d`. This is a delta review of
`8dc85884..15168e14`. The delta is one commit that changes comments and message strings only, in 14 files.

## Summary

- **No BLOCKER, MAJOR or MINOR is open at this head.** One RESIDUE (R865-6-R1, a citation wording) and two
  SUGGESTIONs are recorded below.
- **R865-4-F1 is resolved.** Every "final head" figure in the PR #945 body equals my own `flip_grade.py --check
  --point`, `load_grade.py --check` and the `CPU-TABLE-8c5e2b4f.md` / `CPU-TABLE-92de01f7.md` figures at `15168e14`. No
  Known-limitations bullet names a superseded head as final.
- **R865-4-F2 is resolved.** I reproduced the release export myself at `8c5e2b4f` and `15168e14`, in disposable clones:
  - every loaded file is byte-equal to the author's published hashes;
  - the top Verilog is equal outside its comments;
  - a flipped `bios.bin` byte is refused.
  - The published loaded-identity verifier passes on the receipts alone, and my own planted product hash is refused.
  - The clone-state receipt is consistent and has refused plants. Its "now" half needs the author's scratch clones,
    so I could not re-run it (see Real limits).
- **R865-4-R1 and R2 are resolved.** My own scan of every line the train adds (`cb96336d..15168e14`, code, test, script
  and data files) finds no issue-comment, review or reviewer-finding ID in any source comment or check text. Three JSON
  data records keep one (S1).
- **Nothing executable changed.** My token classifier finds every one of the 14 files identical once comments are
  dropped and string literals masked. A planted executable change is refused in each of the 13 code files, and a known
  code-changing pair is reported as different. Compiling the two changed firmware headers' translation units at both
  heads gives byte-identical objects, and a planted header line is refused.
- **Every self-test refuses every plant at this head:**
  - flip 616/616, rows 1033/1033, shapes 25/25, load 28/28, record classes 26/26;
  - `run.py --self-test` 0 failures. The two changed check texts PASS there, and the queued-constants mutant is caught.
  - Also: the hot list's check and self-test, `queued_bound.py --selftest` and `test_ctrl_memory.py`.

## Findings

### R865-6-R1 — RESIDUE — Docs — `sw/firmware/ctrl/plat/ctrl_split_hot.txt:13-14` — "#665's ruling of 2026-11-17, as amended, item 1" does not say which ruling it means

- **Evidence:** #665 carries two rulings dated 2026-11-17, and each has an item 1:
  - the ruling on the composition STOP, whose item 1 is the ledger;
  - the ruling on the round-3 cut plan, whose item 1 is the third trace window. This is the one the replaced ID named.
- "As amended" names no amending ruling. The amending ruling is #665's ruling of 2026-11-18, item 1 (the link-conflict
  filter), which line 19 cites.
- The surrounding text ("its functions appended after the other two windows'") lets a careful reader find it, so the
  citation is ambiguous but not wrong. It is wording only: it changes no figure, check, code or generated artifact.
- **Exact fix:** "(#665's ruling of 2026-11-17 on the round-3 cut plan, item 1, as amended by its ruling of 2026-11-18,
  item 1)".
- **Verification:** reading the line identifies one ruling. `ctrl_hot.py --check` still passes, because the parser
  skips `#` lines.

### R865-6-S1 — SUGGESTION — Docs — three JSON data records still carry issue-comment IDs

- `scripts/register_descriptions.json` (`CRFT_COUNT`'s description, a link to #726's comment);
- `syn/ooc/pp_resource_baseline.json` (`measured`: three #665 ruling IDs);
- `tb/verilator/nvm_capture_cpu/measurements.json` (`remeasurement_assignment`, an #840 comment URL).

They are data records written by generators or read as provenance. They are not source comments or check messages,
so the owner's source-comment rule does not reach them, and the author's sweep README lists them as kept, with the
reason. Optional: if the owner reads the rule as covering record text, regenerate `pp_resource_baseline.json`'s
`measured` text with dated citations at its next `record --write`. Evidence: `receipts/scan-ids-head.log`.

### R865-6-S2 — SUGGESTION — Docs — the loaded-identity README still calls `8dc85884` the final head

`author-r8/receipts/step16/gating/loaded-identity/README.md` line 4 says "the final head `8dc85884`". This is author-r7's
text, kept as it was. The head's product images are unchanged at `15168e14` (`sweep/product-images-vs-8dc85884.txt`),
so the claim still holds. The packet is an evidence archive, not the PR body, so F1's verification does not cover it.
Optional: add "(at r7; `15168e14`'s are the same images)".

## Prior public findings at this head

These were read after my own pass over the delta, the scan and the classifier.

| Prior finding | Status at `15168e14` | Evidence |
|---|---|---|
| R865-4-F1 (MINOR, Docs: the PR body's "final head" figures) | **RESOLVED** | The body's Status (lines 16-37), "Composed figures at the final head" (198-206) and "Restated at the final head" (208-220) equal my `flip_check_1x1.log` (last 127.31/130, ACMP 29.06/30, txL 47.88/49), `flip_check_8x8.log` (the TRANSMIT 76.81/77, load 0.744), `load_check.log` (0.511 / 0.508; 8x8/2if 0.799) and the CPU tables (1x1/1if 0 of 68 and paced 29,993 cycles 315/315; 8x8/1if 0 of 68, `record.srp` 34,803 within 375, `item.reclaim` 995 within 40). Known limitations (462-470) say the re-measure is done, the bench re-check is pending on `8c5e2b4f`'s bitstreams, and the reported 30,839-cycle paced record. No "final head" names a superseded head (`receipts/pr945-body.md`) |
| R865-4-F2 (MINOR, Docs: the gating firmware and release identities) | **RESOLVED** | `receipts/release/export-{8c5e2b4f,15168e14}.log` (my exports: `bios.bin` 603b9ca3…, AEM bdfde7cf…, mem d1657b93…, rom 621133bb…, sram e3b0c442…, equal to the author's), `compare-8c5e2b4f-15168e14.log` rc 0 and `compare-plant.log` rc 1; `verify-published.log` rc 0 and `verify-published-plant.log` rc 1. The author's `release-identity.log` (8 pairs, rc 0, plant refused) and `gating/clone-state/` (both clones at `8c5e2b4f`, porcelain empty now and as logged, 2 plants refused) were read and are consistent |
| R865-4-R1 (RESIDUE: issue-comment IDs in source comments) | **RESOLVED** | `git grep issuecomment-7044585511` in code prints nothing; `receipts/scan-ids-head.log` |
| R865-4-R2 (RESIDUE: R872-1-F2 in `declaring_outputs.py`) | **RESOLVED** | Lines 296 and 323 no longer carry it; `git grep R872-` in `tb/` prints nothing |
| R865-4-S1 (SUGGESTION: the reported-not-held paced record) | Addressed | It is stated in the body's Known limitations |
| R866-1-R2 / R865-1-RES-2 (`ctrl_split_hot.txt` IDs) | **RESOLVED** | Neither ID remains; the replacement's wording is R865-6-R1 |
| R866-3-R1 (the body's "last made at step 9") | **RESOLVED** | The phrase is gone from the body |
| R866-1-R1 (bench labels B24, L5, L6 in `test_plat_boot.cpp:91,95,116,119` and its assertion messages) | **RETAINED**, RESIDUE | The file is untouched by the delta; existing labels are tracked by #746 |
| R865-1-RES-1 (`docs/design/AREA_BUDGET.md:139,141`, the superseded record and ExtraPostPlacementOpt) | **RETAINED**, RESIDUE | Unchanged. The body's Known limitations name it, as record-only by ruling |

No new bench or lane label, review round, reviewer ID or issue-comment ID enters a source comment in
`8dc85884..15168e14` (I read the full diff, `receipts/classify-delta.log`).

## Lens results at this head

```text
[R865] PASS Conformance — 14 files of 8dc85884..15168e14 (receipts/classify-delta.log); flip_check_1x1.log, flip_check_8x8.log, load_check.log — no clause claim, owner bound or statement moved: every changed token is a comment or a string literal, and the 1x1/1if rows (127.31/130, 29.06/30, 47.88/49), the 8x8/1if TRANSMIT 76.81/77 and the loads 0.511/0.744 under the owner's 0.70/0.75 reproduce. Each rewritten citation resolves to the issue, date and item of the ID it replaced (#665 2026-11-15 item 1; #923 2026-11-16; #665 2026-11-17 cut-plan item 1; #665 2026-11-18 item 1; #665 2026-11-20 item 4), checked against the public comments' dates
[R865] PASS RTL — sw/firmware/ctrl/aecp/aecp_mbx.h, sw/firmware/ctrl/loop/ctrl_loop.h (receipts/obj-spot.log); no HDL in the delta — aecp_mbx.o and ctrl_loop.o compiled at 8c5e2b4f (=8dc85884's sources) and 15168e14 are byte-identical at -O2 -g, line counts kept (124, 643), and a planted header line is refused. The release export's top Verilog is equal outside its comments, and its loaded files are equal (receipts/release/)
[R865] PASS Robustness — receipts/classify-delta.log, receipts/selftests/*.log — no behaviour path is reachable from the delta: comments and literals only, the hot list's non-# lines identical, and the self-tests that exercise the refused, malformed and boundary arms (flip 616, rows 1033, shapes 25, load 28, record classes 26, run.py 0 failures) refuse every plant at the head
[R865] PASS Tests — receipts/selftests/ (run_selftest.tail60.txt, run_selftest.log.gz sha256 43f1823d…), receipts/classify-{delta,control}.log, receipts/verify-published{,-plant}.log, receipts/release/compare-plant.log, receipts/obj-spot.log — the two changed check texts PASS ("the declaring arm refuses a fixture that clears brief"; the queued-constants check) and the queued-constants mutant is caught. Every reviewer probe carries a refused plant. The author's F2 receipts carry scripts, logs, rc and refused plants
[R865] PASS Docs — receipts/pr945-body.md (PR #945 body at head 15168e14), author-r8 RESOLUTIONS.md:794-845, sweep/README.md, release/README.md, gating/clone-state/README.md, ctrl_split_hot.txt:13-19 — F1 and F2 are resolved with evidence. R865-6-R1 is RESIDUE (wording only) and S1/S2 are SUGGESTIONs; none leaves the lens unclean
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the delta's 14 files against the owner bounds and rulings (#665 2026-11-15/17/18/20, #923 2026-11-16); flip and load checks at head; CPU-TABLE-8c5e2b4f/92de01f7 | R865-6 | `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` |
| RTL | CLEAN | `aecp_mbx.h`, `ctrl_loop.h` objects at both heads; release export (top Verilog, loaded files) at `8c5e2b4f` and `15168e14`; no HDL in the delta | R865-6 | `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` |
| Robustness | CLEAN | token classifier over all 14 files; the self-tests' refused, boundary and malformed arms at head | R865-6 | `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` |
| Tests | CLEAN | flip, rows, shapes, load, record classes, hot list, queued bound, `test_ctrl_memory.py`, `run.py --self-test` at head; F2 receipts and their plants; my probes' plants | R865-6 | `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` |
| Docs | CLEAN (R865-6-R1 RESIDUE; S1, S2 SUGGESTION; R866-1-R1, R865-1-RES-1 retained RESIDUE) | PR #945 body at head; author-r8 RESOLUTIONS, sweep, release and gating READMEs; the delta's comments | R865-6 | `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` |

**Code the delta does not touch keeps its prior verdicts.** The delta changes nothing that code depends on, and the
images, objects and self-tests above prove it:

| Prior covering round | Head | Scope |
|---|---|---|
| R865-4 (Conformance, RTL, Robustness, Tests CLEAN) and R866-5 POSITIVE | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` | the SRP cut, item 4, its re-measure |
| R872-2 / R871-2 POSITIVE | #953 at `a16899b1` | step 13 |
| R869-1 POSITIVE | #952 at `f09d82e0` | step 14 |
| R866-3 POSITIVE | `0839453f` | steps 1-12 |

The only artifacts within any lens's scope that changed after those heads are the 14 files' comments and literals.
Those are re-covered here at `15168e14`.

## Real limits

- **Clone-state receipt:** I could not re-run `gating_clone_state.sh`, because it reads the author's gating clones,
  which are not public. I read its script, log, rc and plants.
- **Loaded-identity receipt:** I could not re-run `loaded_identity.sh`, because it needs the author's scratch trees. I
  ran its `verify_published.py` on the published receipts, and my own plant was refused.
- **Images not rebuilt:** I did not rebuild the 12 CPU-budget images, the 4 product images or any bitstream. Their byte
  identity rests on the author's `sweep/img-vs-8dc85884.txt` and `product-images-vs-8dc85884.txt`. My object
  spot-check and token classifier corroborate it: nothing a compiler reads, line numbers included, changed.
- **Not re-run:** the firmware shards, the twin, the boot simulations, the ledger self-test and the docs gates. The
  author's `sweep/q.log` reports them at `15168e14`. Its only failures are the previous heads' exceptions: the full
  `flip_check`'s eleven 8x8/2if base findings, which I reproduce (rc 1, reported not held), and the CI-bound
  `ci_tool_inventory_check`.
- **Shared test clone:** `run.py --self-test` and the quick self-tests ran concurrently in one disposable clone at head.
  Its porcelain stayed 0, and every result is rc 0 except that expected `flip_check`.
- **Calibration and bench:** physical calibration was NOT RUN. Bench and field skips are not hardware proof, and the
  bench re-check on `8c5e2b4f`'s bitstreams is pending.
- **No manager source bank** exists at this head, and this round does not claim one. The current-dev merge candidate
  (source base `cb96336d`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`) is not validated by this round.
- **Hosted contexts:** I took one read-only snapshot (`receipts/hosted-checkruns.txt`, first 40 contexts listed).
  - `rtl-fast` completed success.
  - Several Verilator shards and the fail-fast contexts were still in progress.
  - Physical gPTP was skipped, which is not execution.
  - Acceptance belongs to the manager.
- **Review clone:** it is at the exact head, porcelain 0 with untracked files included, and its index modes and blobs
  equal the HEAD tree (`write-tree` `8f6df0ed…`). Every required submodule gitlink is unchanged
  (`receipts/clone-integrity.txt`). Only a read-only fetch of the evidence archive commit `e1fb397c` touched it.

## Pending manager duties

- Carry R865-6-R1 and the retained residues (R866-1-R1, R865-1-RES-1) to the residue checklist. S1 and S2 are optional.
- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) and link its
  receipts on the PR.
- Own hosted and act acceptance at the exact head, including the Verilator shards still running at my snapshot.
- The bench re-check of F-G5 (h) #25 on the `8c5e2b4f` gating bitstreams remains pending.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`. The scripts are under `scripts/`:
- `scan_ids.sh`: the ID scan;
- `classify_delta.py`: the token classifier, with plants;
- `rel_export_at.sh` and `rel_compare.sh`: the release export and comparison, with a plant;
- `obj_spot.sh`: the object identity check, with a plant;
- `selftests.sh`: the self-test runner.

R865-6 FINISHED
