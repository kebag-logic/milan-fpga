[R398] NEGATIVE - exact head 99bfd4bc3180bab97d47f63056513fb39eea6a37

# R398-3: internal composition review of processor PR #133 (lane C1) after the merge of PR #132

Head `99bfd4bc3180bab97d47f63056513fb39eea6a37`, tree `d8ec1053bf0968ed462d8a419a0cf859c41e9c3c`. It merges processor `main` `d352bbaa` (PR #132, D3 lane 1) into the round-2 head `412efeb7`; the merge base is `c951a9ff`.

## Verdict

**NEGATIVE, on one MINOR (F1, Docs).**

- **The composed RTL is sound.**
  - The merge is mechanical: `git merge-tree` of the two parents rebuilds the published tree exactly.
  - Every lane-only file equals its lane head.
  - Each lane's zero-context patch to the three shared files is identical before and after the merge.
  - The two lanes share no timer-arm face, PRNG client, TX client, SRP net, port or parameter.
- **Every suite and entry point I ran passes on the merge head.** The list: all 33 suites, `run_suites.sh`, lint, `make check`, the module matrix, `nvm_port` figures and `git diff --check`. The mutation campaigns: `srp_top` 78/78 killed (65/65 coverage), D3 83/83 killed with every golden passing, GSI 20/20, admission 12/12, name-write, and retry (62 killed).
- **What stays open.** The composed-head parent-visible list is incomplete for one parent file, `tb/verilator/milan_dp/README.md`. Both lanes' adoption edits meet there, but the PR body says they share no parent file. That is F1.

## 1. How this review was reconstructed

1. **Governance.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` and no submodules (0 gitlinks). I read `README.md`, `docs/README.md` (single-source rules: timing in F08.1, parameters in F01.5), the `Makefile` gates and `scripts/run_suites.sh`.
2. **Issue #108.** I read the body and all comments, including:
   - assignment 5883702094 (items 1-4 and gates);
   - round 2, 5886235840.
3. **Scope.**
   - PR #133: the body, including the "Composed head `99bfd4bc`" note.
   - The manager comments, including evidence comment 5890073527 (combined 16/16 at dev `79c36963`, donor 9/9).
   - The PR #132 body, including "Parent-visible for pin adoption: rounds 1-6, consolidated".
4. **Published evidence.** `kebag-logic/milan-fpga@a6427910:review-evidence/ppC1-r1`: `MANIFEST.json`, `author/HANDOFF.md` (the #65 design and STOP evaluation) and `author/PR-BODY.md`. These are round-1 author records. The executable evidence for this head is the manager's comment and my own runs.
5. **Authorities.**
   - 802.1Q-2014 Table 10-5 rLA!, 10.6, 10.7.4.3, 10.7.5.20 and 10.7.5.22, as quoted in the issue, the PR and docs 10 §6.5.
   - Milan v1.2 Table 4.3, 4.2.7.3, 4.3.2 and 4.4.1.
   - The parent consumer files at dev `79c36963`, read through the public API.
6. **The diff.** `git diff c951a9ff..99bfd4bc`, per lane (`c951..412efeb7` and `c951..d352bbaa`), and history.
7. **Order of reading.** Prior public review findings were read only after my own verdict and ledger draft were written. `receipts/independent_verdict_draft.md`, mtime 15:46:54, predates the extraction of the prior findings at 15:46:59.

## 2. Composition judgement

### 2.1 The merge is mechanical

Receipts: `receipts/composition/structure.txt` and `structure2.txt`.

- `git merge-tree --write-tree 412efeb7 d352bbaa` gives `d8ec1053`, which is the published tree.
- Changed paths since `c951a9ff`: 92. Each of the 89 lane-only paths equals its lane head (0 mismatches). C1-only paths are `hdl/srp`, the `tb/srp_*` suites, docs 10 and docs/10. #132-only paths are the AECP, NVM, validator, `pp_top`, `acmp_nvm` and `dyn_state` files and their docs.
- Three paths are shared: `docs/architecture/08_timing.md`, `docs/guides/integrator.md` and `hdl/top/protocol_processor_top.sv`. For each lane, the zero-context patch-id on these three files is identical before and after the merge:
  - #132's half: `705a91ed…`;
  - C1's half: `3fc415cc…`.

### 2.2 The top-level wiring: no interference

Receipts: `receipts/composition/shared_services_identity.txt` and `structure.txt`.

- **C1 at the top is one comment:** the `srp_active_o` description, head `hdl/top/protocol_processor_top.sv:515-518`. Its wiring is internal to `KL_srp_top`: `KL_srp_encoder.tx_mvrp_o` feeds `KL_srp_vlan`, which feeds the talker FSM `vid_ok_w` (`KL_srp_talker_fsm.sv:804-824`). The LeaveAll re-arm and stale guard are `KL_srp_top.sv:1030-1033` and `:1203`, `:1233-1241`.
- **Byte-identical in `c951a9ff`, `412efeb7`, `d352bbaa` and `99bfd4bc`** (hashed block by block):
  - the timer arm-port priority mux (`:2750`, `ARM_N_C = 8`, the same eight faces and order, the counted newest-drop at `:2842`);
  - the PRNG draw-port owner mux;
  - the `KL_pp_timer_service`, `KL_pp_tx_arbiter` and `KL_pp_tx_slots` instances;
  - the `KL_srp_top` instance (ports and parameters);
  - `KL_mrp_strip`.
- **#132 adds no arm, draw or TX client.** None of its top hunks names an arm, timer, TX or SRP net. `KL_aecp_nvm_writer` counts its deadlines in its own counters (F08.1 rows `08_timing.md:43-46`; `:166` "take no timer-service slot").
- **#132's top hooks are disjoint from the SRP path:**
  - the AECP hold admission (`:2666`) acts on 1722 AECP subtype frames at the validator slot gate, never on the MRP emission path;
  - the ADP enable gate `entity_enable_i && restore_done_o` is at `:1704`;
  - `rs_agg_i` (`:2567`) and `d3_go_i` (`:3622`) are the other two hooks.
- **Ports and parameters.** The composed top's `input`/`output`/`parameter` declaration lines equal `d352bbaa`'s exactly. `hdl/srp` equals `412efeb7`'s.
- **Effect on the arm path.** The SRP arm face's latency and overrun exposure are those reviewed at `412efeb7`. P8 still shows 0 own LeaveAlls at arm delays 3, 4, 8 and 16 (`receipts/suites/srp_top.log:372-375`).

### 2.3 The two shared documents

- **`08_timing.md`.**
  - C1 rewrites one F08.1 row, `T-MRP-LEAVEALL` (`:41`): three starts, rLA! linked to 10 §6.5.
  - #132 rewrites `T-NVM-DEBOUNCE` and `-RS-DEADLINE`, adds `-RS-AGGREGATE` and `-RETRY-BACKOFF` (`:43-46`), adds the saved-state section, and adds the slot-budget note (`:166`).
  - The rows are distinct, and both lanes state "not a timer-service slot" or no new slot. No statement contradicts the other lane.
- **`integrator.md`.** C1 changes only the `srp_active_o` row (`:344`, linking 10 §6.2). #132's rows cover restore, enable, AECP hold and NVM, and none mentions SRP.
- **Gates.** `make check` rc 0 (links 976, matrices, parameters 26/26/26) and `gen_matrix --check` rc 0.

### 2.4 Suites and entry points on the merge head

Tool: Verilator 5.050 (`2026-07-01 rev v5.050`). The supplied tool path did not exist, so I made a scratch wrapper around an existing 5.050 install; see Real limits.

| Command | rc | Result (receipt) |
|---|---:|---|
| every `tb/*/` suite, `make`, at most 8 parallel | 0 | 33 suites, 1,016,272 checks, 0 failing (`receipts/suites/SUMMARY.txt`): `srp_top` 2200, `srp_encoder` 581, `srp_stream_fsms` 1219, `pp_top` 7888 (D3 section included), `acmp_nvm` 360, `rx_validator` 437, `dyn_state` 118 |
| `./scripts/run_suites.sh` (serial entry point) | 0 | "suites: 1016272 checks total, 0 failing" (`receipts/entry/run_suites.log`) |
| count arithmetic | n/a | 1,016,272 = C1's 1,016,051 + #132's 1,016,036 − base 1,015,815 (the base derived from C1's per-suite deltas: +213, +4, +19) |
| `./scripts/lint_hdl.sh` | 0 | `receipts/entry/lint_hdl.log` |
| `make check` | 0 | `receipts/entry/make_check.log` |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `git diff --check c951a9ff..99bfd4bc` | 0 | empty |
| `make -C tb/nvm_port figures` | 0 | `receipts/entry/nvm_port_figures.log` |
| `tb/srp_top/mutants.py` (the `make mutants` driver, unmodified, sharded 24 ways by `--only`) | 0 | 71/71 per-shard controls PASS; 78/78 arms KILLED by their named assertions; the union of kill tags covers 65/65 of the driver's K-R set (`receipts/srp_top_mutants/MERGE.txt`) |
| `tb/pp_top/d3_mutants.py --jobs 8` (four `--only` batches) | 0 each | 83/83 KILLED; 6 goldens PASS (`receipts/d3_mutants/MERGE.txt`) |
| `tb/pp_top/gsi_mutants.py` | 124 (my 590 s cap) | golden and 15 variants passed. The remaining 5 variants and a golden, run with the driver's own table and verdict in private trees (`scripts/gsi_subset.py`), were all DETECTED or PASS: 20/20 |
| `tb/srp_admission/mutants.py` | 124 (cap) | 11 of 12 cells PASS. The last cell (`discarded-round-strobes srp-top`), run with the driver's own tables and judge (`scripts/admission_one.py`), PASS: 12/12 |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence controls, 1 performance control |
| scoped `sv2v` + `yosys` elaboration of the three C1-changed modules | 0 | `KL_srp_encoder`, `KL_srp_vlan` and `KL_srp_talker_fsm` OK (`receipts/entry/yosys_scoped.log`) |

**Stated counts.** In `tb/srp_top/README.md`, the per-arm failure counts agree with my run once the README's re-measurement paragraph (`:376-413`) is applied. The first tables still carry the superseded counts (R399-2 S3, retained).

### 2.5 The parent-visible lists, read together

- C1's cited parent locations hold at dev `79c36963` (`receipts/parent/milan_dp_79c36963_extract.txt`):
  - `sim_crf_licence.cpp:953,956` are the `>= 4` checks (blob `6f9d17b1`);
  - `milan_dp/README.md:443` and `:527-530` are unchanged (blob `3f05559f`).
- The combined edit set of #132's list and C1's crflic edit is the manager's 14-entry bank (comment 5890073527).
- The composed-head note scopes C1's section-4 claims to `412efeb7` against `c951a9ff`, which is correct against the RTL.
- It also says "The two lists touch no common parent file". That is true of the lists' text, but not of the adoption edits they imply: see F1.

## 3. Findings

### F1 - MINOR - Docs - the combined pin-adoption list leaves `milan_dp/README.md` half-updated, and calls the two lists disjoint

- **Where.**
  - PR #133 body, "Composed head `99bfd4bc` (manager note, R399-3 F1)", item 1: "The pin-adoption edits are PR #132's consolidated list … plus section 4 above … The two lists touch no common parent file."
  - Parent dev `79c36963`, `tb/verilator/milan_dp/README.md` (blob `3f05559f`):
    - `:877-883`: "The `[AECP]` checks in `sim_nxn.cpp` grade that path: an answer arrives, it is an `AEM_RESPONSE`, its status is `BAD_ARGUMENTS` …", the no-descriptor-memory degrade arm.
    - `:633-637`: "Every harness that binds a sink starts the restore walk … `sim_main`, `sim_nxn`, `sim_aclk` and `milan_dp_render` now set it at boot."
  - `sim_nxn.cpp` at `79c36963` still carries that arm, `prove_read_descriptor_degrades_with_no_descriptor_memory` (`:2359`). Receipt: `receipts/parent/milan_dp_79c36963_extract.txt`.
- **Authority.**
  - #108 assignment 5883702094 item 4: the parent-visible list for the pin-adoption lane, in the PR body.
  - This round's brief: the PR body's list "must now read together with #132's consolidated list".
  - #132's consolidated list:
    - retires the `[AECP]` degrade arm "in every `sim_nxn.cpp` leg", replacing it with two hold checks;
    - adds the `PP_CTRL[1]` walk to `gmstep`, `gptp`/`gptp-lat` and `ax1x1gptp`;
    - ends the image-less legs on CLOSED.
  - That list names no parent document.
  - Precedent: R398-1 F1 (MINOR, accepted) required exactly this class of entry, the same README, for C1's own edits.
- **Impact.**
  - Applying the combined list as written, the adoption lane edits this README only for C1's `[C]` row (`:443`) and issue-108 sentence (`:528-530`).
  - Its `[AECP]` paragraph would then describe a check that no longer exists, and its walk-starter list would miss three harnesses.
  - No consumer gate reads this prose: `docs_check.py` passed in the manager's 16/16 bank.
  - The note's "no common parent file" tells the adoption lane the two lanes' parent edits cannot meet. Their documentation edits do meet, in this one file.
  - Two limits on scope: this is documentation only, no code or gate is affected, and the missing entry originates in #132's merged list. The README's older sentence "This suite backs no descriptor memory" (`:869`) is already inaccurate at `79c36963` (`sim_nxn.cpp:285` answers descriptor memory). It is not attributed to either lane.
- **Required outcome.** A PR-body amendment, with no source change. The composed-head note either:
  - names the `milan_dp/README.md` edits implied by #132's harness edits (`:633-637` walk starters, `:877-883` the retired `[AECP]` degrade arm, now the two hold checks), to be made in the same edit of that file as C1's `:443` and `:528-530`, and replaces "touch no common parent file" with an accurate statement (the lists' code edits share no file; their README updates meet in `milan_dp/README.md`); or
  - records a public manager ruling that assigns these README updates to the pin-adoption lane (parent evidence owner milan-fpga #76), with the same correction of the sentence.
- **Verification.** Re-read the PR body at the same head. The combined list covers both lanes' `milan_dp/README.md` updates (or points to the ruling), and no sentence says the two lanes' adoption edits share no parent file. No rerun is needed: no source changes.

No other MINOR, MAJOR or BLOCKER finding.

## 4. Prior public review findings at this head

| Finding | State at `99bfd4bc` | Evidence |
|---|---|---|
| R398-1 F1 (MINOR, Docs): the list omits `milan_dp/README.md` | RESOLVED | body section 4 names `:443` and `:528-530`; blob `3f05559f` unchanged at `79c36963` (`receipts/parent/…extract.txt`) |
| R398-1 S1 = R399-1 S2 (VLAN overflow holds the licence closed; the licence bound) | RESOLVED | docs 10 §6.2 `:262-270` and the PR body; docs 10 byte-identical to `412efeb7` |
| R398-1 S2 (three narrow guards unexercised) | RESOLVED | `r-rearm-no-inflight` (M10, P6), `r-rearm-no-deadline` (M10, P8) and `r-flag-ignores-edge-peer` (P7) KILLED here (`receipts/srp_top_mutants/`) |
| R398-1 S3 (integrator ordering assumption) | RESOLVED | docs 10 §6.2 `:278`; `integrator.md:344` links §6.2 |
| R399-1 S1 (latency-dependent guard) | RESOLVED | `KL_srp_top.sv:1030-1033`; `rearm-at-issue` KILLED by P8; ARMDELAY 0/0 at delays 3, 4, 8 and 16 |
| R399-1 S3 (per-type aging caveat) | RESOLVED | docs 10 §6.5 `:649-652` |
| R398-2 S1 = R399-2 S1 (a dropped LeaveAll re-arm silences that application's own LeaveAll) | RETAINED, SUGGESTION | source unchanged; exposure unchanged by the merge (the arm mux is byte-identical, and #132 adds no arm face) |
| R398-2 S2 = R399-2 S2 (no committed `now_ms` wrap check) | RETAINED, SUGGESTION | `tb/srp_top` unchanged since `412efeb7` |
| R399-2 S3 (superseded counts in the `tb/srp_top/README.md` tables) | RETAINED, SUGGESTION | confirmed by my run (§2.4) |
| R399-3 F1 (MINOR, Docs): the list did not read with #132's | RESOLVED as required (items 1-3 of the composed-head note) | the note's items 1-3 against the RTL (§2.5). Its added "no common parent file" sentence is the subject of the new F1 above |
| R399-3 S1 (SUGGESTION, Tests): no in-tree full-top check of C1 under #132's hold | RETAINED, SUGGESTION | `pp_top` has no SRP LeaveAll check under the hold. Non-interference here rests on the structural identity in §2.2 and on P8's arm-latency sweep |
| R399-4 S2 (SUGGESTION, Docs): same substance as F1 | SUPERSEDED by R398-3 F1 at MINOR | I rate it MINOR: this PR's body now defines the combined adoption edits and states they share no parent file, and R398-1 F1 set MINOR for the same class of omission from the same file |

## 5. Lens results

- **Conformance: CLEAN.**
  - Table 10-5 rLA! "Start leavealltimer, Passive" is unchanged at the merge. It applies per application with the 10.7.5.20 scoping (`KL_srp_top.sv:1030-1033`, `:1203`, `:1233-1241`), with the 10.7.5.22 stale-expiry guard.
  - Milan Table 4.3 timers are graded by Q1-Q4, and the 4.3.2 licence term by R1-R4. All pass here: `srp_top` 2200/2200, and ARMDELAY 0 own LeaveAlls.
  - #132's changes touch none of it (§2.2).
- **RTL: CLEAN.**
  - The merge-tree is recomputed and every lane-only blob matches its lane head.
  - The shared-service blocks are byte-identical across the four revisions, and the port and parameter lines equal `d352bbaa`'s.
  - `lint_hdl` rc 0, and the scoped elaboration of the C1 modules is OK.
- **Robustness: CLEAN.**
  - #132 adds no arm, draw or TX client, and its hold admission acts only on AECP subtype frames at the slot gate.
  - The SRP arm path's latency and overrun exposure are unchanged, and P8 covers arm latency up to 16 clocks.
  - The retained dropped-re-arm SUGGESTION is unchanged in exposure.
- **Tests: CLEAN (SUGGESTIONs only).**
  - All 33 suites and `run_suites.sh` pass.
  - The campaigns: `srp_top` 78/78 (65/65), D3 83/83 (goldens PASS), GSI 20/20, admission 12/12, name-write and retry.
  - Stated counts reconcile with my run, and the count arithmetic composes exactly.
  - R399-3 S1 is retained.
- **Docs: UNCLEAN (F1).**
  - `08_timing.md` and `integrator.md` state both lanes' contracts without contradiction, and `make check` and `gen_matrix` are rc 0.
  - The composed-head parent-visible list is incomplete for `milan_dp/README.md` and calls the lists disjoint.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv:1030-1033,1203,1233-1241`; `KL_srp_talker_fsm.sv:804-824`; docs 10 §6.2 and §6.5; `srp_top` P1-P8, Q1-Q4 and R1-R4 at the head (2200/2200, ARMDELAY lines); issue #108 authorities | R398-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| RTL | CLEAN | merge-tree recomputation; per-path lane provenance; zero-context patch-ids; `protocol_processor_top.sv` #132 hunks against the arm mux, PRNG mux, timer, TX arbiter, TX slots, SRP and MRP-strip blocks (hashed in four revisions); port and parameter lines; `lint_hdl`; scoped `yosys` | R398-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Robustness | CLEAN | arm-queue face set and drop path (`:2750-2842`); `KL_aecp_nvm_writer` (no arm, draw or TX ports); validator hold gate; P8 arm-delay sweep; retained dropped-re-arm exposure | R398-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Tests | CLEAN (SUGGESTIONs only) | 33 suites (parallel and `run_suites.sh`); `srp_top` mutants 78/78, 65/65; `d3_mutants.py` 83/83; GSI, admission, name-write and retry drivers; `nvm_port` figures; README counts against the run; hosted jobs at the head | R398-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Docs | UNCLEAN (F1) | `08_timing.md:41,43-46,166`; `integrator.md:344`; docs 10 §6.2 and §6.5; `make check`; `gen_matrix --check`; PR #133 body (section 4, Round 2, composed-head note); PR #132 consolidated list; parent `milan_dp/README.md`, `sim_nxn.cpp` and `sim_crf_licence.cpp` at `79c36963` | R398-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |

## 7. Hosted checks at the exact head (read-only; the manager owns acceptance)

Workflow `hdl` ran twice at `99bfd4bc`: run 36558392722 (pull_request) and run 36558385720 (push). Every job succeeded: `suites`, `docs-gates` and `portability`. Across 44 steps, 42 executed and succeeded. The 2 skipped steps are "Build Verilator v5.050", skipped on a cache hit. Receipts: `receipts/hosted_check_runs.txt` and `receipts/hosted_steps.txt`.

## 8. Real limits

- **Verilator path.** The supplied scoped Verilator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) did not exist. I used a scratch wrapper around an existing Verilator 5.050 install: `Verilator 5.050 2026-07-01 rev v5.050`, `verilator_bin` sha256 `44898b22…`, the same install other manager directories' wrappers point to. The host's default `verilator` is 5.052 and was not used.
- **Campaigns run in pieces.** Every piece used the checked-in driver unmodified, or its own tables and verdict functions:
  - `make -C tb/srp_top mutants` was run as 24 `--only` shards. The driver checks coverage only on an unfiltered run, so I recomputed the 65-assertion union from the shard outputs.
  - `d3_mutants.py` ran as four `--only` batches.
  - GSI and admission hit my 590 s cap and were completed cell by cell (`scripts/gsi_subset.py`, `scripts/admission_one.py`).
- **How long runs were handled.** One D3 batch pair outran a single 10-minute tool call and was moved to the background by the session. I polled it in the foreground until it exited (rc 0) and started nothing else meanwhile, so no more than 8 jobs ran at once.
- **Not run (not allowed):** the full Yosys bank (only the three C1 modules were elaborated), the parent consumer bank, the donor bank, act, and hardware. The parent 16/16 at `79c36963` with the combined edits, and the donor 9/9, are the manager's attested evidence (comment 5890073527). I did not reproduce them.
- **Parent reads only.** Parent files were read at `79c36963` through the public API; I did not build any parent.
- **No top-level SRP probe.** I wrote no full-top LeaveAll probe under the D3 hold. Non-interference rests on the structural identity (§2.2) and on the `srp_top` P8 arm-latency sweep.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - The review clone is byte-identical to the head: HEAD, tree and index tree `d8ec1053`, 0 rehash and 0 mode mismatches, 0 gitlinks (none required).
  - One ignored `tb/pp_top/__pycache__/`, written when this review loaded the D3 table, was removed.
  - All builds ran in a disposable clone under `scratch/`.

## 9. Pending manager duties

1. **F1.** Amend the PR #133 composed-head note, or record the routing ruling. Then a delta check of the body at the same head.
2. **Merge-turn candidate.** Build the final current-dev candidate (source base `c951a9ff`, live dev `79c36963`); it is distinct from this source validation. The manager owns hosted and act acceptance.
3. **At pin adoption:**
   - the combined parent edits: #132's harness and cosim edits, #132's firmware boot-path obligation, and C1's crflic `>= 3` at `sim_crf_licence.cpp:953,956`;
   - the parent documents of both lists, including one edit of `milan_dp/README.md` at `:443`, `:528-530`, `:633-637` and `:877-883`.
4. **Route the retained SUGGESTIONs:** R398-2 S1 = R399-2 S1, R398-2 S2 = R399-2 S2, R399-2 S3 and R399-3 S1.

## 10. Packet

- `REPORT.md`.
- `MANIFEST.sha256`, which lists every published receipt.
- `scripts/`: `run_suites_parallel.sh`, `srp_top_mutants_sharded.py`, `d3_merge.py`, `gsi_subset.py`, `admission_one.py`.
- `receipts/`:
  - `suites/`, `entry/`, `srp_top_mutants/`, `d3_mutants/`, `other_mutants/`;
  - `composition/`, `parent/`;
  - `hosted_*`, `clone_integrity.txt`, `independent_verdict_draft.md`.

R398-3 FINISHED
