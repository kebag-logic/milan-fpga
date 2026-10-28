[R726] NEGATIVE - exact head ca39dc1b0bd917e3e033df9d9db762514318377a

# R726-1: external cleared-context review of PR #802 (issue #799, also #790)

- Head `ca39dc1b0bd917e3e033df9d9db762514318377a`, tree `f48964b216a6d0eed1b025266a42fa88aab999b0`, base dev `97aab1d0`.
- Gitlinks at the head: protocol-processor `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`, gptp-processor `55680bff3b287b9a7b0c759f51471fa617c17335`.
- Reconstructed from public state only, in this order:
  - AGENTS.md;
  - the #799 body, its assignment, the STOP, ruling 6460917634, both TAKEN comments and REVIEW READY;
  - the #790 body, its assignment, its STOP and the manager comment;
  - the PR body;
  - `git diff 97aab1d0..ca39dc1b` and the 20 commits;
  - the processor range `ed211803..f65c8ff7`;
  - Milan v1.2 5.3.7.5 / Table 5.3, read in the standard itself;
  - the author's published receipts under `review-evidence/799-r1` at `0829b8ae`.
- Prior public review findings were read only after my own pass over the diff. Each one is resolved or retained below.
- No manager source bank was run or inferred at this head.
- **Verdict: NEGATIVE.** One MINOR finding is open under `Docs`. I found it independently, and it was first raised by the internal review. The other four lenses are clean.

## Findings

### F1 - MINOR - Docs - `docs/design/MAILBOX_SPLIT.md:990-992` and `:1102` - the census figures on the design page describe the base, not this head (retained from the prior internal review, independently reproduced)

- **Authority/evidence:**
  - `:990-992` reads: "At this head every shape has the same 25 population nets and the same 39 reads, and four nets are unread. Of the 39 reads, 10 are on the wire and map to the block, 14 are CSR status, and 15 are the answer face".
  - The evidence row at `:1102` repeats "the 39 reads of the 25 class-D nets".
  - My census run at this head prints `26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESULT: PASS` (`receipts/runs/light.log:90`).
  - Counting `CENSUS` rows by kind gives 41 at the head (11 field, 14 status, 16 processor) and 39 at `97aab1d0` (10 / 14 / 15).
  - The change is this PR's own: `src_stream_id_o` is added to `CLASS_D_PORTS` (`sw/mailbox/publication_census.py:157`), with rows `tx_sid_w` (`:199`, field) and `gsi_osid_w` (`:222`, processor).
  - The PR edited this page elsewhere (`:816`, `:835`, `:1103` onward, `:1320`) but not these figures.
  - AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs."
- **Impact:**
  - The authoritative split-placement page understates the census's scope at merge.
  - It omits the one new wire read that `SRC_SID_LO` exists to carry.
  - A reader sizing the split firmware's publication duty gets the wrong count.
  - It is a figure claim, so it is not RESIDUE.
- **Required outcome:** `:990-992` and the `:1102` row state the head's census: 26 nets (4 unread), 41 reads, of which 11 are on the wire, 14 CSR status and 16 the answer face.
- **Verification:** the summary line of `python3 sw/mailbox/publication_census.py --check` equals the page's figures at the merge head.
- **Not counted:** "116 defects, plants two more" (`:1000`) and "118 plants" (`:1102`) were already stale at the base. They may be fixed in the same edit.

### R1 - RESIDUE - Docs - `sw/mailbox/mailbox.yaml:63` - a new issue-comment ID in a source comment (also raised by the prior internal review; retained)

- **Authority/evidence:** the owner rule of 2026-10-15 forbids issue-comment IDs in source comments. This line is new in the delta: `# Minor 3 (#799, the ruling on its STOP, comment 6460917634; #665 decision`.
- No generated output carries the ID. I checked `KL_mbx_pkg.sv`, `KL_mbx.sv`, `mbx_contract.h` and `MAILBOX_CONTRACT.md`.
- `sw/litex/milan_soc.py:2659` `comment 6088423771` is a re-wrap of an existing instance (tracked by #746), not a new one.
- **Exact fix:** change the line to `# Minor 3 (#799; #665 decision`. The rest of the comment is unchanged. Re-run `gen_mailbox.py --check`.

### R2 - RESIDUE - Docs - PR #802 body, "Linked Issue / roles" - `Relates to #790` (also raised by the prior internal review; retained)

- **Authority/evidence:**
  - The #799 acceptance says "#790 closes with this PR". The PR title says "closes #790", and so do `CHANGELOG.md` and `docs/reference/SUBMODULES.md`.
  - The body's "Not 'Closes'" paragraph gives a reason only for #799, whose bench re-runs are owed.
  - Every acceptance item of #790 is met in this PR (see Conformance).
- **Exact fix:**
  - Replace `Relates to #790` with `Closes #790`.
  - Begin the next paragraph with `Not "Closes" for #799:`.
  - Otherwise #790 must be closed by hand at merge (AGENTS.md section 7 allows either).

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_sid_move.cpp:863-868`, `tb/verilator/milan_dp/Makefile:358` (`NAMED_UID_TALKER_TB=1`) (also raised by the prior internal review; retained as optional)

- `sidmove8` names talker 1's TCTX uid as 1, which equals its derived uid. Before the move, `[A]` cannot tell `SID_PP_P = 1` from `0` for that talker; only `[AFTER]` discriminates.
- `sim_nxn.cpp:7604` (TCTX uid 5, expected 1) already covers the override before any move.
- Optional: name a uid distinct from every source's ID.

## Lens results (each with the artifact examined at this head)

```text
[R726] PASS Conformance - protocol-processor gitlink f65c8ff7; milan_datapath.sv:1530,1553,2558,2563,6193,7504,9653; KL_aaf_packetizer.sv:505; KL_pp_shadow.sv:716,1451; mailbox.yaml:73,328,393,406; publication_census.py:157,199,222; sim_nxn.cpp:2570; pp_shadow/sim_main.cpp:3855; gsi_mutants.py:96-101; milan_datapath.sv:6005-6019; syn/ooc/pp_resource_baseline.json; issue #800 - each focus item checked against #799/#790, ruling 6460917634, Milan v1.2 5.3.7.5/Table 5.3, 5.4.2.10.1/Table 5.9, IEEE 1722-2016 4.4.4.8, IEEE 1722.1-2021 7.4.16.2
[R726] PASS RTL - milan_datapath.sv:1457-1460,1524-1553,2542-2567,6190-6193,7501-7504,9650-9653; KL_aaf_packetizer.sv:119-132,162-168,500-506; KL_pp_shadow.sv:710-716,1448-1451; KL_mbx.sv:149-188,276-337,373-385; KL_mbx_pkg.sv:17-20,338-356 - widths, indexing, generate branches, decode exclusivity, reset, write gating; lint 89<=89; census 6-shape sv2v/Yosys elaboration
[R726] PASS Robustness - KL_mbx.sv:178,297-337 (hole/out-of-range/reset, mbx P1/P4/P5 and reviewer arm); milan_datapath.sv:2561-2567 (shapes without a CRF source); sim_sid_move.cpp phase_move (conflict, withdraw, re-declare, no stale-ID PDU 50 ms after Leave); sim_nxn.cpp:2570 (probing, settled, PROBING_PASSIVE stale ID, unbound) - against Milan 5.5.4.1, Table 5.9, 1722 4.4.4.8
[R726] PASS Tests - receipts/runs/{notify,gsi790,gsi_sel2_probe,sidmove,sidmove8,probe_*,ppshadow,mbx,mbx_src_probe,aaf,aaf_audio_loop,capture_coherence,light,static2}.log - every new check run at this head, and every new defect class planted and caught by name
[R726] MINOR Docs - docs/design/MAILBOX_SPLIT.md:990-992,1102 - F1 (stale census figures); RESIDUE R1, R2
```

### Conformance (focus items 1 to 7)

1. **Gitlink and pin-derived records.**
   - `f65c8ff7` is the processor's live `main` (API) and the merge commit of PR #208.
   - #204 (`097a7987`) and #207 (`8438382a`) are its ancestors, and `ed211803` is an ancestor (24 commits).
   - The ROM rows (`syn/yosys/rom_digests.tsv:75-76`) equal the `sha256sum` of the `ltn_rom.hex` and `ucode.hex` my clone generated at the pin (`23cc67ee...`, `1f78804e...`).
   - `check_submodule_docs.py` reports 6 exact gitlinks; `check_diagram_pngs.py` rc 0.
   - The author's static bank at `ca39dc1b` re-recorded the ROM digests with no diff and ran `submodule_boundaries.gen.py --check` rc 0 (receipt inspected).
2. **#202 wiring.**
   - The chain is `src_stream_id_o` (`KL_pp_shadow.sv:716`, `:1451`) to `pp_cd_src_stream_id_w` (`milan_datapath.sv:9653`) to `tx_sid_w` (`:2558`). From there it feeds:
     - the AAF framer through `aaf_tx_sid_w` with `SID_PP_P = 1` (`:1530`, `:1553`; `KL_aaf_packetizer.sv:505`);
     - the CRF output through `crft_tx_sid_w` (`:2563`, `:7504`);
     - GET_STREAM_INFO selector 2 through `gsi_osid_w` (`:6193`).
   - Recovery legs: `sidmove` passes 50/50 and `sidmove8` 52/52 at this head.
   - My three fault probes each fail the leg on the source they target:
     - `gsi_osid_w` back on `pp_src_sid_w` fails `[AFTER]: GET_STREAM_INFO selector 2 is src_stream_id_o` for sources 0 and 1;
     - the CRF stamp back on the CSR ID fails source uid 1's `[AFTER]: every one carries src_stream_id_o` and the withdrawn-ID check;
     - `SID_PP_P (1'b0)` fails the same checks on source uid 0.
   - Milan v1.2 5.3.7.5 is headed "(informative)" and "does not preclude any other implementation". Table 5.3 allows "another Stream ID". So the torture plan's new reading (`tb/tools/torture_campaign.py:2643-2671`) is correct.
3. **Mailbox contract 2.3.**
   - It adds exactly `SRC_SID_LO`/`SRC_SID_HI` per source at `0x80 + 8*s` (`mailbox.yaml:328`, `:393`, `:406`), minor 3 (`:73`).
   - It is generated: `gen_mailbox.py --check --crosscheck` rc 0, and `--selftest` 0 arms failed.
   - `KL_mbx` gains `pub_src_sid_o` (`KL_mbx.sv:337`); the sink entries stay at `0x100`.
   - Both stamps map through the one per-source `tx_sid_w` read to `SRC_SID_LO.SID`.
   - The census passes: RESULT: PASS over 6 shapes, 246 checks, 0 failures; self-test 0 of 120 arms failed. It ran with the pinned sv2v v0.0.12 and Yosys 0.66.
   - The split firmware writer is recorded as #665's (`MAILBOX_SPLIT.md`), as the ruling requires.
4. **#790.**
   - G11's four cases are at `sim_nxn.cpp:2570` and pp_shadow's group at `sim_main.cpp:3855`.
   - The ledger is restated at `milan_datapath.sv:6005-6019`.
   - Clean `notify` passes 499/499. `gsi_mutants.py 12 13 14` returns rc 0, and each arm is caught by the named G11 PROBING_PASSIVE check (3, 1 and 1 failures).
   - My extra arm, selector 2 alone passed through, is caught by "...the stale ID: stream_id is zero".
   - The 0x52000000 mask is STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID, which matches the bench capture in the issue.
5. **Old behaviour updated.**
   - The torture plan entry and both behave steps cite 802.1Q 35.2.2.8 and Table 5.3.
   - `sim_nxn.cpp:7582-7604` (uid 5 to 1) cites IEEE 1722-2016 4.4.4.8.
   - The capture-coherence anchor was rewritten; that leg passes (42/42 runner checks, 847 in the datapath leg).
   - `REGISTER_MAP.md:1596`, `:1599` state that the STRMW SID words keep the first ID and that the TCTX uid is no longer stamped.
   - #205: no parent test grades the listener fields of an unknown-uid answer. `sim_nxn.cpp:9372` checks status only, and `acmp_walk.cpp` TW2 checks status. So nothing needed updating.
   - A search for stale "2 LeaveAll" claims finds only the corrected entries.
6. **Resource record.**
   - All three endpoints carry the owner exception citing issuecomment-6460917634.
   - The figures (route-1x1 52,012 / 53,707 / 15,780, WNS 0.44, WHS 0.036; ooc-1x1 24,346 / 20,404; ooc-8x8 34,156 / 29,782) equal the published `check-against-new-record` logs (every delta 0, RESULT: PASS). The route status shows 0 routing errors.
   - `check-baseline` rc 0 here.
   - `git diff 8b76de69..ca39dc1b` touches no synthesis input, which supports measuring at `8b76de69`.
7. **#800** is open with the width table and evidence. `PP_SRC_IDX_W_C` (`milan_datapath.sv:2580`) is unchanged by the diff.

**Item 8 (consumer gates).** Published author receipts inspected:
- sweep at `41a78877`: 2,191,647 checks, 0 in-suite failures;
- gPTP physical at `ca39dc1b`: 155 + 6 + 20 + 14 + 14 checks, 0 failures;
- firmware set at `ca39dc1b`: 8 of 8 rc 0, with `ctrl_boundary` rc 0 on its documented rerun after a first run that lost its SDK, rc 2;
- Yosys at `ca39dc1b`: rc 0, tap-purity PASS;
- static bank at `ca39dc1b`: 22 of 22 rc 0.

The later commits after `41a78877` touch only docs, the record and string literals.

### RTL

- `tx_sid_w` is `ACMP_SRC_C*64` wide, the same as the shadow port (`N_STREAM_OUT_P = ACMP_SRC_C`).
- `aaf_tx_sid_w` takes the low `N_STREAMS*64` bits, and `stream_id_i[64*32'(et_r) +: 64]` is indexed by the talker already used for the other per-talker files.
- The CRF branch exists only where `ACMP_SRC_C > N_STREAMS`. Otherwise the CSR value stays, as before.
- `pub_src_w` / `pub_sink_w` are mutually exclusive. Writes are gated by `pub_at_w`, which bounds `src_entry < 16`, and the 16 entries exactly fill `0x80..0xFF`.
- Every interface-register write and read now also excludes `pub_src_w`.
- Reset clears both words.
- The census's sv2v/Yosys elaboration covers all six shapes. Lint holds at 89 <= 89 with 0 justified `lint_off`.
- My probe dropping `!pub_src_w` from the DA_GATE write is caught (P1). So the exclusion is load-bearing and graded.

### Robustness

- Covered at this head:
  - reset (mbx P5 arm, and sidmove's after-reset IDs equal the configured `{MAC, uid}`);
  - holes and past-the-last entries (the hole-alias arm);
  - shapes without a CRF source (census `arty_current`);
  - a real MAAP conflict during streaming, with withdraw, re-declare under 2 s, no PDU on the withdrawn ID 50 ms after its Leave, and distinct IDs;
  - an input dropping back to PROBING_PASSIVE with a stale binding view (G11 and pp_shadow).
- The half-written-ID ordering rule for the split owner is a documented contract (`mailbox.yaml` SRC_SID_LO doc; Milan 5.5.4.1). Its writer is #665's, so there is no executable path here to fault.

### Tests

- Every new check was run at this head, all with rc 0:
  - G11 / notify 499;
  - pp_shadow 651 / 651 / 691 / 317, with 126 `[GSI]` lines;
  - sidmove 50, sidmove8 52;
  - mbx: Wishbone 404, AXI4-Lite 449, cosim 32; two interfaces 406 / 451, model 391;
  - the AAF benches on the default `SID_PP_P = 0` path (`aaf`, `aaf_audio_loop`) PASS;
  - capture_coherence PASS;
  - behave: 14 features, 406 scenarios, 1,979 steps.
- Each new defect class was shown to be detectable:
  - 3 #790 arms plus my selector-2 arm;
  - 3 sidmove probes;
  - the 8 source-entry mbx arms plus the rewritten hole arm (10, all caught);
  - my DA_GATE guard arm (2).
- S1 is the only weakness found, and it is optional.

### Docs

- These are correct at this head:
  - `REGISTER_MAP.md`, `MILAN_COMPLIANCE_MATRIX.md`, `MAAP_FABRIC.md`, `TESTING.md` (17 ordinary legs);
  - the milan_dp README (its G11 ledger and the 3/1/1 failures match my run);
  - `SUBMODULES.md`, `CHANGELOG.md` (70 slices free: 15,850 - 15,780);
  - `AREA_BUDGET.md`;
  - the generated `MAILBOX_CONTRACT.md` (`gen_mailbox.py --check`).
- `docs_check.py`, `check_feature_status.py`, `check_gptp_docs.py`, `check_port_contracts.py` and `pp_srcs.py --check` are each rc 0.
- F1 leaves this lens unclean. R1 and R2 are wording only.

## Reviewer runs at this head

All runs used disposable clones at the exact head under `scratch/`, with pinned Verilator 5.050 (`rev v5.050`), and sv2v v0.0.12 / Yosys 0.66 for the census. Each rc is the command's own.

| Run | Command | Result | Receipt |
|---|---|---|---|
| Generator, census, static | `scripts/light_gates.sh` | gen `--check --crosscheck` 0; `--selftest` 0; census `--check --selftest --jobs 4` 0 (6 shapes, 246 checks, 0 failures; 0 of 120 arms failed); submodule docs 0; lint 0; both idiom gates 0; `check-baseline` 0; `behave -f progress` 0. The script's one rc 2 step is my own malformed `behave -k` invocation (no such option), superseded by the full behave run | `receipts/runs/light.log` |
| Docs and port gates | diagram PNGs, port contracts, docs_check, feature status, gPTP docs, `pp_srcs --check`, gen `--check` | 7 / 7 rc 0 | `receipts/runs/static2.log` |
| notify (G11) | `make notify` | rc 0, 499 checks, 0 failures | `receipts/runs/notify.log` |
| #790 arms | `python3 gsi_mutants.py 12 13 14` | rc 0, 4 / 4 (clean + 3 caught by name) | `receipts/runs/gsi790.log` |
| Selector-2 probe | `scripts/gsi_sel2_probe.py` | rc 0, caught by "...the stale ID: stream_id is zero" | `receipts/runs/gsi_sel2_probe.log` |
| pp_shadow | `make` | rc 0: 651, 651, 691, 317 checks, 0 failures | `receipts/runs/ppshadow.log` |
| sidmove / sidmove8 | `make sidmove`, `make sidmove8` | rc 0: 50 / 0, 52 / 0 | `receipts/runs/sidmove*.log` |
| #202 fault probes | `scripts/sid_probes.sh` (gsi_osid, crft_csr, aaf_derive) | each CAUGHT (RESULT: FAIL, 2 named failures, on the targeted source) | `receipts/runs/probe_*.log`, `sidprobe_*.out` |
| mbx | `make && make run-if2` | rc 0 (404 / 449 / 32; 406 / 451 / 391) | `receipts/runs/mbx.log` |
| mbx source-entry arms | `scripts/mbx_src_probe.py --jobs 6` | rc 0: controls ok; 12 of 12 caught | `receipts/runs/mbx_src_probe.log` |
| AAF benches (default SID path) | `make` in `aaf`, `aaf_audio_loop`, `capture_coherence` | rc 0 each | `receipts/runs/aaf*.log`, `capture_coherence.log` |
| Hosted snapshot | check-runs API at the head | mixed: census, behave, lint and most firmware jobs success; Verilator/Yosys shards in progress; physical gPTP skipped | `receipts/hosted_checks_snapshot.tsv` |
| Clone integrity | after all runs | HEAD/tree as above; index == HEAD; `ls-files -s` equals `ls-tree` (blob, mode); no dirty file; gitlinks and submodules clean and equal to the pre-run snapshot | `receipts/clone_integrity.txt` |

## Prior public findings at this head

| Prior finding | Status at this head |
|---|---|
| internal F1 MINOR Docs (`MAILBOX_SPLIT.md` census counts) | **Retained** as F1, reproduced from my own census run |
| internal R1 RESIDUE (`mailbox.yaml:63` comment ID) | **Retained** as R1 (found independently) |
| internal R2 RESIDUE (PR body `Relates to #790`) | **Retained** as R2 (found independently) |
| internal S1 SUGGESTION (sidmove8 named uid equals derived) | **Retained** as S1, optional |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlink and processor range; the wiring lines; mailbox.yaml; census rows; G11 / pp_shadow / gsi_mutants; datapath ledger; resource record and Vivado logs; #800; Milan 5.3.7.5 text | R726-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| RTL | CLEAN | `milan_datapath.sv`, `KL_aaf_packetizer.sv`, `KL_pp_shadow.sv`, `KL_mbx.sv`, `KL_mbx_pkg.sv` deltas; lint; census elaboration | R726-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Robustness | CLEAN | mbx decode / reset / holes; shapes without CRF; sidmove conflict path; G11 stale case | R726-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Tests | CLEAN | every new check run; 19 planted defects caught (4 for #790, 3 sidmove, 12 mbx: the 8 source-entry arms, the 2 rewritten hole arms and my 2 DA_GATE arms); S1 optional | R726-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |
| Docs | UNCLEAN | F1 open (`MAILBOX_SPLIT.md:990-992`, `:1102`); R1, R2 residue | R726-1 | `ca39dc1b0bd917e3e033df9d9db762514318377a` |

## Real limits

- I did not run the full four-shard sweep, milan_dp's other legs, the physical gPTP leg, the firmware gate set, `syn/yosys/run.sh`, the docs gates under GNU Make 4.3, the builder bank, xvlog or Vivado. Those are inspected only as the author's published receipts.
- The physical calibration was NOT RUN, and field skips are not hardware proof.
- The hosted Verilator and Yosys shards were still in progress at my snapshot.
- I did not measure the `--ctrl-mailbox` SoC's area with contract 2.3; the PR records this as not measured.
- The split firmware's `SRC_SID_*` writer does not exist yet (#665), so the publication ordering rule has no executable test here.

## Pending manager duties

- After F1 is fixed, a re-review of `Docs` at the new head. The other four lenses stay banked only if that commit touches nothing in their scope.
- Carry R1 and R2 to the residue checklist.
- Hosted and act acceptance at the final head.
- The current-dev merge candidate (live dev `5fcec84b`) on the builder and native banks.
- Closing #790 at merge, by `Closes #790` or by hand.
- #799's owed in-house qualification re-runs on the built image, with the gPTP adoption.

R726-1 FINISHED
