[R669] NEGATIVE - exact head 63a187e1579474bca562d85304b9a91466877c33

# R669-1: internal cleared-context review of #637 / PR #768

- Head `63a187e1579474bca562d85304b9a91466877c33`, tree `45c859e17681896f2fa3db26c04de75ef9f125d4`; diff `e9cbb676..63a187e1` (11 commits, 22 files).
- Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and its four public comments (scheduling 6257040284, assignment 6257168886, TAKEN, REVIEW READY), the D3 page (`docs/design/SAVED_STATE_MATERIALIZATION.md` 3, 5.2, 6.1 to 6.3, 8.1, 8.8, 18.4), FASTCONNECT 9.3, REGISTER_MAP, the processor's `07_memory_maps.md` 5.1 at pin `2cbed0a9`, the diff and history, the published evidence tree `270c5c99:review-evidence/637-r1`, and the hosted check runs at this exact head.
- Prior public review findings on this PR: **none exist**. The PR has no review and no review comment; its only comment is the review-start notice. Nothing to resolve or retain.
- Scope derived from the acceptance: (1) the parent restores 0x60/0x70 at boot under the D3 rules (well-formed only; torn or corrupt keeps the default) and resets on roll-back; (2) ownership stated on the contract pages and matching the processor; (3) a planted power cycle after a map change, plus a torn-record control; (4) capture timing and census unchanged or re-measured; the #763 additions (EMPTY both ways and a non-empty non-default list survive; record format kept); every new check has a planted mutant; every touched gate rc 0.

## Verdict basis

Four MAJOR and two MINOR findings are open, so every lens is unclean and the verdict is NEGATIVE. The core restore and writer behave as the
desk evidence claims: I reproduced the dynmap leg (331 checks, 0 failures) and pp_shadow (610, 610, 650 and 317 checks, 0 failures) at this head.
Four things block it:

- the map restore's outcome never reaches the combined restore verdicts, so a lost saved map reads as a clean first boot (F1);
- six restore arms have no executable evidence: all six planted probes survive (F2);
- the protected `docs-check` context fails at this exact head (F3);
- two more gates fail that the hosted fail-fast never reached (F4).

## Findings

### F1 MAJOR — Conformance, RTL, Docs, Tests — `hdl/milan/KL_pp_shadow.sv:1630`, `:1641`; `hdl/milan/milan_datapath.sv:5228`, `:5583` — the map restore's verdict is invisible: PP_STAT reads "blank" after maps were restored, and "not failed, blank" after a device error lost them

**Authority.**
- D3 page section 3 rule 7 (`SAVED_STATE_MATERIALIZATION.md:376`): "blank is a restore that did not fail and in which neither walk validated a record".
- D3 page 5.2 (`:611-613`): "restore blank reads 1 only for a restore that did not fail, so a device error that loses the one saved record never reads as a clean first boot (H8)".
- D3 page 6.2: the map record's refusal is an abort (cause 4).
- `REGISTER_MAP.md:2391`: PP_STAT `[3]` "either walk failed" and `[7]` "the completed restore validated **zero** records".
- Issue acceptance 1: "under the same D3 rules as the processor's records".

**Evidence.**
- `restore_fail_o` and `restore_blank_o` are still the processor's combined verdicts alone (`KL_pp_shadow.sv:1630`, `:1641`).
- The map restore's roll-back flag `amr_rs_fail_r` (`milan_datapath.sv:5228`, set at `:5583`) is wired to nothing a host can read. Its own comment calls it "for diagnosis".
- The reviewer's instrumented copy of the leg (`scripts/ppstat_probe.sh`, `receipts/dynmap-instrumented-ppstat-run.log`; the leg's own tally is unchanged at 331/0) prints PP_STAT after each planted power cycle:
  - `saved`: two map records validated and applied, and PP_STAT reads `done=1 fail=0 blank=1`.
  - `roll-back` (a device error), `slow memory` (the aggregate deadline) and `silent memory` (the per-wait deadline): the saved maps are lost and rolled back (`map_rs_fail=1`), and PP_STAT still reads `done=1 fail=0 blank=1`.

  This is exactly the H8 case the contract forbids. A slot whose only saved state is channel maps is common: a user who only re-routes channels.
- The deviation is recorded nowhere. Section 18.4 documents the one-pass deviation but not this one, and the PR body does not mention it either.

**Impact.**
- After a device error or a deadline, an entity that lost its saved maps reports a clean first boot.
- An entity that restored them reports that nothing came back.
- The firmware's boot line prints these bits (`sw/firmware/milan_baremetal/milan_baremetal.c:1782`), so the on-board qualification this release item depends on would misread both cases.
- A host's durability reading inherits the same error.

**Required outcome.** One of two:
- the map restore's outcome joins the combined verdicts the D3 rules define: fail on its transport roll-back or a refused put-back, and blank 0 when a map record was validated or lost;
- or the deviation is ruled on publicly and stated in D3 18.4 and REGISTER_MAP `[3]`/`[7]`.

Either way, an executable check grades it. If the fold needs any processor register-map change, that is the assignment's STOP condition.

**Verification.** `[MAPREC]` grades PP_STAT `[3]`/`[7]`:
- after `saved` (blank 0);
- after `roll-back` and `silent memory` (fail 1, blank 0);

and a planted control that removes the fold is caught.

### F2 MAJOR — Tests, Robustness — `hdl/milan/milan_datapath.sv:5567`, `:5409`, `:5456`, `:5415`, `:5422`, `:5333` — six restore arms have no executable evidence: every planted probe survives

**Authority.**
- Acceptance 1: "a torn or corrupt record keeps the default".
- The assignment: "Every new check needs a planted mutant".
- AGENTS.md section 5: test negative, boundary and failure paths.

**Evidence.** `scripts/maprec_probes.py` plants one defect each in a copy of the datapath. Each mutant builds through the leg's own recipe and passes the full leg at 331 checks, 0 failures (`receipts/probe-round1-summary.txt`, `receipts/probe-*.tail.txt`). The clean control passes.

| Probe | Arm (head line) | Survived |
|---|---|---|
| `no_putback` | a framed, CRC-clean record the ADD rule refuses: the port is left EMPTY instead of getting its reset set back (`:5567`) | yes |
| `no_hole_rule` | a mapping after an UNUSED entry is accepted (`:5409`) | yes |
| `no_layout_id` | layout_version and record_id are not judged (`:5456`) | yes |
| `no_range_refuse` | an entry outside every ADD range is dropped silently, so the rest applies (`:5415`) | yes |
| `no_dup_cluster` | one input cluster, two mappings: the later one wins (`:5422`) | yes |
| `restore_on_pass0_defaults` | a D3 pass-0 abort (DEFAULTS, `restore_rb` 0, cause not 0) still restores the maps (`:5333`) | yes |

The put-back is reachable in the field. A format record and a map record have different writers, each with its own 500 ms window. A power cut between a narrowing SET_STREAM_FORMAT's record and the map edit's record, or a map record given up with the alarm, leaves a saved set that the restored format refuses. Only the CRC-corruption arm of "corrupt" has a control.

**Impact.** A defect in any of these arms ships unseen. For the put-back that means a port with no map after a power cycle (Milan 5.3.10.1). For the others, it means a malformed or foreign record is partly applied.

**Required outcome.** Each arm above has a check that fails for its defect, with a planted control caught. The case set must include at least:
- a CRC-clean set the ADD rule refuses, which proves the reset set comes back;
- a CRC-clean malformed record (hole, range, duplicate, wrong id or layout);
- a pass-0 DEFAULTS terminal.

**Verification.** `scripts/maprec_probes.py` rerun at the fix head: all six caught, and the clean leg still passes.

### F3 MAJOR — RTL, Docs — `hdl/milan/milan_datapath.sv:9106` — the protected `docs-check` context fails at this exact head: a literal-bound port without its rationale

**Authority.** CONTRIBUTING.md: `docs-check` is one of the seven required contexts. The docs workflow runs `scripts/check_port_contracts.py` (`.github/workflows/docs.yml:361`).

**Evidence.**
- At this head, hosted job 118063268343 (docs-gates-0) failed at step 38 with "UNJUSTIFIED CONNECTION: hdl/milan/milan_datapath.sv:pp_shadow.mrec_offset_i is open or literal-bound with no rationale comment" (`receipts/hosted-docs-gates-0.log`).
- I reproduced it locally: rc 1 (`receipts/gate-check_port_contracts.log`).
- Its fail-fast then cancelled every exact-head Verilator and Yosys shard and skipped docs-gates-0 steps 39 to 55 (`receipts/hosted-check-runs.tsv`, `receipts/hosted-docs-gates-0-steps.txt`).
- The author's evidence lists "the docs gates ... all rc 0", but no receipt for this gate exists in the published tree.

**Impact.** The head cannot satisfy the merge ruleset. No exact-head `verilator-suites` or `yosys-portability` evidence exists.

**Required outcome.** `check_port_contracts.py` and `--selftest` both return rc 0 at the fix head, with the port's binding justified in place as the gate requires.

**Verification.** Local rc 0 for both, and the hosted docs-gates-0 step passes at the new head.

### F4 MAJOR — Tests, Docs — `tb/verilator/milan_dp/sim_nxn.cpp:4814`, `:4815`, `:4864`, `:5240` — two more required docs-workflow gates fail at this head (never reached hosted, because of F3's fail-fast)

**Authority.** `.github/workflows/docs.yml` steps "C and C++ idiom gate" and "Test-evidence ratchet" (docs-gates-0, under `docs-check`).

**Evidence** (`receipts/skipped-docs-gates-local.log`).
- `scripts/check_cpp_idiom.py` returns rc 1: "multi-declarator declaration 2 > ratchet 0" and "long function 1 > ratchet 0". The sites are all new code: `sim_nxn.cpp:4814` and `:4815` (`uint32_t want_r[8] = {...}`, `want_k`), and `:4864` (`dynmap_map_records_section`, 448 lines).
- `scripts/measure_test_evidence.py --check` returns rc 1: "4 wall-clock-dependent suite file(s) > ratchet 3". `sim_nxn.cpp` is newly classified: the gate's C clock pattern matches `alarm (` in the new check name at `:5240`. At base `e9cbb676` the same detector finds no match in the file.
- The other skipped steps I could run pass locally: fail-fast, TODO ownership, hygiene, SV/Python/shell idiom, doc paths and archive.

**Impact.** `docs-check` fails again once F3 is fixed.

**Required outcome.** Both gates return rc 0 at the fix head without loosening their ratchets.

**Verification.** Local rc 0, then the hosted docs-gates-0 job completes.

### F5 MINOR — Conformance, Docs — `hdl/milan/milan_datapath.sv:4913`, `:4399-4405`; `docs/design/SAVED_STATE_MATERIALIZATION.md:2860` — the multi-port ordering limitation is stated only in the PR body

**Evidence.**
- The restore walks ports in order (`amr_fsm` `AS_RNEXT`).
- An output ADD is accepted only where the key's owner is free or is the same port (`:4399-4405`).
- Every later port still holds its reset identity at that point. So on a shape with several dynamic output ports, a valid saved set that claims another port's stream keys is refused. I confirmed this by reading the code; the PR body's "Known limitations" says so too.
- The authoritative page says only "the 8x8 obligations above remain open" (`:2860`), and the RTL comment (`:4913`) is silent.

**Impact.** A saved multi-port configuration is silently not restored (Milan 5.3.10.1), and a cold reader of the contract cannot know it.

**Required outcome.** The limitation is stated in D3 18.4 and the restore's RTL comment, with a public ruling that accepts it for non-shipping shapes (and a tracking issue), or it is fixed.

**Verification.** A docs read. If it is fixed instead, a multi-port check.

### F6 MINOR — Docs — `docs/reference/REGISTER_MAP.md:2391` — PP_STAT `[4]` `nvm_alarm` still names only the binding manager and the D3 writer

**Evidence.**
- `KL_pp_shadow.sv:1180` ORs the map writer's alarm into `nvm_alarm_o`.
- The `[MAPREC] failing writes` check grades PP_STAT `[4]` raised by it.
- The row's `[11]` was updated, but `[4]` was not.

**Impact.** The register contract misattributes the alarm's sources.

**Required outcome.** `[4]` names the parent map writer (#637).

**Verification.** A docs read, and the doc gates rc 0.

### Residue (wording only; manager carries to the residue checklist)

- **R1** — `hdl/milan/milan_datapath.sv:4931`: "(scripts/check_nvm_record_space.py, check 13)" should read "check 15". The gate's own docstring numbers it 15.
- **R2** — `hdl/milan/KL_pp_shadow.sv:966`: "(D3 18.3, lane 3)" puts a lane name in a source comment, which is a new instance under the 2026-10-15 rule. Fix: "(D3 18.3)".
- **R3** — `tb/verilator/milan_dp/sim_nxn.cpp:5183`: "as the parent has not adopted the name stage (lane 3)" is a new lane name in a source comment. Fix: drop "(lane 3)".

### Suggestions

- **S1** — `milan_datapath.sv` `AS_WREQ`: an ungranted 1,000 ms request wait counts as a failed attempt, while D3 6.3 counts an attempt from the grant. This is harmless against the backend's 50 ms capture hold, but worth stating in 18.4.
- **S2** — PP_STAT `[1]` `restore_busy` does not cover the map restore, so a host reads done while the maps are still being put back. The faces are held, so this only affects reporting. Consider it with F1.
- **S3** — check 15 holds only the layout literal. The parent's per-port payload-length formula (`amr_rec_shape`) is held to the census only by the 1x1 leg, so a divergence at another shape would read every record as unframed. Consider holding the formula in `check_nvm_record_space.py`.

## Clean results within each lens (evidence for the parts that passed)

- **Conformance.**
  - Acceptance 1's roll-back: the clean leg has executed cases for D3 roll-back, parent roll-back, slow memory and silent memory.
  - Acceptance 2: the processor's `07_memory_maps.md:461` at `2cbed0a9` reads "The maps are the integrator's to persist ... the processor writes and restores no map record".
  - Acceptance 3 and #763: EMPTY both ways, saved, and torn cases at 331/0 in `receipts/dynmap-clean-run.log`.
  - Acceptance 4: `check_nvm_capture.py` rc 0 and `check_nvm_record_space.py` rc 0, self-test rc 0 with `parent_layout` caught.
  - Record framing (`amr_frame_byte`, crc16 step) matches the codec's bytes (the leg compares against `gen_nvm_window.py`).
  - DR2a/DR2b/DR2c and the DR3a deadlines match D3 6.1 and 6.3 by reading `amr_fsm`.
- **RTL.**
  - One clock domain: `pp_shadow` is on `axis_clk`/`axis_resetn` (`milan_datapath.sv:9030-9031`), so no CDC is added.
  - The arbiter's grant and drain timing hold against `KL_nvm_backend.sv:857` and `:901` (registered grant, busy from the next clock). An abort's cycle is always covered by busy or gnt.
  - Counter widths fit: `amr_bi_r` is 11 bits for at most 1,032 bytes, and the deadlines are 11 bits, guarded at 2,000 ms.
  - `lint_rtl.py --check` passes at its ratchet, 90 of 90 (`receipts/lint_rtl-check.log`).
  - DR4 area: hdl/ is unchanged since the measured `90b15366` (`git diff --stat 90b15366..HEAD -- hdl/` is empty).
- **Robustness.**
  - Silent, slow and erroring memory, an abandoned read drained, and contention on the shared device face are all executed in the clean leg.
  - The holds measured 553 to 635 clocks on healthy restores, against the 4,096-clock watchdog (`receipts/dynmap-clean-run.log`).
- **Tests.**
  - The clean dynmap leg and pp_shadow reproduce the author's tallies (`receipts/dynmap-clean-run.log`, `receipts/pp_shadow-suite.log`, rc 0).
  - The author's 37-mutant campaign was not rerun (see limits).
- **Docs.** Ownership is stated consistently in D3 18.4, FASTCONNECT, SNAPSHOT_OWNERSHIP, REGISTER_MAP `[11]` and PP_NVM_STAT `[4]`, the compliance matrix ("partial", cold cycle open), TESTING and the suite READMEs.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F5) | issue acceptance and #763 additions; D3 3, 5.2, 6.1-6.3, 8.1, 18.4; FASTCONNECT 9.3; processor 07 5.1 at `2cbed0a9`; `amr_*` blocks; `dynmap-clean-run.log`; `dynmap-instrumented-ppstat-run.log` | R669-1 | `63a187e1579474bca562d85304b9a91466877c33` |
| RTL | UNCLEAN (F1, F3) | `milan_datapath.sv` `amr_*`, edit-face mux, holds, enable gate; `KL_pp_shadow.sv` arbiter, pend, alarm; `KL_nvm_backend.sv` grant/drain timing; lint; `check_port_contracts.py` | R669-1 | `63a187e1579474bca562d85304b9a91466877c33` |
| Robustness | UNCLEAN (F2) | restore validation arms, roll-back, deadlines, drain, contention; six planted probes | R669-1 | `63a187e1579474bca562d85304b9a91466877c33` |
| Tests | UNCLEAN (F1, F2, F4) | `sim_nxn.cpp` `[MAPREC]`, `dynmap_mutants.py`, `pp_shadow/sim_main.cpp`; clean leg 331/0; pp_shadow 610/610/650/317; probe survivors; cpp-idiom and test-evidence gates | R669-1 | `63a187e1579474bca562d85304b9a91466877c33` |
| Docs | UNCLEAN (F1, F3, F4, F5, F6) | the 9 changed docs pages, both READMEs, `check_nvm_record_space.py` docstring, PR body, REVIEW READY evidence list | R669-1 | `63a187e1579474bca562d85304b9a91466877c33` |

## Real limits

- **Hosted evidence at this head.** Only docs-gates-0 failed for a real reason (F3). The Verilator and Yosys shards, `rtl-fast` and the aggregates were cancelled by fail-fast, and the aggregates' "failure" conclusions follow from that. No exact-head long-gate result exists. The manager owns hosted and act acceptance.
- **Not rerun here:** the full suite sweep, Yosys, route-1x1, ooc-1x1 and ooc-8x8, and the author's 37-mutant campaign. All are taken as author receipts only; they were out of this round's allowed scope or wall-time. No manager source bank ran at this head, and none is inferred.
- **Not exercised:** the gen_toc anchor and contents gates could not run, because the pinned Markdown renderer is not installed and shared installs are not allowed. The author's `gen_toc_check.log` reports rc 0.
- **Not proven by anything here:** the board cold cycle (#763) is NOT RUN. Physical calibration is NOT RUN, and skips are not hardware proof. The DDR latency added to the measured hold is unmeasured. The 8x8 has no executable map-record evidence.
- **Tool identity:** the pinned simulator was verified as 5.050 (`sha256 905795b9...e92f`). Every build used it; the host default is 5.052 and was not used.
- **Clone state:** after the probes, the review clone was verified at `63a187e1` with the index tree equal to `45c859e1`, the worktree and index clean, and the five submodule gitlinks at their recorded commits. A `scripts/__pycache__` that my runs created was removed. All builds and probes ran in disposable copies under `scratch/`.

## Pending manager duties

- Hosted and act acceptance at the fix head, once F3 and F4 let docs-gates-0 complete and the long gates run.
- The current-dev merge-candidate builder and native banks at the merge turn (source base `e9cbb676`, live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`).
- Carry R1 to R3 to the residue checklist.
- Route F1's design question, and F5's scope ruling for multi-port shapes, to the maintainer if the author proposes a deviation rather than a fix.
- The board cold cycle (#763) stays owed on #637. The PR correctly says "Relates to".

R669-1 FINISHED
