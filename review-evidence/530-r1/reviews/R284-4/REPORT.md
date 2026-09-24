[R284] POSITIVE - exact head f814d37d94e17435f3b6dcc424f8b2b606cdd3e9

Round R284-4: internal, cleared-context, independent re-review of issue #530 / PR #549.

- Head: `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9`, tree `f431f698deafcc625d738714b960f109d82012df`. I verified both in my own detached clone.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06`. The silicon-tested head is `c593cbeffaffa647cda70fb1a233455bf9c80d55`.
- This round's delta on the R284-3 head `e65dccfe`:
  - `44ad6991` ([A239]): one `--no-ff` merge of dev `f86c34fe` (#540).
  - `b7887343`, `35f2a54b`, `f814d37d` ([A241]): comments and Markdown only, for R284-3 F1 and R284-3 S1 = R285-3 S1.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open under any lens at this head. Two SUGGESTIONs are recorded (S1, S2). They do not affect coverage.
  - The merge's conflict resolution is the exact union of both sides:
    - the processor pin comes from this PR, and the gPTP pin and donor links from #540;
    - every `milan_dp` target, clean entry and README section from both sides is kept.
  - The diagram, SVG, PNG raster and manifest reproduce byte for byte from the repository generator. All three ROM images regenerate to their recorded digests at the merged pins.
  - `make gmstep` gives 44/48 at this head. That is identical, check by check and value by value, to dev `f86c34fe`, and the README documents those four failures as expected.
  - R284-3 F1 is fixed at every site. The `hdl/` delta is comments only: comment-free `milan_datapath.sv` is identical to `c593cbef`.

## Reconstruction (public state only)

In order, I read:
1. `AGENTS.md`, `CONTRIBUTING.md` (sections 2, 6 and 6.1) and `docs/README.md`.
2. The issue #530 body and every issue comment:
   - the A205 DECISION and BLOCKED;
   - the manager decisions of 2026-09-23 and the processor issue 106 note;
   - the A229, A236, A238, A239 and A241 assignments and REVIEW READY comments;
   - the silicon-rerun note, the [A237] PASS on `c593cbef` and the archive note (`1b3fa460`).
   - The A239 assignment freezes the merge scope: keep both pins and every target and README row, regenerate the diagram with the repository tooling, and make no other change. The A241 assignment freezes round 3: comments and Markdown only, with the comment-free `milan_datapath.sv` identical to `c593cbef`.
3. The PR #549 body at this head (read only). It is open, not a draft, based on `dev`, and GitHub reports it `CONFLICTING` against live dev.
4. The authorities behind the round-3 text:
   - `hdl/milan/milan_datapath.sv:1855-1916,2015-2026,2474-2512,3057,5280-5319,6570-6652`;
   - `hdl/common/csr/milan_csr.sv:348-351,2824-2827,2912-2921`;
   - `REGISTER_MAP.md` rows `0x694`, `0x698` and `0x82C` (`:1524`), and the slope-ordering paragraph `:1105-1135`;
   - `EGRESS_QUEUE_MAP.md:77-106`;
   - `ieee8021q.md:50-72`;
   - `CHANGELOG.md:29-62`.
5. For the merge:
   - `docs/diagrams/submodule_boundaries.gen.py` and `scripts/png_artifact.py`;
   - `syn/yosys/ooc.sh:405-470` (the ROM digest law);
   - `docs/reference/SUBMODULES.md`;
   - `tb/verilator/milan_dp/Makefile` and `README.md`.
6. `git diff 50e78097..f814d37d`, `e65dccfe..44ad6991`, `f86c34fe..44ad6991` and `44ad6991..f814d37d`, with the first-parent history.
7. The public evidence:
   - the tree `9d1b176c` `review-evidence/530-r1` (its manifest; the round-1 author and correction-a236 packets);
   - the `530-review-evidence` branch tip `5f8c585c` (directory listing only);
   - the exact-head hosted state.

My independent pass over the diff and the merge ran first. A draft verdict and ledger were written to this file before I read any prior public review report. The disposition of prior findings follows the ledger.

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - lenses: RTL, Docs - the refused-branch `0x82C` sentence omits the window's index-0 SRP mirror

- **Where:** `hdl/milan/milan_datapath.sv:6615-6619`: "The snap-latched 0x82C talker window holds the AAF sources only, never the CRF output: its gate bit [3] pulses at every index, its lobs bit [2] only at index > 0 ...".
- **Evidence.** The per-index claims are correct:
  - `[3]` is `i_tlk_gate_v[idx]` = `aaf_stream_en_w` (`milan_csr.sv:2917`, `milan_datapath.sv:2478,2017-2026`);
  - `[2]` is `acmp_lobs_v_w[idx]`, which is `listener_observed_w` at index 0 and `lwsrp_stream_gate[gj]` above it (`:1879-1888`, `:2483`);
  - the window spans `N_STREAMS` AAF indices only.

  The same talker word also carries `[27:19]` = `snap_srp9_w`. At index 0 that is `LWSRP_STATUS[8:0]` (`milan_csr.sv:2826-2827,2916`), so `0x82C[25]` mirrors `LWSRP_STATUS[6]` (`|ACTIVE`, which includes the CRF output) and `[27]` mirrors `LWSRP_STATUS[8]`. Read strictly, "never the CRF output" is true of the per-index talker bits but not of this mirror.
- **Why a SUGGESTION and not a MINOR:**
  - Both mirrored bits are already named in the same sentence by their `LWSRP_STATUS` identity, with the correct scope.
  - The authoritative `0x82C` row (`REGISTER_MAP.md:1524`) documents `[27:19]` as the low 9 bits of `A_STRMW_SRP`.
  - No reader is sent to a bit that does not pulse, which was R284-3 F1's defect. This is an omission, and it is resolved by the row it cites.
- **Optional change:**
  - Add ", and at index 0 its `[27:19]` mirror of `LWSRP_STATUS[8:0]` carries `[6]` and `[8]`".
  - For uniformity with the pages round 3 changed, the ADMITTED line `:6600` could read "LWSRP_STATUS[6] (ACTIVE ORed over sources)". It already marks `(|ACTIVE)`.
  - Comments only.

### S2 - SUGGESTION - lenses: Docs - the PR body's image-identity sentence and status block predate the merge

- **Where:** the PR #549 body (manager-owned), in three places:
  - "Linked Issue / roles": "Every `hdl/` change after `c593cbef` is a comment, so the tested image is still the one this head builds."
  - "Status": "GREEN at `e65dccfe` ...".
  - "How to get into the same state": it checks out `e65dccfe`. The disposition table stops at round 2.

  The [A241] REVIEW READY on the issue carries the same identity claim: "The silicon PASS on `c593cbef` covers this head, since the RTL is identical".
- **Evidence:**
  - The merge moves the `gptp-processor` gitlink from `c1b61743` to `e5dcea6e` (#540). That changes `hdl/ucode/gen_gptp_ucode.py` and hence the product's `gptp_ucode.hex`: digest `83f14a7d...` at `c1b61743` and `4afe436d...` at `e5dcea6e` (`syn/yosys/rom_digests.tsv`; receipt 04 regenerates the latter).
  - The parent-owned RTL is comment-identical to `c593cbef` (receipt 09). The image this head builds is not bit-identical to the silicon-tested one.
- **Why a SUGGESTION:**
  - The differing content is dev's own #540 change, reviewed in its own PR. Any merge into current dev carries it.
  - #530's acceptance (no self-Leave, no emission before Listener Ready) does not depend on the gPTP step policy.
  - The claim sits outside the tree, and the manager rewrites the body at publication.
- **Optional change:** say "parent RTL comment-identical to `c593cbef`; the merged image also carries #540's gPTP microcode, which the silicon run did not exercise". Refresh Status, the checkout line and the disposition table to `f814d37d`.

### Observation (not a finding against this PR)

- **The PR conflicts with live dev.** It no longer merges cleanly into `3d2f3e3131c9db5898e1db9dd3e2a35149843109` (#537). `git merge-tree` reports one conflict, in `docs/reference/FR_NFR.md`, on adjacent rows: dev rewrote FR-MVU-01..03, and this PR rewrote FR-CONN-01/02 (`1ac86025`). Dev's side of the FR-CONN row still has the pre-#530 "the CBS/classifier programming ..." text. The candidate resolution must keep dev's FR-MVU row and this PR's FR-CONN row (receipt 14). This belongs to the manager's candidate-merge turn.

## Independent evidence at this head

Receipts are under `receipts/` and scripts under `scripts/`. Local paths are redacted to placeholders. The simulator is the scoped 5.050 build; the wrapper hash and version string are in receipt 00. I confirmed that every build used that root: the three build directories record the same scoped root in `VERILATOR_ROOT`, and the mutant campaign's sub-make inherits the command-line override. Builds ran with at most 8 jobs, in disposable extracted trees under `scratch/` only.

**Merge replay** (receipt 01)
- `git merge-tree --write-tree e65dccfe f86c34fe` conflicts in exactly six paths: `PNG_MANIFEST.json`, `submodule_boundaries.drawio`/`.png`, `SUBMODULES.md`, and the `milan_dp` `Makefile` and `README.md`.
- Outside those six paths, the merge commit's tree equals the automatic merge. There is no hidden edit. The two clean-merged overlaps, `submodule_boundaries.svg` and `rom_digests.tsv`, equal the automatic result.
- Exactly eight files differ from both parents: the six above, `.svg` and `rom_digests.tsv`.

**Union replay** (receipt 05, `git merge-file --union` against base `50e78097`)
- `README.md` differs from the union only by one separating blank line before `## GM step re-base leg (#387)`.
- `Makefile` `.PHONY` and `clean` are the token unions (`gmstep gmstep-build` + `crflic crflic-build crflic-mutants`; `obj_crflic` + `obj_gmstep`). Every recipe from both sides is present.
- `SUBMODULES.md:20-27` takes gPTP `e5dcea6e` and processor `09f9bf38`, and `:96-99` keeps the `e5dcea6e` donor links. The README keeps both Contents rows and both sections. `gen_toc --check` is OK.

**Diagram regeneration** (receipt 03, `scripts/regen_submodule_diagram.sh`)
- Running the generator in write mode at the merge tree reproduces `.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json` byte for byte. The decoded raster sha256 is `920b41da...` = the manifest.
- Rendering each parent's committed SVG with the local renderer reproduces that parent's recorded raster. So the renderer is the one the manifest was made with.
- I inspected the head PNG visually: protocol-processor pin `09f9bf384651`, gptp-processor pin `e5dcea6e351a`.
- Every file was restored afterwards.

**Merge gates** (receipt 02): `submodule_boundaries.gen.py --check` and `--selftest`, `check_diagram_pngs` and `check_submodule_docs` all pass.

**ROM digests** (receipt 04): at the merged pins, `ltn_rom.hex` and `ucode.hex` (processor `09f9bf38`) and `gptp_ucode.hex` (gPTP `e5dcea6e`) all regenerate to the rows `rom_digests.tsv` records. All three MATCH.

**gmstep, head vs dev** (receipt 06)
- `make gmstep` at `f814d37d` and at `f86c34fe` (processor `424c688f`) gives 48 checks and 4 FAIL at both.
- The verdict lists, including every got/exp value, are identical. The four FAILs are the two render re-base checks and the two `mr`/MEDIA_RESET checks, as the README's "It is not in the default sweep yet" paragraph documents.
- So this PR's ACTIVE gate changes nothing on that leg.

**Combined pins, gPTP leg** (receipt 13): `make gptp` at head gives 181 PASS, 0 FAIL on the combination neither parent tested (processor `09f9bf38` with gPTP `e5dcea6e`).

**Round-3 `hdl/` delta is comments only** (receipt 09, `scripts/strip_sv_comments.py`)
- `milan_datapath.sv`, stripped of `//` and `/* */` (string-aware) and whitespace-normalised, has sha256 `327d63f9...` at `c593cbef`, `e65dccfe`, `44ad6991` and `f814d37d`.
- The canary `50e78097` gives `2deefa5a...`, which differs.
- `milan_datapath.sv` is the only `hdl/` file changed since `c593cbef`. Every changed line in `44ad6991..f814d37d` is a `//` comment, with 0 metacomment tokens. All five files are mode 100644, and no gitlink changed.

**Round-3 claims against RTL** (receipt 07 is the patch)
- `CRFT_CTRL[6]`/`[7]` = `crft_res_active_w`/`crft_emit_en_w` (`:5318-5319`).
- `LWSRP_STATUS[8]` = `lwsrp_stream_gate[0]` and `[6]` = `lwsrp_res_active = |pp_cd_srp_active_w` (`:2502-2508,6652`). An OR over sources pulses only while no other source is ACTIVE, as the text says.
- `0x82C[3]`/`[2]` are as stated (S1). The window holds AAF indices only (`8'(acmp_lobs_v_w[N_STREAMS-1:0])`, `:2483`).
- The CHANGELOG (`:37-38,50-51`), `REGISTER_MAP.md:1130-1134,1169-1170`, `EGRESS_QUEUE_MAP.md:99-104` and `ieee8021q.md:66-71` say the same thing.

**Residual search** (receipt 08)
- Every `LWSRP_STATUS[6]` hit at head is marked as the OR, or is the `0x694` field definition.
- The only talker-lobs hit is the scoped `CHANGELOG.md:38`.

**Leg and mutants at head**
- `make crflic` gives 85 checks, 0 failures (receipt 10).
- `make crflic-mutants` gives 4 PASS, 0 FAIL: the clean leg plus three mutants, each caught on its named check (receipt 11). It took 168 s wall.
- The merge's Makefile union does not disturb these targets. Their recipe lines are identical to `e65dccfe` (receipt 15).

**Tests-scope artifacts untouched since `c593cbef`** (receipt 15): `sim_crf_licence.cpp`, `crflic_mutants.py`, `tests/features/milan_streaming_licence.feature`, `tests/steps/milan_streaming_licence_steps.py`, `scripts/measure_test_evidence.py` and `tb/verilator/pp_shadow/sim_main.cpp`.

**Docs and source gates on the head bytes** (receipt 12), all rc 0:
- `docs_check`: 0 findings, scrub 23/23.
- `check_em_dash --base 50e78097` (0 findings over 1100 lines) and `--base f86c34fe` (0 over 269), arms 57/57.
- `check_doc_style`, `gen_toc --check` and `--verify-anchors`, `check_doc_paths` (840 paths), `check_feature_status`, `gen_module_matrix --check`, `check_rtl_source_lists`.
- `xvlog_gate --check`: PASS, 4 == ratchet, 0 in `hdl/`.
- `check_gptp_docs` and `timesync_chain.gen.py --check`.
- `git diff --check` from `50e78097` and from `f86c34fe`.
- `behave features/milan_streaming_licence.feature`: 5 scenarios and 26 steps passed.

**Idiom and evidence gates** (receipt 16), all rc 0: `check_cpp_idiom`, `check_py_idiom`, `measure_test_evidence --check`, `check_hygiene --check`, `check_wire_accountability`, `check_sv_idiom`, `measure_naming --check`, `check_port_contracts`, `measure_fail_fast --check` and `check_todo_ownership`.

**Hosted state at the exact head (read only)**
- 0 check runs, 0 workflow runs and a combined status of `pending` with 0 statuses for `f814d37d`.
- The PR's mergeable state is `CONFLICTING`, which is consistent with no `pull_request` run.
- There was no hosted evidence at this head to distinguish.

**Clone integrity after all work** (receipt 17, `scripts/verify_clone.sh`)
- HEAD, tree and index tree equal the head.
- 876 tracked blobs match in bytes and mode, with 0 assume-unchanged or skip-worktree flags.
- 0 untracked or ignored leftovers. The `__pycache__` directories my gate and generator runs created, one inside `protocol-processor`, were removed before the final check.
- The gitlinks `protocol-processor 09f9bf38`, `gptp-processor e5dcea6e` and `third_party/verilog-axis 48ff7a7e` are checked out at their pins and clean. `external` `efeb541a` is not initialised, as it was in the clone.

## Per-lens results (R284-4, exact head `f814d37d`)

```text
[R284] PASS Conformance - receipts/10 (crflic 85/0 at head: item 1 per-type LeaveAll, item 2 no emission before Listener Ready, item 3 FRAMES_TX), receipts/09 (parent RTL comment-identical to c593cbef, the [A237] silicon PASS image), receipts/02+03+04 (SUBMODULES.md, the diagram and rom_digests.tsv agree with the merged gitlinks 09f9bf38 / e5dcea6e), receipts/13 (gptp 181/0 on the combined pins) - #530 acceptance items 1-3 still met at the merged head; the merge adds no behaviour of its own; the round-3 text states the Milan 5.3.7.3 licence and 5.3.7.7 Table 5.4 effects unchanged from round 3
[R284] PASS RTL - milan_datapath.sv:6570-6652 comment block (ADMITTED/REFUSED) against :1879-1888,1913-1916,2017-2026,2478-2483,2502-2508,5318-5319 and milan_csr.sv:2824-2827,2912-2921 (receipt 07 patch); receipt 09 (comment-only, canary DIFFERENT); gitlinks at head - every bit the refused branch names pulses with ACTIVE for its own source; only S1 (SUGGESTION) remains
[R284] PASS Robustness - receipts/06 (gmstep 44/48 identical to dev, value for value: the ACTIVE gate adds nothing under a GM step), receipts/13 (gptp 181/0 on the untested pin combination), receipts/15 (no logic, harness or step change since c593cbef), milan_datapath.sv:6604-6622 (refused branch: invalid-ordering corner bounded by the window, nothing before a registered Listener) - the merge introduces no new state, reset or configuration path
[R284] PASS Tests - receipts/10 (crflic 85/0), receipts/11 (crflic-mutants 4/4: three mutants caught on their named checks plus the clean control), receipts/06 (gmstep baseline equality), receipts/12 (behave licence feature 5/5), receipts/05+15 (Makefile/README union exact; crflic recipe lines identical to e65dccfe; test sources untouched since c593cbef) - the merged Makefile keeps every target and clean entry of both sides
[R284] PASS Docs - CHANGELOG.md:29-62, REGISTER_MAP.md:1128-1135,1169-1170,1524, EGRESS_QUEUE_MAP.md:97-106, ieee8021q.md:62-72, milan_datapath.sv:6597-6622 comments, SUBMODULES.md:20-27,96-99, milan_dp README.md:37-45,342-493, submodule_boundaries.{drawio,svg,png}+PNG_MANIFEST.json (receipts 03, 05, 08, 12) - R284-3 F1 and S1 fixed at every site, the merged pages carry both pins and both legs, gates green; S1 and S2 are SUGGESTIONs
```

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #530 acceptance against `obj_crflic` at head (receipt 10); parent RTL comment-identical to the silicon-tested `c593cbef` (receipt 09); gitlinks, `SUBMODULES.md`, diagram and ROM digests (receipts 02-04); `gptp` leg on combined pins (receipt 13) | R284-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| RTL | CLEAN | `milan_datapath.sv:1879-1888,1913-1916,2017-2026,2478-2483,2502-2508,5318-5319,6570-6652`; `milan_csr.sv:2824-2827,2912-2921`; receipts 07 and 09 | R284-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Robustness | CLEAN | `gmstep` head vs dev (receipt 06); `gptp` combined pins (receipt 13); refused-branch bound `milan_datapath.sv:6604-6622`; no logic, harness or step change since `c593cbef` (receipt 15) | R284-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Tests | CLEAN | `crflic` 85/0, `crflic-mutants` 4/4, `gmstep` baseline equality, behave licence 5/5; merged `Makefile`/`README.md` union (receipts 05, 06, 10, 11, 12, 15) | R284-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Docs | CLEAN | `CHANGELOG.md`, `REGISTER_MAP.md`, `EGRESS_QUEUE_MAP.md`, `ieee8021q.md`, in-RTL comments, `SUBMODULES.md`, `milan_dp` `README.md`, submodule diagram and manifest, PR body (read only); receipts 03, 05, 08, 12 | R284-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |

Every lens is covered clean at the exact head. S1 and S2 are SUGGESTIONs and do not affect coverage.

## Prior public findings on this PR, resolved or retained at this head

I read these after the verdict and draft ledger above were written.

| item | disposition at `f814d37d` | basis |
|---|---|---|
| **R284-3 F1**, MINOR (RTL, Docs): the refused-branch paragraph said the `0x82C` talker lobs pulse with ACTIVE | **RESOLVED.** `milan_datapath.sv:6613-6619` now names each bit against its own source. The window holds AAF sources only, never the CRF output. `[3]` pulses at every index, `[2]` only at index > 0, and index 0's lobs is source 0's registered Listener level. The CHANGELOG scopes the lobs "above index 0" (`:38`). No logic changed | receipts 07, 08, 09; `milan_csr.sv:2917-2918`; `REGISTER_MAP.md:1524`; S1 records the one optional addition |
| **R284-3 S1 = R285-3 S1** (Docs): `LWSRP_STATUS[6]` listed as the CRF output's own bit | **RESOLVED** on the three named pages, the `0x694[9]`/`0x698` rows and the CHANGELOG (`:51`) | receipt 08 |
| R285-3 S1 (RTL, Docs): the same lobs overstatement as R284-3 F1 | **RESOLVED** with R284-3 F1 | as above |
| R284-3 S2 (Docs, PR body): the Contents line and first Definition of Done box | **RESOLVED.** The body's Contents says "closes #530; the silicon rerun passed at `c593cbef`", and the first box reads the same | PR body read at this head; the body's post-merge staleness is S2 of this round |
| R284-1 F1/F2 = R285-1 F1/F2, R284-2 F1 = R285-2 F1 | Stay **RESOLVED** as recorded in rounds 2 and 3. Round 3 touches only the lines in receipt 07, which reintroduce none of them | receipts 07, 08 |
| R284-2 S1, R284-2 S2 = R285-2 S1, R284-1 S1/S2, R285-1 S1/S3, R285-2 builder observation | Retained as SUGGESTIONs or observations, unchanged. No coverage effect | receipt 07 (not touched) |

## Limits

- Physical calibration and hardware: NOT RUN by this round. The [A237] silicon PASS is on `c593cbef`. At this head, parent-owned RTL is comment-identical to it (receipt 09), but the image also carries #540's gPTP microcode (S2). Field skips are not hardware proof. I did not audit the silicon archive beyond the published comments.
- The refused-branch corner rests on reading RTL. No bench stages it, and I built none. #551 owns that design question.
- Not run, per scope: the full parent, processor, gPTP, Yosys and builder banks; the other `milan_dp` legs; `pp_shadow`; the full BDD suite; the old-pin and gate-reverted failing arms (unchanged since round 1); `lint_rtl`; act, Docker and hardware.
- The specification text (Milan v1.2, 802.1Q) was not re-read. Round 3's text makes no new clause claim.
- The review brief says the manager's full source static/builder and native banks passed at this head. I found no public receipt for them at `f814d37d`: not in tree `9d1b176c`, not at the `530-review-evidence` tip `5f8c585c` (listing only), and not in any issue or PR comment. This round does not rely on them.
- No hosted run existed at the exact head when I queried it.

## Pending manager duties

- Candidate-merge validation against live dev `3d2f3e3131c9db5898e1db9dd3e2a35149843109`. The PR is `CONFLICTING`. Resolve `docs/reference/FR_NFR.md` by keeping dev's FR-MVU-01..03 row and this PR's FR-CONN-01/02 row (receipt 14), then run the post-merge containment.
- Exact-head (or candidate-head) hosted evidence: `rtl-fast`, and after the PR is marked ready, `verilator-suites` and `yosys-portability`. Also act acceptance.
- Publish the bank receipts for this head, if they are to be cited as evidence.
- Optional: refresh the PR body per S2, and triage S1 together with the retained suggestions.
- A second independent positive review at this head (R285-4), then closing #530 through "Closes #530" on merge and moving it to Done.

Publishable receipts and scripts are listed in `MANIFEST.sha256`. Disposable trees and fetched comment copies live only under `scratch/`.

R284-4 FINISHED
