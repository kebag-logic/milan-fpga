[R831] NEGATIVE - exact head e18c822536ebeaf1cb0f42abea74513501aa26c7

# R831-1: internal cleared-context review of PR #893 (issue #883)

- Head `e18c822536ebeaf1cb0f42abea74513501aa26c7`, tree `be1aea4667ad7572f109c68fb492a7c15c45ab56`, source base dev `46c971fa`.
- Live dev is `fa6c094b`. Compared with `46c971fa` it is 4 ahead, 0 behind, and changes only `docs/testing/CI_WORKFLOWS.md` and `scripts/act_ci.py`. It shares no file with this PR (`receipts/dev_46c971fa_to_fa6c094b.txt`).
- Order of reconstruction:
  1. AGENTS.md and CONTRIBUTING.md (2.2, 3, 5, 6).
  2. docs/README.md.
  3. The #883 body, the TAKEN and STOP comments, the option (b) ruling (issuecomment-6805166676) and REVIEW READY.
  4. The clause texts: IEEE 802.1Q-2018 10.7.6.3, 10.7.7 with Table 10-3, 10.7.8 with Table 10-4, and 10.7.9 with Table 10-5; Milan v1.2 Table 4.3; IEEE 1722.1-2021 6.2.2.15, Figure 6-2 and Table 7-2.
  5. NFR-RES-01 and AREA_BUDGET.
  6. `git diff 46c971fa..e18c8225` and its 15 one-line commits.
  7. The public author packet at `e99c3d13` (`review-evidence/883-r1`).
- Prior public review findings on this PR: none existed when this round read the thread. The only comments were the two review-start notices (6806806298, 6806812291), and there were no PR reviews. So nothing is carried in or retained.
- No manager source bank is claimed or inferred. Every execution below is this reviewer's own, at the exact head or in a disposable old-pin copy of it.

## Verdict basis

One MINOR finding is open (F1, under Tests and Robustness), so the verdict is NEGATIVE.

Everything the issue's frozen acceptance asks for was reproduced or verified:
- the processor fast-forward and the gPTP revert;
- [MRPAPP], [MVRPLA] and [AIDX] passing at the new pin and failing at the old one, each by its own words;
- every campaign arm caught: crflic-mutants 16 of 16, gsi-mutants 19 of 19;
- the route record's internal consistency;
- the ROM ledger and the doc gates.

F1 is a one-pattern fix in the parent C++ idiom gate: the #495 residue fix this PR carries removes a detection the gate had at dev. There are also two RESIDUE wording rows and three SUGGESTIONs.

## Findings

### F1 - MINOR - Tests, Robustness - `scripts/check_cpp_idiom.py:270-271` (selftest arms `:706-710`): the brace-initialiser fix stops counting a multi-declarator line whose initialiser nests braces

- **Authority and evidence:**
  - #495 row 6758088112 asks the gate to "exclude commas inside `{...}` initializers". AGENTS.md section 8 says never to weaken a test.
  - The new `_DECL_TEXT = (?:[^;(){}\n]|\{[^{}\n]*\})*` admits only a flat `{...}`. On any line with a nested `{`, the whole pattern fails to match, commas between declarators included.
  - Probe `scripts/probe_cpp_edges.py` against `scripts/probe_cpp_edges_old.py` (dev `46c971fa`'s pattern swapped into the head's `scan()`), on `int a[2][2] = {{1, 2}, {3, 4}}, b = 0;`: the head counts 0, dev counted 1 (`receipts/probe_cpp_edges.log`, `receipts/probe_cpp_edges_old.log`).
  - The flat cases are right: `uint32_t x[3] = {1, 2, 3};` gives 0, and `int a{1}, b{2};` and `int a = 1, b = 2;` give 1.
  - No selftest arm covers nested braces, so the selftest passes 78 of 78 with the blind spot in place (`receipts/cpp_idiom_selftest.log`).
  - Nested brace initialisers are in active use in the tree's C++ (for example `tb/verilator/csr/sim_lock.cpp:471`, `tb/verilator/media_phase/sim_render.cpp:194`).
- **Impact:** a two-declarator line with a nested initialiser now escapes the multi-declarator ratchet. Dev's gate counted it, and nothing in the selftest would notice if it regressed further. The tree count is 0 under both patterns today (`receipts/cpp_idiom_tree.log`, `receipts/probe_cpp_old_regex_tree.log`), so no existing line is hidden.
- **Required outcome:**
  - The rule ignores commas inside a brace initialiser at any nesting depth the gate claims to read, or at least one nested level.
  - Commas between declarators still count on such a line.
  - Selftest arms pin both cases: the nested single declarator gives 0, the nested two-declarator line gives 1.
- **Verification:**
  - `python3 scripts/check_cpp_idiom.py --selftest` passes with the new arms.
  - `scripts/probe_cpp_edges.py <repo>` prints 1 for the nested two-declarator line and 0 for the nested single one.
  - The planted dev pattern (`scripts/probe_cpp_old_regex.py <repo> --selftest`) still fails "a brace initialiser's commas separate elements, not declarators (#495)". Today it fails it, 77 of 78 (`receipts/probe_cpp_old_regex_selftest.log`).
  - The tree scan stays at `multi-declarator declaration: 0 <= 0`.

### R1 - RESIDUE - Docs - PR #893 body, "#495 rows" table, row 6731336971

- **Problem:** the row is described as "the milan_dp Makefile's `crflic-mutants` comment omits the #851 arm | Taken with this PR's own comment edit". Row 6731336971 has four items.
  - The Makefile item is taken: `tb/verilator/milan_dp/Makefile:667-670` now names the #851 arm.
  - The baseline JSON item is moot, because the route note was rewritten.
  - Two items are still in the tree at this head: `docs/reference/SUBMODULES.md:813` "Dev `0a75aa77` is #843's record." and `docs/testing/TESTING.md:357` "the three gate mutants" (see R2).
- **Exact fix (PR body):** "6731336971: its Makefile item is taken here (`tb/verilator/milan_dp/Makefile:667-670`); its JSON item is moot (the route note is rewritten); its `SUBMODULES.md:813` and `TESTING.md:357` items stay open on #495." Alternatively, take them as R2 says.

### R2 - RESIDUE - Docs - `docs/testing/TESTING.md:357`: "the three gate mutants" in a row this PR rewrote

- **Problem:** `crflic_mutants.MUTATIONS` carries six gate mutants: three licence arms and three #551 real-grant arms. The same row's Makefile comment says "Six additional elaborations remove ACTIVE or the real grant". This is #495 row 6731336971's own item, left in a line the PR edited.
- **Exact fix:** "#530 streaming licence, the three gate mutants," becomes "#530 streaming licence, the six gate mutants (#530, #551),".

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_nxn.cpp:3062,3108`: [AIDX] D is labelled "is the wire's", but its oracle is the constant 0

- The ENTITY_DEPARTING on the wire carried 34 in this run (`receipts/head_legs/notify.log`: "D: the ENTITY_DEPARTING carried available_index 34").
- The expected 0 comes from 6.2.2.15's reset, not from a frame. The DEPARTING's own available_index is printed but not graded.
- Optional:
  - label D "available_index (octets 36..39) is 0 after ENTITY_DEPARTING (6.2.2.15)", and keep `gsi_mutants.AIDX_D` in step;
  - consider grading the DEPARTING's index against `docs/design/MAILBOX_SPLIT.md:373` (it carries the current index).

### S2 - SUGGESTION - Tests - `tb/verilator/milan_dp/crflic_mutants.py:146` (`PP_MUTATIONS`): the [MVRPLA] Table 4.3 bounds have no planted arm

The campaign plants only "no LeaveAll". This round planted two processor-copy probes through the campaign's own `run_pp_mutant()`, and [MVRPLA]'s "each LeaveAll 9.5 to 15.5 s after its timer's last start" caught both by name (`scripts/probe_mvrpla_bounds.py`, `receipts/probes/mvrpla_{long,short}.log`):
- MVRP leavealltimer +5 s, so 15 to 20 s;
- MVRP leavealltimer halved, so 5 to 7.5 s.

Adding them as campaign arms would bank the bound checks. This is optional; the checks are proven to bite.

### S3 - SUGGESTION - Docs - `docs/reference/FR_NFR.md:473` (NFR-RES-01): pre-existing stale shipping-image figure

- The requirement still says the shipping image "measures 52,008 LUTs (82.03 %)". Dev's record was 53,534 and this record is 53,461.
- This line is outside the delta. The authoritative figure is AREA_BUDGET's gate table, which this PR updates.
- Optional: file it to #495 or #797's sweep, or reword the requirement to point at the gate record instead of carrying a number.

## Per-lens results (artifact evidence at this head)

```text
[R831] PASS Conformance - protocol-processor gitlink 801ef228 (git ls-tree HEAD); donor compare 044cb25f...801ef228 ahead 20 / behind 0, donor main tip == 801ef228; gptp-processor gitlink 1616fc8f == dev 46c971fa; tb/verilator/milan_dp/sim_crf_licence.cpp:929-1070 against IEEE 802.1Q-2018 Table 10-3 (VN tx! sN -> AN; AN tx! sN -> QA or AA by note 8; AA tx! sJ), 10.7.6.3 (JoinIn only with the Registrar IN), 10.7.9 and Table 10-5 (leavealltimer! -> Active, tx! -> sLA whatever is declared, note a requests the opportunity) and Milan v1.2 Table 4.3 (leavealltimer 10-15 s, 9.5 to 15.5 s); tb/verilator/milan_dp/sim_nxn.cpp:2091-2114,3019-3121 against IEEE 1722.1-2021 Table 7-2 (ENTITY offset 36, 4 octets, "the same as" ADP's field), 6.2.2.15 and ADPDU octets 50..53; reproduced at AX7101 1x1: crflic 458/0 at the head and 451/458 at processor 044cb25f (the 7 named [MRPAPP]/[MVRPLA] checks), notify 535/0 at the head and 531/535 at 044cb25f (A1-A3, R2) (receipts/head_legs, receipts/oldpin_legs); acceptance 1 to 5 as worded after the option (b) ruling
[R831] PASS RTL - protocol-processor hdl/top/protocol_processor_top.sv 044cb25f..801ef228: no input/output, parameter or localparam line changed; no hdl/ file in the parent delta; KL_srp_top.sv:272 elaboration guard satisfied (N_VIDS_P 4 <= ENC_DEPTH_P 12, top overrides neither); FPGA-gPTP 1616fc8f..a64be73d changes 4 docs/ and tb/ files only, so the a89802c8 route's synthesis inputs equal the head's; lint_rtl.py --check 89 <= 89 (receipts/lint_rtl_check.log); ROM images regenerated at the head equal syn/yosys/rom_digests.tsv rows (ucode 264fbb03.., ltn_rom 23cc67ee.., gptp_ucode e83709d9..; receipts/rom_regen.log); author route receipts at e99c3d13 vivado/w__ax7101*: three directives, route_status 0 routing errors, 12 of 12 signoff *_negative.rpt "No timing paths found", placed utilization 53,461 LUT / 54,971 FF / 15,849 of 15,850 slices for ExtraPostPlacementOpt, gate/check-route-1x1.log RESULT PASS with corners 0.334/0.045 ns slow and 1.35/0.017 ns fast; syn/ooc/pp_resource_baseline.json figures equal the AREA_BUDGET, finding 234 and SUBMODULES tables; check-baseline PASS (receipts/pp_resource_gate_check_baseline.log)
[R831] MINOR Robustness - scripts/check_cpp_idiom.py:270-271 - F1 (nested-brace boundary input shape). Otherwise applied clean to: [AIDX]'s "no ADPDU left while it was answered" guard and its bounded waits (10 s per advertisement, 1 s for DEPARTING), the DEPARTING and re-enable path, the [MVRPLA] gap checks under too-long and too-short timers (reviewer probes caught both), the old-pin and mutant failure paths, and the 1-slice margin (disclosed; the gate passes within tolerance)
[R831] MINOR Tests - scripts/check_cpp_idiom.py:270-271,706-710 - F1. Otherwise applied clean to: crflic-mutants 14 of 14 arms plus clean crflic 458/0 and tspec8 61/0 (16 of 16); gsi-mutants 18 of 18 arms plus clean notify (19 of 19), each arm its own process (receipts/ARMS_SUMMARY.txt); the five #883 crflic arms equal the processor's own patches (domain-one-new, vlan-one-new, vlan-joinin-registrar-mt, mvrp-leaveall-needs-content, leaveall-expiry-lost); the #851 control's KL_srp_top.sv edits equal push-twice-encoder-appends, and dev's encoder-only arm survives at 801ef228 (receipts/probes/851_encoder_only.log), so the two-layer control is a repair, not a weakening; C++ gate selftest 78/78 and the planted dev pattern fails the new arm by name; consumer legs gptp 212/212 and gptp-lat 212/212 (receipts/head_legs2)
[R831] PASS Docs - CHANGELOG.md, docs/design/AREA_BUDGET.md, docs/findings/234_PP_SHADOW_AREA_BASELINE.md, docs/reference/SUBMODULES.md, docs/reference/MILAN_COMPLIANCE_MATRIX.md, docs/traceability/ieee8021q.md, docs/testing/TESTING.md and tb/verilator/milan_dp/README.md against the code and measured figures; the 11 gPTP-derived paths a89802c8 touched are byte-identical to 46c971fa; the boundary diagram differs from dev only in the processor pin; the ROM ledger's extra a64be73d gptp row is disclosed and equals 1616fc8f's; doc and pin gates 12 of 12 rc 0 (check_submodule_docs, check_gptp_docs --with-submodule, check_diagram_pngs, docs_inventory --check, check_em_dash --base 46c971fa, gen_toc --check, docs_check, check_doc_paths, check_doc_style, check_py_idiom long module 10 <= 10 and 0 / 0, pp_srcs --check, git diff --check; receipts/docgates); comment rule: no lane label, review round, reviewer ID or comment ID in any added source line; all 15 commits one line, no trailers. RESIDUE R1 and R2 and SUGGESTION S3 do not uncover the lens
```

## Focus checks

1. **Gitlink and revert.**
   - The processor's main tip is `801ef228`, and it is a fast-forward of `044cb25f`: 20 commits ahead, 0 behind.
   - `8edfae99` reverts only the gPTP gitlink.
   - `f746d659` returns all 11 gPTP-derived paths to dev's bytes: the time-sync diagram's three files, four gPTP guides, GPTP_PLANE, TIME_SYNC, the ieee8021as traceability page and the gitlink.
   - The only gPTP-related row that differs from dev is the ROM ledger's `a64be73d` row. Its digest is identical to `1616fc8f`'s, the generator keeps such rows by design, and the PR discloses it.
2. **Parent-level tests at AX7101 1x1** (`endstation_ax7101_1x1_tdm8`, `SHAPE_AX1x1`).
   - At the head:
     - [MRPAPP]: the Domain sends `0 0 1` and VID 2 `0 0 3`; there are no VID or Talker Advertise JoinIns.
     - [MVRPLA]: MVRP sends 3 LeaveAlls at gaps of 13.0 to 14.6 s, and MSRP 3 at gaps of 10.8 to 13.4 s.
     - [AIDX]: the reads give 31, 32 and 33, then 0, then 0 and 1.
   - At `044cb25f` (disposable copy, same harness), each fails by its own words:
     - [MRPAPP]: the Domain and VID 2 send `0 1 1`, with 185 VID JoinIns.
     - [MVRPLA]: MVRP sends 0 LeaveAlls (3 checks fail).
     - [AIDX]: 4 reads give 0.
3. **#495 rows.**
   - Row 6758088112 is fixed, with three selftest arms and the planted old pattern failing by name. It also introduces F1.
   - The Makefile item of row 6731336971 is taken; see R1 and R2 for the rest of that row.
   - The processor and FPGA-gPTP rows (6758048783, 6777009988) are donor files, correctly left with the donors.
4. **Route and area.**
   - The three #818 directives came from one synthesis checkpoint: the selected route ran `baseline_integrated.tcl`; the two comparison routes ran `baseline_implementation.tcl`.
   - Every corner of every directive is above +0.030 ns. The worst setup is +0.162 ns (AltSpreadLogic_high) and the worst hold is +0.017 ns.
   - Against `46c971fa`: -73 LUT, +121 FF and +29 slices, inside the 500, 600 and 80 tolerances; RAM and DSP are unchanged.
   - The slice count is 15,849 of 15,850, 1 free. This meets NFR-RES-01's shipping-image clause ("MUST fit `xc7a100t`; the resource gate holds it at its recorded figures").
   - The gate passed, so no maintainer area acceptance was needed (see the limits).
5. **Full sweep and consumer legs.**
   - The 65 of 65 full sweep is the author's (at `6c6706e5`) and was not re-run here (not allowed).
   - This round ran these at the head: gptp 212/212, gptp-lat 212/212, crflic, notify, tspec8 and all campaign arms.
   - The dynmap-mutants fresh-clone fault is pre-existing and goes to its own issue; it was not examined.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlinks; donor compare; `sim_crf_licence.cpp:929-1070`; `sim_nxn.cpp:2091-2114,3019-3121`; the clause texts; head and old-pin legs | R831-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| RTL | CLEAN | processor top-level diff; no parent `hdl/` change; `KL_srp_top.sv:272` guard; lint 89 <= 89; ROM regeneration; route receipts and the resource JSON | R831-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Robustness | UNCLEAN (F1) | `check_cpp_idiom.py:270-271`; [AIDX] guards; [MVRPLA] bound probes; failure paths | R831-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Tests | UNCLEAN (F1) | `check_cpp_idiom.py:270-271,706-710`; crflic-mutants 16/16; gsi-mutants 19/19; three reviewer probes; gptp and gptp-lat legs | R831-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Docs | CLEAN (R1, R2 RESIDUE; S3) | 8 changed pages; 11 gPTP-derived paths; 12 doc and pin gates; comment rule; commit shape | R831-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |

A fix for F1 touches `scripts/check_cpp_idiom.py` only. It must be re-covered under Tests and Robustness at the new head. Conformance, RTL and Docs stay banked unless the fix touches their scope.

## Real limits

- **Not re-run here** (each was forbidden or out of reach):
  - no Vivado route or synthesis; the area and timing verdict rests on the author's public receipts, checked for internal consistency;
  - the full 65-suite sweep, the rtl-fast, rtl and elaborate job replay, `test_builder.py --require-rv32`, behave, the Yosys gates and `xvlog_gate.py` (no Vivado on this box);
  - dynmap-mutants and unb-mutants, beyond the crflic, notify and tspec8 legs and the two campaigns.
- **Hosted workflows:** at this head docs, rtl-full, rtl-fast and elaborate are all `queued` with no executed job (`receipts/hosted_runs_e18c8225.tsv`). No hosted result is claimed.
- **Not examined:** the processor RTL beyond its parent-visible interface and the arms' patch text. It was reviewed on processor PRs #218 and #219.
- **Not located:** a distinct "11-10" area acceptance in public state. The issue's "11-10 rule" concerns bundling, and this record needs no acceptance because the gate passes within every tolerance.
- **Interpretation, not contested:** the [AIDX] oracle takes "the same as" ADP's field to mean the index the last ENTITY_AVAILABLE carried, not the post-increment value. This follows processor #217 and `docs/design/MAILBOX_SPLIT.md:373-381`.
- **Hardware:** physical calibration and qualification were NOT RUN. Field skips are not hardware proof.
- **Merge candidate:** the current-dev candidate merge (`fa6c094b`) was not built here.
- **Probe hygiene:** every probe ran in a disposable copy or under the packet's `scratch/`. The clone was restored, and `receipts/restore_verification.txt` shows:
  - an empty status, ignored files included;
  - the index tree equal to the head tree `be1aea46`;
  - identical mode, blob and path listings;
  - no assume-unchanged or skip-worktree entries;
  - gitlinks `801ef228` and `1616fc8f`, with clean submodules.

## Pending manager duties

- **Merge turn:** build and validate the current-dev candidate (builder and native banks) and link its receipts.
- **Hosted contexts:** own their acceptance, including exact-head verilator-suites and yosys-portability after ready.
- **F1:** route it to the executor and schedule the re-review of Tests and Robustness at the fixed head.
- **Residue:** carry R1 and R2 to #495's checklist. S1 to S3 are optional.
- **New issues** (from the author's handoff): the dynmap-mutants fresh-clone fault and the resource gate's `inputs_sha256` sensitivity to the exporter's `/* */` hierarchy comment.

## Receipts

Every file is listed in `MANIFEST.sha256`, with paths relative to this packet.

**Scripts** (`scripts/`):
- `run_legs.sh`
- `launch_arms.sh`
- `launch_rest.sh`
- `run_crflic_pp_arm.py`
- `run_crflic_dp_arm.py`
- `probe_mvrpla_bounds.py`
- `probe_851_encoder_only.py`
- `probe_cpp_old_regex.py`
- `probe_cpp_edges.py`
- `probe_cpp_edges_old.py`

**Raw logs and rc files** (`receipts/`):
- `head_legs/`, `head_legs2/`, `oldpin_legs/`
- `arms/`, `arms_rest/`, `ARMS_SUMMARY.txt`
- `probes/`
- `docgates/`
- `cpp_idiom_*`, `probe_cpp_*`
- `lint_rtl_check.log`, `rom_regen.log`
- `pp_resource_gate_check_baseline.log`
- `hosted_runs_e18c8225.tsv`
- `dev_46c971fa_to_fa6c094b.txt`, `pr_files.txt`
- `issue883.json`
- `tool_identity.txt`
- `restore_verification.txt`

R831-1 FINISHED
