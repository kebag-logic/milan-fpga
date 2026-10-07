[R530] NEGATIVE - exact head 13e715136b0b7c8d9763e0b730d9709f2c9f5932

# R530-5: internal cleared-context review of PR #688 (issue #665, lane F3, round 6)

- **Head:** `13e715136b0b7c8d9763e0b730d9709f2c9f5932`, tree `4b04d6dd962ddf0daee9cf64fc23abf5fb18f927`. This matches the published `665-f3-acmp` and the PR head.
- **Source base:** FC head `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`. Live dev is `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`, merged here as `aa0fdd01`.
- **Previously covered head:** `39adc58f` (R530-4 and R531-4, both POSITIVE).
- **Assignment:** #665 comment 6037650104 (round 6). It covers:
  1. merging dev `e21c1ca0` with both sides kept;
  2. composing ADP, MAAP and ACMP: every channel's IRQ bit plus the events', disjoint timer slots, and tested attach order and refusals;
  3. the linked image with MAAP and ACMP, at both shapes, against dev;
  4. keeping every check, arm and defect, and re-running the gates.
- **Reconstruction order:**
  - AGENTS.md and CONTRIBUTING.md, then docs/README.md;
  - the #665 body, the F3 assignment (6026721148), decisions 6029368753, 6030870481 and 6033962557, and round assignments 6030067436, 6032450078, 6034423349, 6036721467 and 6037650104;
  - REQUIREMENTS.md section 1 (the `maap` and `adp` rows) and FR_NFR 3.4.1/3.4.2;
  - `git diff 021b9c1f..13e71513` and the history. I read the merge resolution with `--remerge-diff` and the seven post-merge commits line by line;
  - the public evidence, REVIEW READY 6040171459 and the PR body, then prior reviews (only after this pass).
- **Verdict: NEGATIVE.** One open MINOR leaves the `Tests` lens unclean.
  - **R530-5-F1:** at two interfaces, the composed MAAP may advertise a source MAC that the filter's own-unicast row does not admit, and every arm still passes.
- **Everything else holds at this head:**
  - the merge resolution;
  - the composition's order, IRQ mask, filter set, slots and refusals;
  - the pass-bound arithmetic and the linked-image table;
  - every gate, the full 465-defect ctrl campaign, the mbx suite and the docs gates.
- One prior RESIDUE (R530-4-R1) is retained at this head.

## Findings

### R530-5-F1 | MINOR | Tests | `sw/firmware/ctrl/app/ctrl_app.c:21-23` with `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1002-1063` | the composed MAAP's per-interface source MAC is pinned by no check

- **Authority:**
  - REQUIREMENTS.md:73 says the `maap` row passes "own unicast on the receiving AVB interface for MAAP_DEFEND only".
  - REQUIREMENTS.md:91-93 and IEEE 1722-2016 B.2.1 send a MAAP_DEFEND unicast to the source MAC of the PROBE that triggered it.
  - So the composition must give MAAP, on each interface, the MAC that `ctrl_app_open()` writes as that interface's own unicast MAC (`ctrl_app.c:58-62`). Otherwise a DEFEND answering this station's probe on that interface is filtered out before it reaches MAAP.
  - `maap_compose()` is this lane's code (commit `32c41bbb`), and round 6 requires the composition tested at one and two interfaces. The ctrl README's `acmpif2` row claims "the three-way composition".
- **Evidence:**
  - I planted `mac[k] = cfg->entity->mac + k;` at `ctrl_app.c:22`. That puts interface 1's MAAP on a MAC the filter does not hold.
  - The defect **escapes every arm that composes MAAP**: `acmp`, `acmpif2`, `maap` and `maap_if2` all exit 0 with no `[FAIL]` (`receipts/runs/probes_composition.log`, probe `maap-mac-per-interface`).
  - It escapes because:
    - U6 checks acquisition, slots, IRQ and filter, but not MAAP's frames' source;
    - F2's `ExplicitAppComposition` does not check it;
    - F2's own adapter tests deliberately use `kMac + k` per interface (`test_maap_mbx.cpp:61`), so they cannot pin the app's choice.
  - A one-test check fixes this (`scripts/probe_maap_mac.py`, `receipts/runs/probe_maap_mac.log`). It asserts that every MAAP frame the composed app sends carries `model.own_mac[interface]` as its source.
    - At the head it **passes** in both arms (`acmp` 85 of 85, `acmpif2` 23 of 23).
    - With the planted defect it **fails** in `acmpif2`: "R530 MAAP's source is the interface's own unicast MAC, interface 1".
  - So the head's behaviour is correct, and only the check is missing.
- **Lens attribution:** Tests only.
  - The behaviour at head conforms; the passing check above shows it. So Conformance and Robustness bank no defect from this.
  - The gap is a missing check of a composition property that the round-6 assignment puts under test.
  - The same gap existed in F2's `ctrl_app_start_maap` at dev `e21c1ca0`. It is now in F3's `maap_compose()`, which this lane wrote and tests.
- **Impact:** a later change that keys MACs per interface (the redundancy path #665 keeps open) could leave MAAP on interface 1 unable to hear a DEFEND. It would then keep a conflicting address, and no gate would notice.
- **Required outcome:**
  - The composition test (U6 or a sibling, run by both `acmp` and `acmpif2`) asserts that the composed MAAP's frames on every interface carry that interface's own unicast MAC as source. An equivalent check is acceptable: a DEFEND to that MAC on every interface reaches MAAP.
  - A planted defect (`mac[k]` differing per interface, or from the entity's MAC) must be caught by `acmpif2`, with its test named.
- **Verification:**
  - the new check passes at the fixed head in both arms;
  - the planted defect is caught by name in the campaign;
  - the campaign stays at N of N.

### R530-5-S1 | SUGGESTION | Tests | `sw/firmware/ctrl/app/ctrl_app.h:62-66`, `test_acmp_mbx.cpp:970` | the three-way pass bound is checked only from above the observed worst

- Dropping MAAP's share (`#define CTRL_APP_PASS_MAX (ACMP_MBX_PASS_MAX)`, 568 accesses understated) escapes every arm (`probes_composition.log`, probe `pass-bound-drops-maap-share`).
- F6 compares its worst pass (231) with a bound of 1,580, so any value of 231 or more passes.
- This is the methodology already accepted for `ACMP_MBX_PASS_MAX`, and the figures are correct: `receipts/pass_max_if1.txt` and `pass_max_if2.txt` give 1,012 + 568 = 1,580 and 1,043 + 616 = 1,659, matching the README, design page and PR body.
- Optional: a `_Static_assert` or test that ties `CTRL_APP_MAAP_PASS_SHARE` to its stated terms. No lens effect.

### R530-5-S2 | SUGGESTION | Docs | `docs/design/MAILBOX_SPLIT.md:677-683` and `:692-706` | the owed-frame T_svc sentence is not restated for the three-way pass

- The two-way paragraph says the owed-frame bound (9,108 accesses) "fits T_svc" at the assumed 1 us per access. That stays true for the ADP and ACMP composition.
- With MAAP composed, the new table gives 14,220 accesses (0.70 us per access for T_svc), which does not fit at 1 us. The table and the Open items line (0.57 us) carry the right figures, so nothing false is stated.
- Optional: one sentence after the new table saying which bounds fit at 1 us. No lens effect.

### Commit-message note (not a finding)

- `dd3fc113`'s subject says "the three rings", but F6 fills events plus the acmp and maap rings.
- The author disclosed this in REVIEW READY 6040171459. Commit messages cannot change without a rewrite, which the lane rules forbid. Nothing to do.

## Prior public review findings (read after the pass above)

I read prior reports only after my own pass and the F1/S1/S2 probes. I did not read the concurrent external report.

| Finding | Disposition at this head | Evidence |
|---|---|---|
| R530-4-R1 RESIDUE, Docs: author handoff claims an unpinned-compiler run "would fail the audit" | **RETAINED** (RESIDUE, verdict-neutral) | The round-6 public handoff repeats it verbatim: `origin/665f3-review-evidence`, `review-evidence/665f3-r1/author-r6/HANDOFF.md:482-483` (added in `16497e02`). **Exact fix** (unchanged): replace "and its images would fail the audit (as round 4's do)" with "and, since no library is linked, its images pass the audit with the same figures; only round 4's library-linked images fail it". |
| R530-4-S1 SUGGESTION, Robustness: the identity is printed, not checked against the pin | Retained, optional | `ctrl_image.py:312-316` is unchanged in this respect. |
| R530-4-S2 SUGGESTION, Robustness: `ctrl_image.py` fails under `python3 -I` | Retained, optional | `python3 -I sw/firmware/ctrl/test/ctrl_image.py --help` still exits 1. |
| R530-3-F1 / R531-3-F1 MINOR (linked image), R530-3-R1 | Still RESOLVED | I reproduced the round-6 table byte for byte (below). The PR title is unchanged. |
| R531-2-F1 MAJOR; R530-2-F1..F3; R530-2-R1..R3; R531-1-F1..F5; R530-1-F1..F5, R1 | Still RESOLVED | These files are byte-identical to `39adc58f`, where R530-4 and R531-4 confirmed them: `sw/firmware/ctrl/acmp/*`, `hdl/milan/mailbox/*`, `sw/mailbox/*` and `sw/firmware/ctrl/mbx/*` (`receipts/rtl_and_contract_delta.txt`). Their tests pass at this head. The full campaign catches all 465 defects, including every planted defect from those rounds. |
| R530-2-S1..S3 SUGGESTION | Unchanged | No lens effect. |

## What was checked, by lens

### Conformance

- **Round-6 assignment:**
  - **Item 1 (merge):** the `--remerge-diff` of `aa0fdd01` keeps both sides in all nine conflicted files:
    - the README;
    - `ctrl_app.c` and `ctrl_app.h`;
    - `ctrl_arms.py`, `ctrl_build.py` (F2's `-DNDEBUG` kept; ACMP's guard is `CTRL_REENTRY_ASSERT`, `acmp.c:34`) and `ctrl_mutants.py`;
    - `test_ctrl_firmware.py`;
    - the ratchet (re-measured);
    - the mbx `Makefile`.
  - **Item 2 (composition):**
    - `ctrl_app.c:32-52` attaches ADP, then ACMP, then MAAP, before `ctrl_app_open()`;
    - `ctrl_loop_open()` (`ctrl_loop.c`) enables exactly the bound channels plus the events' IRQ and the filter;
    - the slots are 0..N-1, N..2N-1 and 2N..3N-1, held inside the 16-slot bank by `ctrl_app.c:12`. With N = 1 MAAP gets slot 2 and with N = 2 slots 4-5 (`receipts/pass_max_if*.txt`);
    - each adapter's sink ignores the others' slots (`maap_mbx.c:92-105`, `acmp_mbx.c:101`, `adp_mbx.c:92`).
  - **Item 3 (linked image):** the image composes all three modules, the base links through `ctrl_app_start_maap()`, and both shapes are measured against dev `e21c1ca0`. Reproduced below.
  - **Item 4 (checks kept):**
    - all 16 arms pass;
    - the 4 re-planted defects keep their test and words (`acmp_mutants.py:914`, `ctrl_mutants.py` `APP_BRING`, and `maap_mutants.py` `app-missing-rx-interrupt` and `app-channel-closed`);
    - the full campaign catches 465 of 465.
- **IEEE 1722-2016 Table B.9 / B.4 pool:**
  - `maap_compose()` refuses `preferred < MAAP_POOL_BASE` and `preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count`, and accepts the last range. The arithmetic is uint64 with `count <= 65535`, so it cannot wrap. `maap_init` refuses `count == 0` and `count > MAAP_POOL_SIZE` (`maap.c:170-172`).
  - U7 tests the three boundaries.
  - `maap_mbx_start()`'s ignored return (`ctrl_app.c:74`) can be false only for a range the compose already refused (`maap.c:187`).
- **Earlier F3 acceptance (items 1-6 and the common rules):**
  - The ACMP core, adapters, store owner, RTL and contract are byte-identical to `39adc58f`.
  - Their arms pass at this head: `acmp` 84, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 22, `unit`, `model`, `walk`, `adp`, `port`, `entity`, `rv32`, and reentry 122 + 122.
  - The default build and shipping image are unchanged. Nothing changed against dev under `sw/builder`, `sw/litex`, `configs`, `syn`, `constraints` or `hdl/top`, and `--ctrl-mailbox` stays default-off (`sw/litex/milan_soc.py:2479`).
- **Open integration point (author-disclosed):** MAAP's allocation does not reach ACMP's talker `source` port inside the app. This is outside round 6's frozen items and is stated in both READMEs and the PR body (pending manager duty below).

### RTL and architecture

- No HDL, contract or generator change since `39adc58f`. The only change on those paths is the mbx `Makefile`'s firmware source list, which picks up F2's MAAP sources for the co-simulation link (`receipts/rtl_and_contract_delta.txt`).
- `gen_mailbox.py --check`: 0 findings.
- `make -C tb/verilator/mbx -j2 VBUILD_JOBS=4` with Verilator 5.050 (identity in `receipts/toolchain_identity.txt`), in an export of the head (`receipts/runs/mbx_make.log`, rc 0):
  - Wishbone 382/0 and AXI4-Lite 427/0;
  - at two interfaces, 384/0 and 429/0;
  - the model at two interfaces, 369/0;
  - the co-simulation, 32/0;
  - the quick RTL mutants, 5 of 5.
- **Firmware architecture contracts:**
  - per-channel TX rings (`mbx.c:193-217`), so MAAP cannot take ACMP's TX room;
  - `ctrl_loop` capacity: 3 of 8 sinks and polls (U6 asserts it);
  - the `_Static_assert` keeps the three slot runs inside `MBX_N_TIMERS`.
- **Resources:**
  - the image is 46,608 B (35.6 %) at the shipping shape and 56,980 B (43.5 %) at the largest, of the 128 KB budget;
  - MAAP adds 1,104 B to `struct ctrl_app`;
  - the area figure (357 LUT / 86 FF) stands, since no RTL changed.

### Robustness

- Each refusal stops the composition before the later modules attach, and touches no mailbox register: the pool, an ACMP configuration, a MAAP range below or past the pool, an entity with no talker source, and the F2 entry without a port. U7 asserts this; the probe `acmp-refusal-after-maap` is caught.
- `ctrl_app_open()` returns false before any write for another contract. MAAP starts only after the channels are open; the probe `maap-start-before-open` is caught by F6, U6 and `maap`.
- At two interfaces, U6 and F6 run in `acmpif2`: worst pass 233 of 1,659, and 14 events, 12 acmp and 7 maap records drained.
- Reviewer composition probes: 10 single-defect probes (`scripts/probe_composition.py`, `receipts/runs/probes_composition.log`). 8 are caught:
  - slot overlap by one at two interfaces;
  - count forced to 1;
  - preferred range dropped at start;
  - allocation context dropped;
  - start before open;
  - entry dropping ctx;
  - ACMP refusal masked;
  - upper pool bound unchecked.
- Two escape: F1, and S1, which is intentionally loose.

### Tests

- `test_ctrl_firmware.py --require-rv32 --jobs 4`: PASS, all 16 arms (`receipts/runs/ctrl_firmware.log`). The tallies match REVIEW READY:
  - `acmp` 84, `acmpif2` 22, `acmpwalk` 127, `acmpnvm` 7;
  - `maap` 37 + 12, `maap_if2` 13, `maap_debug` 1;
  - reentry 122 + 122.
- F6 prints the worst pass: 231 at one interface, 233 at two.
- `fw_coverage.py --check --jobs 4`: PASS, 20 files. `ctrl_app.c` is at 42/42 lines and 40/40 branches.
  - The new exclusion (`maap_compose`, arc 4 of 4: the attach refusal) is justified. `maap_mbx_attach()` refuses only a full sink or poll table or a bound maap channel. After ADP and ACMP, the loop holds 2 of 8 of each, and nothing else binds channel `maap`.
  - The re-keyed ACMP row (arc 5 of 6) matches `if (cfg->acmp != NULL &&`.
  - The README says "All sixteen rows", and the table has 16 rows.
- **Full ctrl campaign** at this head, in four slices of `--self-test --slice K/4` (`receipts/runs/campaign_slice_*of4.log`): 117 + 117 + 117 + 114 = **465 of 465 caught**, 0 escaped.
  - Slice 2's log stops after 115 lines with rc 0, so I re-ran its last two entries (232-233) through the same grading: 2 of 2 caught (`campaign_slice_2of4_tail.log`).
  - A focused run of the 23 composition defects also caught 23 of 23 (`focused_campaign.log`).
- **F1** (above) is the open test gap.

### Documentation

- **Docs gates, all rc 0** (`receipts/runs/docs_gates.log`):
  - `docs_check.py`;
  - `check_em_dash.py --base e21c1ca0` (759 added lines, 7 pages);
  - `check_doc_style.py`, `check_baremetal_only.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_doc_paths.py`;
  - `gen_toc.py --verify-anchors` and `--check`.
  - The renderer-dependent gates ran under the pinned cmarkgfm/html5lib environment.
- **Figures re-derived and matched in the ctrl README, the design page and the PR body:**
  - pass bounds 1,012 / 568 / 1,580 / 1,659, and the four three-way bounds (4,740 / 17,380 / 34,760 / 14,220) with their access times, rounded down;
  - the defect counts: 269 F3 (with round 6's 15), 96 F2, 465 in all;
  - the helper bytes: 508 at both head and base (`riscv32-linux-nm`);
  - the 26-per-slice campaign recipe in the PR body;
  - the linked-image table.
- **Linked image** (`receipts/runs/ctrl_image.log`): `ctrl_image.py --base e21c1ca0`, run with the pinned SDK, reproduced the README and PR table exactly. Toolchain identity checks:
  - archive sha256 `d42680e9...`;
  - version line `Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`;
  - libgcc sha256 `d8ebca8c...`.

  The figures:
  - text 33,444/33,448, rodata 748, bss 12,416/22,784, totals 46,608/56,980, and +15,648 at both shapes;
  - audit `rv32i2p1`, 8,361/8,362 words;
  - app 7,904 B, of which MAAP is 1,104 B.
- **Residues:** R530-4-R1 is retained (above). S2 is a suggestion.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_app.c:12-92`, `ctrl_app.h:48-115`, merge `aa0fdd01` (remerge-diff), REQUIREMENTS.md:71-93, assignment 6037650104 items 1-4, IEEE 1722-2016 Table B.9 boundaries (U7), `acmp/*` byte identity to `39adc58f`, builder/litex/configs delta vs dev (empty) | R530-5 | `13e715136b0b7c8d9763e0b730d9709f2c9f5932` |
| RTL | CLEAN | `hdl/milan/mailbox/*`, `sw/mailbox/*`, `sw/firmware/ctrl/mbx/*` identity to `39adc58f`, `gen_mailbox.py --check`, mbx suite + co-simulation + if2 + quick mutants (`mbx_make.log`), `mbx.c:193-217`, `ctrl_loop.c` open/bind capacity, slot `_Static_assert` | R530-5 | `13e715136b0b7c8d9763e0b730d9709f2c9f5932` |
| Robustness | CLEAN | U6/U7/F6 at one and two interfaces, 10 composition probes (`probes_composition.log`), `maap_compose` arithmetic, `maap_mbx.c:60-153`, `maap.c:166-204` | R530-5 | `13e715136b0b7c8d9763e0b730d9709f2c9f5932` |
| Tests | **UNCLEAN** (R530-5-F1 MINOR open) | `test_acmp_mbx.cpp:904-1089`, `acmp_review_mutants.py` round 6, re-planted defects, full 465 campaign, focused 23, coverage ratchet and 16 exclusion rows, `probe_maap_mac.log` | R530-5 | `13e715136b0b7c8d9763e0b730d9709f2c9f5932` |
| Docs | CLEAN (R530-4-R1 RESIDUE retained, verdict-neutral) | `sw/firmware/ctrl/README.md` (composition, host test, linked size), `maap/README.md:76-135`, `MAILBOX_SPLIT.md:435-436,692-707,948-952`, `gtest/README.md:229-306`, PR #688 body, docs gates | R530-5 | `13e715136b0b7c8d9763e0b730d9709f2c9f5932` |

## Executed here (all at the exact head; the clone is unmodified)

| Command | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 4` | rc 0, 16 arms PASS | `receipts/runs/ctrl_firmware.log` |
| `test_ctrl_firmware.py --require-rv32 --jobs 4 --self-test --slice K/4`, K = 1..4, plus the 2-entry tail re-run (`scripts/index_campaign.py`) | 465 of 465 caught | `receipts/runs/campaign_slice_*` |
| `scripts/focused_campaign.py` (23 composition defects, the head's grading) | 23 of 23 | `receipts/runs/focused_campaign.log` |
| `fw_coverage.py --check --jobs 4` | rc 0, 20 files | `receipts/runs/fw_coverage_check.log` |
| `ctrl_image.py --base e21c1ca0...` (pinned SDK) | rc 0, table reproduced | `receipts/runs/ctrl_image.log` |
| `make -C tb/verilator/mbx -j2 VBUILD_JOBS=4` (Verilator 5.050, export of the head) | rc 0 | `receipts/runs/mbx_make.log` |
| docs and idiom gates (9 commands, renderer gates under the pinned environment) | rc 0 | `receipts/runs/docs_gates.log` |
| `scripts/probe_composition.py` (10 probes) | 8 caught, 2 escaped (F1, S1) | `receipts/runs/probes_composition.log` |
| `scripts/probe_maap_mac.py` (the F1 check at head and with the defect) | head PASS; defect caught at two interfaces | `receipts/runs/probe_maap_mac.log` |
| `scripts/pass_max.c` at one and two interfaces | 1,580 / 1,659 | `receipts/pass_max_if1.txt`, `pass_max_if2.txt` |
| clone state | HEAD, index tree and gitlinks exact; 0 tracked paths differ | `receipts/clone_state.txt` |
| hosted check runs on the head | snapshot | `receipts/hosted_check_runs.tsv` |

Probes ran only in exports under the packet's scratch directory. The clone was only read:
- its index tree equals the head tree `4b04d6dd`;
- `git status` is clean;
- the four gitlinks are at their recorded commits;
- `protocol-processor` is checked out at its pin.

A read-only `git fetch` refreshed the remote-tracking refs, so that I could read the public evidence branch. Ignored `__pycache__` directories are present. Some detached background runs were stopped by the session before writing an rc; each was re-run to completion in the foreground, and only completed runs are reported.

## Real limits

- Physical calibration was NOT RUN, and hardware was not used. Field skips are not hardware proof.
- I did not run the RTL mutation campaign (`tb/verilator/mbx/mutants.py`, 147). The mailbox RTL, contract and suite sources are byte-identical to `39adc58f`, and the quick arms pass (5 of 5).
- I did not run the store campaign (`test_ctrl_nvm.py --self-test`), `test_ctrl_nvm.py`, the builder bank, lint, Yosys or Vivado. `sw/firmware/ctrl_nvm` and the builder are dev's apart from the store README, and no HDL changed.
- The access time (A4) is unmeasured, so every bound is in mailbox accesses.
- **Hosted CI at the head** (snapshot 15:20 UTC):
  - `rtl-fast`, `firmware-unit`, `docs-check`, `elaborate`, `verilator-lint`, `yosys-elaboration`, all four Yosys shards, and Verilator shards 0, 2 and 3: success;
  - Verilator shards 1 and 4: in progress;
  - `Physical gPTP`: skipped. That is a skipped context, not an executed one.

## Pending manager duties

- Carry R530-4-R1 (RESIDUE, retained) to the residue checklist with its exact fix above.
- Record the author-disclosed integration point publicly if it is not already an Issue: MAAP's allocation is not connected to ACMP's talker `source` port in the app.
- Own hosted and `act` acceptance on the exact head, including Verilator shards 1/5 and 4/5.
- Build the final candidate on current dev, with the merge-turn validation.
- A4 (the access-time measurement) belongs to the F2-F5 bench pass.

R530-5 FINISHED
