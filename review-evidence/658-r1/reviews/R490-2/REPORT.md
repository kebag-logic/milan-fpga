[R490] POSITIVE - exact head 5747a8cb99495cb0331658cdd499b9c44e3eda91

Round R490-2, internal cleared-context review of issue #658 / PR #670.
Head `5747a8cb99495cb0331658cdd499b9c44e3eda91`, tree `d1d63caa2490c515624194cb5711ddb76c1601dd`.
Source base dev `e617275074e370cec342af99b929e2588fc8d43f`; round 2 is six commits on `fb4953bd` plus the `--no-ff` merge `57155256` of dev `510fae60`.
Assignment: round-2 comment 5997263077 on #658.

All five lenses were applied at this head and each is clean.
Every R490-1 finding is resolved: F1, F2, R1 (as a gate-compliant split, accepted), R2.
The other reviewer's R491-1 F1 is resolved with its exact text.
Two SUGGESTIONs remain, neither blocking.

## What round 2 changed

- **RTL: nothing in the parent.** `git diff fb4953bd..5747a8cb -- hdl` is empty. Dev changed no parent `hdl/` file between the base and `510fae60`. The only RTL movement is dev's processor pin, `631eeb34` to `ead80360` (#661).
- **The pin and this lane's interfaces.** I read the pin's diff for the faces this lane depends on. `restore_done_o`, `restore_closed_o` and the `amap_edit_wait_i` contract are unchanged: no `+`/`-` line of `KL_aecp_nvm_writer.sv` touches CLOSED, done or the format rows, and `amap_edit_wait` has no diff line.
- **Tests.**
  - `[DYNMAP]` gains the guard-arm section, `sim_nxn.cpp:4295-4532`, compiled in the dynmap leg alone through `#ifdef DYNMAP_DEFAULT_TB`.
  - `await_aecp` gains a per-clock callback (`:930-939`).
  - `dynmap_probes.vlt` opens six more signals.
  - `dynmap_mutants.py` gains seven guard-arm removals (`:86-151`).
- **Docs.** The README section and its table; R491-1 F1 at `SAVED_STATE_MATERIALIZATION.md:1216-1219`; R490-1 R2 at `REGISTER_MAP.md:2160-2161`; R490-1 R1 as `CHANGELOG.md:55-56`; and the merge resolutions in `CHANGELOG.md` and design section 5.2.

## Findings

### S1 - SUGGESTION - Tests - the render RAM site of the CSR hold is live, and ungraded, on the Arty input shapes

- **Artifact:**
  - The RAM-side hold: `hdl/milan/milan_datapath.sv:6783-6789` (render) and `:1256-1262` (capture).
  - The boot writer's render leg: `:4595-4601`, which drives only keys whose `ADP_DMAP_IN_RPHYS_C[k][6]` is set.
  - The keys: `configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh:86`, and the same line in `endstation_arty_8ch` and `endstation_arty_current`.
  - The rationale: `tb/verilator/milan_dp/README.md:800-813`.
- **Authority and evidence:**
  - **The README is true for the shipping shape.** On `endstation_ax7101_1x1_tdm8` all eight input keys have a physical render key (`RPHYS` `0x42`..`0x49`). There are eight dynamic output keys, so `AMAP_BOOT_KEYS_C` is 8 and both registered write strobes are high on every busy clock. The one exception is the first clock after reset, where no CSR commit can occur, and later window laps rewrite every key anyway. Each leaf's mux gives that strobe priority over the CSR writer.
  - **Executed confirmation.** My probes Q1, Q2 and Q3 (capture RAM site, render RAM site, both) each SURVIVE with 162 checks and 0 failures (`receipts/probes_A.log`). I accept the README's reason for this shape.
  - **The Arty input shapes differ.** There, only input keys 0 and 1 have a physical render key, and the cursor walks `max(in, out)` keys. So the render strobe is idle on most sweep clocks. Only the render RAM site then stops a CSR render write (keys 0 and 1, `:1829-1834`) from landing in the RAM while the store site refuses it. A write that lands after the sweep has passed its key leaves the store and the RAM split.
  - **The README admits the gap.** It says "an input key with no physical render key ... No leg grades that today", but it does not name the Arty inputs as that case.
  - **R490-1's pointer was wrong.** It named "the 8x8 render side". On 8x8 the single input key has no physical render key, so `cfg_chmap_rphys_w[6]` gates every CSR render write off, and the RAM site is inert there too.
- **Impact:** small. The guard is correct by inspection. Its loss would show only for a CSR map write (a bring-up window with no firmware user) inside the roughly 32-clock sweep after the restore's terminal, on an Arty image. Arty is #583 future work, out of this issue's scope.
- **Suggested outcome:** when the #583 Arty work resumes, stage a CSR render write against the sweep on an Arty shape and plant the render RAM site alone. Until then, the README could name the Arty shapes' input keys 2 and up as the live case. Optional.
- **Verification:** a planted removal of `:6786`'s term is caught on that leg.

### S2 - SUGGESTION - Tests - retained from R490-1 S1: the talker end-to-end check runs inside the boot window

`tb/verilator/capture_coherence/sim_dp.cpp` is unchanged since `fb4953bd`.
The post-release capture RAM is still graded by readback in `[DYNMAP]`.
A post-release run of the talker check would be the more literal proof.
Optional; unchanged.

No BLOCKER, MAJOR, MINOR or RESIDUE was found at this head.

## Prior public review findings at this head

These were read after my own pass over the diff. The verdict and ledger above were drafted before I read R491-1.

| Finding | Status at `5747a8cb` | Evidence |
|---|---|---|
| R490-1 F1 (MINOR, Tests): the guard arms are untested | **RESOLVED** | See the table below and S1. |
| R490-1 F2 (MINOR, Docs and Tests): the PR body overstated the gPTP leg | **RESOLVED** | See the text after the table. |
| R490-1 R1 (RESIDUE): `CHANGELOG.md:54` | **RESOLVED, split accepted** | See the text after the table. |
| R490-1 R2 (RESIDUE): `REGISTER_MAP.md:2157-2158` | **RESOLVED** | The exact text is present at `REGISTER_MAP.md:2160-2161` (`receipts/exact_text_checks.txt`). |
| R490-1 S1 (SUGGESTION) | **RETAINED** as S2 | Optional. |
| R491-1 F1 (MINOR, Docs): the persistence sentence | **RESOLVED** | The reviewer's three sentences are present verbatim at `SAVED_STATE_MATERIALIZATION.md:1216-1219`, and the replaced sentence is gone (`receipts/exact_text_checks.txt`). They agree with section 1 (`:195`, the phase-5 live-write pulse held sticky) and with stage 3 owning the writer. |
| R491-1 S1 (SUGGESTION, RTL): a shipping-shape specialization of the edit wait | **Unchanged, optional** | The RTL is unchanged. Any specialization must keep the edit-wait arm's behaviour wherever a sweep can meet an edit. That arm is now graded by "edit meets the sweep". |

**R490-1 F1: what kills each round-1 probe.**
- Round 1's own probe script, byte-identical to its published copy (sha256 `75d05af1...19cb`), run at this head (`receipts/round1_probes_at_head.log`, `round1_probes_results.json`, rc 0):
  - P1 KILLED (4 of 162), P2 (2), P3 (6), P5 (2), P9 (4).
  - P4 (6), P6 (5), P7 (2), P8 (13), P10 (6) and P12 (18) are still KILLED.
  - P11 SURVIVES, equivalent as in round 1.
- Each arm has a planted control in the lane's campaign, caught on its named check (`receipts/campaign_full.log`, 16 of 16, rc 0).
- My own probes Q4 to Q7 narrow the arms further, and each is KILLED (`receipts/probes_A.log`, `probes_B.log`):
  - the store holds active only in the window;
  - the edit wait active only in the window;
  - the terminal not rewinding the cursor;
  - the sweep starting at key 5.
- **Where each arm is staged.**
  - The CSR-hold arm places one commit per clock from CLOSED-2 to CLOSED+12. It records refused through +9 and landed from +10, never split (`receipts/dynmap_clean.log`). That boundary is the one the RTL gives: the terminal clock, eight sweep clocks (`:4570-4578`), then the drain clock (`:4569`).
  - The roll-back arm invalidates both rows on the clock CLOSED ends the window.
  - The edit arm holds the sweep for 1000 clocks, and the ADD is answered at 1190.
- **The RAM sites alone:** see S1. Their rationale is accepted for the shipping shape.

**R490-1 F2: the gPTP sentence.**
- The PR body now says the leg writes the eight capture keys after the walk, that its payload check needs those words, and that it does not grade the refusal while the hold is up.
- This matches `tb/verilator/milan_dp/sim_ax1x1gptp.cpp`:
  - `:705-718`: the walk is polled to done in 64-clock steps;
  - `:735-739`: then several CSR writes, then eight `0x908` loopback words (`0xD000 | ...`);
  - `:885`: the payload check against the peer ramp.
- The sentence also matches what P1 does at the head: it is KILLED by `[DYNMAP]`.

**R490-1 R1: the CHANGELOG split.**
- The exact one-sentence text has 13 words. `scripts/check_doc_style.py:39` caps a sentence at 10, and its own analyzer reports "sentence has 13 words; maximum is 10" for that line (`receipts/changelog_r1_wordcap.txt`).
- The head carries the same words as two bullets, `CHANGELOG.md:55-56`. The analyzer finds nothing in them, and the gate passes (`receipts/gate_check_doc_style.log`).
- The meaning is unchanged: the window refuses writes, and the refusal lasts until one sweep after the terminal. I accept the split.

## Lens results

- `[R490] PASS Conformance - hdl/milan/milan_datapath.sv:4393-4547,4629-4632,4762-4767 (unchanged since fb4953bd); receipts/dynmap_clean.log 162/0 - power-on identity on SPI 0/SPO 0 against rulings 5988293154/5988843004; Milan v1.2 5.4.2.7 (8->4 refused 7, REMOVE 4..7, 8->4 SUCCESS, 4->8 keeps 4); restored 4 ch with 4 identity and SET 8 SUCCESS; nothing prunes or adds at run time (round-1 P12 KILLED 18); the processor pin ead80360 leaves restore_done_o/restore_closed_o and the edit-wait contract unchanged, and the leg passes on it`
- `[R490] PASS RTL - hdl/milan/milan_datapath.sv:1155,1259,4358,4549-4608,4642-4653,4742,4754,6786 (byte-identical to fb4953bd); protocol-processor/hdl/aecp/KL_aecp_engine.sv:466,2355; receipts/gate_lint_rtl.log (90 <= 90, no hit in 4393-4660) - cursor width/wrap, busy = window || sweep || drain, write-strobe priority at both leaf muxes, CSR hold at all four sites, merge adds no parent RTL; area +337 LUT after opt (+137 in the touched instances) read as published, with the rest in instances whose RTL and connections are unchanged (own-logic rule)`
- `[R490] PASS Robustness - tb/verilator/milan_dp/sim_nxn.cpp:4334-4532; receipts/dynmap_clean.log, probes_A.log, probes_B.log, legs/*.log - CLOSED terminal on a chosen clock, a D3 roll-back on the terminal's clock, a CSR write on every clock across the window's end per side, an edit meeting a held sweep inside the 4096-clock phase bound; static-output and non-RPHYS shapes judged from configs/generated/*/gen/adp_shape_defaults.svh:73-86 (S1); obj_nxn 1967/0, obj_nxndv 1969/0, obj_nxn8 3751/0, obj_nxn4c 1967/0 at the head (the four legs 5747a8cb repairs)`
- `[R490] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:4295-4532, dynmap_mutants.py:86-151, dynmap_probes.vlt:10-23; receipts/campaign_full.log 16/16 rc 0, round1_probes_at_head.log, probes_A.log, probes_B.log - every guard arm with an effect on the shipping shape fails a named check when removed; failure counts equal README:784-797 and the PR body; the RAM-site rationale is verified by Q1-Q3 surviving and by the RTL argument (S1, optional); vacuity guard requires all 15 offsets per side`
- `[R490] PASS Docs - tb/verilator/milan_dp/README.md:753-772,778-813; docs/testing/TESTING.md:274; CHANGELOG.md:43-61; docs/design/SAVED_STATE_MATERIALIZATION.md:195,603-614,1211-1220; docs/reference/REGISTER_MAP.md:2160-2165; PR #670 body at 5747a8cb - R490-1 R1/R2 and R491-1 F1 resolved (receipts/exact_text_checks.txt); counts (162, 13 planted, 16 of 16, P-probe failures 4/2/6/2/4) match executed receipts; the gPTP sentence matches the leg; merge resolutions keep both sides; docs_check, check_doc_style, check_doc_paths, measure_test_evidence --check rc 0`

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv` image/clip/terminal (unchanged since `fb4953bd`); processor pin `ead80360` diff for the restore terminal and edit-wait faces; `[DYNMAP]` 162/0; round-1 P12 | R490-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| RTL | CLEAN | `milan_datapath.sv:1155-6789` hunks; `KL_aecp_engine.sv` wait contract; 5 generated shape headers; lint ratchet; published area delta (own-logic rule) | R490-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Robustness | CLEAN | CLOSED, roll-back, CSR-across-terminal and edit-meets-sweep arms; probes Q4-Q7; obj_nxn, obj_nxndv, obj_nxn8, obj_nxn4c at the head; static-output and non-RPHYS shapes | R490-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Tests | CLEAN | `sim_nxn.cpp` guard section; `dynmap_mutants.py`; `dynmap_probes.vlt`; full campaign 16/16; round-1 probes P1-P12; probes Q1-Q7 (S1, S2 optional) | R490-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |
| Docs | CLEAN | milan_dp README section and table; TESTING.md row; CHANGELOG entry and merge; design page sections 1, 5.2, 8.4; REGISTER_MAP 0x900; PR body | R490-2 | 5747a8cb99495cb0331658cdd499b9c44e3eda91 |

## Executed evidence (this round, at the exact head)

Simulator: the pinned wrapper `--version` reports "Verilator 5.050 2026-07-01 rev v5.050" (wrapper sha256 `905795b9...e92f`, binary hashes in `receipts/verilator_identity.txt`).
Builds ran in the isolated review clone, with mutants and probe objdirs under the packet's scratch.
The environment is in `scripts/env.sh`.
In the build logs the simulator's install prefix is replaced by `<pinned-root>`.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp dynmap` | rc 0, 162 checks, 0 failures | `receipts/dynmap_clean.log`, `.rc` |
| `python3 dynmap_mutants.py` (all 13 mutants, 3 clean controls) | rc 0, 16 checks, 16 PASS; per-mutant failure counts equal the README table | `receipts/campaign_full.log`, `.rc` |
| `scripts/round1/r490_mutants.py --jobs 3 --vjobs 2` (P1-P12) | rc 0; 11 KILLED, P11 SURVIVED (equivalent) | `receipts/round1_probes_at_head.log`, `round1_probes_results.json` |
| `scripts/r490_2_probes.py Q1 Q2 Q3 Q4` | rc 0; Q1-Q3 SURVIVED (expected), Q4 KILLED | `receipts/probes_A.log`, `.rc` |
| `scripts/r490_2_probes.py Q5 Q6 Q7` | rc 0; all KILLED | `receipts/probes_B.log`, `.rc` |
| `make -f Makefile -f scripts/r490_2_legs.mk r490-{nxn,nxndv,nxn8,nxn4c}` | rc 0 each: 1967/0, 1969/0, 3751/0, 1967/0 | `receipts/legs/*` |
| `scripts/lint_rtl.py --check`, `check_rtl_source_lists.py`, `pp_srcs.py --check` | rc 0 each | `receipts/gate_*.log`, `gates_summary.txt` |
| `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `measure_test_evidence.py --check` | rc 0 each | `receipts/gate_*.log` |
| `check_em_dash.py --base 510fae60`, `gen_toc.py --check` | NOT JUDGED: rc 2, the pinned Markdown renderer dependency is absent on this host | `receipts/gate_check_em_dash.log`, `gate_gen_toc.log` |
| exact-text and word-cap checks | see the prior-findings table | `receipts/exact_text_checks.txt`, `changelog_r1_wordcap.txt` |
| hosted check runs on the exact head (04:11 UTC) | executed and green: rtl-fast, elaborate, verilator-lint, yosys-elaboration, Yosys shards 0-3, Verilator shards 0 and 3, bdd-conformance, wire-accountability, docs-check, docs-check-no-git, full-ci-gate, changes; in progress: Verilator shards 1, 2, 4; skipped: Physical gPTP | `receipts/hosted_checks_snapshot.txt` |
| clone integrity after the round | HEAD and tree exact; porcelain and ignored empty; 1014 tracked blobs re-hashed equal with modes; index equals the HEAD tree; 4 gitlinks unchanged; submodule worktrees clean | `receipts/clone_integrity.txt` |

**Two run notes.**
1. A first split campaign, eight parallel invocations, gave the same 16 PASS. Its rc files were not captured, so it is superseded by `campaign_full` and not published.
2. One probe rerun was invalid and is not published. My cleanup had removed the leg's generated ROM files, which the campaign recipe deliberately does not remake, so every probe in that rerun died by signal. I regenerated the ROMs (`receipts/regen_roms.log`), and the published Q1-Q7 receipts come from a later run that treats a death by signal as non-evidence.

## Real limits

- **Not run in this round:**
  - the full `milan_dp` pool, `milan_dp_render` and `capture_coherence` suites as wholes, and `pp_shadow` (their round-2 inputs are unchanged apart from the pin merge);
  - `milan_dp_mclk`, Yosys, the builder bank, `xvlog_gate.py`, the nightly physical gPTP leg;
  - any Vivado measurement.

  The campaign's clean controls ran the listener (`T18`) and talker (`--quick`) legs at the head.
- **Area:** the published +337/+137 figures were read, not reproduced.
- **Em-dash and TOC gates:** not judged here (missing dependency).
- **Not hardware proof:** physical calibration was NOT RUN, and no bench read was made. Field skips are not hardware proof.
- **Hosted evidence:** three Verilator shards were still in progress at the snapshot.
- **Author material:** I did not read the published author handoff or scratch material. I read the issue, the PR body, the REVIEW READY comments and the executable logs.

## Pending manager duties

- **Candidate merge:** build the current-dev candidate (source base `e6172750`, live dev `28f9666f`) and validate it. If #645 lands first, re-run `dynmap` and `dynmap-mutants`, because both lanes edit `milan_datapath.sv`.
- **Resource gate** (`docs/design/AREA_BUDGET.md`): `route-1x1` and `record --write` on the merge result belong to the merge bank.
- **Bench read** of the power-on maps on the AX7101 after flashing ("Closes #658" excepts it).
- **Hosted and local-replica acceptance**, including Verilator shards 1, 2 and 4.
- **Carried owner decision**, non-blocking: the 8x8 output identity onto unbacked loopback clusters.
- **Carry S1 to #583** if the Arty work resumes. Carry R491-1 S1 as optional area work.

R490-2 FINISHED
