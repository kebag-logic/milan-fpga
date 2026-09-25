[R307] NEGATIVE - exact head 6a9828c172aa4d5d8ee49725e357a10bae2caa52

# R307-1 external review: issue #508 / PR #560

- Head `6a9828c172aa4d5d8ee49725e357a10bae2caa52`, tree `e43b64d9421ce0892f1bc620de942fc1f1fe50f8`.
- Source base `573f0052a0e4412e81f0845438fcec2086ce5d55`. Merged dev `c266432dcb0cdd464205823a3d82cad260eedde2`.
- Processor gitlink `990f96526bb89356c963a260ebbdcf2a77e6623a`. That is processor `main`.
- The review covered all five lenses independently.
- Two MINOR findings are open, F1 (`Docs`) and F2 (`Conformance`), so the verdict is NEGATIVE.
- `RTL`, `Robustness` and `Tests` are covered clean at this head.
- Neither MINOR finding needs a code change in the RTL or in the tests.

## Reconstruction

Sources read, in order:

1. `AGENTS.md` and `CONTRIBUTING.md`.
2. `docs/README.md`.
3. The #508 issue body and its frozen acceptance 1-6.
4. The assignment (comment 5819498419).
5. Decisions 5822047670 and 5824708827.
6. The two REVIEW READY comments (5822002238 and 5825445388).
7. The PR #560 body.
8. The processor interface authorities at the pin:
   - `protocol-processor/hdl/top/protocol_processor_top.sv:3083-3150` holds the STREAM_INPUT seam and the notify OR.
   - `docs/architecture/05_acmp_engine.md` holds the pbsta encodings, the boot admission contract and the listener transitions at lines 320-324.
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md:318` records that a bind probes at once (Milan 5.5.3.5.3).
9. The diff `573f0052..6a9828c1`, split into the lane-owned `c266432d..6a9828c1` (28 files) and the merge commit `cec6b99da`.
10. The public evidence tree `0c5b761b/review-evidence/508-r1`, read for `gates.jsonl` and `completion-check.json` only.

No private material was read. Before this verdict, no public review finding existed on PR #560 or on #508.

## Findings

### F1 - MINOR - lenses: Docs

**Location:** `CHANGELOG.md:113-116`, in the section "Unreleased - licence and LeaveAll scope".

**Title:** round 2's processor #116/#113 lines were also inserted into the #530 section.

**Evidence:** `git blame` puts all four lines in `e9f8ea5aa` (round 2):

- "Processor issue 116: parent-gate comments and mutation deadlines corrected."
- "No behavior or external port changes; parent ratchets stay unchanged."
- "Processor issue 113: latency-only input changes now push GET_STREAM_INFO."
- "Unchanged refreshes stay silent; simultaneous field changes coalesce."

They are correct in the new "processor pin 990f9652" section at lines 51-54. They are wrong at lines 113-116. That section records #530 and the processor pin move to `09f9bf38` (processor issue 106), which adopted neither change. In `receipts/changelog_530_section_dev_vs_head.diff`, the #530 section at dev `c266432d` equals this head's section except for exactly these four lines. The line "Its ROM digests are re-recorded; the images are unchanged." appears in both sections. The insertion looks anchored on it, and that anchor matches twice.

**Impact:** the product changelog now says the #530 revision adopted processor #116 and #113. It did not. The history is falsified for anyone bisecting adoption by changelog. No gate checks this.

**Required outcome:**

- The #530 section is byte-identical to dev `c266432d`'s.
- The four lines stay only in the 990f9652 section.

**Verification:** the section diff in the receipt comes back empty, and `grep -c 'Processor issue 116' CHANGELOG.md` returns 1.

### F2 - MINOR - lenses: Conformance

**Location:** issue #508 acceptance 2, against `tb/verilator/milan_dp/sim_nxn.cpp` G1/G3 and `tb/verilator/milan_dp/README.md:483-486`.

**Title:** acceptance 2 is not met as frozen, and no decision records the reinterpretation.

**Evidence:** acceptance 2 requires "PASSIVE after bind". The leg grades something else:

- G1: ACTIVE with `acmp_status` 0 immediately after BIND_RX.
- G3: PASSIVE only after an unanswered retry with no discovered talker.

The processor authority supports the lane's reading:

- `05_acmp_engine.md` and `00_MILAN_COMPLIANCE_REVIEW.md:318` say a canonical bind sends PROBE_TX at once (Milan 5.5.3.5.3).
- PASSIVE (PRB_W_AVAIL) follows a retry or a teardown when the talker is gone.

I believe the implementation is the Milan-correct behavior, and I do not ask for it to change. But AGENTS.md sections 2 and 4 freeze acceptance criteria. On an Issue/requirement conflict they require a published decision, not a lane interpretation. The executors published the conflict: 5822002238, 5825445388 and the PR body all say "independent review should retain that distinction". No maintainer or manager decision on it exists. 5822047670 decides only the docs-check blocker, and 5824708827 does not mention it.

**Impact:** the completion bar's first bullet ("all acceptance criteria are met") cannot be read off the contract. A later reviewer or maintainer could hold the lane to the literal text.

**Required outcome:** a public decision on #508 recording one of two outcomes:

- acceptance 2's "PASSIVE after bind" reads as "ACTIVE with acmp_status 0 on bind (the bind probes), PASSIVE after an unanswered retry with no discovered talker", as G1/G3 grade;
- or a different required scenario.

No source change is required if the first outcome is chosen.

**Verification:** the decision comment exists on #508, and G1/G3 still pass (`make -C tb/verilator/milan_dp notify`).

### S1 - SUGGESTION - lenses: Tests, Docs, Conformance

**Location:** `tb/verilator/milan_dp/sim_nxn.cpp:2174` (G8 "the withdrawal pushed" is `pushes >= 1`), and `tb/verilator/milan_dp/README.md:481` with the banner at `sim_nxn.cpp:1668` ("exactly one"/"exactly once").

**Evidence:** reviewer probe `scripts/probe_gsi_latency_and_g8.py`, receipt `receipts/probe_latency_g8.log`.

- The withdrawal pushes 2 GET_STREAM_INFO(sink 0) to each controller. They land 1,220 cycles (about 12 processor ms) apart.
- Both carry identical content: PASSIVE, `acmp_status` 0, no failure.
- The processor reads its owners live at each beat. So the SRP-unregistration push already carries the later COMPLETED to PASSIVE teardown, and the listener push repeats it.

Two real events each push once, so this is not a fabricated transition. But the leg leaves G8's count unbounded. A regression that adds spurious pushes on withdrawal would pass, and the "exactly one per transition" text is not graded in G8.

**Suggested outcome:** pin G8 to the measured count (2 per controller, sink 1 at 0) and say why.

### S2 - SUGGESTION - lenses: Docs

**Location:** `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:1419-1427`.

The doc comment for `start_the_boot_restore_walk()` ("The boot restore walk, as the firmware's nvm_boot() starts it...") sits above `boot_the_entity()`, merged with that function's own comment. `start_the_boot_restore_walk()` at line 1438 is left without a banner. Moving the comment back gives each function its own banner.

## Focus items, verified

| Item | Result | Evidence |
|---|---|---|
| Gitlink and `rom_digests` row produced by the repository tool | yes | Recomputed with the same generators and flags `syn/yosys/ooc.sh` uses: `ltn_rom.hex` `23cc67ee...`, `ucode.hex` `23605682...` match `syn/yosys/rom_digests.tsv:29-30` (`receipts/rom_digest_repro.txt`). The ledger is `LC_ALL=C` sorted as the record mode writes it, and every other pin's rows are retained (record-mode logic `ooc.sh:489-540`). The published final-head gate row `rom-digests` has rc 0, with the clean tree asserted after it. The gitlink `990f9652` equals processor `main`, and first-parent `09f9bf38..990f9652` is exactly the merges of PRs 109, 110, 111, 114, 117 and 115 |
| SUBMODULES, diagram and CHANGELOG pin text | yes, except F1 | `SUBMODULES.md:25`; `submodule_boundaries.svg` shows `990f96526bb8`; `submodule_boundaries.gen.py --check`, `check_submodule_docs.py` and `check_diagram_pngs.py` all rc 0. The 990f9652 CHANGELOG section is correct; F1 is the misplaced copy |
| Adopted-change table covers #109 #110 #111 #114 #116 #113 with correct parent effects | yes | `SUBMODULES.md:30-38`. The `protocol_processor_top` port list is identical at `09f9bf38` and `990f9652` (205 ports). The only interface delta is the defaulted parameter `NVM_RS_TMO_CYC_P = CLK_HZ_P/50`, which `KL_pp_shadow` leaves derived from its `CLK_HZ_P`. PR 117's HDL delta is comments only (`a8f8ce81..265d6762`). PR 115 adds the latency event term to `stri_events` |
| Datapath no longer answers selectors 5/7 or the failure-code byte | yes | `milan_datapath.sv:4776-4800`: an input's selector 4 is `{dmac,16'd0}` or zero, selector 5 answers only `gsi_ofail_w` (output-only), and selector 7 falls to `default: 0`. The processor intercepts input selectors 5/7 before `gsi_req_o` (`protocol_processor_top.sv:3097-3099`) and replaces bits [15:8] of selector 4 (`:3119-3121`). `pp_cd_srp_snk_fail_code_w` still feeds `LWSRP` (`milan_datapath.sv:6698-6699`), so the parent SRP status word is kept |
| milan_dp GSI leg grades processor fields for two sinks; tie-to-zero and wrong-sink mutants fail | yes | Reproduced: clean leg 345/0; `make gsi-mutants` 8/8 (control plus 7 caught by their named checks, failure counts 7, 7, 7, 7, 17, 30 and 10, identical to the README). Reviewer mutants: status read from the other sink only is caught (14 failures); the listener-status notification raised on the other sink is caught (37 failures) |
| Every harness that binds a sink starts the restore walk | yes | `sim_main.cpp`, `sim_nxn.cpp` (boot and G10), `sim_aclk.cpp` [RENDER-BIND], and `sim_tdm8_render.cpp` (`boot_the_entity`, used by T1 and [MULTI]) set `PP_CTRL[1]` and wait for `PP_STAT[2]`. `sim_prune` binds through the 0x800 window, not ACMP; `sim_crf_licence` drives only the talker side; `sim_gptp`, `sim_gmstep` and `sim_ax1x1gptp` bind no sink. Reproduced `pp_shadow` 371/0 |
| `nvm_cosim` wires the arbiter, cause, abort and deadline as the top does | yes | `cosim_top.sv:253-375` compared port by port with `protocol_processor_top.sv:2460-2600`: same m0/m1/p connections, m1 idle, `nvm_err_cause`/`nvm_abort` looped, and `RS_TMO_CYC_P = CLK_HZ_P/50`. `port_busy_o` is now the arbiter's `m0_busy_o`, which equals `p_busy_i` with m1 idle. Reproduced 465/465 and 39/39 mutants |
| Merge resolutions keep both sides | yes | For each of the five conflict files, every line added on either side (base `573f0052`) was checked against HEAD. The only absent lines are intended rewrites: the a8f8ce81 pin text became 990f9652, the two `.PHONY` lines were unioned (`Makefile:202` holds `notify`, `notify-build`, `gsi-mutants`, `gmstep-mutants` and `option-off-build`), and the README table became one table with both measurement columns. TESTING keeps the #447, #530, #508 and #387 campaign rows; `measure_test_evidence.py` keeps both sides' dispositions |
| Does the latency notification reach a milan_dp notify check? | no, as the handoff states | Reviewer mutant R3 drops `srp_evt_tk_latency_chg_w` from the processor's `stri_events` and the leg still passes 345/0. The reviewer probe drives an isolated latency-only Talker Failed refresh through the real parent wiring: exactly one push to each controller, the push equal to the solicited answer, sink 1 quiet. So #113 reaches the parent response path, but no shipped parent check grades it |
| `check_port_contracts`, `measure_naming --check`, `measure_test_evidence --check` | rc 0 | `receipts/static_summary.txt`. This resolves the round-1 author-declared docs-check blocker at this head |
| Redundancy path | kept open | No change adds a single-port assumption. The GSI seam is per sink index, and only the harness section owns the one MAC port of its test shape |

## Lens results

```text
[R307] PASS RTL - hdl/milan/milan_datapath.sv:4391-4412,4771-4801,6579-6694 and hdl/milan/KL_pp_shadow.sv:296-301,389-391 at 6a9828c1 - GSI arm removal against protocol_processor_top.sv:3083-3125 (intercept before gsi_req_o, index guard before narrowing, byte replace); widths of the 64-bit answer; no remaining reader of the removed arms; sink fail-code still feeding LWSRP; processor port list and parameter delta 09f9bf38..990f9652; lint_rtl --check 90<=90 (Verilator 5.050); nvm_cosim cosim_top.sv:253-375 wiring vs top :2460-2600
[R307] PASS Robustness - sim_nxn.cpp G0/G8/G10 plus probes at 6a9828c1 - missing descriptor answers NO_SUCH_DESCRIPTOR with an all-zero body including processor fields; out-of-range index guarded before narrowing (top :3104); reset returns both sinks DISABLED with no failure; withdrawal clears per sink while the other keeps its values; latency-only refresh isolated to its sink (probe); walk-never-started behavior documented (TROUBLESHOOTING 27, REGISTER_MAP PP_CTRL) with the 20 ms deadline; wrong-sink status and wrong-sink notification mutants caught
[R307] PASS Tests - receipts/notify_leg_clean.log, gsi_mutants.log, reviewer_mutants.log, pp_shadow.log, nvm_cosim.log at 6a9828c1 - clean leg 345/0; seven lane mutants fail their named checks; two extra reviewer wrong-sink mutants caught; pp_shadow 371/0; nvm_cosim 465/465 with 39/39 mutants; the checks can fail for the defects they name; S1 is a SUGGESTION only
[R307] UNCLEAN Docs - CHANGELOG.md:113-116 - F1 (MINOR). Otherwise checked: SUBMODULES table and pin, diagram/PNG/submodule-docs gates, INTEGRATION_GUIDE boot sequence, REGISTER_MAP PP_CTRL[1] and issue-112 text, TROUBLESHOOTING section 27, compliance matrix 5.4.2.9/.10 row, TESTING campaign row, milan_dp README seam table and lineage, docs_check (git), gen_toc, em-dash from both bases, doc_style, doc_paths, module matrix: all rc 0
[R307] UNCLEAN Conformance - issue #508 acceptance 2 vs sim_nxn.cpp G1/G3 - F2 (MINOR). Otherwise checked: acceptance 1 (lineage table, README section), 3 (code and 64-bit bridge id per sink on two sinks, change, withdrawal, reset, missing descriptor), 4 (solicited equals unsolicited, requester excluded on STOP_STREAMING, no push on refresh or duplicate probe), 5 (tie-to-zero, wrong-sink, restored approximation each fail), 6 (docs updated after evidence); acmp_status 0 outside ACTIVE
```

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #508 acceptance 1-6; `sim_nxn.cpp` G0-G10; processor `05_acmp_engine.md`, `00_MILAN_COMPLIANCE_REVIEW.md:318`; `protocol_processor_top.sv:3083-3150` | R307-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| RTL | CLEAN | `milan_datapath.sv` GSI block and SRP comments; `KL_pp_shadow.sv`; processor top seam and ports; `cosim_top.sv`; lint ratchet | R307-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Robustness | CLEAN | G0/G8/G10, index guard, per-sink isolation, reviewer probe and mutants, walk-not-started docs | R307-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Tests | CLEAN | obj_notify 345/0, gsi-mutants 8/8, reviewer mutants R1-R3, pp_shadow 371/0, nvm_cosim 465/465 and 39/39 | R307-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Docs | UNCLEAN (F1) | CHANGELOG, SUBMODULES, diagram set, INTEGRATION_GUIDE, REGISTER_MAP, TROUBLESHOOTING, compliance matrix, TESTING, suite READMEs; docs gates | R307-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |

Prior public findings: none on PR #560 or #508. The round-1 author-declared BLOCKER was three parent docs-check gates refusing processor content. It was decided in 5822047670 and fixed by processor #116. It is resolved at this head: `check_port_contracts.py`, `measure_naming.py --check` and `measure_test_evidence.py --check` all return rc 0.

## Real limits

- Not run by this reviewer:
  - the full milan_dp default sweep (36 commands);
  - `milan_dp_render`, the builder in either mode, behave, Yosys, xvlog and `act`.
- For those, this review relies on the published final-head `gates.jsonl`: 70 rows at `6a9828c1`, all rc 0. `completion-check.json` reports `all_rc_zero: true` (`receipts/published_evidence_check.txt`).
- Two superseded nonzero rows (`em-dash` and `toc` at `ee8812c9`) were re-run rc 0 at the final head.
- Hosted snapshot (`receipts/hosted_checks_snapshot.tsv`):
  - required contexts `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability` and `elaborate` succeeded, as did Yosys shards 0-3;
  - Verilator shards 1/5 and 4/5 were still in progress;
  - "Physical gPTP" is a skipped context, not an executed job.
- `gen_toc.py --check` and `check_em_dash.py` return rc 2 under the default interpreter because the pinned Markdown renderer is absent. They pass (rc 0) in a disposable local environment built from `tools/markdown/requirements.txt` with hashes. Nothing was installed system-wide.
- Parallelism: `nvm_cosim` ran with its defaults `JOBS=8` / `POOL=8`. Its build phase runs up to four builds at `-j 8` at once, so it briefly exceeded the 8-job budget. Every other run stayed within 8 jobs.
- No Milan text was available locally. The Milan clause readings (5.3.8.6, 5.5.3.5.3/.29/.41/.47) rely on the processor's documented contract and on this reviewer's reading. F2 asks for a decision, not a behavior change.
- Physical calibration was not run, and nothing here is hardware proof.
- Receipt hygiene: absolute host paths in receipts were replaced by placeholders (`<PACKET>`, `<TOOL-BIN>`, `<TOOL-ROOT>`, `<HOME>`, `<TMP>`). Only path strings were changed.
- All probes ran in a disposable full copy under `scratch/`. The reviewed clone was restored and verified:
  - HEAD and index tree are `e43b64d9`;
  - 885 tracked blobs match in bytes and mode;
  - 4 gitlinks are at their recorded pins, and all three required submodules are clean;
  - the one ignored `scripts/__pycache__/` this review created was removed (`receipts/clone_integrity.txt`).

## Pending manager duties

- Record the acceptance-2 decision (F2) on #508.
- Have F1 corrected on the lane, then run a re-review round at the new head covering `Docs` and `Conformance`. `RTL`, `Robustness` and `Tests` stay covered only if the fix leaves their scope untouched.
- Build and validate the candidate merge against live dev.
- Accept the hosted runs, including the Verilator shards still in progress at the snapshot, and the `act` replica.
- Post-merge containment.
- Physical calibration remains NOT RUN.

R307-1 FINISHED
