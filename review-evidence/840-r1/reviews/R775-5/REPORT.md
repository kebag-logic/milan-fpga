[R775] POSITIVE - exact head 8ab3a930d6e2d217caf729d38c5ef17e98e292b3

# R775-5: internal independent review of PR #842 (issue #840)

- Head `8ab3a930d6e2d217caf729d38c5ef17e98e292b3`, tree `050690f80b699e9e85d9782313c341552c627ecc`.
- Delta reviewed: `27df6e08..8ab3a930`, the merge of dev `3f6bef88` (PR #841) and a regenerated audit page.
- Source base `87e9d03a`. Live dev `3f6bef88`, rechecked at review time; it is this head's second merge parent.
- Reviewed in an isolated detached clone. No source edits, commits, pushes or GitHub writes were made.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open, and all five lenses are clean at this head.

The composition holds. #841's hold releases with the new MAC. It also survives the link flap that #840's auto-negotiation restart causes on every boot. That second point was the main risk in this merge, so it was tested as well as read.

This verdict covers source review at this head. It is not hosted acceptance, candidate-merge validation or hardware proof.

**No author gate receipt exists for this head.** The newest author evidence is for `27df6e08`, and the merge has none. The execution results below are this reviewer's own focused runs. They are not a source bank.

## Assigned focus

### 1. The merge is what it claims: holds

I replayed the merge of `27df6e08` and `3f6bef88` independently (`receipts/merge_composition.txt`).

- The replay's only conflict is `docs/DOCUMENTATION_AUDIT.md`. Its only auto-merges are the three named files.
- Against the merge commit, the replay differs in that audit page alone. `3670da88` to `8ab3a930` also touches only that page.
- Of the 18 files that differ from `27df6e08`, 14 are byte-identical to dev. The other four are the audit page and the three named files.
- `hdl/milan/milan_datapath.sv` is dev's blob, so #840 adds no RTL of its own.
- The firmware, builder and PHY peer are not in the delta. The three gitlinks equal dev's.

### 2. The hold releases with the new MAC: holds

`tx_sa_ok_w` (`milan_datapath.sv:3115`) depends only on the two write latches (`:3106`). It reads no address value and no link state. So the new value cannot affect release, and the run confirms it.

| Check at this head | Result | Receipt |
|---|---|---|
| Words the firmware writes | LO `0x4b4c4b02`, HI `0x0000014c`, wire order `024b4c4b4c01` | `legs/bootsa.log` |
| `bootsa` leg, the firmware's own `configure_fabric()` | 67 of 67; pair complete at cycle 40088; 999 frames | `legs/bootsa.log` |
| gPTP ROM address | `024B4C4B4C01`, the same MAC | `legs/bootsa.log` |
| Builder U/L warning | Printed, build completes, so the recipe is unaffected | `legs/bootsa.log` line 1 |
| `bootsa_mutants.py`'s own list, at the new MAC | Clean leg passes; 12 of 12 mutants caught by name | `legs/bootsa_mutants.log` |

`gen_boot_fw.py` still extracts `configure_fabric()` from #840's firmware. Nothing in the #841 leg hard-codes an old identity: each value comes from the generated header.

Four reviewer faults show the leg grades this configuration rather than passing by default:

| Fault | Result | Meaning |
|---|---|---|
| Firmware drops the `MAC_ADDR_HI` write | Fails; the entity never advertises | The hold really waits for both halves |
| Firmware writes HI before LO | 67 of 67 | "Either order" is true (positive control) |
| Stamp reverses the octets | Fails every control-lane source-address check | The leg reads the exact new value |
| gPTP ROM keeps `02:00:00:00:00:01` | Fails "every gPTP frame's source address" | The ROM and CSR agreement is graded |

### 3. The 1000BASE-T-only configuration: holds

**Order.** `milan_init()` calls `configure_fabric()` at `milan_baremetal.c:1981`, with the pair written at `:1900-1901`. `phy_live` is only set later, in `nvm_boot()` at `:1747`. So the PHY init at `:1145` cannot run before the pair, and nothing waits on link. A partner without 1000BASE-T therefore cannot stop the hold from releasing.

**The flap.** This was the real risk. The latch clears only on `axis_resetn`, firmware writes the pair once per boot, and #840 restarts auto-negotiation on every boot. If the link guard's reset reached `axis_resetn`, the transmitters would stay shut until the next reset.

It does not reach it. `axis_resetn` is `~ResetSignal(milan_cd)` (`sw/litex/milan_soc.py:857`). `reinit` extends only the shadow domains `macsys` (`:1742`) and `macdp` (`:1877`). `eth_rst` reaches the two `maceth` domains (`:1800-1802`).

I then flapped `i_link_up` in a copy of the leg, starting just after release (`scripts/patch_flap.py`):

| Flap | Advertise bound | MAC stalled | `tx_sa_ok` | Result |
|---|---|---|---|---|
| None (control) | 8000 ms | no | n/a | 67 of 67 |
| 50 ms | 3000 ms, as shipped | no | 1 throughout | 67 of 67 |
| 3 s | 8000 ms | no | 1 throughout | 67 of 67 |
| 3 s | 8000 ms | yes | 1 throughout | 67 of 67 |
| 2.5 s and 3 s | 3000 ms, as shipped | both | 1 throughout | 65 of 67 |

The two failures in the last row are a time bound, not a defect, and the widened rows prove it. Both checks ask for `ENTITY_AVAILABLE` within the leg's 3000 ms bound. A link rise while enabled draws `T-ADP-DELAY`, 0 to 4 s (`protocol-processor/hdl/common/KL_pp_prng.sv:155`), and the measured 2749 processor ms from link-up to `ENTITY_AVAILABLE` falls inside that. With only the bound widened, all 67 pass. Every source-address, hold and arbiter check passed in every flap run. The `tx_sa_ok=0` lines late in those logs belong to the leg's later full resets, not to the flap.

### 4. The auto-merged files read correctly together: holds

- **`sim_gptp.cpp`.** #840's AECP target (`:662`) and comment sit cleanly beside #841's pair writes (`:849-850`). The leg passes 210 of 210. With the two writes removed it fails 87 of 210, so they are needed here. One wording item: RES-7.
- **`Makefile`.** #840's `--mac 0x024b4c4b4c01` (`:597`) and #841's `bootsa` recipe (`:504`, `:717`, `:740`) do not interact. `make -n run` includes the leg, and it builds and runs through the recipe.
- **`BAREMETAL_FIRMWARE.md`.** "Step 2" (`:113`) is the step that writes the MAC. The table row (`:217`) agrees with the builder and with `README-parameters.md:70`. The PHY section (`:2177` on) makes no claim about the hold, and neither text contradicts the other.

The merge also carries #840's identity changes into `gmstep`, which passes 196 of 196.

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-6 - RESIDUE - Docs - PR #842 body, opening lines and Status

- **Authority/evidence:** The body's round lines stop at `27df6e08`, and Status names `cadb63b4`. Neither the merge of `3f6bef88` nor `8ab3a930` appears. AGENTS.md section 6 asks that the PR hold enough for a cold reviewer.
- **Impact:** A cold reader cannot tell that the head now carries #841, or that nothing was validated by the author at it. No stated figure is false.
- **Required outcome, exact fix:** Add above the Round 5 line: `Merge of dev `3f6bef88` (PR #841): head `8ab3a930`. The only conflict was the generated documentation audit, regenerated through `docs_inventory.py`. The gates below ran at the heads they name, not at this one.`
- **Verification:** Read the PR body.

### RES-7 - RESIDUE - Tests, Docs - `tb/verilator/milan_dp/sim_gptp.cpp:846`

- **Authority/evidence:** The comment says `configure_fabric()` writes the pair "first thing". It clears two enables and writes four identity words first (`milan_baremetal.c:1894-1899`). The text arrived with dev, so this is not new to #840.
- **Impact:** A small inaccuracy in a comment. The hold does not depend on what precedes the pair.
- **Required outcome, exact fix:** `the station MAC are written, as configure_fabric() does.`
- **Verification:** The comment reads so.

The comment rule has no new instance. A scan of the lines this delta adds under `hdl`, `tb`, `sw` and `scripts` finds no bench lane label, review round, reviewer ID or comment ID.

### Suggestions

- **S10 - Tests, Robustness - `tb/verilator/milan_dp/sim_boot_sa.cpp`.** The flap above is a reviewer probe, so nothing in the repository keeps it true. An arm that flaps the link after release, with a bound covering the 4 s `T-ADP-DELAY`, would. `scripts/patch_flap.py` is a starting point.
- **S11 - Tests - `tb/verilator/milan_dp/test_sim_pool.py:76`.** `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` fails at this head. It is **not caused by this PR**: it fails identically at `87e9d03a`, `27df6e08` and `3f6bef88` (`receipts/gates/sim_pool_attribution.txt`). `LEGACY_LEGS` has lacked `obj_sidmove` and `obj_sidmove8` since `18444ac64e` added them to the recipe. The other 16 arms pass. I found no caller in the workflows, the milan_dp Makefile or `docs/testing`, which is how this went unnoticed. I did not class it MINOR because the cause and the fix sit outside #840's scope and this delta does not change the failure. It does mean the arm stops before it can check #841's `bootsa` row. It should become its own Issue.
- **S12 - Docs - `CHANGELOG.md`.** #839 has an Unreleased section and #840 has none, although it changes the station identity and the link behaviour. CONTRIBUTING.md does not require an entry, so this is optional.
- **S13 - Tests - `configs/endstation_ax7101_1x1_tdm8.yaml:67`.** Octets 1 and 3 of the new MAC match, as do 2 and 4, so the leg cannot see a stamp that swaps either pair. This comes from reading, not a probe. The old MAC hid more, so it is not a regression.

## Prior public findings

I read these after my verdict and ledger were drafted.

| Finding | Class | State at this head | Evidence |
|---|---|---|---|
| R775-3 N3 = R776-3 F6 | MINOR | **Resolved**, stays resolved | The PHY peer and firmware are not in the delta; `test_phy_firmware.py` rc 0 here |
| All earlier BLOCKER, MAJOR and MINOR findings | various | **Resolved**, stay resolved | R775-4 and R776-4 closed them; the delta touches none of their files |
| RES-1 = R5, PR title | RESIDUE | **Retained**, rechecked live. Fix: `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` | `receipts/public_evidence.txt` |
| RES-4 = R6, `STRICTER_READINGS.md:45` | RESIDUE | **Retained.** Fix: `- Gate 28b refuses a zero octet in any tracked config.` | File unchanged |
| RES-5 = R7, `397_SERVICE_BUDGET.md:290-291` | RESIDUE | **Retained.** Fix: move line 291 below the table | File unchanged |
| RES-A, `phy_host.c:123-134` | RESIDUE | **Retained.** Fix as published in R775-4 | File unchanged |
| RES-B, `test_phy_firmware.py:84` | RESIDUE | **Retained.** Fix: `#: #840: each kept field the host driver grades: its register, its bits and the` | File unchanged |
| R8, `phy_host.c:130-134` | RESIDUE | **Retained.** Fix as published in R776-4; it overlaps RES-A | File unchanged |
| R9, PR body lines 15 and 113 | RESIDUE | **Retained**, line 15 rechecked live. Fix as published in R776-4 | PR body |
| R775-3 S6 = R776-3 S6 | SUGGESTION | **Retained**, for #838 | Merge changes no digest-pinned file (`receipts/gates/table_pins.txt`) |
| S7, S8, S9 and earlier suggestions | SUGGESTION | **Retained, not taken** | Delta does not touch them |

## Lens results

[R775] PASS Conformance - `receipts/legs/bootsa.log`, `milan_baremetal.c:1900-1901,1981`, issue comment 6670627857 item 4 - frames carry `024b4c4b4c01` from the first boot frame, entity `024b4cfffe4b4c01`; item 2's PHY behaviour is unchanged (`test_phy_firmware.py` rc 0); the certification gitlink is unchanged.

[R775] PASS RTL - `milan_datapath.sv:3106-3115,8815-8822,8934`, `milan_soc.py:854,857,1742,1877`, `legs/bootsa_mutants.log` - the datapath is dev's blob; the latch shares `axis_clk` with the CSR slave, so no new crossing; its reset is outside the guard's reach; 12 of 12 mutants caught.

[R775] PASS Robustness - `receipts/probes/flap_*.log`, `fw_no_hi.log`, `fw_hi_first.log` - link flap with and without a stalled MAC, a missing half, reversed write order; all behave as documented.

[R775] PASS Tests - `receipts/legs/{bootsa,gptp,gmstep}.log`, `probes/gptp_no_pair.log`, `probes/stale_gptp_rom.log`, `probes/dp_reversed.log` - 67, 210 and 196 checks pass; each of the three faults fails its named checks. S11 is pre-existing and unchanged by this delta.

[R775] PASS Docs - `BAREMETAL_FIRMWARE.md:113,217,2177`, `DOCUMENTATION_AUDIT.md`, `receipts/gates/summary.txt` - the composed text matches behaviour; `docs_inventory.py --check`, `docs_check.py`, `check_doc_style.py` rc 0; only RESIDUE is open.

## Published evidence

- **Archived packet at `194f3733`:** 299 rows. A 30-file spread matches `published_sha256` with no mismatch (`receipts/packet_spotcheck.txt`).
- **It is not signed.** The manifest has no signature field, and GitHub reports the commit `unsigned`. Integrity rests on hashes stored in the same commit. It also dates from round 1 (`dd764ed7`), so it says nothing about this head.
- **Author evidence:** the newest `REVIEW READY` is for `27df6e08`. None names `8ab3a930`.
- **Hosted, at 2026-11-06T21:48:59Z:** 17 check runs at this head, all queued, none executed (`receipts/hosted_snapshot.txt`). I draw nothing from them.

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | identity and hold on the wire; firmware order; PHY peer; scope decision | R775-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| RTL | CLEAN | hold latch, gates and stamp; reset and CDC topology; mutant campaign | R775-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Robustness | CLEAN | link flap matrix; firmware write faults | R775-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Tests | CLEAN | `bootsa`, `gptp`, `gmstep` legs; 12 mutants; reviewer faults; PHY peer; budget self-test | R775-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Docs | CLEAN | three composed texts; audit regeneration; docs gates | R775-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |

## Real limits

- **`ax1x1gptp` did not complete.** Attempt 1 ended on an external SIGTERM with no verdict, at 1.25 simulated seconds; I do not know what sent it. My rerun reached 1.50 simulated seconds with 25 checks ok and none failed, including `GET_AVB_INFO` naming thisClock `0x24b4cfffe4b4c01`. I then stopped it, because the full leg belongs to the scheduled physical suite and, by my estimate from its remaining windows, needs over an hour here. It is partial evidence and is not a pass.
- **Measured figures predate #841's RTL.** `fw_service_budget` elaborates the real datapath, and its oracle and `measurements.json` were taken at `4ab1bca0`. I expect no change, because the gate is transparent once open and the stamp adds no cycle, but that is reasoning. A rerun needs the pinned RV32 SDK, LiteX and a cached netlist, which are absent here. The self-test (55 checks) and `check_nvm_capture.py` pass, but neither re-measures. The text states those figures at `4ab1bca0`, so none is false.
- **Not run: `check_em_dash.py` and `ci_tool_inventory.py --check`.** Both refused with rc 2 because a pinned tool is missing here. This is neither a pass nor a failure. The first was stopped by a missing renderer, the second by an unset `CI_IMAGE_SHFMT` parser pin. For the digests I compared the merge's changed files with the command table directly.
- **Not run at this head:** full sweep, service plans, capture arms, standalone builder, behave. No manager source bank ran here and I infer none.
- **The flap is a model.** It drives `i_link_up` and `tready`. The SoC's `macsys` and `macdp` resets are outside this bench, so that half rests on reading `milan_soc.py`.
- **#841's RTL was reviewed for composition only.** I judged what #840 depends on, not the whole of that PR again.
- **Clause text.** I opened no IEEE or Milan text. Clause references are quoted from the repository.
- **Hardware.** Physical calibration NOT RUN, and field skips are not hardware proof.
- **Reading order.** While triaging I listed the first line of each public comment, which showed earlier verdict tokens but no finding text. I also read the manager's identity decision first, as scope. Prior findings came after my draft verdict and ledger.
- **My own errors, all corrected before any conclusion:**
  - My first attribution of S11 used archives without submodules and proved nothing. I redid it in a full copy.
  - My first packet check read the wrong digest field and showed false mismatches. I fixed the script and reran it.
  - I predicted that a 2.5 s flap would pass. It did not, which led to the widened-bound test and the `T-ADP-DELAY` explanation.

## Pending manager duties

- Decide whether the missing author gate receipt at this head needs answering before the merge turn.
- Build and validate the current-dev merge candidate, with builder and native banks, and own hosted and act acceptance.
- Make sure `ax1x1gptp` and the `--enforce-service` plans run on that candidate, since both have gaps here.
- Carry RES-1, RES-4, RES-5, RES-6, RES-7, RES-A, RES-B, R8 and R9 on the residue checklist.
- Open an Issue for S11. Decide whether S6 goes onto #838.
- The #840 title and body still state the round-1 identity, so a cold reader needs a pointer to the later decision.
- The PR has no closing keyword, so #840 needs closing by hand after the merge. #839 also still shows OPEN after PR #841's merge.
- The second independent positive review, which this report does not supply.

## Clone state

No probe touched the clone; every build ran in a disposable copy. At the end, HEAD, tree, index and worktree equal the head, with 1477 tracked entries matching in blob and mode, no status entries, and the three gitlinks unchanged (`receipts/clone_state.txt`).

## Reproduce

Verilator 5.050 identity is in `receipts/verilator_identity.txt`. `VERILATOR_DIR` overrides its location in the scripts. Work in a disposable copy of the clone.

```sh
make -C <copy>/tb/verilator/milan_dp ci-prepare
scripts/run_leg.sh <copy>/tb/verilator/milan_dp <log dir> bootsa bootsa
python3 scripts/bootsa_parallel.py <copy>/tb/verilator/milan_dp <work dir> 5
python3 scripts/patch_flap.py <copy>/tb/verilator/milan_dp/sim_boot_sa.cpp
echo 'public_flat_rd -module "milan_datapath" -var "tx_sa_ok_w"' >> <copy>/tb/verilator/milan_dp/bootsa_probes.vlt
sed -i 's/kAdvertiseBoundMs = 3000/kAdvertiseBoundMs = 8000/' <copy>/tb/verilator/milan_dp/sim_boot_sa.cpp
scripts/run_flap_wide.sh <copy>/tb/verilator/milan_dp <log dir>
python3 scripts/cmp_sim_pool.py <copy>/tb/verilator/milan_dp
scripts/verify_clone.sh <clone> <head> <tree>
```

`scripts/run_probes.sh` holds the firmware, stamp and gPTP faults. `bootsa_parallel.py` and `run_flap_wide.sh` had comment-level or dead-code cleanups after they ran, with no change in behaviour.

R775-5 FINISHED
