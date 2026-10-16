[A585] REVIEW READY
Commit: `5c6f50eefa4c5545f052ec843363ace5e7936e8a` (branch `708-pin3`, not pushed; merge of dev `734eb780` at `a1dfbfad`)
Changed:
- gitlink `protocol-processor` `2ad2f845` -> `2cbed0a9`, with no other processor change (`75a28523`);
- the pp170 `parent-name-evidence.patch` (`scripts/measure_test_evidence_readers.py`);
- F3 ACMP normalisation retired in `sw/firmware/ctrl/test/acmp_walk.cpp`: raw bytes, with LD1 to LD3 as controls that fail if the old answer returns (Milan v1.2 Table 5.36, 5.5.3.5.30 step 2, 5.5.4.2 step 1 and Table 5.44; IEEE 1722.1-2021 8.2.1.5 and Table 8-3);
- records re-recorded by their generators: ROM digests, pin page, boundary diagram, port census;
- after the dev merge: the resource records re-recorded with `pp_resource_gate.py record --write` at all three endpoints, and the re-baseline documented (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md`, `docs/reference/SUBMODULES.md`).
Validation (all rc 0). Heavy gates ran in clean clones; only quick read-only checks ran in the worktree. The RTL, firmware and suite tree is `82227af0`, which differs from the head only in the resource record and four Markdown pages:
- Re-route with the unchanged recipe, under the exclusive lock, measured at `435af429`, whose image inputs equal the head's: `route-1x1` WNS **+0.215** / WHS +0.036 ns. That is 0.185 above the +0.030 floor; the fall is 0.018 from #696's record and 0.131 from dev's +0.346 reference. LUT 49,613, FF 52,353, slices 15,725 (125 free). The worst path is SoC-side (AXI-Lite-to-Wishbone FSM to the SPI-flash PHY counter). No register boundary, directive change, pblock or floor exception.
- `pp_resource_gate.py check`: rc 0 for route-1x1, ooc-1x1 (23,314 / 19,821) and ooc-8x8 (30,211 / 27,451), against #696's record. Records then written; `check` against them and `check-baseline` rc 0.
- Parent sweep: 63/63 suites, 2,187,249 checks, 0 failures, 0 timeouts (five shards).
- Physical gPTP suite: rtl.yml `physical-gptp`'s steps, run at the head in a fresh clone. 197 checks, 0 failures: physical 143/0, plus the setup-abort, no-TX, no-Pdelay and recentre controls.
- Processor `2cbed0a9`: `run_suites.sh` 34/34 suites, 1,029,620 checks (sv2v v0.0.13; see risks).
- gPTP processor `e4869fd0`: `make contract tb lint` passes, with 48 mutants caught, 0 escapes, and the tsn-gen `deca300c` arm run.
- Yosys: 58/58 tops. `xvlog_gate.py --check`: 0 findings.
- Builder bank `test_builder.py --require-elaboration --require-rv32`: all gates pass, except two the bank records as not runnable here.
- Firmware: `fw_rv32_selftest` and `test_ctrl_firmware.py --require-rv32 --self-test`, with 520 mutants caught and 0 escapes; `acmpwalk` 127/127.
- Other gates: lint 90 <= 90, BDD 406 scenarios, `check_nvm_capture.py`, `measure_test_evidence.py --check`, and the port, naming and submodule records.
- docs.yml: wire-accountability and docs-gates at the head, 70 steps run and 7 hosted-bookkeeping steps skipped; docs-check-no-git.
- Image: the measured route's bitstream with the shipping configuration properties; 3,825,992 bytes, DRC 0/0. `aem_desc.bin` byte-identical to dev's.
Acceptance criteria:
1. Met: gitlink `2cbed0a9`, the adaptations, nothing else in the processor.
2. Met: re-baselined under the rule, with the route at +0.215 ns.
3. Met: the firmware digest did not move, so the capture was not re-measured; `check_nvm_capture.py` passes.
4. Met, with one declared difference (below).
5. Post-merge, for the manager.
Open risks/questions:
- The image build is the gated route's own bitstream. The shipping launcher's eight-worker synthesis exceeds this lane's memory budget, so it was stopped and none of its output is used.
- Dev has since moved to `8eacc408` (PRs #745 and #753: CI and docs only, no image input). The lane was merged at `734eb780` as assigned. A scratch trial merge with `8eacc408` is conflict-free, and the docs gates pass on it. The candidate-merge validation is still owed.
- The processor's `tb/nvm_port` Yosys guard fails under the parent's pinned sv2v 0.0.12 at the old pin too, and passes under v0.0.13. It is not caused by the adoption, and it may want its own issue.
- The physical gPTP suite and the gPTP processor tests were re-run in this continuation, because a host shutdown cut their first runs.
Records: HANDOFF and PR body in the lane's output directory.
