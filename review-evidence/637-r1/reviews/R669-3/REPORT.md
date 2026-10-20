[R669] POSITIVE - exact head 1e914414557874648ac5041aff88b96908e0e053

R669-3, internal cleared-context review of issue #637 / PR #768, round-3 delta. Head tree `033e6bc1fb66904e7faf7b57929d6c7a28d89732`. The previously reviewed head is `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` (R669-2). The source base is `e9cbb676`. The delta is three commits, `dc7dd727`, `600565b4` and `1e914414`, and touches seven files: two docs pages, TESTING.md, and the `tb/verilator/milan_dp` Makefile, README, `dynmap_mutants.py` and `sim_nxn.cpp`. `git diff --name-only 8000520c..1e914414 -- hdl syn constraints` is empty. The processor pin stays `2cbed0a9`.

All three named prior findings are resolved at this head. Every lens is covered clean. No BLOCKER, MAJOR or MINOR is open. This round adds one SUGGESTION and four RESIDUE items, listed below with their exact fixes.

## Reconstruction and independence

I read the following, in order:
- AGENTS.md and CONTRIBUTING.md.
- docs/README.md.
- The issue's frozen acceptance and the round-2 and round-3 assignments (PR #768 comments 6269988820 and 6295599722).
- D3 (`SAVED_STATE_MATERIALIZATION.md`) section 3 rule 7, 8.7 and 18.4, and REGISTER_MAP PP_STAT.
- The full round-3 diff and its history.
- The author's public round-3 receipts at evidence commit `4d31fa3d8b9bd09b15b2f4b78ed7b8f2c2d04a47` (`review-evidence/637-r1/author-r3/`).

I wrote my preliminary verdict and lens ledger before opening the R669-2 and R670-2 finding bodies. I read no private author material, no management checkout, no concurrent round-3 review, and no other review's packet under `review-evidence/637-r1/reviews/`. I made no source edit, commit, push, GitHub write, merge or author contact.

## Prior findings, reconciled at this head

| Finding | Disposition | Evidence at `1e914414` |
|---|---|---|
| R669-2-F1 MINOR (Tests): the validated-record test behind PP_STAT blank was unproven term by term | **RESOLVED** | See "R669-2-F1 in detail" below. |
| R669-2-F2 MINOR (Docs): "both cause fields then read 0" was false when the binding walk also failed | **RESOLVED** | See "R669-2-F2 in detail" below. |
| R670-2-F1 MINOR (Tests, Docs): the round-2 account reported the full campaign as rc 0 | **RESOLVED** | See "R670-2-F1 in detail" below. |
| R670-2-R1, R670-2-R2 (comment provenance) | RETAINED for the merge checklist (assignment item 4) | Still present: `milan_datapath.sv:4922`, `sim_nxn.cpp:5565` (moved from `:5528`), and `dynmap_mutants.py:29`, `:35`, `:154`, `:168`, `:316`, `:345`, `:386-387`. The delta adds no new instance. |
| R670-2-R3 (round-2 role lines) | RESOLVED for round 2 | The PR body roles now read "round 2 assigned, notice ...". Their new round-3 staleness is RES-1 below. |
| R669-2 RES-1 to RES-5 | RETAINED for the merge checklist | Unchanged. For RES-4, the new docstring paragraph at `dynmap_mutants.py:42-46` covers rows 61-63 correctly, but the 19-versus-23 count for rows 38-60 remains. RES-5 is still at `milan_datapath.sv:5490-5491`. |
| R669-2 S1, S2, S3 | Remain optional suggestions, not assigned | No change in the delta. |

### R669-2-F1 in detail

Four new cases are in `sim_nxn.cpp:5496-5529` (`maprec_lone_record_case` and `maprec_lone_record_section`), called at `:5553`:

| Case | Edit | Re-sealed |
|---|---|---|
| crc16 | entry 0 payload byte 13, cluster 0 changed to 4 | no |
| layout | byte 2, `0x02` changed to `0x03` | yes |
| id | `0x70` record byte 3 changed to `0x71` | yes |
| magic | byte 0, `0x17` changed to `0x18` | yes |

- The edits match `milan_datapath.sv:5418-5425` and `AMR_LAYOUT_C = 8'h02` (`:4939`). Each case fails exactly one operand of `amr_rs_valid_r`'s condition (`:5487`).
- Each case checks that the codec frames the record and that the restore ends. It grades SPI 0 and SPO 0 on GET_AUDIO_MAP, render RAM keys 2..9 and capture RAM keys 0..7 against the identity reset sets, and reads PP_STAT done 1, busy 0, fail 0, blank 1 over AXI. The dynmap leg is the 1x1 shape (`endstation_ax7101_1x1_tdm8`, `Makefile:78`), so SPI 0 and SPO 0 are every port it has.
- In my clean leg, each case reads `PP_STAT 5b000484` (`receipts/dynmap_clean.log:1145`, `:1164`, `:1183`, `:1202`).
- The vacuity guard went from 51 to 59 pages, which is the eight new pages (`:5557`).
- Rows 61-63 (`dynmap_mutants.py:415-424`) remove the crc16, layout/id and magic/length operands. I reran them myself: they are caught by their named blank checks with 1, 2 and 1 failures of 649 (`receipts/probes.log`). The author's single full campaign reports the same counts.

### R669-2-F2 in detail

The fixed text is at `REGISTER_MAP.md:2378-2380`, at the PP_STAT `[3]` row (`:2403`), and in D3 8.7 (`SAVED_STATE_MATERIALIZATION.md:1500-1502`). It now says the map restore adds no cause of its own, `[20:18]` reads 0, and `[22:21]` keeps the binding walk's cause.

I checked this against the RTL:
- The AS_BOOT gate (`milan_datapath.sv:5347-5348`) enters the map restore only on `pp_restore_done_w` with no roll-back, `pp_rs_cause_w == 0` and no CLOSED.
- `[22:21]` comes from the binding walk alone (`milan_csr.sv:670`).
- No other copy of the old sentence remains. A tree-wide search for "both cause" or "cause fields" finds only the RTL comment `milan_datapath.sv:5765`, whose converse statement is true.

### R670-2-F1 in detail

The PR body's round-2 account rows (body lines 173-176), HANDOFF `:294-296` and the issue's round-3 REVIEW READY (6298458163) now keep these separate:
- the full campaign: rc 2, 63 of 65;
- the listener rerun: rc 0, 2 of 2;
- the aggregate: 60 of 60 caught and five clean legs passed across the two executions, with the full command not exiting 0;
- synthesis, rc 0, in its own rows.

Both round-2 receipts are linked and resolve at `180fc3a8` (`receipts/round2-receipt-links.txt`). Round 3 also carries its own full campaign: one command from a clean clone at `600565b4`, rc 0, 68 checks, 68 PASS, with five clean legs and 63 of 63 caught (`author-r3/receipts/round3/campaign/`). That receipt is hash-verified below. The `600565b4..1e914414` diff touches only `tb/verilator/milan_dp/README.md` and a Makefile comment.

## Findings (this round)

### R669-3-S1 SUGGESTION - Tests, Robustness - `hdl/milan/milan_datapath.sv:5422-5423`; `tb/verilator/milan_dp/sim_nxn.cpp:5523-5529` - no committed case checks the record's length field on its own

- **Evidence.** My probe (`scripts/probe_mutants.py`, row `L`) replaces both length arms with `amr_hframe_r <= amr_hframe_r`. It builds and passes the clean dynmap leg (`receipts/probes.log`: "mutant SURVIVED: reviewer probe: the record's length field is never compared"; the driver exits 1 by design). Row 63 removes the whole frame operand and is caught by the wrong-magic case. No case puts a framed, re-sealed record with only a wrong length field in the window, on either the accept path or the blank path.
- **Authority.** The round-3 assignment item 1 makes a magic/length control optional, so this does not affect any lens. The CRC covers bytes 4-5, so a length-only fault needs a re-sealed or foreign-shape record.
- **Optional outcome.** Add a fifth lone case (byte 5 changed, re-sealed) graded blank 1. Optionally add a length-only control row.
- **Verification.** The probe `L` above is caught.

### Residue (wording only; no lens left unclean; for the merge checklist)

| ID | Artifact | Defect | Exact fix |
|---|---|---|---|
| R669-3-RES-1 | PR #768 body, Linked Issue / roles (lines 25-26) | Both role lines still say "round 3 to be assigned". The round-3 review-start notices are 6298509526 (internal) and 6298519097 (external). | Replace "round 3 to be assigned" with "round 3 assigned, notice 6298509526" on the internal line, and with "round 3 assigned, notice 6298519097" on the external line. |
| R669-3-RES-2 | `review-evidence/637-r1/author-r3/HANDOFF.md:80` (Gates, round 3) | It says "`600565b4` (tb, hdl equal to the head)". `tb/verilator/milan_dp/README.md` and the Makefile comment differ between `600565b4` and the head. | Replace "(tb, hdl equal to the head)" with "(differs from the head only in the milan_dp README and a Makefile comment)", the PR body's own wording. |
| R669-3-RES-3 | `review-evidence/637-r1/author-r3/HANDOFF.md:191` (round-2 prose) | "So at the head: 60 of 60 caught, all five clean legs pass." It lacks the qualifier the corrected tables carry. | "So across those two executions at the head: 60 of 60 caught and all five clean legs pass; the full campaign command itself exited 2." |
| R669-3-RES-4 | PR #768 body, Validation account (round 3), rows for the legs, campaign, docs and builder (lines 106-110) | The rows cite no receipt, although the round-2 rows now link theirs and the receipts are published. | Link `4d31fa3d.../review-evidence/637-r1/author-r3/receipts/round3/legs/`, `.../campaign/campaign-600565b4.verdicts.txt` and `.log.excerpt`, `.../docs/rc.tsv`, and `.../builder/rc.tsv`. |

Comment rule (owner 2026-10-15): the new source comments in the delta are clean. These are `sim_nxn.cpp:5496-5502` and `:5524`, `dynmap_mutants.py:42-46` and `:414`, and `Makefile:569-570`. They state behaviour and reason with issue and D3 IDs, and none names a bench lane, lane, review round, reviewer or comment ID.

## Clean results by lens

- `[R669] PASS Conformance - REGISTER_MAP.md:2378-2380, :2403 ([3], [7]); SAVED_STATE_MATERIALIZATION.md:1497-1505 (8.7); sim_nxn.cpp:5496-5529; receipts/dynmap_clean.log:1130-1205 - D3 3 rule 7 and 8.7 blank ("neither walk validated a record, nor did the parent's map restore") is met: a lone framed record failing one validated-record operand reads blank 1, fail 0, done 1, reset sets kept. The cause-field contract matches milan_datapath.sv:5347-5348 and milan_csr.sv:669-670. Issue acceptance is unchanged from round 2. The on-board cold cycle is not claimed.`
- `[R669] PASS RTL - git diff --name-only 8000520c..1e914414 -- hdl syn constraints (empty); milan_datapath.sv:5347-5348, :5418-5425, :5487-5491, :5769-5773 - no RTL, synthesis or constraint byte changed. The round-3 docs claims were checked against the AS_BOOT gate and the PP_STAT composition. Nothing the R669-2 RTL verdict depends on changed, so it carries forward: amr_fsm, the composition, the route-1x1 receipt at 887b6bf2, and lint.`
- `[R669] PASS Robustness - sim_nxn.cpp:5509-5521; receipts/dynmap_clean.log:1130-1205 - malformed and truncated-header input: a crc-torn payload and a re-sealed wrong layout, wrong id and wrong magic each end with every port on its reset set and no fail. The hold is 672 clocks, inside the documented 598 to 672. The length-only gap is S1 (optional). Other failure paths keep the R669-2 verdict; the delta does not change them.`
- `[R669] PASS Tests - dynmap_mutants.py:415-424; sim_nxn.cpp:5523-5557; receipts/probes.log; receipts/dynmap_clean.log (649/0); receipts/readme-vs-verdicts.log; author-r3/receipts/round3/campaign/campaign-600565b4.verdicts.txt - each new control is planted (exact single-match pattern), builds, and fails its named check: reproduced, 1, 2 and 1 of 649. The clean leg passes. The author's full campaign is rc 0, 68/68, with five clean legs. All 63 README rows (name, count, total) agree with the verdicts. The vacuity guard is 59.`
- `[R669] PASS Docs - REGISTER_MAP.md:2378-2380, :2403; SAVED_STATE_MATERIALIZATION.md:1500-1502; TESTING.md:277 (63 controls, 43 [MAPREC] arms, counted against MUTATIONS 54/5/2/1/1); Makefile:569-570; milan_dp README:833-902, :988-997; the PR body, HANDOFF and issue 6298458163 validation accounts; author docs rc.tsv (95/95 rc 0 at 1e914414); receipts/gates (5 gates rc 0) - the changed contracts are stated correctly and the counts are current. The validation account separates the executions. Wording residue is RES-1 to RES-4.`

## Execution evidence (source evidence only; no manager source bank is claimed or inferred)

| Evidence | Result |
|---|---|
| Published round-3 receipts, 20 files under `author-r3/` (PR-BODY, HANDOFF, review-ready, the campaign verdicts, excerpt and identity, the three leg logs and `rc.tsv`, docs `rc.tsv` and identity, builder `rc.tsv` and identity, scripts) | All 20 match `MANIFEST.json` `published_sha256` (`receipts/evidence-manifest-verify.log`). GitHub reports evidence commit `4d31fa3d` as unsigned, so this is hash integrity, not signer authentication. |
| Author legs at `1e914414` | dynmap 649/0, maprec8 219/0, maprec4 137/0; rc 0 each. |
| Author campaign at `600565b4` | Clean clone, empty `git status`. `CAMPAIGN rc=0`, "68 checks: 68 PASS, 0 FAIL". |
| Author docs gates at `1e914414` | 95 commands, rc 0 each. |
| Author builder legs at `1e914414` | rc 0 (824 s) and rc 0 (310 s). Builder gate 11 is declared NOT RUN by the builder. |
| My clean dynmap leg at `1e914414` | Pinned simulator 5.050 (`receipts/verilator-identity.txt`), `make dynmap` rc 0, 649 checks, 0 failures. |
| My controls | Rows 61, 62, 63 caught (1, 2, 1 of 649). Probe `L` survives (S1). The driver total is 4 PASS and 1 FAIL, and that FAIL is the expected survivor. |
| My gates at `1e914414` | `check_cpp_idiom.py`, `measure_test_evidence.py --check`, `check_doc_style.py`, `docs_check.py` and `check_port_contracts.py`: rc 0 each (interpreter in `receipts/gates/python-version.txt`). |
| Hosted, exact head | The check-runs API returns 0 runs for `1e914414` (`receipts/hosted-check-runs-1e914414.tsv`). No hosted execution is claimed. |
| Clone integrity after probes | Head and tree match. The index equals the HEAD tree in paths, modes and ids. All 1,422 tracked blobs re-hashed equal, with no skip or assume flags and no untracked or ignored entries. All five required gitlinks are as pinned (`external` is optional and uninitialized). The populated submodules are clean. My build outputs and caches were removed (`receipts/clone-integrity.txt`). |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | D3 3 rule 7, 8.7; REGISTER_MAP PP_STAT `[3]`, `[7]`, `[20:18]`, `[22:21]`; `milan_datapath.sv:5347-5348`; `milan_csr.sv:669-670`; lone-record cases and their PP_STAT reads | R669-3 | `1e914414557874648ac5041aff88b96908e0e053` |
| RTL | CLEAN | empty hdl/syn/constraints delta; `milan_datapath.sv:5347-5348`, `:5418-5425`, `:5487-5491`, `:5769-5773` (R669-2 verdict carried forward, dependencies unchanged) | R669-3 | `1e914414557874648ac5041aff88b96908e0e053` |
| Robustness | CLEAN | `sim_nxn.cpp:5496-5529`; my clean leg's lone-record windows and hold; probe `L` (S1, optional) | R669-3 | `1e914414557874648ac5041aff88b96908e0e053` |
| Tests | CLEAN | `dynmap_mutants.py:415-424`; `sim_nxn.cpp:5523-5557`; my clean leg and rows 61-63; the author's campaign verdicts; README table against the verdicts | R669-3 | `1e914414557874648ac5041aff88b96908e0e053` |
| Docs | CLEAN (RES-1 to RES-4 recorded) | `REGISTER_MAP.md` delta; D3 8.7 delta; `TESTING.md:277`; milan_dp README and Makefile delta; PR body, HANDOFF and issue accounts; 95 author docs gates and 5 of my own | R669-3 | `1e914414557874648ac5041aff88b96908e0e053` |

## Real limits

- I re-ran no full parent, PP, gPTP, Yosys or builder bank, no full `dynmap-mutants` campaign, no maprec8 or maprec4 leg, no sweep, and no route, ooc or xvlog. For those I read the author's hash-verified receipts. Round 2's synthesis and route records (`887b6bf2`, `af5eefc6`) stand because no hdl, syn or constraints file changed.
- My own executions are the clean dynmap leg, rows 61-63, one probe and five gates. My gates ran under the host interpreter recorded in `receipts/gates/python-version.txt`, not the hosted CPython 3.12.3. The author's docs receipts used 3.12.3.
- No hosted check run exists at this exact head. Exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` evidence is absent, and the manager owns hosted and act acceptance.
- Physical calibration and the on-board cold cycle are NOT RUN. Field skips and desk power cycles over a zero-latency window model are not hardware proof. DDR latency adds to the 598 to 672 clock hold. The 8x8 hold (about 13,700 clocks) stays open against the 4,096-clock watchdog under D3 18.4.
- The evidence commit is unsigned, so signer authentication was not possible. Only hash integrity was verified.

## Pending manager duties

- Build and validate the current-dev merge candidate against live dev `78ca9bdf104819265588726bce4322696c38b8c2` (source base `e9cbb676`), with the builder and native banks, and link its receipts on the PR.
- Hosted and act acceptance at the final head: exact-head `rtl-fast`, `verilator-suites` and `yosys-portability`, separating executed jobs from skipped contexts.
- Carry these to the residue checklist: R669-3-RES-1 to RES-4, R669-2 RES-1 to RES-5, and R670-2-R1 and R670-2-R2.
- The external review's round-3 verdict, the completion ledger across both reviews, maintainer merge authorization, post-merge containment, and the on-board cold cycle owed under #637 ("Relates to #637").

## Receipts (listed in MANIFEST.sha256)

- `receipts/dynmap_clean.log`, `.rc`: my clean dynmap leg at the head.
- `receipts/probes.log`, `.rc`: rows 61-63 and probe `L`.
- `receipts/gates/*`: five focused gates, their logs, rc files and the interpreter version.
- `receipts/evidence-manifest-verify.log`, `readme-vs-verdicts.log`, `round2-receipt-links.txt`, `hosted-check-runs-1e914414.tsv`, `verilator-identity.txt`, `clone-integrity.txt`.
- `scripts/run_clean_dynmap.sh`, `run_probes.sh`, `probe_mutants.py`, `verify_manifest.py`, `readme_vs_verdicts.py`, `clone_integrity.sh`.

R669-3 FINISHED
