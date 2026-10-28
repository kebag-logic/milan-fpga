[R721] NEGATIVE - exact head c1bc9e21a273fd8506b4806a2470fb7bab13f72f

# R721-1: independent internal review of FPGA-gPTP PR #93 (issues #87, #88)

- Repository: Mister-M-alt/FPGA-gPTP. PR #93 is at exact head `c1bc9e21a273fd8506b4806a2470fb7bab13f72f`, tree `8673c3750bb610ae5eab239f0675ba94326f67e7`. The base is main `55680bff3b287b9a7b0c759f51471fa617c17335`.
- Review clone: a detached clone, cleared context. It is unchanged at the exact head after every probe (`receipts/clone_integrity.txt`).
- Companion: `milan-fpga-companion.patch` from the public evidence tree `kebag-logic/milan-fpga@df89292c…/review-evidence/gptp88-r1/author-r1/a690b/`. Its sha256 is `fa3c22f0a2856f4e3fd79fda60cdfdcd9b281492da564ca4123c69145d71a986`, which matches the assignment.
- The companion was applied to a scratch clone of milan-fpga dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, with the gptp-processor submodule at the exact head. The gitlink was staged in the index; nothing was committed.
- Authorities:
  - IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015: 10.3.10.2.1 a)-d), 10.3.12.1.1, 10.3.12.1.4 i) (Cor1) and the 10.5.3.3.4 NOTE.
  - IEEE 1722.1-2021 7.4.41.2 (GET_AS_PATH) and Milan v1.2 Table 5.22.
  - Scope: the issue #88 assignment (issuecomment-6434676531), the STOP (issuecomment-6440962747) and ruling (A) (issuecomment-6442193793). Ruling (A) authorises exactly one top-level change: an explicit entry-zero path output.
- Reconstruction order: README/docs map (the repository has no AGENTS.md or CONTRIBUTING.md), then the issue bodies and manager comments, then the diff and its five commits, then the public author evidence, then the PR text.
- Prior public review findings on PR #93: none. The PR has only the manager's review-start comment and no review threads, so nothing needed resolving or retaining.

## Verdict

NEGATIVE. The engine, parser and ABI change are correct and conform to the ruling. Three MINOR findings stay open:

- **F1:** the engine mutation arm does not enforce the named checks for the two #87 keep-previous mutants.
- **F2:** the companion leaves a current parent reference document stating the retired count-zero and grandmaster-at-entry-0 behaviour for 0x7DC–0x7E4.
- **F3:** no check exercises the companion's two entry-0 change detectors. A planted removal of either survives every parent bench run.

There is also one SUGGESTION, S1. No BLOCKER or MAJOR was found.

## What was checked, by assignment item

1. **Qualification is a)-c) only.** Met.
   - Removed from `hdl/wire/KL_gptp_rx_parser.sv`: the count refusal (`lengthField/8 != stepsRemoved+1`), the head refusal (`gm_r`, `ann_head_bad_w`, its `bad_r` arm and its `fin_ok_r` term) and the zero-length refusal (`:318-322`).
   - An empty PathTrace still marks presence and singularity (`:569-571`).
   - Kept: 8N framing, containment, a single PathTrace, and the all-hop loop verdict for c). a) and b) remain in the microcode.
   - Head parser suite: 378/378. The head harness run against the **base** parser RTL fails 44 checks, all count, head, empty and presence checks (`receipts/head-parser-harness-on-base-rtl.log`), so the new checks catch the shipped defect.
   - a), b) and c) each removed from the microcode is caught on every named check (engine arm rows 81-83).
2. **pathTrace from the received head plus thisClock; keep-previous without a TLV.** Met.
   - Word 12 carries presence at bit 63 (`KL_gptp_rx_parser.sv:398`).
   - The engine captures w16..w23 and presence (`KL_gptp_engine.sv:319-324`).
   - Address 7 copies entries from entry 0, appends thisClock to any present path including an empty one, and writes nothing without a TLV (`:986-1003`).
   - Reset and self-mastership load `self_path_w` = {thisClock} (`:737`, `:845`, `:977`).
   - Engine suite: 1875×3 + 54, all pass. It covers both issue shapes deferring from priority1 247 (elected, not master, one coherent commit, no Announce for 1.05 s), entry 0 being the received head, G1→G2 without a TLV keeping G1's path, a warm reset with a TLV-less grandmaster keeping {thisClock}, and an empty TLV giving {thisClock}.
3. **ABI.** Met, and it is exactly the authorised change.
   - The only port change is `pub_path_o` going from `[7*64-1:0]` to `[8*64-1:0]` (entry k at `64*k`). `pub_path_count_o` counts the published entries.
   - No parameter or register-map change in this repository. The region-3 read face (internal) maps addresses 7..14 to entries 0..7.
   - `docs/INTEGRATION.md:456-506` documents it. The bench top leaves the port open, and lint is rc 0.
4. **Named checks with planted mutants.** Met in substance; F1 is a gate gap.
   - Parser arm: 16/16, each mutant failing every named check, 6 of them new.
   - Engine arm: run in parallel through the arm's own code. 84/84 caught, matching the author's per-mutant FAIL counts.
   - Re-graded strictly, every mutant whose `breaks` are check names (52) fails all of them. That includes the two #87 mutants, which the shipped arm grades only on "any failure" (F1).
5. **Companion.** The RTL is correct; F2 and F3 are open.
   - The patch applies cleanly. The CSR AS_PATH face is a combinational pass-through (`milan_csr.sv:2851-2853`), so the entry-0 head and entries 1..7 are coherent on every cycle.
   - GET_AS_PATH entry 0 comes from `asp_owner_head_w` (IEEE 1722.1-2021 7.4.41.2), and `REGISTER_MAP.md` 0x7DC is rewritten.
   - The tsn_fuzz fixtures and README are updated, and `TEST_RESULTS.md` is regenerated.
   - Results with the companion: the consumer list run here (14 commands; the builder test is excluded) is rc 0 except one environmental refusal inside command 5. That command's suite passes 320/320; only its mutation arm could not run. Details are in the Gates section.
6. **ROM images.** Met. The shipping, request-seeded, Sync-seeded and priority1-255 images generated from base and head are byte-identical (`receipts/rom_images.sha256`). No committed `.hex` changed.
7. **Generator.** Met. The generator's AST, with docstrings and comments stripped, is identical at base and head (`receipts/generator_ast_compare.txt`), so the change touches comments and docstrings only.
8. **Comment rule.** Clean. No lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs were added in source comments. New comments cite issue IDs and clauses only.

## Findings

### F1 MINOR: the engine arm does not enforce the named checks of the two #87 keep-previous mutants

- **Lenses:** Tests.
- **Where:** `tb/verilator/engine/mutants.py:894`. `named_verdict` enforces "fail every named check" only for `breaks` starting with `#82 `, `#84 `, `#85 `, `#88 ` or `p1 255 `. The two #87 mutants (`:696` "the empty sequence published without a TLV" and `:714` "a TLV-less Announce publishes {thisClock}") name `#87 …` checks first, so the arm passes them on *any* failing check.
  - This contradicts the arm's own contract at `:913` ("True when the harness catches it, through every check it names").
  - It also contradicts the PR text "Mutants, each caught by every check it names".
- **Evidence:** `receipts/engine-arm/summary.tsv` rows 78-79, graded `any-failure`. Strict re-grading shows both fail all their named checks *at this head* (`all-named-fail`, 45 and 35 FAIL lines).
- **Impact:** keep-previous is the #87 acceptance, and it is the one rule whose named checks the gate does not hold. A later change that silences "#87 G1 to G2 without a TLV" or "#87 post-warm-reset TLV-less …" would still pass the arm on an unrelated failure.
- **Required outcome:** add `"#87 "` to the prefix tuple at `:894` and its comment at `:892`, so #87 controls must fail every check they name.
- **Verification:** run `make -C tb/verilator/engine mutants`; it should still pass 85/85 (strict re-grading here already shows `all-named-fail` for both). Then confirm in the output that each #87 control prints every named FAIL line.

### F2 MINOR: the companion leaves a current parent reference doc stating the retired 0x7DC–0x7E4 behaviour

- **Lenses:** Docs, Conformance.
- **Where:** milan-fpga `docs/reference/REGISTER_MAP_CLASSES.md:102` at dev `97aab1d0`. The companion patch does not touch this file. The 0x7DC–0x7E4 row says:
  - "The fabric engine supplies the full bounded PathTrace, preserving count zero for a selected no-TLV Announce";
  - "Table 5.22 compares `(count ? GM : 0, count, active tails)`: fabric 0/1 is a real edge, fabric GM changes at count zero are silent".
- **Authority:** the #87 assignment ("Update the milan-fpga-facing description so it no longer states the cross-edition behaviour") and ruling (A) item 4 (REGISTER_MAP 0x7DC). With the companion, a TLV-less Announce keeps the previous pathTrace (802.1AS-2011 10.3.10.2.1 d)), never count zero with a known grandmaster. Entry 0 is the received head or thisClock, and the comparator in `milan_datapath.sv` now compares `(count ? entry 0 : 0, count, tails)`.
- **Impact:** a current reference page for the very addresses this change re-specifies states the 802.1AS-2020 count-zero rule and the GM-at-entry-0 comparator that this PR retires. Its sibling `REGISTER_MAP.md` now says the opposite. This is a behaviour and conformance claim, not wording only. The `docs/history/**` pages are dated records and are out of scope.
- **Required outcome:** the companion patch updates that row to the 2011 rules:
  - entries from entry 0;
  - no-TLV keeps the previous pathTrace;
  - an empty TLV gives {thisClock};
  - the comparator works on entry 0.
- **Verification:** `grep -n "count zero\|count ? GM" docs/reference/REGISTER_MAP_CLASSES.md` is empty on the patched parent, and `scripts/docs_check.py` is rc 0.

### F3 MINOR: no check exercises the companion's entry-0 terms in its two path-change detectors

- **Lenses:** Tests.
- **Where (companion):**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` `pub_path_changed_w`: the served-path generation published at CSR 0x7E4 (`A_ASP_CMD`).
  - `hdl/milan/milan_datapath.sv:6509` `gsi_asp_chg_w`: the Milan Table 5.22 GET_AS_PATH push.
  - With entry 0 no longer the grandmaster, both now watch entry 0 directly. The companion text says so: "the path generation compares count and entries only, so entry 0 counts"; "the Table 5.22 AS_PATH comparator watches entry 0".
- **Evidence:** reviewer probes, each planted alone on the patched scratch parent (`receipts/companion-probes/`):
  - C2, shadow generation compares entries 1..7 only: gptp_shadow 320/320, milan_dp `gptp` 192/192, tsn_fuzz `ptp` 675 pass, 0 fail. It survives every bench. The tsn_fuzz rc 2 there is only the freshness gate, explained under Gates.
  - C3, datapath comparator without its entry-0 term: milan_dp `gptp` 192/192. It survives.
  - Control C1, GET_AS_PATH entry 0 served from the grandmaster: milan_dp `gptp` fails 4 named checks.
  - Every generation step in the gptp_shadow harness (`sim_main.cpp:914-993`) also changes the count, so an entry-0-only change is never presented.
- **Impact:** a path that changes only its head at equal count and tail (for example a TLV `{X,S}` replaced by `{Y,S}` from the same parent) must bump the 0x7E4 generation and push GET_AS_PATH (Milan Table 5.22, "the path sequence changes"). Both behaviours are new in the companion and neither is held by a test. The RTL is correct today.
- **Required outcome:** add parent checks with an entry-0-only change at equal count and tail:
  - gptp_shadow: one generation step;
  - milan_dp `gptp`: one GET_AS_PATH push and the new entry 0 served.
- **Verification:** with those checks, probes C2 and C3 (`scripts/companion_probes.sh`, `scripts/companion_probe_c3.sh`) each fail a named check, and the unmutated benches pass.

### S1 SUGGESTION: a formatting regression in the parser arm

- **Lenses:** Tests.
- **Where:** `tb/verilator/parser/mutants.py:134` reads `PAIRS =((…` (the space after `=` was lost in the delta).
- **Change:** restore `PAIRS = ((`. It changes no behaviour.

## Gates and runs (all foreground-waited, each with its own log and rc)

### Repository at exact head (`receipts/head-repo/results.tsv`)

| Gate | Result |
|---|---|
| `make contract` | rc 0, PASS |
| `make -C tb/verilator/ucpu` | rc 0, 768/768 |
| `make -C tb/verilator/parser run` | rc 0, 378/378 |
| `make -C tb/verilator/parser mutants` | rc 0, 16/16, all named (`receipts/parser-arm/`) |
| `make -C tb/verilator/engine run` | rc 0, 1875/1875 ×3 (shipping, request-seeded, Sync-seeded) + 54/54 (priority1 255) |
| Engine mutation arm (its own code, run in parallel by `scripts/engine_arm_parallel.py`) | 84/84 caught, clean control pass; strict re-grading: 52/52 named-check mutants fail every named check (`receipts/engine-arm/`) |
| `make -C tb/verilator/gaskets` | rc 0, 81/81, arm 5/5 |
| `make -C tb/tsngen` | rc 0, 288/288, arm 4/4 |
| `make -C bench/arty test` | rc 0, PASS |
| `make lint` | rc 0 |
| `make docs` | rc 0, source evidence 20 exact |
| `syn/ooc/check_ooc_clock.py --selftest` | PASS, 30 arms |

Toolchain: the pinned HDL simulator, identity verified as `5.050 2026-07-01 rev v5.050`. My wrapper maps `-j 0` to `-j 4` and changes nothing else.

### Reviewer probes on the engine and parser (`receipts/reviewer-probes/`)

Six disposable mutants of my own, outside the shipped arms. All six were caught:

- R1, count written without a TLV: 9 FAIL, all of them #87 or keep-previous checks.
- R2, the address-6 self path rewrites entry 0 only: 18 FAIL.
- R3, presence at bit 62: engine 180 FAIL, and the parser is caught.
- R4, the parser reports an empty TLV as absent: engine 6 FAIL, including "#88 empty path from the parent", and the parser is caught.
- R5, keep-previous only while the GM is unchanged: 6 FAIL, "#87 G1 to G2 without a TLV".
- R6, entry 0 captured from w17: 130 FAIL.

### Parent consumer list with the companion

Scratch parent `97aab1d0` with the patch applied in the worktree and the gitlink staged at `c1bc9e21` (`receipts/head-parent/results.tsv`):

| # | Command | Result |
|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 |
| 2 | `scripts/check_py_idiom.py` | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0 |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0 |
| 5 | `make -C tb/verilator/gptp_shadow -j8` | suite 320/320 and lifecycle PASS. The `mutants` target REFUSED: "modified input bytes/mode", because it requires committed inputs. rc 2, environmental, NOT RUN (see limits) |
| 6 | `scripts/check_port_contracts.py` | rc 0 |
| 7 | `scripts/measure_naming.py --check` | rc 0 |
| 8 | `scripts/measure_test_evidence.py --check` | rc 0 |
| 9 | `scripts/docs_check.py` | rc 0 |
| 10 | `scripts/lint_rtl.py --check` | rc 0 |
| 11 | `make -C tb/verilator/milan_dp gptp` | rc 0, 192/192 |
| 12 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 192/192 |
| 13 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 |
| 14 | `make -C tb/verilator/milan_dp_gptp` (own copy, `receipts/head-dpg/`) | rc 0, RESULT PASS (5057 s). Its verdict lines are identical to the author's published head run |
| — | `sw/builder/test_builder.py` | NOT RUN: builder bank, owned by the manager at the merge turn |

- tsn_fuzz `ptp` ran on its own copy with tsn-gen built at the parent CI pin `deca300c9eb4863fa13383b45ba6cb6fd0828671` (`scripts/build_tsngen.sh`).
- The campaign gives **675 pass, 0 fail, 0 known gaps**. The make rc is 2 only because its freshness gate compares against the git-committed base copy (677) and the patch is uncommitted.
- The fresh output equals the companion's regenerated `TEST_RESULTS.md` byte for byte, with only the line-7 timestamp normalised (`receipts/head-fuzz/freshness_vs_companion.txt`). Once the adoption commits the companion, that gate is satisfied.
- Companion probe C1 is caught; C2 and C3 survive (F3).

### Hosted evidence

At `c1bc9e21` there are 0 check runs and 0 commit statuses. No hosted job ran at the exact head; nothing hosted is claimed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | 802.1AS-2011+Cor1/Cor2 10.3.10.2.1 a)-d), 10.3.12.1.1, 10.3.12.1.4 i), 10.5.3.3.4 NOTE against parser `:310-336`, `:558-631`, engine `:716-737`, `:965-1003`; 1722.1-2021 7.4.41.2 entry 0 in companion `milan_datapath`; parent docs `REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md`, README | R721-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| RTL | CLEAN | `KL_gptp_rx_parser.sv`, `KL_gptp_engine.sv` (ports, Announce capture, staging, reset/self, read face, assertion), generator AST identity, ROM byte identity, companion `KL_gptp_shadow.sv`, `milan_datapath.sv`, `milan_csr.sv`; lint rc 0 | R721-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Robustness | CLEAN | presence vs zero-gap successor capture (`:241-344`), stale-entry gating at address 7, empty TLV at EOF and mid-chain, duplicate after empty, refused-frame staging, warm reset; reviewer probes R1-R6 all caught; CSR head/tail same-cycle coherence | R721-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Tests | UNCLEAN (F1, F3; S1) | parser `sim_main.cpp` + arm (16/16), engine `sim_main.cpp` + arm (84/84, strict 52/52), tsngen arm, head harness on base RTL (44 FAIL), companion gptp_shadow/milan_dp/tsn_fuzz, companion probes C1-C3 | R721-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |
| Docs | UNCLEAN (F2) | `docs/INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md`, `SOURCE_EVIDENCE.md` (anchors spot-checked + `make docs`), parser README/Makefile, source comment rule, companion README/REGISTER_MAP/tsn_fuzz README, parent `REGISTER_MAP_CLASSES.md` | R721-1 | c1bc9e21a273fd8506b4806a2470fb7bab13f72f |

## Real limits

- **No manager source bank** was run or is claimed at this head. Source-head execution evidence is the author's published receipts plus the reviewer runs listed above.
- **Base-side runs:** no repository gates or parent consumer list were run at the base. The base comparison relies on the author's published base receipts, the ROM and AST identity checks, and the head-harness-on-base-parser run.
- **gptp_shadow `mutants` target** (inside consumer command 5) was NOT RUN. It refuses uncommitted inputs, and this review makes no commits. Its suite and lifecycle passed. The author's arm receipts are on a committed scratch snapshot.
- **tsn_fuzz freshness gate** is rc 2 only against the uncommitted base copy. Substance equality with the companion file is shown instead.
- **Not run:** `sw/builder/test_builder.py` (builder bank) and the parent `csr` and `gptp_txts` suites (the companion changes only comments in `milan_csr.sv`).
- **No synthesis or resources:** `make ooc` beyond its selftest was not run, and Vivado was not run.
- **Clone hygiene:** an early read-only import of the arms' Python modules left three ignored `__pycache__` directories in the review clone; the first integrity record shows three ignored entries. I removed them. The final record shows zero porcelain lines including ignored files, every tracked file's bytes hashing to its index blob, index modes and blobs equal to the HEAD tree, and no gitlinks (this repository has no submodules).
- **No hardware:** physical calibration NOT RUN, and no hardware or field evidence exists. Field skips are not hardware proof.
- **Observations, not findings, outside the ruling's enumerated scope:**
  - The parser still refuses a second PathTrace TLV, a non-8N PathTrace length, and every Announce before thisClock is installed. Ruling (A) did not ask for these to be removed.
  - The HANDOFF records a pre-existing timing nuance: d) is applied at the BTCA `take` rather than after the role becomes SlavePort. It is unchanged here.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `55680bff`, live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`) with the builder and native banks, and link the receipts.
- Hosted/act acceptance; no hosted job exists at this head.
- At the gPTP pin adoption, land the companion with F2 and F3 addressed. Re-run tsn_fuzz `ptp` once both companions (#89/#90/#91 and this one) are in, regenerating `TEST_RESULTS.md` once, and run the gptp_shadow mutation arm on the committed adoption.
- Close F1-F3 and re-review before merge (two independent positive reviews are required).

R721-1 FINISHED
