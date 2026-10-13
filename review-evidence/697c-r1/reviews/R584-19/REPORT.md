[R584] POSITIVE - exact head d40e4e9827be2516f8f34b9d65f0a483fff2194c

Round R584-19, internal independent review of PR #705 (issue #697), cleared context. Head `d40e4e9827be2516f8f34b9d65f0a483fff2194c`, tree `2d70c1b4c386ec562bd3830ee1118bea1132202c`, confirmed by `git rev-parse` and by the PR API (`headRefOid`).

This is a delta review from `97e71316`, the head that holds two POSITIVE reviews (R584-17 and R585-18). It answers the composition review R584-18 under the round-20 ruling (#697 comment 6140933191). All five lenses were applied, and each lens below names what it examined. No BLOCKER, MAJOR or MINOR is open. One RESIDUE (documentation wording) and one SUGGESTION are recorded.

## What the delta is

- `a71b0e41` merges dev `e81ce82f` (#726, PR #729) into `97e71316`. Its tree, `c857c6a9`, is exactly what `git merge-tree --write-tree 97e71316 e81ce82f` produces. So the merge is mechanical and resolves no conflict by hand.
- `d40e4e98` changes eight files, all of them gate code, Makefile wiring or documentation:
  - `stream_counter_f5.py:43-54,74,91-94`: `--stack`, the shared pin check before staging, and `--build-only`.
  - `ctrl_configs.py:122-124`: F5 is the sixth builder, at both shapes. `:153-154` classifies the milan_dp Makefile `OUTSIDE`.
  - `ctrl_plants.py:193-198`: two removal controls.
  - `ctrl_pin.py:229-230,699-708,948-957`: a counter-target prerequisite census, and four direct F5 pin arms.
  - `ctrl_pin_bench.py`: the bench helper moved out of `ctrl_pin.py`, plus three unpinned-target plants.
  - `tb/verilator/milan_dp/Makefile:34,545,667-688`: `STACK_DIR`, the `stack-pin` target, prerequisites, and `--stack` forwarded.
  - `sw/firmware/ctrl/README.md` and `docs/testing/CI_WORKFLOWS.md:80-82`: the new statements.
- No firmware source, image builder, configuration, RTL file or gitlink changes in `97e71316..d40e4e98` except what the dev merge brings (`receipts/image_inputs.txt`).

## Judgements requested for this round

| Item | Verdict | Evidence |
|---|---|---|
| The F5 build-only capture records its compiler invocations, and the boundary judges them | Holds | Local gate: both `stream_counter_f5.py --build-only` runs are captured, and the totals are 2852 sources of 3082 invocations, 0 findings (`receipts/boundary_selftest_without_verilator.log:8-10,283-284`). Planted control: an F5-only capture is judged by the gate's own `Places`/`judged`. It is clean with 0 findings. With `aecp/aecp_mbx.c` including `tsn-c-stack/examples/adp_port.h`, it gives two findings attributed to `stream_counter_f5.py` (`receipts/f5_capture_judged/judged-only-{clean,planted}.log`). The full `--capture` judge stops first at the capture-completeness check, as designed (`judge-*.log`). |
| Removing the registry entry or the capture is refused by name | Holds | Self-test lines `[ok] boundary control the F5 builder removed from the registry` and `the F5 builder's own capture is missing`, locally (`boundary_selftest_without_verilator.log:35-36`) and hosted (job 115214486404, excerpt lines 11-12). |
| R584-18's `held_text_probe.py` reports 0 program refusals | Holds | Same blob as R584-18's (`9f0fe3d9`). Head: 0 program refusals (`receipts/held_text_probe_head.log`). The 7 non-program refusals come from the stand-in holding no compile, which the probe documents. Control: the pre-fix merge `a71b0e41` gives 1 program refusal, `tb/verilator/milan_dp/stream_counter_f5.py` (`held_text_probe_a71b0e41_control.log`). |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` ends PASS on the merged tree | Holds | rc 0, `ctrl_boundary: PASS`, 0 findings, 112 boundary, 120 pin and 4 figure controls, 0 misbehaved, wall time 14:36 under concurrent load. The figures equal hosted `firmware-boundary` exactly. The Verilator side (`--only verilator`) also passes: 829/926, 6/120/4, 0 misbehaved (`boundary_selftest_only_verilator.log`). |
| An off-pin or modified stack is refused before the F5 build, and before `counters`, `counters-f5` and `counters-mutants` (planted control) | Holds | `probe_pin_order.py`: 41 of 41 cases. It covers four spoils (an `#error` poison in `wire.h`, `HEAD~1`, an edited `src/adp.c`, an added header) against F5 at shapes 1 and 8, `--build-only` and `--variant late`. Each case refuses with rc 2 before F5 creates its work directory or stages anything. The same spoils run against `make counters`, `counters-f5`, `counters-mutants` and `run` serially, and against `counters-mutants` and `counters-f5` with `-j16`, in a mirrored milan_dp. Each refuses on the pin check: the recorder Verilator never ran, nothing was staged and no recipe line ran. The clean positive control (pinned clone, F5 `--build-only`) built. |
| Removing a prerequisite is caught | Holds | `pin_wiring_mutants.py`: each counter target unpinned gives a finding. Unpinned with `--stack` also dropped, only the new `COUNTER_TARGETS` census catches it, and it does. F5 with its own pin call removed builds an edited clone (rc 0), so the gate's F5 pin arms would fail. The probe also expected a finding for `run` without `stack-pin` and got none (hence its rc 1). That expectation was wrong: `run` reaches the stack only through `$(MAKE) counters`, whose own pin check precedes every counter recipe (`run_without_stackpin_dryrun.log:57-61`). See S1. |
| #726's own tests still pass on the merged tree | Holds | `make counters`: four RESULT: PASS. `make counters-f5`: both shapes rc 0. `make counters-mutants`: 12 RTL cases and 3 F5 cases, each failing by name, each with a passing check-omission escape. `tkdiag` 5/5, `avtp_rxmon` 5/5 and `crf_rx` 69 checks pass, with 10/10 mutants. All use the pinned Verilator 5.050 (identity printed in `boundary_selftest_only_verilator.log:1`). |
| README and CI_WORKFLOWS.md stack-consumer statements hold as written | Holds | `sw/firmware/ctrl/README.md:180,235-238` and `CI_WORKFLOWS.md:96-98,322-326` re-read true against the probes above. R584-18-F2's four cited statements now hold. The test-prerequisite pages are a separate matter (RES-1). |
| Images equal dev `e81ce82f` | Holds | Executed: `ctrl_image.py --base e81ce82f`, all five shapes. Five of five head/base ELFs are byte-identical (same SHA-256), with +0 delta in every section (`ctrl_image_compare.txt`). For the 60 SRP-fixture images, the image-builder trees differ between head and `e81ce82f` only by the PR's own patch. That patch is byte-identical file by file to the one already proven against `d5858bbe`, apart from documentation and gate modules. Dev changed only `aecp/README.md` there (`image_inputs.txt`). The author's 65/65 manifest pair is equal as published. |
| The pin is unchanged | Holds | Gitlink `405dc68310a18f669049ffc10cc23eef7300dcff` at `97e71316` and `d40e4e98`. lwSRP is `08ee86e8` at `c20c85bd`, `97e71316`, `e81ce82f` and `d40e4e98`. |
| Hosted green at the head | Partly observed | Snapshot at 09:33Z: green for `rtl-fast` (aggregate), every firmware job (`firmware-boundary` 651 s, 36 % of 30 min), `docs-check`, `elaborate`, all Yosys shards and Verilator shard 1. Physical gPTP is a skipped context. Verilator shards 0, 2, 3 and 4 were still running, so the `verilator-suites` aggregate was pending (`hosted_checks_snapshot.txt`). Manager duty. |
| Residue applied | Holds | R584-17-RES-1 and RES-2 are applied with their exact text in the live body (lines 84, 94, 140). R585-18-RES-1 is resolved: no "unpushed" text remains, and its wording is quoted at line 174 (`pr705_body_at_review.md`). Every Round 20 file:line in the body resolves at the head. |

## Findings

### R584-19-RES-1 - RESIDUE - Docs - test prerequisite pages omit `third_party/tsn-c-stack`, which milan_dp now needs

- **Artifact:** `docs/testing/TESTING.md:150` and `:418-420`, `tb/verilator/README.md:7-9`, `tb/verilator/milan_dp/README.md:114-119`, `docs/testing/726_STREAM_COUNTERS.md:155-156`. Also the reason sentence at `QUICKSTART.md:157`.
- **Evidence:** since `d40e4e98`, milan_dp's default target (`all` -> `run: stack-pin`) and `counters` run the stack pin check. In the merged tree, F5 also builds the stack from the submodule. The pin check refuses an uninitialised submodule ("initialise the tsn-c-stack submodule", `receipts/f5_negative_args.txt`). These pages list the three other submodules as what the Verilator suites read, and `TESTING.md:419-420` says "The CI workflow initializes the same three". `rtl.yml:161` initialises four. That sentence was already stale at `97e71316` for `mbx`, and the delta adds milan_dp. `README.md:191` and `QUICKSTART.md:161` do initialise the submodule for running everything.
- **Impact:** wording only. A reader who follows those pages gets a clear, named refusal. No measurement, figure, verdict, test, code or generated artifact depends on the text.
- **Exact fix:**
  - `TESTING.md:150` and `:418`: the command becomes `git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack`. Add to `:150`: "`mbx` links the firmware cores from `third_party/tsn-c-stack`, and `milan_dp`'s default sweep and counter targets run its pin check first."
  - `TESTING.md:419-420`: "The CI workflow initializes the same four before the full sweep."
  - `tb/verilator/README.md:7-9`: "the four submodules the suites read", with the same four-submodule command.
  - `tb/verilator/milan_dp/README.md`, after line 119: "The complete `make` sweep and the `counters*` targets also need `third_party/tsn-c-stack` at its gitlink; they run its pin check first."
  - `726_STREAM_COUNTERS.md:156`: append ", with `third_party/tsn-c-stack` initialised at its gitlink".
  - `QUICKSTART.md:157`: "The `mbx` suite links the firmware cores from a submodule, and `milan_dp` checks that submodule's pin before its sweep and counter targets."
- **Verification:** re-read the pages; `scripts/docs_check.py`, `check_doc_paths.py` and `check_em_dash.py --base <dev>` pass.

### R584-19-S1 - SUGGESTION - Tests, Docs - `run`'s own `stack-pin` prerequisite is redundant, and no control covers it

- **Artifact:** `tb/verilator/milan_dp/Makefile:545`; PR body Round 20 ("aggregate `run` pins first too").
- **Evidence:** removing `stack-pin` from `run` gives no gate finding (`pin_wiring_mutants.log`). `run` still refuses an off-pin stack through the sub-make's pin check, after its RTL legs (`run_without_stackpin_dryrun.log`). Nothing reaches the stack unpinned either way.
- **Optional outcome:** keep it and describe it as early-fail convenience, or drop it. No change is required.

No other defect was found. Two suspicions were tested and refuted:
- F5 with a non-default `--stack` reading the submodule's `tests/`: refuted, because `acmp_fake.hpp` is included only under `AECP_TEST_APP` and F5 builds mailbox mode (`receipts/f5_stack_tests_override_probe.txt`).
- The milan_dp Makefile `OUTSIDE` reason being untrue: refuted, because no milan_dp recipe or source names a firmware or stack path except the `stack-pin` recipe.

## Per-lens results

[R584] PASS Conformance - #697 body acceptance; rulings 6091228902, 6092176555, 6116488747, 6140933191; `stream_counter_f5.py:43-54`; `ctrl_configs.py:122-124,153-154`; Makefile `:667-688`; gitlinks at `97e71316`/`d40e4e98` - checked: every round-20 item (merge, F1 classification with a load-bearing control, F2 pin before building with a planted control, images, pin, #726 tests) against the ruling. The `OUTSIDE` reason "its own compiler recipes build RTL harnesses" is true: no milan_dp file names a firmware or stack path outside the `stack-pin` recipe. Executed: 5/5 images equal, input identity for the rest, pin and lwSRP unchanged.

[R584] PASS RTL - `a71b0e41` tree `c857c6a9` equals `git merge-tree --write-tree 97e71316 e81ce82f`; `git diff a71b0e41 d40e4e98` holds no `hdl/` or harness C++ file; milan_dp Makefile recipes unchanged apart from prerequisites and `--stack`; `rtl.yml:161` verilator shards initialise `tsn-c-stack` for `run`; `firmware-boundary` hosted 651 s of 1800 s - checked: the composition adds #726's RTL unchanged. The sub-makes that `milan_dp_gptp`, `milan_dp_gm_steps`, `milan_dp_mclk` and `milan_dp_render` run (`ax1x1gptp`, `gmstep`, `print-*`) carry no new prerequisite. The physical-gPTP job's three-submodule checkout is therefore still sufficient. #726 RTL suites and mutants pass on the merged tree.

[R584] PASS Robustness - `receipts/probe_pin_order.log` (41/41), `pin_wiring_mutants.log`, `f5_negative_args.txt`, `run_without_stackpin_dryrun.log` - checked: four spoil kinds at every F5 and counter entry point, serial and `-j16`; refusal before any staging, simulator or recipe; `--build-only` with a variant refused; a missing stack refused by name; the order-only prerequisite holds under parallel make.

[R584] PASS Tests - `boundary_selftest_without_verilator.log` (112/120/4, 0 misbehaved), `boundary_selftest_only_verilator.log` (6/120/4), `f5_capture_judged/`, `held_text_probe_*`, `pin_wiring_mutants.log`, `make_counters*.log`, `suite_*.log`, `ci_selftests.txt` - checked: each new control can fail for its defect. The registry and capture removals are refused. The F5-only capture with a planted private include is caught and attributed. Each unpinned counter target is caught, the doubly-mutated one by the census alone. F5 without its pin call would fail its pin arms. The held-text probe flips from 1 to 0. The pin population 106 -> 120 adds up (4 F5 arms + 7 milan_dp bench arms + 3 plants), as does the boundary population 101 -> 103. `ci_events.py --selftest` (2169 items, 3064 arms), `ci_scope.py --selftest` and `suite_shards.py --selftest` pass. S1 is optional.

[R584] PASS Docs - `sw/firmware/ctrl/README.md:126-128,162,180,235-240`; `CI_WORKFLOWS.md:80-82,96-98,322-326`; `ctrl_configs.py:101` comment; PR body Round 20 table and residue paragraph (`pr705_body_at_review.md`); `docs_gates.txt` - checked: each new sentence against the code and the probes. The figures 103/120 are confirmed by the gate's own figure controls. `docs_check`, `check_doc_style`, `check_doc_paths`, `check_em_dash --base e81ce82f`, `gen_toc --check`/`--verify-anchors`, `check_submodule_docs`, `check_py_idiom`, `check_hygiene`, `measure_naming`, `measure_fail_fast`, `ci_events --check`, `check_todo_ownership` and `check_solution_docs` pass. RES-1 is wording residue and does not leave Docs unclean.

## Prior public findings at this head

| Finding | Status at `d40e4e98` | Evidence |
|---|---|---|
| R584-18-F1 (BLOCKER, boundary refuses the composed tree) | RESOLVED | gate PASS locally and hosted; held-text 0 at head, 1 at `a71b0e41`; removal controls |
| R584-18-F2 (MINOR, stack consumer without the pin check) | RESOLVED | `probe_pin_order.log`; Makefile prerequisites; README/CI_WORKFLOWS statements hold |
| R584-17-RES-1, R584-17-RES-2 | RESOLVED, applied with exact text | live body lines 84, 94, 140 |
| R585-18-RES-1 | RESOLVED (same defect, R584-17 wording applied; R585-18 wording quoted) | live body line 174 |
| R585-16-RES-1 (allowlist "names a program") | RETAINED RESIDUE, carried; text unchanged at `README.md:196`, `ctrl_build.py:199,551-552` | source |
| R584-17-S1, R584-17-S2 | RETAINED SUGGESTION; `ctrl_configs.py:143,156` unchanged | source |
| R584-16-S1 / R585-17-S1 and the earlier carried suggestions and #495 residue | RETAINED as R584-17/R585-18 list them; the delta touches none of their artifacts | `git diff 97e71316 d40e4e98` |
| R584-1 ... R584-17 and R585-1 ... R585-18 blocking findings | RESOLVED at `97e71316` per R584-17 and R585-18; not reopened by the delta | delta diff |

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 rulings; F5 classification and pin wiring; images (5 executed, input identity); gitlinks | R584-19 | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` |
| RTL | CLEAN | mechanical merge; delta has no RTL; milan_dp recipes and CI submodule init; #726 RTL suites | R584-19 | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` |
| Robustness | CLEAN | 41-case spoil probe; negative args; parallel make | R584-19 | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` |
| Tests | CLEAN (SUGGESTION S1) | both boundary self-tests; planted F5 capture; held-text flip; pin-wiring mutants; #726 campaigns | R584-19 | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` |
| Docs | CLEAN (RESIDUE RES-1; SUGGESTION S1) | README, CI_WORKFLOWS, PR body, 17 documentation commands | R584-19 | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` |

## Limits

- **No manager source bank** ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts plus this round's own runs listed above.
- **Not run here:** the full parent, PP, gPTP and Yosys banks; the firmware execution and mutation campaigns (`test_ctrl_firmware.py --self-test`, store, coverage); the full milan_dp sweep (`run`); act or any replica.
- **SRP images:** the 60 SRP-fixture images were not relinked here, because their runtime needs externally provisioned Picolibc and compiler-rt sources. Their equality rests on the input-identity proof and the author's published 65/65 pair.
- **ELF hashes are environment-specific:** my five composed ELFs have the author's sizes but different absolute hashes. Head and base are equal within each environment.
- **Physical calibration NOT RUN:** field skips and the skipped physical-gPTP context are not hardware proof.
- **Discarded setup attempts:**
  - A first boundary run under a Python without the pinned LiteX packages was stopped before its fifth capture. It was rerun in a private environment with `sw/litex/litex_pins.txt`.
  - Three documentation commands first failed for want of the pinned Markdown renderer. They were rerun after installing `tools/markdown/requirements.txt` with hashes.
  - Both attempts stay in the receipts. Neither counts as a result.
- **Paths:** local paths in receipts are normalised to `$CHECKOUT`, `$PACKET`, `$HOME`, `$TOOLROOT` and `$VERILATOR_DIR`.
- **Clone restored:** the review clone is back at exact head bytes. The index equals HEAD's tree (1315 entries); no file differs in bytes or mode; there are no flags and no residue; the five initialised submodules sit at their gitlinks, clean (`receipts/verify_restore.txt`). `external` was not initialised.

## Pending manager duties

- Accept hosted at the head once Verilator shards 0, 2, 3 and 4 and the `verilator-suites` aggregate finish. Shard 4 runs `milan_dp`, whose `run` now requires the stack pin.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn. The source base is `c20c85bd`, live dev `e81ce82f`.
- Carry R584-19-RES-1 and the retained R585-16-RES-1 to the residue checklist.
- Publish this report and the manifest-listed receipts.

R584-19 FINISHED
