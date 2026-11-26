[R935] NEGATIVE - exact head 0ad0e5180558a376f6064d0b33884ed40af6e196

# R935-1: internal cleared-context review of kebag-logic/milan-fpga PR #1015 (Relates to #970)

- Head `0ad0e5180558a376f6064d0b33884ed40af6e196`, tree `d89ab4e42af51456f1bd2855a4025668bfa0ca57`.
- Source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.
- Three commits:
  - `ef764d73b`, the change, on `5de21ff36`;
  - `f13845710`, a merge of `c34e7d8b`;
  - `0ad0e5180`, one README row.
- The merge is clean: `git diff 5de21ff36 ef764d73b` and `git diff c34e7d8b f13845710` have the same patch-id, `8a37de05481a`.
- Every submodule gitlink is the same at base and head, including tsn-c-stack `715589c1`.
- Context, read in order:
  - AGENTS.md and CONTRIBUTING.md;
  - the #970 body and its rulings of 2026-11-22 (`issuecomment-7080789556`) and 2026-11-25 (`issuecomment-7174054394`);
  - the PR body;
  - FR_NFR 2.1.1;
  - the diff;
  - the stack core at the pin (`third_party/tsn-c-stack/src/adp.c`);
  - the author's public packet at `40ce56ee:review-evidence/adp970-r1`.
- No prior public review findings exist on this PR. At reading it had two review-start comments, 0 reviews and 0 inline comments, so none needed to be resolved or retained.

**Verdict: NEGATIVE.** The firmware change itself is sound:
- the seed is 6.2.4.2.2's sum, mixed with the entity ID and the interface;
- the draw ranges and the declared 6.0 s are unchanged;
- no LINK_UP hold exists anywhere;
- the adapter writes no stack state;
- the draw is uniform under an independent model that matches the code bit for bit.

The verdict is NEGATIVE because of these findings:

- **F1, MAJOR.** The delta turns two required documentation-workflow gates red. The hosted docs-gates-0 fails on one of them, and the hosted exhaustive suites at this head were cancelled.
- **F2, MINOR.** The documented `rom` cost (+344 to +384 B) is measured against older figures. Against the change's own base it is +288 to +328 B.
- **F3, MINOR.** The platform test B25 cannot fail for a coarse clock or a late-wired clock. Three planted defects escape it.
- **F4, MINOR.** The author's REVIEW-READY and the PR title claim a seed at each LINK_UP. The code does not take one.

## Findings

### F1 - MAJOR - Tests, Docs - two required docs-workflow gates fail at the head

- **Where:**
  - `tb/verilator/ctrl_service_budget/scenario.py`: 1,001 lines, and `:264` is 121 columns;
  - `sw/firmware/ctrl/test/adp_first_mutants.py:4` (150 columns) and `:5` (163 columns);
  - `CHANGELOG.md:93`: the new section is not in the page's contents list.
- **Authority:**
  - `docs/development/CODE_QUALITY.md` Rule 12, enforced by `scripts/check_py_idiom.py`: `LONG_MODULE_LINES` 1000 and `MAX_COLUMNS` 120, ratchets 10 and 0;
  - the per-page contents gate, `scripts/gen_toc.py --check` (docs workflow `gate_45`);
  - AGENTS.md section 7: required gates pass, and existing regressions remain green.
- **Evidence:**
  - `check_py_idiom.py` exits 0 at base `c34e7d8b` and 1 at head, with `long module 11 > ratchet 10` and `over-long line 3 > ratchet 0` (`receipts/py-idiom-*.log`, `receipts/py-long-lines.txt`). `scenario.py` had 1,000 lines at base.
  - `gen_toc.py --check` exits 0 at base and 1 at head: `TOC DRIFT CHANGELOG.md` (`receipts/gen-toc-*.log`).
  - Hosted docs-gates-0 at this head fails its "Python idiom gate" step with the same two lines (job 139589710505).
  - "Fail fast across this head" then cancelled the exhaustive Verilator shards and the Yosys jobs. So this head has no executed `verilator-suites` or `yosys-portability` evidence. The hosted contexts are 64 fail, 20 pass and 1 skipped.
  - The PR body's "documentation checks | pass" is not true at this head.
- **Impact:** the head cannot merge with required contexts red. The ready-state hosted gates never executed on it.
- **Required outcome:**
  - both gates exit 0 at the next head: the three lines within 120 columns, `scenario.py` back within the module rule, and CHANGELOG's contents list regenerated with a description for the new section;
  - the PR's "documentation checks" row restated from a run at that head.
- **Verification:**
  - `python3 scripts/check_py_idiom.py` exits 0;
  - `scripts/gen_toc.py --check`, run with the pinned Markdown venv, exits 0;
  - hosted docs-gates-0 passes, and the exhaustive suites execute rather than cancel.

### F2 - MINOR - Docs, RTL - the change's `rom` cost is stated against older figures

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:755` ("344 B more", "384 B", "352 B", "376 B") and the PR body's "rom 344 to 384 B more".
- **Evidence:** `plat_ledger.py`, run by this review at base `c34e7d8b`, at `5de21ff3` (the change's parent) and at head (`receipts/ledger-*.log`):

| Point | Base and `5de21ff3` (identical) | Head | This change | Doc's figure |
|---|---:|---:|---:|---:|
| 1x1, one interface | 127,568 B | 127,856 B | +288 B | +344 B |
| 1x1, two interfaces | 129,352 B | 129,680 B | +328 B | +384 B |
| 8x8, one interface | 141,680 B | 141,968 B | +288 B | +352 B |
| 8x8, two interfaces | 143,432 B | 143,744 B | +312 B | +376 B |

- The head figures equal the author's. `sram`, the tiles and `ctrl_plat` are unchanged, as documented.
- The doc's deltas are taken against the earlier train's table on the same page (`d6c398c8`: 127,512, 129,296, 141,616 and 143,368 B). They therefore also count 56 to 64 B from other `dev-soft-core` changes merged before this change's base, such as the lwSRP pin move.
- **Impact:** the ledger attributes to #970 a resource cost 19 to 22 % above its own. These are measurement figures, so this is not residue.
- **Required outcome:** state the change's own cost against its base (+288 to +328 B). Alternatively, name the reference the deltas are taken from and that it includes the other merged changes.
- **Verification:** `plat_ledger.py` at base and head reproduces the stated deltas.

### F3 - MINOR - Tests - the platform's microsecond clock and its wiring order are not proven by any test

- **Where:**
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:1338` (B25);
  - `sw/firmware/ctrl/plat/ctrl_plat.c:136-140` (`adp_clock`);
  - `ctrl_plat.c:401`, where `adp_mbx_set_clock` comes before the release at `:432`.
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect". B25 claims "the platform seeds ADP's draw from its microsecond clock".
- **Evidence:** the reviewer's plants, run with the repository's own `plant()` and arms (`scripts/adp_probe.py`, `receipts/adp_probe.log`). These three pass every check of `platboot1`, `platboot2` and `plat`:
  - `r-plat-clock-in-ms`: `adp_clock` returns `now_us / 1000`;
  - `r-plat-clock-1024us-granule`: `now_us & ~0x3FF`;
  - `r-plat-clock-wired-after-release`: `adp_mbx_set_clock` is moved after `ctrl_app_release_adp`. On hardware every boot would then seed from NOW_MS.
- B25's clock origins differ by 1,234,567 us, which still differs at millisecond resolution. The test only requires the two seeds to differ, so it also passes when one boot seeds from NOW_MS and the other from the clock.
- The adapter-side equivalents are caught: `r-seed-sample-low-bits-dropped` and `r-seed-interface-not-set`.
- **Impact:** a platform-layer regression to a millisecond or NOW_MS seed would leave every gate green.
- **Required outcome:** a platform test fails for each of the three plants. For example:
  - two boots whose clock origins differ by 1 us seed differently;
  - the generator state at ready equals the one formed from the flash clock's reading at the enable;
  - or the adapter's clock is cleared before each boot and must be wired before ADP's release.
- **Verification:** the three plants are caught by their test's own words.

### F4 - MINOR - Docs, Conformance - the public handoff and the PR title claim a seed at each LINK_UP

- **Where:**
  - `review-evidence/adp970-r1/author/REVIEW-READY.md` at `40ce56ee`: "seeded per IEEE 1722.1-2021 6.2.4.2.2 ... at startup and at each qualified LINK_UP (Milan v1.2 5.6.3.5.2 and 5.6.3.5.3)";
  - the PR title: "per host, interface and link-up".
- **Evidence:**
  - At this head the seed port is called only from `adp_set_enable` (`third_party/tsn-c-stack/src/adp.c:232`, reached from `adp_mbx.c:167-172`).
  - A LINK_UP (`adp.c:257-260`) draws from the state seeded at the enable.
  - The PR body's Known limitations, `FR_NFR.md:223` and the CHANGELOG say the same.
- **Impact:** a clause-level claim about 5.6.3.5.3 behaviour that the head does not have. The ruling's "each draw mixes a fresh sample" is deferred at this head to a stack change and a pin move.
- **Required outcome:** retitle the PR and publicly correct the handoff to "seeded at the enable, at this pin", or land the pin move that makes the claim true.
- **Verification:** the title and the handoff agree with `adp.c` at the head under review.

### R1 - RESIDUE - Docs - `docs/reference/FR_NFR.md:222`

"H4 to H7 hold the first draws ... uniform over both ranges" names H7, which tests the seed's terms, not uniformity.

Exact fix: "H4 to H6 hold the first draws of neighbouring entities started together, and of one entity's boots, uniform over both ranges; H7 holds the seed's terms."

### Suggestions

- **S1:** `tb/verilator/mbx/README.md:225` predates the change and says "The firmware's random delays are seeded from NOW_MS". That is still true where no clock is wired, but the seed is now NOW_MS mixed with the MAC address, the entity ID and the interface.
- **S2:** B25 leaves `clock_origin_us` non-zero if an `ASSERT` returns early. Reset it in the fixture.
- **S3:** the author's `cpi-8x8-head.txt` shows +2.9 to +3.1 % CPI in every 8x8 group, including `aecp` and `datapath-events`. The hot region is unchanged and no verdict moved, but the PR does not mention or explain it.
- **S4:** not this PR's defect; a separate issue is suggested. The split boot simulation refused once in this review because the generated CSR map's ISA string came out in a different order in two generator runs (`zicsr_zifencei` against `zifencei_zicsr`). The cause is hash-randomised set order (`receipts/boot-head-1x1-attempt1-hashseed-flake.log`). With `PYTHONHASHSEED=0` it passes.

## Lens results at this head

```text
[R935] PASS Robustness - sw/firmware/ctrl/adp/adp_mbx.c:50-79,167-172; third_party/tsn-c-stack/src/adp.c:217-245; receipts/draw_model.txt, draw_diff.txt, gate-head.log (H6) - no clock (NOW_MS fallback, H6 uniform); a zero state guarded by the core; end-around carry at the wrap (H7, model); a 64-bit clock truncated to its low word; disable takes no seed and re-enable re-seeds by XOR; seed_interface always < MBX_N_IF; boot-time only, no pass work added (adp.link_up still 11 accesses)
```

**Conformance** was applied. It is UNCLEAN only through F4's claim. The code meets:

- 6.2.4.2.2's seed: the low 32 bits of MAC address plus clock, with an end-around carry;
- 6.2.4.2.2's generator: xorshift32 (13, 17, 5), a 2^32 - 1 sequence;
- Milan's ranges: `draw_ms` is unchanged, 0 to 2,000 and 0 to 4,000 ms;
- FR_NFR 2.1.1: the 6.0 s and the 4,311 ms are unchanged (the diff adds four lines after them).

Item 1 of the 2026-11-25 ruling holds: no link hold. The diff touches no PHY, publication or adapter link path, and `adp_link_change` is reached directly from the LINK event (`adp_mbx.c:143-144`). The adapter writes no stack state: `port_seed` only reads `adp.entity`, and its own state is three file-level variables.

The draw is uniform under an independent model (`scripts/draw_model.py`). It matches the real `adp.c` plus the head's `port_seed` and `mix` bit for bit over 4,096 tuples (`receipts/draw_diff.txt`). 14 of 14 scenarios pass both the 99 % chi-square bound and the Kolmogorov-Smirnov bound:

- EUI-64 neighbours at one sample;
- EUI-64 neighbours with jitter;
- strides of 2 and 256;
- one entity's boots 1 us apart;
- interface 1 against interface 0;
- consecutive neighbours within 5 ms of each other, at the rate independent draws give.

Under the base seed, 16 EUI-64 neighbours draw between 339 and 343 ms.

**RTL** was applied. It is UNCLEAN only through F2. The delta has no HDL. Firmware architecture (`receipts/image_diff.txt`):

- The hot region bounds are identical at all four points (`_ctrl_hot_end` 0xdde4, 0xe30c, 0xdda0 and 0xe2b8).
- No function below the first changed one moves.
- The image adds `mix` (60 B), `adp_mbx_set_clock` (20 B) and `adp_clock` (40 B); `adp_mbx_set_enable` grows +8 or +24 B and `ctrl_plat_boot` +20 to +32 B.
- The ledger passes at all four points.

**Tests** were applied. They are UNCLEAN through F1 and F3.

- Firmware gate at head (`--require-rv32`): PASS, rc 0, 85 suite verdicts (`receipts/gate-head.log`).
- 19 of 19 plants are caught by their own test's words: `adp_first_mutants.py` plus `latency-extra-read` (`receipts/adp_probe.log`, `adp_probe_walk.log`). The two walk plants need the gate's prepared reuse directory.
- Split boot simulation 1x1: PASS, 0 findings (`receipts/boot-head-1x1.log`).
- Reboot simulation: PASS, 0 findings (`receipts/reboot-head.log`). It reproduces the changed `tb/verilator/ctrl_reboot/README.md:120` row exactly: 842.550 ms, 3,500 ms, 3 ms, 85.645 ms to ready, 871.322 ms to the first ENTITY_AVAILABLE, and 5,216.872 of 20,000 ms.
- The scenario change awaits the full 0 to 4 s draw with 2,000 ms more simulation time per group. It was read and agrees with Milan 5.6.3.5.3.

**Docs** were applied. They are UNCLEAN through F1, F2 and F4; R1 is residue.

- These docs-workflow checks pass at head (`receipts/docs-gates-head.txt`): doc paths, archive, inventory, C/C++ and shell idiom, hygiene, doc style, docs_check, em dash against base, anchors, port contracts, TODO, naming, fail-fast, test evidence, SoC and RTL source lists, and baremetal-only.
- The new source comments state behaviour, reason, and issue and clause IDs. They carry no lane, round, reviewer or comment ID. `seed-one-round` names the mix's rounds.
- MAILBOX_SPLIT, the adapter header's THE DRAW and the CHANGELOG text agree with the code.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | `adp_mbx.c`/`.h` THE DRAW; `ctrl_plat.c:136-140,401`; stack `adp.c:43-62,217-268`; FR_NFR 2.1.1; #970 rulings; draw model and differential | R935-1 | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| RTL | UNCLEAN (F2) | `plat_ledger.py` at base, `5de21ff3` and head; ELF symbol diff; hot region bounds; no HDL in the delta | R935-1 | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Robustness | CLEAN | `adp_mbx.c:50-79,167-172`; `adp.c:217-245`; draw model; H6 (see the PASS line) | R935-1 | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Tests | UNCLEAN (F1, F3) | `test_adp.cpp` H4 to H7; `test_plat_boot.cpp` B25 and B26; `adp_first_mutants.py`; budget `scenario.py` and `build.py`; `hooks.py`; firmware gate; 19 plants plus 5 probes; split boot 1x1; reboot simulation | R935-1 | 0ad0e5180558a376f6064d0b33884ed40af6e196 |
| Docs | UNCLEAN (F1, F2, F4; R1 residue) | FR_NFR, MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY, CHANGELOG, `ctrl_reboot/README.md`, PR body and title, author packet; docs-workflow gates | R935-1 | 0ad0e5180558a376f6064d0b33884ed40af6e196 |

## Real limits

- **No hardware.** Physical calibration was NOT RUN and no hardware was used. How uniform the draw is over real boots depends on how far the clock reading at the enable varies across boots on the device, and that is not measured. The tests vary it in steps of 1 us and 1 ms.
- **Not re-run by this review:**
  - the CPU budget legs at 1x1/1if and 8x8/1if;
  - the hooks self-test;
  - the twin;
  - the split boot at 8x8.
- **Author receipts used in their place** (`validation-r2/summary.txt`, `cmp-*.txt`, `cpi-*.txt`), inspected only:
  - 75 and 90 probes paired;
  - 0 misses at 1x1;
  - the same 7 known 8x8 `backlog-owed` misses on both sides;
  - 0 passes over the share.
- **Hosted results.** They were inspected, not accepted (F1).
- **Manager source bank.** None runs at this head, and none is claimed or inferred.
- **Probe hygiene.**
  - The probes, the base builds and the evidence copies ran under the packet's `scratch/`: disposable clones and copies of base `c34e7d8b` and `5de21ff3`, made with local submodules.
  - Verilator was the pinned 5.050 (`receipts/verilator-identity.txt`).
  - After the probes, the clone's worktree and index equal HEAD (index tree `d89ab4e4`) and every required gitlink checkout equals its gitlink and is clean.
  - The seven ignored build outputs this session created were removed (`receipts/clone-integrity.txt`).

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- Accept hosted and act results at a head that fixes F1.
- Land the tsn-c-stack change and the pin move that the PR's own Definition of Done still requires. They change `adp_mbx.c` and the LINK_UP path bound (12 accesses), so they un-cover Conformance, RTL, Robustness and Tests.
- Run the bench re-run after #972.
- Carry R1 to the residue checklist.

R935-1 FINISHED
