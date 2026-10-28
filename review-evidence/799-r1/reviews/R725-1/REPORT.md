[R725] NEGATIVE - exact head ca39dc1b0bd917e3e033df9d9db762514318377a

# R725-1: internal cleared-context review of PR #802 (issues #799 and #790)

- Head: `ca39dc1b0bd917e3e033df9d9db762514318377a`, tree `f48964b216a6d0eed1b025266a42fa88aab999b0`. Base: dev `97aab1d0`.
- Gitlinks at the head: protocol-processor `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`, gptp-processor `55680bff3b287b9a7b0c759f51471fa617c17335`.
- Reconstructed from public state only:
  - AGENTS.md and CONTRIBUTING.md;
  - the #799 issue body and its assignment, STOP, ruling 6460917634, TAKEN and REVIEW READY comments;
  - the #790 body, its assignment, its STOP and the manager comment closing it with the pin adoption;
  - the PR body;
  - `git diff 97aab1d0..ca39dc1b`;
  - the processor range `ed211803..f65c8ff7`;
  - the author's published receipts under `review-evidence/799-r1` at `0829b8ae`.
- No manager source bank was run or inferred at this head.
- Verdict: **NEGATIVE**, because of one open MINOR finding under `Docs`. The other four lenses are clean.

## Findings

### F1 - MINOR - Docs - `docs/design/MAILBOX_SPLIT.md:990-992` and `:1102` - the census counts on the design page are stale after this PR's census change

- **Authority/evidence:**
  - The page states: "At this head every shape has the same 25 population nets and the same 39 reads, and four nets are unread. Of the 39 reads, 10 are on the wire and map to the block, 14 are CSR status, and 15 are the answer face". Its evidence row at `:1102` repeats "the 39 reads of the 25 class-D nets".
  - The census at the base prints `25 class-D net(s) ... 4 unread; 39 read(s) of 21 class-D net(s)` (`receipts/census_base.log`), so the page was true at `97aab1d0`.
  - At this head the census prints `26 class-D net(s) ... 4 unread; 41 read(s) of 22 class-D net(s)` (`receipts/census.log`).
  - This PR added `src_stream_id_o` to `CLASS_D_PORTS` and two rows (`sw/mailbox/publication_census.py:199`, `:222`):
    - `tx_sid_w`, a field read that reaches the wire;
    - `gsi_osid_w`, an answer-face read.
  - So the true split is 26 nets and 41 reads: 11 on the wire, 14 CSR status, 16 answer face.
  - The PR edited this page (`:816`, `:835`, `:1103` to `:1109`, `:1320`) and updated the adjacent mbx counts, but not these.
  - AGENTS.md section 6, `Docs`: "Changed contracts are reflected in authoritative docs."
- **Impact:**
  - The authoritative page for the split placement misstates the census's own scope at merge.
  - It omits the new wire read that `SRC_SID_LO` now carries.
  - A reader auditing which class-D reads the split firmware must publish undercounts them.
  - This is a figure claim, so it is not RESIDUE.
- **Required outcome:** the counts at `:990-992` and in the `:1102` row match the census output at the merge head (26 nets, 41 reads, 11 / 14 / 16).
- **Verification:** `python3 sw/mailbox/publication_census.py --check` summary line equals the page's figures.
- **Out-of-scope note, not counted:** "116 defects, plants two more" (`:1000`) and "118 plants" (`:1102`) were already stale before this PR. `docs/testing/CI_WORKFLOWS.md:2607` records 120 arms at an earlier head, and this head's self-test runs 120 arms. They can be corrected in the same edit.

### R1 - RESIDUE - Docs - `sw/mailbox/mailbox.yaml:63` - a new issue-comment ID in a source comment

- **Authority/evidence:** the owner rule of 2026-10-15 says source comments never show issue-comment IDs. The added line reads `# Minor 3 (#799, the ruling on its STOP, comment 6460917634; #665 decision`.
- **Impact:** wording only. No generated output carries it (the contract page and the generated SV/C outputs do not contain it).
- **Exact fix:** `# Minor 3 (#799, the ruling on its STOP, comment 6460917634; #665 decision` becomes `# Minor 3 (#799; #665 decision`. The rest of the sentence is unchanged.
- **Not counted:** `sw/litex/milan_soc.py:2656-2657` carries `comment 6088423771`. That is a re-wrap of an existing instance (tracked by #746), not a new one.

### R2 - RESIDUE - Docs - PR #802 body, "Linked Issue / roles" - `Relates to #790` contradicts the PR title and the recorded closure

- **Authority/evidence:**
  - The #799 acceptance says "#790 closes with this PR", and the manager comment on #790 says the same.
  - The PR title says "closes #790". `CHANGELOG.md:70` and `docs/reference/SUBMODULES.md:284` say "This closes #790".
  - The body links `Relates to #790`. Its "Not 'Closes'" paragraph justifies only #799, whose bench re-runs are owed.
- **Impact:** PR wording only. As written, the merge does not close #790, and it would have to be closed by hand.
- **Exact fix:** in the PR body, replace `Relates to #790` with `Closes #790`, and begin the following paragraph with `Not "Closes" for #799:`.

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_sid_move.cpp:863-868` (boot), `tb/verilator/milan_dp/Makefile` `SIDMOVE8_BUILD`

- The sidmove8 leg names talker 1's TCTX uid as 1, which equals the derived uid. Phase `[A]` therefore cannot tell `SID_PP_P = 1` from `0` for that talker.
- Only the `[AFTER]` checks discriminate. My planted `SID_PP_P = 0` (probe B) was caught there (4 failures) and not in `[A]`.
- `sim_nxn.cpp`'s uid 5 case (`:7582-7604`) already covers the pre-move override.
- Optional: name a uid different from the derived one (and from every source's ID), so the pre-move phase grades the override too.

## Reviewer's probes and runs at this head

All runs were in disposable copies of the head under the packet's `scratch/`. The pinned Verilator 5.050 (`rev v5.050`) was used; sv2v v0.0.12 and Yosys 0.66 for the census. The log and rc file of each run are under `receipts/`, and `scripts/plant_probes.sh` plants the three probes.

| Run | Command | Result | Receipt |
|---|---|---|---|
| sidmove (1x1, AAF talker 0 + CRF output) | `make sidmove` | rc 0, 50 checks, 0 failures; conflict to new declaration 1,735 ms | `clean_sidmove_chain.log` |
| sidmove8 (8x8, talkers 0 and 1) | `make sidmove8` | rc 0, 52 checks, 0 failures; 1,816 ms | same |
| Probe A: `gsi_osid_w` back on `pp_src_sid_w` | `make sidmove` | caught: rc 2, `[AFTER]: GET_STREAM_INFO selector 2 is src_stream_id_o` x2 | `mutA_sidmove.log` |
| Probe B: `SID_PP_P (1'b0)` on the datapath's AAF framer | `make sidmove8` | caught: rc 2, `[AFTER] no PDU carries the withdrawn ID...` x2 and `[AFTER]: every one carries src_stream_id_o` x2 | `mutB_sidmove8.log` |
| Probe C: `crft_tx_sid_w = eff_crft_sid_w` in `g_crft_sid_pp` | `make sidmove` | caught: rc 2, the CRF source's `[AFTER]` withdrawn-ID and every-PDU checks | `mutC_sidmove.log` |
| #790 arms | `make notify && python3 gsi_mutants.py 12 13 14` | rc 0: clean leg 499/499; the 3 #790 arms each caught by the named G11 PROBING_PASSIVE check (3, 1, 1 failures) | `gsi790.log` |
| pp_shadow | `make run` | rc 0: base 651, vid73 651, crf 691, pending PASS; 123 `[GSI]` passes, the PROBING_PASSIVE stale-ID case among them | `pp_shadow.log` |
| mbx | `make`, `make run-if2`, `make mutants` | rc 0: WB 404, AXI4-Lite 449, cosim 32; if2 406 / 451 / model 391; 183 of 183 mutants caught, the 8 new source-entry arms by P1/P2/P5 | `mbx.log` |
| Publication census | `publication_census.py --check --selftest --jobs 2` | rc 0: 6 shapes, 246 checks, 0 failures; selftest 0 of 120 arms failed | `census.log` |
| Census at base `97aab1d0` | `--check --jobs 2` | rc 0: 25 nets, 39 reads (for F1) | `census_base.log` |
| Mailbox generator | `gen_mailbox.py --check --crosscheck`; `--selftest` | rc 0; 0 arms failed | `gen_mailbox.log` |
| Static | `pp_resource_gate.py check-baseline`; `lint_rtl.py --check`; `check_cpp_idiom.py`; `check_py_idiom.py`; `check_submodule_docs.py`; `gen_mailbox.py --check --crosscheck` | each rc 0 (baseline PASS, 3 endpoints) | `static.log` |
| ROM digests at the pin | `sha256sum` of the generated `ltn_rom.hex`, `ucode.hex` | `23cc67ee...`, `1f78804e...`, equal to the new `f65c8ff7` rows in `syn/yosys/rom_digests.tsv` | `rom_digests_at_f65c8ff7.txt` |
| Clone integrity | after all runs | HEAD, tree, index identical to `git ls-tree`; no dirty file; gitlinks `f65c8ff7` / `55680bff`; submodules clean | `clone_integrity.txt` |

**Author receipts inspected (public, `0829b8ae`), not re-run:**
- full sweep at `41a78877`, the RTL-final head (2,191,647 checks, 0 in-suite failures);
- gPTP physical at `ca39dc1b` (209 / 0, tally rc 0);
- firmware set at `ca39dc1b`: 8 of 8 rc 0; `ctrl_boundary` rc 0 on its documented rerun after a first-run rc 2;
- docs gates at `ca39dc1b` (44 steps, 0 failed, 2 skipped by rule);
- the rtl-fast replica README;
- the Vivado resource-gate logs.

## Focus items

1. **Gitlink:**
   - `f65c8ff7` is the public processor `main` and the merge commit of PR #208. PRs #204 (`097a7987`) and #207 (`8438382a`) are merged on `main`.
   - The ROM digests, the boundary diagram (the docs gates) and the pin table (`check_submodule_docs.py` rc 0) are regenerated. I reproduced the ROM digests myself.
2. **The #202 wiring:**
   - `src_stream_id_o` (`KL_pp_shadow.sv:716`, `:1451`) arrives as `pp_cd_src_stream_id_w` (`milan_datapath.sv:9653`), then `tx_sid_w` (`:2558`).
   - The AAF framers take it through `.stream_id_i (aaf_tx_sid_w)` with `SID_PP_P = 1` (`:1530`, `:1553`; `KL_aaf_packetizer.sv:505`).
   - The CRF output takes it through `crft_tx_sid_w` (`:2563`, `:7504`), and GET_STREAM_INFO selector 2 through `gsi_osid_w` (`:6193`).
   - After reset the published ID equals the configured `pp_src_sid_w` (`:9516`; processor `KL_acmp_talker.sv:1512`).
   - Probes A, B and C show that each of the three legs is graded on the wire and in the answers, before and after a real conflict.
   - `o_srp_ctx_sid` is unconnected (`milan_datapath.sv:2958`), so a staged talker SID reaches nothing, and the ignored TCTX uid leaves no second ID source.
   - A move changes only `stream_id[15:0]` (bytes 28-29, one beat), and the source is withdrawn across it, so no frame can carry a torn ID.
3. **Mailbox contract 2.3:**
   - It adds exactly the per-source `SRC_SID_LO`/`SRC_SID_HI` (`mailbox.yaml:328`, `:393`, `:406`), generated (`--check --crosscheck` rc 0).
   - `KL_mbx` gains `pub_src_sid_o` (`KL_mbx.sv:337`); the decoder is at `:178`.
   - Both stamps are mapped through the one shape-independent `tx_sid_w` read to `SRC_SID_LO.SID`, and the census passes.
   - Nothing else in the register map moved: the sink entries stay at `0x100`.
4. **#790:**
   - The four G11 cases are at `sim_nxn.cpp:2570`, and pp_shadow's at `sim_main.cpp:3855`.
   - The three `gsi_mutants.py` arms plant in the processor copy (`:96-101`), and each is caught by name.
   - The ledger is restated at `milan_datapath.sv:6005-6019`.
5. **Old-behaviour updates:**
   - The torture plan entry and its features cite Milan 5.3.7.5. That clause is informative per the author's published excerpt, and the excerpt allows a new Stream ID. The entries also cite 802.1Q 35.2.2.8.
   - `sim_nxn.cpp`'s uid 5 to uid 1 change cites IEEE 1722-2016 4.4.4.8, and the capture-coherence pattern was re-anchored.
   - No parent test expected #205's zeroed fields: `acmp_walk.cpp` TW2 grades only status for the unknown case and the listener fields on SUCCESS (Table 5.47).
6. **Resource record:**
   - All three endpoints carry the owner-exception text citing issuecomment-6460917634.
   - The figures equal the published `check` logs: route-1x1 52,012 / 53,707 / 15,780, WNS 0.440, WHS 0.036; ooc-1x1 24,346 / 20,404; ooc-8x8 34,156 / 29,782.
   - `check-baseline` rc 0. The commits after the measured `8b76de69` touch no synthesis input.
   - The AREA_BUDGET arithmetic checks: 82.04 %, 13,972 over, 70 slices free, a 0.190 ns fall bound.
7. **#800:** it is open with the evidence. The diff does not touch `PP_SRC_IDX_W_C`.
8. **Gates:** my runs are above. The author's receipts cover the sweep, gPTP physical, the firmware set, rtl-fast, Yosys, the static bank and the docs gates.

## Clean lenses (same format as findings)

- `[R725] PASS Conformance` — `milan_datapath.sv:1530,1553,2558-2565,6193,7504`, `KL_acmp_talker.sv:1512` (processor `f65c8ff7`), `mailbox.yaml:393-411`, `sim_sid_move.cpp:817-990`, `sim_nxn.cpp:2570-2613`, `pp_shadow/sim_main.cpp:3855-3888`, `gsi790.log`, `clean_sidmove_chain.log`. Checked against:
  - IEEE 1722-2016 4.4.4.8 (the wire ID is the declared one);
  - IEEE 1722.1-2021 7.4.16.2 (an output's current ID);
  - Milan v1.2 5.4.2.10.1 / Table 5.9 (the four settled cases on the wire answer);
  - Milan v1.2 5.3.7.5 / Table 5.3 (another Stream ID allowed);
  - Milan v1.2 5.5.4.1 (the SRC_SID write order in the contract);
  - the ruling 6460917634 items 1-3.
- `[R725] PASS RTL` — `KL_aaf_packetizer.sv:119-168,500-506`, `milan_datapath.sv:1457-1460,2542-2567,6193,9653`, `KL_pp_shadow.sv:716,1451`, `KL_mbx.sv:149-188,284-340,373-385`, `KL_mbx_pkg.sv:341-356`. Checked:
  - widths: `N_STREAM_OUT_P = ACMP_SRC_C`, and `CRF_TUID_C = N_STREAMS` only under `ACMP_SRC_C > N_STREAMS`;
  - the decoder's precedence (sink, then source, then interface) and the write/read guards;
  - reset of the new registers;
  - the per-beat stamp read;
  - Verilator lint (rc 0, ratchets held) and six-shape census elaboration.
- `[R725] PASS Robustness` — `census.log` (six shapes, including the no-CRF `endstation_arty_current` taking the CSR arm), `mbx.log` (a hole, entries past the last, reset clears, partial strobe, two interfaces), and `mutA`/`mutB`/`mutC` logs. Checked:
  - the configuration-dependent CRF arm;
  - reset during activity (P5; the processor's ID returns to its configured slice at reset);
  - repeated conflicts and distinct IDs (`[AFTER]` distinctness and quarantine are in the processor);
  - MAAP disabled leaves the configured ID.
- `[R725] PASS Tests` — probes A, B and C (`receipts/plant_probes.txt`, `mut*_sidmove*.log`), the 3 #790 arms (`gsi790.log`), mbx 183/183 (`mbx.log`) and census selftest 0/120 (`census.log`). Each new test fails for the defect it claims; positive and negative cases are covered; the real integration wiring is tested through the whole datapath. S1 is optional.
- `[R725] UNCLEAN Docs` — F1 open. R1 and R2 are RESIDUE and do not affect coverage. Examined:
  - `CHANGELOG.md`, `docs/reference/SUBMODULES.md`, `REGISTER_MAP.md:1596,1599`, `MAILBOX_CONTRACT.md`, `MILAN_COMPLIANCE_MATRIX.md:122`;
  - `docs/design/MAAP_FABRIC.md`, `MAILBOX_SPLIT.md`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`;
  - `docs/testing/TESTING.md`;
  - the `milan_dp`, `pp_shadow` and `mbx` READMEs;
  - the PR body.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | see PASS line; sidmove/sidmove8, G11, pp_shadow GSI runs; clause excerpt for Table 5.3 | R725-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| RTL | CLEAN | packetizer, datapath wiring, KL_pp_shadow port, KL_mbx decode/regs, lint, census elaboration | R725-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Robustness | CLEAN | six-shape census, mbx holes/reset/if2, probe runs | R725-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Tests | CLEAN | probes A/B/C, gsi arms 12-14, mbx mutants, census selftest | R725-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Docs | UNCLEAN (F1) | the documents listed above, PR body | R725-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |

**Prior public findings:** after my own pass I checked the PR's reviews, review comments and issue comments, and #799's thread. They hold no prior review findings, only the two review-start notices. There is nothing to resolve or retain.

## Real limits

- **Not run by me:** the full four-shard sweep, milan_dp's other legs, the gPTP physical leg, the firmware gate set (including the 523 ctrl mutants and the two model twins), `syn/yosys/run.sh`, `xvlog_gate.py`, behave, the docs gates and Vivado. For these I relied on the author's published receipts at the stated heads, read but not re-executed.
- **The sweep:** its receipt is at `41a78877`. The later commits are docs, the record and two Python string-literal splits; I verified this with `git diff --stat 8b76de69..HEAD`.
- **Clause text:** I did not check it against the standards themselves. Milan 5.3.7.5's informative status comes from the author's published excerpt (`clauses.txt`).
- **Hosted CI:** at the time of writing, the runs at this exact head were not concluded: rtl-fast and rtl-full queued, elaborate and docs in progress. I accept none of them.
- **Hardware:** physical calibration NOT RUN. No hardware or bench was used; field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the ready-gate `verilator-suites` / `yosys-portability` evidence.
- The current-dev candidate merge (source base `97aab1d0`, live dev `5fcec84b`) with its builder and native banks.
- F1's fix and its re-review under `Docs`.
- R1 and R2 on the residue checklist; #790 needs `Closes` or closing by hand.
- The in-house qualification re-runs (es-12.3, es-7.1, es-8.19) on the built image together with the gPTP adoption.
- #665 (the split firmware's `SRC_SID_*` writer) and #800 stay open.

R725-1 FINISHED
