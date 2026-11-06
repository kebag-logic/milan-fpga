[R776] POSITIVE - exact head 8ab3a930d6e2d217caf729d38c5ef17e98e292b3

# R776-5: external independent review of PR #842 (issue #840)

- Head `8ab3a930d6e2d217caf729d38c5ef17e98e292b3`, tree `050690f80b699e9e85d9782313c341552c627ecc`.
- Delta reviewed: `27df6e08..8ab3a930`, the merge of dev `3f6bef88` (PR #841) and the regenerated audit page.
- Live dev is `3f6bef88`, so the head already contains it. Merging dev with this head gives this exact tree.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open, and all five lenses are clean at this head. #841's hold releases with this PR's MAC and 1000BASE-T-only firmware, and the three auto-merged files read correctly together.

One new RESIDUE and two new SUGGESTIONs are recorded. Six earlier RESIDUE items are retained.

This verdict covers source review of the composition. It is not hosted acceptance, candidate-merge validation or hardware proof. **No executor gate receipt exists for this head**, so the execution evidence below is this review's own focused runs (see Real limits).

## The composition

### The hold releases with the new MAC: yes, measured

The `bootsa` leg had never run with this PR's identity, because #841 was built on the old MAC. It now takes `02:4b:4c:4b:4c:01` from the generated config (`boot_fw.h`: LO `0x4b4c4b02`, HI `0x0000014c`, entity `024b4cfffe4b4c01`).

| Run at this head | Result | Receipt |
|---|---|---|
| `make bootsa` | rc 0, 67 checks, 0 failures | `receipts/bootsa_clean.log` |
| Pair completes, first frame leaves | Cycle 40088, then MSRP at cycle 40112 with source `024b4c4b4c01` | same, lines 476 and 490 |
| Early-enable boots, pair unwritten | MAAP and CRF offered, then AAF and CRF offered; 0 frames left in either | same, lines 544 and 559 |
| #841's twelve mutants | 12 of 12 caught by their named checks; positive control passes | `receipts/bootsa_mutants.log` |
| `make gptp` | rc 0, 210 checks, 0 failed | `receipts/gptp_leg.log` |
| `make gmstep` | rc 0, 196 checks, 0 failures | `receipts/gmstep_leg.log` |
| `make ax1x1gptp` | **Partial, no verdict**: 22 ok, 0 failed, AAF flowing at 0.50 simulated s, then stopped by this review | `receipts/ax1x1gptp_leg.log` |

The hold does not depend on the address value. `mac_addr_seq` (`milan_datapath.sv:3106-3115`) reads only reset and the write handshake. The `gptp` leg confirms this, because it writes zeros and still passes.

### The hold releases under 1000BASE-T only: yes, by construction

The hold has no link term, and the firmware writes the pair before any PHY access:

1. `milan_init()` calls `configure_fabric()` at `milan_baremetal.c:1981`, which writes the pair at `:1900-1901`.
2. `phy_live` is set only inside `nvm_boot()` (`:1747`), called at `:1990`.
3. `phy_link_tick()` runs only behind `phy_live` or `nvm_started` (`:1175-1182`), and it is the only caller of the advertisement (`:1144-1145`).

So a partner without 1000BASE-T, a refused MDIO read or a missing PHY cannot keep the transmitters held.

The gate compares the same 16 address bits the CSR decodes (`milan_soc.py:861`, `milan_csr.sv:1121`), so it cannot disagree with the register write on the product.

### The auto-merged files read correctly together

- **`sim_gptp.cpp:844-859`.** Three identities coexist and each comment is accurate: the CSR MAC stays zero by #841's write, the AECP target is this PR's `024B4CFFFE4B4C01`, and thisClock comes from the leg's program (`THIS_CLOCK`, the generator's default MAC).
- **`milan_dp/Makefile`.** `:504` takes the MAC from the config, `:597` carries this PR's `--mac 0x024b4c4b4c01`, and the default `gptp_ucode.hex` keeps the generator default the leg expects. The `bootsa` recipe and the `ORDINARY_CASES` entry (`:717`, `:740`) are intact.
- **`BAREMETAL_FIRMWARE.md:112-116`, `:217`, `:2177` onward.** The hold text, the boot table row and the PHY section do not conflict. The claim that the builder writes the same MAC into the ROM holds at `endstation_builder.py:5957-5961`.

### The merge itself

- Re-deriving the three-way merge conflicts only in `docs/DOCUMENTATION_AUDIT.md`. Every other path is byte-identical to the automatic result.
- `sw`, `configs`, `avdecc` and `ci` have 0 changed paths since `27df6e08`. All six gitlinks are unchanged.
- No fixture from #841 reintroduces the old identity. `sim_boot_sa.cpp` and `gen_boot_fw.py` take the station MAC from the generated header, with no old or new station-MAC literal.
- Command-table stale rows are 36 at dev and 36 at head, with none added.
- `oracle.json` and `measurements.json` bind firmware and config, not datapath RTL. The `ax1x1gptp` ROM digest `04b59447...` equals the pinned `gptp_ucode_sha256`.

## Findings

No BLOCKER, MAJOR or MINOR.

### R10 - RESIDUE - Docs - PR body lines 3 and following

- **Lenses:** Docs.
- **Authority/evidence:** The body names `27df6e08` on dev `87e9d03a` as the validated head and has no line for this merge. The reviewer lines stop at round 3. AGENTS.md section 6 asks that the PR hold enough for a cold reviewer.
- **Impact:** A cold reader cannot tell from the PR what changed at this head. The omission changes no figure or result.
- **Required outcome, exact fix:** Add above the Round 5 line: `Round 6: merged dev `3f6bef88` (PR #841) and regenerated the audit page through `docs_inventory.py`. Head `8ab3a930d6e2d217caf729d38c5ef17e98e292b3`. The only conflict was `docs/DOCUMENTATION_AUDIT.md`. Firmware, builder, configs and gitlinks are unchanged since `27df6e08`.` Bring the reviewer lines up to date.
- **Verification:** Read the PR body.

### S10 - SUGGESTION - Tests - `tb/verilator/milan_dp/test_sim_pool.py:873`

- **Lenses:** Tests.
- **Evidence:** `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` fails, 16 of 17 pass. The list omits `sidmove` and `sidmove8`, so `make -n run` hands over 48 words against 42 expected.
- **Why this is not a finding against this PR:** It fails identically at `87e9d03a`, `3f6bef88`, `27df6e08` and this head (`receipts/test_sim_pool_*.log`), so the delta neither caused nor changed it. No workflow, Makefile or suite script runs this file.
- **Impact:** The arm cannot guard the recipe while it stays red, and nothing reports that. Its docstring's "fifteen legs" is also stale against eighteen.
- **Suggested outcome:** Open a public Issue. Add the two legs to `LEGACY_LEGS`, correct the docstring, and decide whether a gate should run the file.

### S11 - SUGGESTION - Tests - `configs/endstation_ax7101_1x1_tdm8.yaml:67`

- **Lenses:** Tests.
- **Evidence:** In `02:4b:4c:4b:4c:01`, octets 1 and 3 are equal, as are octets 2 and 4. A stamp that swapped those positions would emit identical bytes, so no source-address comparison could see it. This follows from the bytes and was not run.
- **Impact:** Small, and an improvement on the old MAC, whose octets 1 to 4 were all zero.
- **Suggested outcome:** Optional: give the `bootsa` leg a test MAC with six distinct octets.

The comment rule has no new instance. A scan of lines added in the delta finds no bench lane label, review round, reviewer ID or comment ID.

## Prior public findings

Read only after my own verdict and ledger were written to this packet.

| Prior finding | Severity | Disposition at this head | Evidence |
|---|---|---|---|
| R775-3 N3 = R776-3 F6 | MINOR | **RESOLVED**, kept | `sw` unchanged since `27df6e08` |
| R775-2 N1; R775-2 N2 = R776-2 F5; R776-2 F4 | MINOR | **RESOLVED**, kept | Same |
| R775-1 and R776-1 findings | MAJOR, MINOR | **RESOLVED**, kept | Same; the composition runs above add nothing against them |
| R5, PR title | RESIDUE | **RETAINED.** Still names `02:4B:4C:00:00:01`. Fix: `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` | Live title |
| R6, `STRICTER_READINGS.md:45` | RESIDUE | **RETAINED.** Fix: `- Gate 28b refuses a zero octet in any tracked config.` | Line unchanged |
| R7, `397_SERVICE_BUDGET.md:290-291` | RESIDUE | **RETAINED.** Fix: move line 291 below the table | Lines unchanged |
| R8 = RES-A, `phy_host.c:130-134` | RESIDUE | **RETAINED**, fix as published in R776-4 | `sw` unchanged |
| RES-B, `test_phy_firmware.py:84` | RESIDUE | **RETAINED**, fix as published in R775-4 | `sw` unchanged |
| R9, PR body lines 15 and 113 | RESIDUE | **RETAINED.** Fix: `with the gates at `3d1ca52f``; `at `3d1ca52f` and at dev` | Both phrases still live |
| R775-3 S6 = R776-3 S6, `tool-inventory.json` | SUGGESTION | **RETAINED**, for #838. Its pin was already stale at dev, and this delta adds nothing | `final_checks.log` |
| S9, R775-3 S7, S8, R776-3 S7 and the earlier suggestions | SUGGESTION | **RETAINED**, optional | Untouched by the delta |

## Lens results

This merge changes artifacts in every lens's scope, so section 7 needs each lens covered again here. Code the delta does not touch keeps its R776-4 result.

```text
[R776] PASS Conformance - milan_baremetal.c:1144-1145,1747,1900-1901,1981-1991; receipts/bootsa_clean.log; configs/endstation_ax7101_1x1_tdm8.yaml:67 - #840 identity and advertisement bytes unchanged since 27df6e08; every graded frame leaves with the decided station MAC, so #839's source-address result holds with #840's identity
[R776] PASS RTL - milan_datapath.sv:3106-3115,8815-8822,8934; milan_soc.py:861; milan_csr.sv:1121; receipts/bootsa_mutants.log - the PR adds no RTL; the gate reads only reset and the write handshake, shares the CSR's address bits and has no link or value term; 12 of 12 mutants caught on the composed tree
[R776] PASS Robustness - milan_baremetal.c:1175-1182; receipts/bootsa_clean.log lines 544,559; receipts/gptp_leg.log - no link, no PHY or a refused MDIO read cannot keep the hold; held sources sent 0 frames; a zero value still completes the pair
[R776] PASS Tests - receipts/bootsa_clean.log, bootsa_mutants.log, gptp_leg.log, gmstep_leg.log, pinned_measurements.log, test_sim_pool_*.log - each identity-carrying leg completed except ax1x1gptp (partial, 0 failed); the one red arm predates the PR base and is recorded as S10
[R776] PASS Docs - BAREMETAL_FIRMWARE.md:112-116,217,2177; REGISTER_MAP.md; TESTING.md; CHANGELOG.md; DOCUMENTATION_AUDIT.md; receipts/docs_gates.log - the merged text agrees; docs_inventory --check and --selftest, docs_check, doc style, feature status, wire accountability, baremetal-only and the module matrix pass; only RESIDUE remains
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Boot order, generated MAC words, `bootsa` frame log, config | R776-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| RTL | CLEAN | Hold, stamp, address wiring, twelve mutants | R776-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Robustness | CLEAN | PHY poll gating, early-enable boots, zero-value write | R776-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Tests | CLEAN (S10, S11 optional) | `bootsa`, `gptp`, `gmstep`, partial `ax1x1gptp`, pool test at four commits, pinned measurements | R776-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |
| Docs | CLEAN (RESIDUE R5 to R10, RES-B carried) | Three merged docs, CHANGELOG, audit page, PR body, gates | R776-5 | `8ab3a930d6e2d217caf729d38c5ef17e98e292b3` |

## Real limits

- **No executor evidence at this head.** There is no REVIEW READY and no gate receipt for `8ab3a930`. The issue's last one names `27df6e08`. This review's runs cover the composition, not the full gate list.
- **`ax1x1gptp` did not finish.** It runs at real simulated time, so I stopped it at 0.50 simulated s. Its rc 2 is my termination, not a verdict. Treat it as partial evidence only.
- **Not run at this head, by assignment:** full sweep, builder, behave, and the milan_dp legs other than those listed.
- **Service plans not rerun.** `fw_service_budget` elaborates the datapath, so #841's RTL is in that simulation. Only its offline self-test and `check_nvm_capture.py` ran. I expect no effect because the hold is off the CPU path, but that is reasoning, not measurement.
- **`check_em_dash.py` not run.** Its pinned renderer is not installed here. A direct count of added delta lines found 0, which is a weaker check.
- **Mutant driver.** I ran the suite's own `run_mutant()`, `run_leg()` and `verdict()` through a four-worker pool (`scripts/run_bootsa_mutants_pool.py`), not through `make bootsa-mutants`.
- **Evidence integrity.** The assigned `194f3733` packet is round 1 at `dd764ed7`, in an unsigned commit, so no signature was verified. Its manifest matched on 4 of 4 sampled files. The evidence branch's latest commit predates this head.
- **Clause text.** I did not open the standards. Citations rest on the source comments.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof.
- **Hosted.** At review time all 17 check runs at this head were queued, none complete. The 70 successes and 1 skip seen are for `27df6e08`, not this head. I draw no acceptance from either.
- **Reading order.** Listing PR comments early showed me each prior round's verdict line, and the PR body summarises earlier answers. I opened the findings themselves only after writing my verdict. I read R776-4 in full and R775-4 and earlier rounds by section. I did not read R775-5.
- **Corrected along the way.** Two early checks gave false results from my own commands and were redone: a filtered diff returned nothing, and a manifest sample read the wrong key. A broad process-stop command also ended my own shell before acting; the leg was then stopped by executable path, and no other process was touched.

## Pending manager duties

- Build and validate the current-dev candidate, builder and native banks, and link the receipts. While dev stays at `3f6bef88`, that candidate is this exact tree.
- Decide how the missing executor REVIEW READY at this head is closed (AGENTS.md section 5).
- Include a `--enforce-service` plan or accept the limit above, and let `ax1x1gptp` finish on its schedule.
- Own hosted and local-replica acceptance at the exact head.
- Carry R5 to R10 and RES-B to the residue checklist. R8 and RES-B edit source comments, so taking them creates a new head and the ledger rule applies.
- Open an Issue for S10 if wanted.
- Confirm the second positive and the full completion bar. Merge needs explicit maintainer authorization.

## Clone state

Probes ran in a scratch copy. One read-only test run in the clone left an ignored `scripts/__pycache__/`, which I removed. `HEAD` and tree match the assignment, `git status --porcelain --ignored` is empty, index and `HEAD` digests match (`b5c9ba6baa4563a1`), and all six gitlinks are unchanged (`receipts/final_checks.log`).

R776-5 FINISHED
