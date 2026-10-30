# [A707b] FPGA-gPTP #96 documentation sweep, round 2: handoff

Status: REVIEW READY. Nothing pushed; PR #97 not edited (not allowed in this lane).

- Repository: Mister-M-alt/FPGA-gPTP, branch `96-docs-sweep` (PR #97 head on the remote is still `86073476`)
- Base: main `135afd043309369a87ddbc8d6550aff8ec52a157`
- Round 1 head: `8607347675743fe8d1ccaa370c63905c5ca1ccd5`
- **Round 2 head: `806957b35c3c23a36505744d205f9692720d19e2`** (local only, 8 commits on top of `86073476`; no rebase, no force)
- TAKEN on #96: issuecomment-6520396161
- REVIEW READY on #96: issuecomment-6520923345
- Brief: the [A10] round 2 comment on #96, which covers R739-1 F1 to F5 and R740-1 F1 to F4. Round 1 handoff: `gptp96-a707/HANDOFF.md`.

## Commits in this round (one-line subjects, no body, no trailers)

| Commit | Subject | Resolves |
|---|---|---|
| `08f171c` | Cite 802.1AS-2011 11.4.4 and 11.4.7 for the Follow_Up companions, not the Sync clause | R740-1 F4 = R739-1 F1 |
| `1e0c4d7` | State that publication outputs are sampled on pub_commit_o and can change while microcode stages them | R740-1 F1 = R739-1 F3, plus R739-1 RES-1 to RES-3 |
| `2d91d72` | Link the archived PR #76 measurement reports themselves at parent 4999d8d6 | R739-1 F2 |
| `4f82b02` | Find constants and ROM rows by name, and report a formatted, missing or duplicate row | R740-1 F2 = R739-1 F4, R739-1 S-3 |
| `2e2643e` | Name each protocol constant and link its row instead of restating its value | R740-1 F3 = R739-1 F5 |
| `bcdfce9` | Fail the docs gate when a current page restates a unit-bearing protocol constant | R740-1 F3 = R739-1 F5 (keeps copies out) |
| `0a079c2` | State the constants table's row and copy rules beside the table | Doc of the gate's guarantee |
| `806957b` | Make each constants and ROM self-test arm isolate the rule it names | Self-test strength (two checker mutants survived before it) |

Delta `86073476..806957b`: 10 files, +263/-72.
- Eight Markdown files: README, GLOSSARY, INTEGRATION, HDL_DEVELOPER, TEST_DEVELOPER, MANAGER, SOURCE_EVIDENCE, and the history page RESOURCE_DELTAS_2026_10.
- Two docs-gate scripts: `scripts/check_docs.py` and `scripts/check_source_evidence.py` (one claim key renamed).
- No RTL, generator, generated file, test, Makefile or build input changed: `git diff --stat 86073476 HEAD -- hdl tb bench syn Makefile` is empty.

Whole PR `135afd04..806957b`: 14 files. 12 are Markdown; the other two are the two docs-gate scripts.

## Acceptance (issue #96)

| Item | Met | Evidence |
|---|---|---|
| Every document has a status | Yes | `docs/README.md` "Document status" covers all 14 maintained pages and the archive. `make docs` fails on a missing, wrong, duplicate or dangling row. The 18 archive pages carry Historical banners, which the archive check enforces. |
| No current document contradicts the code or a clause | Yes, for every contradiction found | Round 1 fixed C1 to C7. This round fixes the Follow_Up clause and the publication-timing claim, the two contradictions both reviews found. |
| Start-here path exists | Yes | `README.md#start-here`, `docs/GLOSSARY.md`, and a summary at the top of each long page. |
| Docs gates pass | Yes | All repository gates are rc 0 at base `86073476` and at head (gate table below). |
| Rule: values in one table, linked, never copied | Yes | Every constants-table value outside its row was replaced by the constant's name and a link to the row. A new rule fails `make docs` if a unit-bearing value comes back. The remaining numbers are not copies; see "Single-source decisions". |

## Review findings: resolution at head

### R740-1 F4 = R739-1 F1: Follow_Up clause

- `docs/GLOSSARY.md:19` now reads `| Follow_Up companion | Two-step timestamp message: Follow_Up or Pdelay_Resp_Follow_Up | 11.4.4, 11.4.7 |`.
- Authority, read in the 802.1AS-2011 text:
  - 11.4.3 is Sync.
  - 11.4.4 is Follow_Up (Table 11-9; preciseOriginTimestamp 11.4.4.2.1).
  - 11.4.7 is Pdelay_Resp_Follow_Up.
  - Cor1 and Cor2 keep that numbering; Cor1's PICS rows MDFDPP-15 and -16 cite 11.4.3 for Sync and 11.4.4 for Follow_Up.
- The term covers both companions: `docs/INTEGRATION.md:219` says "Responses and both companions always keep service". So both clauses are cited, per R739-1's required outcome.

### R740-1 F1 = R739-1 F3: publication timing

- **RTL facts.**
  - `hdl/top/KL_gptp_engine.sv:994-997` writes `pub_gm_r`, `pub_parent_r` and `pub_flags_r` on separate state-port writes, and `:1037-1053` writes the path.
  - `:1134-1146` assigns those registers straight to `pub_*_o`, with `pub_commit_o = ucpu_commit_w || boot_pub_commit_r`. No register holds the outputs at commit.
  - Microcode stages before `COMMIT`: for example `gen_gptp_ucode.py:1940-1953`, where BECOME writes publish words 0, 1 and 6, then `COMMIT`.
- **Doc changes.**
  - `docs/INTEGRATION.md:16` (summary): "Sample publication outputs on `pub_commit_o`; they change while staging."
  - `docs/INTEGRATION.md:557-567` (Publication): states that each output follows its staging register, no register holds them at commit, fields are written over several instructions, outputs can show a partial tuple between pulses, and only the commit cycle presents a complete tuple.
  - `docs/INTEGRATION.md:623`: "The grandmaster and its path complete in one commit." It previously said they "change in one commit".
  - `docs/HDL_DEVELOPER.md:12` (summary), `:319`, `:321`: `OP_COMMIT` marks the staged tuple complete; staging writes reach the outputs at once.
  - Equivalent claims reconciled, as R739-1 asked:
    - `README.md:60`;
    - `docs/MANAGER.md:20` and `:34` (the latter said "Atomic commit pulse");
    - `docs/GLOSSARY.md:36`.
- **Residue, also fixed.**
  - RES-1, `docs/INTEGRATION.md:14-15`: PHC step and rate writes are pulses; `phc_slew_active_o` is a level.
  - RES-2, `:12-13`: credit gates initiating transmissions; a low `port_enabled_i` starts no frame (matches `:233`).
  - RES-3, `docs/MANAGER.md:45`: "latest dated synthesis figures".

### R739-1 F2: archive evidence link

- `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32` now reads "The parent tree at `4999d8d6` holds the [measurement reports](tree URL)". The visible text is label-free.
- The URL is the tree path base `docs/MANAGER.md:70` linked: `review-evidence/.../author` at `4999d8d6`.
- Listing it at that commit shows the `.rpt` files: `baseline-engine_timing.rpt`, `baseline-engine_util.rpt`, `candidate-engine_timing.rpt`, `candidate-engine_util.rpt` and the `ucpu_util` reports.
- The archive rule "preserve commit references for reproducibility" is restored. No content was added.

### R740-1 F2 = R739-1 F4: constants gate escapes

`scripts/check_docs.py`:
- `CONSTANT_ROW_RE` now matches a row by its backticked name alone, so the value cell can hold anything.
- `decimal()` accepts only plain or comma-grouped decimals. Anything else is a named finding, for example "SYNC_RTO_MS_C value '**376**' is not a plain decimal".
- `CONSTANTS` lists the 17 expected names, so a deleted row, or a row whose name lost its backticks, fails with "no protocol constant row for NAME".
- ROM budget rows are found by image name the same way, then parsed strictly. A duplicate row fails; R740-1's supplementary duplicate-identical-row probe is now caught.
- `load_generator` sets `sys.dont_write_bytecode`, so `make docs` no longer writes `hdl/ucode/__pycache__/` (R739-1 S-3). Verified: the directory was removed, `make docs` ran without the environment override, and the directory did not reappear.

### R740-1 F3 = R739-1 F5: copied values

- Every copy in both reviews' lists, plus a fresh audit grep, now names the constant and links its row (commit `2e2643e`). The audit covered unit-converted and spelled-out forms (`20 us`, `five-minute`, `fifth`, `two good exchanges`, `0.5 s`, `bit 32`, `1022`).
  - **INTEGRATION.**
    - `:277`, `:279`: ASCAP_UP_C, CEASE_MS_C.
    - `:366-371`: the threshold table now names STEP_LINKUP_NS_C and STEP_LOCKED_NS_C.
    - `:385`, `:406`, `:410`: SYNC_RTO_MS_C and the named thresholds.
    - `:418-452`: RATE_PPM_C, the formula written with `RATE_PPM_C`, and `STEP_LOCKED_NS_C / RATE_PPM_C` ms in place of "0.5 s".
    - `:464`: SLEW_SETTLED_NS_C.
    - `:501`, `:503`, `:515`, `:543`: the event table, "slew watchdog", "applicable step threshold".
    - `:721-765`: announceReceiptTimeout, SYNC_RTO_MS_C, FU_RTO_MS_C.
    - `:809-819`: "Pdelay_Req interval" and LOST_CLEARS_AT_C.
    - `:838`: `--p1 248` dropped from the command; `P1_C` is named as the default. The documented command still runs (rc 0, 1,022 words).
  - **HDL.** `:166`, `:172`, `:174`, `:203`, `:255`.
  - **TEST.** `:129`, `:143`, `:147-148` (the 250 ms and 60 ms figures are now labelled stimuli), `:154-155`.
  - **MANAGER.**
    - `:47`, `:49`: the copied commit, date and 100 MHz now point at the HDL table.
    - `:64-66`: thisClock's words point at ROM_CID_HI_C.
  - **SOURCE_EVIDENCE.**
    - `:26`: "Microcode ROM depth". The `check_source_evidence.py` key was renamed with it, and it is still 20 exact anchors.
    - `:42`: "Lost-response limit clears asCapable".
- New rule `copy_findings` (commit `bcdfce9`):
  - The units come from the table itself: a Meaning cell ending ", ms", ", ns" or ", ppm".
  - For each such constant it builds the plain, comma-grouped, next-unit (ms to s, ns to us/µs) and spelled-minute forms of the live generator value.
  - It rejects them on every current page outside the "Protocol constants" section and outside fenced code.
  - Limit: a wrong value written fresh (for example "376 ms", never the true value) is not a copy and is not caught. No green state can hold a copy for the generator to drift away from, because the true value is rejected while it is true.
- `docs/INTEGRATION.md:856-860` states these row and copy rules beside the table.

## Single-source decisions (numbers that remain, and why they are not copies)

- **ROM budget table** (`docs/MANAGER.md:61-62`, "1,022 of 1,024"): generator output, bound by `rom_findings` to the generator's own word count and depth on every `make docs`.
- **Cadence table** (`docs/INTEGRATION.md`, same "Protocol constants" section): literals inside generator legs, held once under the table heading. They are still not machine-checked, as the page says.
- **Test values** (the `--cease-ms` engine-suite value; "250 ms", "60 ms" stimuli): test inputs, not configuration values, and labelled as such.
- **Standard and structural facts**, not generator constants:
  - priority1 255 (gmPresent);
  - "Sixty-four" scratch words, "Four-entry" queue, "Eight timer slots", "Sixteen registers" (RTL sizes, gate-bound line anchors in SOURCE_EVIDENCE);
  - "last two words" of the ROM;
  - "two-pair completion" (Issue #75 policy, no generator constant in the table).

## Inventory (round 2 head)

Status legend:
- **Current**: checked at head against the source and against IEEE 802.1AS-2011 with Cor1/Cor2 and Milan v1.2 chapter 4.
- **Historical**: archived and bannered.

The full per-page purpose, audience and evidence is in the round 1 handoff. The table below gives the status at this head and the round 2 evidence.

| Page | Lines | Purpose / audience | Describes | Status | Round 2 evidence |
|---|---:|---|---|---|---|
| `README.md` | 98 | Start here; every reader | Scope, layout, risks | Current (edited) | `:60` publication line matches `KL_gptp_engine.sv:1134-1146`. |
| `docs/README.md` | 88 | Map and status table; every reader | All pages | Current | Status gate rc 0. |
| `docs/GLOSSARY.md` | 52 | Defined terms; every reader | 802.1AS-2011, Milan 4.2.6, engine terms | Current (edited) | `:19` 11.4.4/11.4.7 read in the 2011 text. `:36` matches the commit semantics. |
| `docs/MANAGER.md` | 127 | Readiness, ROM budget; manager | Delivery status | Current (edited) | ROM table gate-bound, strict parse. `:20`, `:34`, `:45-49`, `:64-66` edited. |
| `docs/INTEGRATION.md` | 916 | External contract; integrator | Ports, policy, publication, constants | Current (edited) | 17 constants rows gate-bound by name. No unit-bearing copy remains (copy rule rc 0). Publication text matches the RTL lines above. |
| `docs/HDL_DEVELOPER.md` | 418 | Structure, invariants; HDL contributor | `hdl/` | Current (edited) | `:12`, `:319-321` match the output assigns. Constants are linked. |
| `docs/TEST_DEVELOPER.md` | 217 | Verification layers; test developer | `tb/`, `bench/`, `scripts/` | Current (edited) | Stimuli are labelled. Constants are linked. Suite tallies are unchanged. |
| `docs/SOURCE_EVIDENCE.md` | 59 | Claim-to-source ledger; reviewer | RTL and generator anchors | Current (edited: two claim names) | `check_source_evidence.py`: 20 exact, 0 findings; selftest 7 arms. |
| `docs/diagrams/README.md` | 81 | Diagram sources; maintainer | `docs/diagrams/` | Current (unchanged) | Diagram check and selftest rc 0. |
| `tb/verilator/engine/README.md` | 20 | Suite entry; test developer | Engine suite | Current (unchanged) | 2048 × 3 + 60 pass. |
| `tb/verilator/parser/README.md` | 24 | Suite entry | Parser suite | Current (unchanged) | 378 + 16 pass. |
| `tb/verilator/ucpu/README.md` | 18 | Suite entry | MicroCPU suite | Current (unchanged) | 768 pass. |
| `tb/verilator/gaskets/README.md` | 20 | Suite entry | Gasket loopback | Current (unchanged) | 81 + 5 pass. |
| `tb/tsngen/README.md` | 20 | Suite entry | Independent decode | Current (unchanged) | 288 + 4 pass, not skipped. |
| `docs/history/v1/README.md` + 18 pages | - | Archive | Superseded records | Historical | Archive check rc 0. `RESOURCE_DELTAS_2026_10.md:32` link repaired (57 lines). |

## Findings the docs cannot fix (source comments; for a code lane)

| # | Location | Observation | Clause / source | Which side is wrong |
|---|---|---|---|---|
| G1 (new) | `hdl/top/KL_gptp_engine.sv:43-45` | The header says the publish bank "becomes wires, latched by OP_COMMIT". No latch exists: `:1134-1146` assign the staging registers straight to `pub_*_o`, and `pub_commit_o` is a separate pulse. The assertion comment at `:874-876` agrees that raw state changes before publication. | RTL `:994-997`, `:1037-1053`, `:1134-1146` | The source comment. The RTL is what R739-1 and R740-1 confirmed, and the docs now match the RTL. |
| G2 (new) | `hdl/ucode/gen_gptp_ucode.py:2499` | The `--p1` CLI default is the literal `248`, a second home beside `P1_C = 248` at `:513`. Changing one would not change the other, and the docs gate reads `P1_C`. | Milan v1.2 4.2.6.2.1 (default priority1) | The generator; it should use `default=P1_C`. The docs are right today. |
| F1 (round 1) | `gen_gptp_ucode.py:284` | History note says asCapable falls "at the fourth" lost response. The code clears at `LOST_CLEARS_AT_C`. | 802.1AS-2011 Figure 11-8 as Cor1 changes it | The source comment. |
| F2 (round 1) | `gen_gptp_ucode.py:292-296` | History note says syncReceiptTimeout "clears the sync-ok verdict". Since #89 it ages when gmPresent. | 10.3.11, Figure 10-13 (Cor1) | The source comment. |
| F3 (round 1) | `gen_gptp_ucode.py:315-317` | History note lists the Milan 4.2.6.2.5 cease as "still deliberately out". It is implemented. | Milan v1.2 4.2.6.2.5 | The source comment. |
| F4 (round 1) | `KL_gptp_engine.sv:43-45` | A repeated phrase: "becomes direct fabric wires becomes wires". Same lines as G1. | n/a | Source comment wording. |
| F5 (round 1) | `docs/HDL_DEVELOPER.md` OOC table | The figures are dated (main `5dce647a`, 2026-10-11); later RTL has landed. | n/a | Neither; needs `make ooc` with the synthesis tool. |

## Planted defects (every new check fails a planted mutant)

The probe script (`receipts/plant_probes.py`) copies `git archive` of the head into a fresh scratch tree for each probe. For each tree it runs the head checker, and the round-2 base checker (`86073476`) as a comparison. Log: `receipts/plant_probes.log`, probe failures 0.

| Real-tree defect | Head rc | Base checker rc | Head finding |
|---|---:|---:|---|
| control (unmutated) | 0 | 0 | PASS |
| `SYNC_RTO_MS_C` 376 | 1 | 1 | is 376, generator has 375 |
| `**376**` | 1 | 0 | value '**376**' is not a plain decimal |
| `-1` | 1 | 0 | value '-1' is not a plain decimal |
| `376 ms` | 1 | 0 | value '376 ms' is not a plain decimal |
| row deleted | 1 | 0 | no protocol constant row for SYNC_RTO_MS_C |
| name not backticked | 1 | 0 | no protocol constant row for SYNC_RTO_MS_C |
| generator `SYNC_RTO_MS_C = 376`, docs untouched | 1 | 1 | is 375, generator has 376 |
| ROM `**1,021** of 1,024` | 1 | 1 | Shipping row ... is not plain 'N of M' |
| identical duplicate ROM row | 1 | 0 | duplicate ROM budget row: Shipping |
| HDL prose "375 ms" re-added | 1 | 0 | '375 ms' restates SYNC_RTO_MS_C |
| threshold table "20 us" restored | 1 | 0 | '20 us' restates STEP_LINKUP_NS_C |
| "five-minute countdown" restored | 1 | 0 | 'five-minute' restates CEASE_MS_C |
| TEST "200 ppm" restored | 1 | 0 | '200 ppm' restates RATE_PPM_C |
| band "-100 ns through +100 ns" restored | 1 | 0 | '100 ns' restates SLEW_SETTLED_NS_C |
| status row names a missing page | 1 | 1 | status row names a missing page |

Checker mutants: each edits `check_docs.py` in a fresh copy; `--selftest` must fail.

| Checker mutant | Selftest | Arm that catches it |
|---|---|---|
| required-name set emptied | rc 1 | deleted constant row escaped |
| round-1 numeric-only row regex restored | rc 1 | bold constant cell escaped |
| `decimal()` strips markup and sign | rc 1 | bold constant cell escaped |
| constants section not excluded from the copy rule | rc 1 | linked constant or its home row failed |
| no ns to us conversion | rc 1 | converted constant copy escaped |
| no spelled minutes | rc 1 | spelled constant copy escaped |
| duplicate ROM row ignored | rc 1 | duplicate ROM row escaped |

- Before `806957b`, two checker mutants survived: the round-1 row regex and the ignored ROM duplicate. Their arms were satisfied by another rule. `806957b` makes each arm require its own diagnostic, and both now fail.
- Self-test: 23 arms at round 1, 41 at head.

The reviewers' own probes (R739-1 `scripts/`) were run against the head. The run used a copy whose `/tmp` temp file was moved to scratch. Logs: `receipts/reviewer_*`.
- `reconcile_probes.sh`:
  - the three formatted or negative cells now fail (rc 1);
  - the control passes;
  - the two drift probes are no-ops, because the copies they edit no longer exist.
- `plant_probes.sh`:
  - every expect=fail probe fails, and both expect=pass controls pass;
  - the two former "limit" escapes (deleted row, reformatted cell) now fail;
  - the cadence-literal limit still passes, because the cadence table is unchecked and the page says so.
- One probe, `row_for_missing_page`, first returned rc 0 because of my quoting change to that copy: `$WORK` landed inside a single-quoted `sed` script, so no row was inserted. Re-run correctly, it returns rc 1. The receipt records both runs.

## Gate table

Environment:
- Verilator 5.050 (pinned build, identity checked).
- Python 3.14.
- `TMPDIR` and all copies under scratch.
- Every command ran in the foreground, unpiped, with output redirected to a log and rc taken from the command.

### Repository gates

The repository has no hosted workflow files. The docs and CI-hygiene gates are the Makefile targets plus `git diff --check`.

| Gate | Base `86073476` | Head `806957b` |
|---|---|---|
| `make docs` | rc 0 (selftest 23 arms; 20 exact) | rc 0 (14 current, 18 historical; selftest 41 arms; source evidence 20 exact, selftest 7) |
| `make diagrams-check` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `git diff --check` from `135afd04` | rc 0 | rc 0 (also rc 0 from `86073476`) |
| `make -C tb/verilator/ucpu` | rc 0 (768) | rc 0 (768) |
| `make -C tb/verilator/parser` (run + mutants) | rc 0 (378, 16) | rc 0 (378, 16) |
| `make -C tb/verilator/engine run` | rc 0 (2048 × 3, 60) | rc 0 (2048 × 3, 60) |
| `make -C tb/verilator/gaskets` (run + mutants) | rc 0 (81, 5) | rc 0 (81, 5) |
| `make -C tb/tsngen` (run + mutants) | rc 0 (288, 4; no skip) | rc 0 (288, 4; no skip) |
| `make -C bench/arty test` | rc 0 | rc 0 |
| `make -C tb/verilator/engine mutants` | NOT RUN | NOT RUN |
| `make ooc` | NOT RUN | NOT RUN |

- Base suites ran in a `git archive` copy of `86073476` under scratch, since removed. Head suites ran in the lane.
- **Engine mutants:** about 137 full rebuilds, longer than one foreground command allows. Their inputs are byte-identical between base and head.
- **`make ooc`:** needs the synthesis tool.

### Parent consumer gates

These are required because two docs-gate scripts changed.

Setup:
- A scratch clone of kebag-logic/milan-fpga at PR #805 head `e06ade31`, with submodules.
- The gptp-processor checkout was set to each SHA and the gitlink set with `update-index`. `--show-toplevel` was verified before each git command.
- Restored to the `f97c1803` pin afterwards. Nothing was committed or pushed.
- Script: `receipts/parent_gates.sh`.

| Gate | Gitlink `f97c1803` (PR #805 pin) | Gitlink `86073476` | Gitlink `806957b` |
|---|---|---|---|
| `check_gptp_docs.py` | 0 | 1 | 1, findings identical to `86073476` |
| `check_gptp_docs.py --with-submodule` | 0 | 1 | 1, identical |
| `check_gptp_docs.py --selftest` | 0 | 1 | 1, identical |
| `make -C gptp-processor docs` | 0 | 0 | 0 (41 arms) |
| `check_submodule_docs.py` | 0 | 1 | 1, identical |
| `check_submodule_docs.py --selftest` | 0 | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 | 0 |
| `measure_fail_fast.py --check` | 0 | 0 | 0 |
| `measure_test_evidence.py --check` | 0 | 0 | 0 |
| `check_hygiene.py --check` | 0 | 0 | 0 |
| `check_gptp_docs.py --with-submodule`, parent docs re-pinned from `f97c1803` to the gitlink (13 files, scratch only, restored) | n/a | 0 | 0 |

- **The rc 1 rows are pin-driven, as in round 1.**
  - The parent pages deep-link to `f97c1803` ("donor reference must use gitlink ...").
  - `check_submodule_docs.py` compares the documented pin and the boundary diagram.
  - The findings at `86073476` and `806957b` are byte-identical once the SHA is normalised.
- With the parent pins rewritten, as an adopting PR would do, the gPTP-docs gate passes at both: "8 current pages, donor checkout verified".
- The parent needs only that the submodule doc paths exist and that its anchors resolve. No heading changed this round.

## Not done / follow-ups

- Engine mutation arm and `make ooc`: not run (see above).
- G1, G2 and round 1 F1 to F4: source-comment or generator cleanups for a code lane. F5: re-measure OOC.
- R739-1 S-2 was not taken. The suggestion is to check the `--sync-seq-seed 0x10000` image as well as `--seq-seed 0x200000`. Both build 1,023 words today. A new check needs a planted mutant, and that would mean editing the generator.
- The cadence table stays literal and unchecked; the page says so. Binding it needs generator constants (a code change).
- The parent bump must re-pin the parent gPTP docs and the submodule-docs page and diagram.

## Postings on #96

- TAKEN: issuecomment-6520396161
- REVIEW READY with head `806957b35c3c23a36505744d205f9692720d19e2`: issuecomment-6520923345
