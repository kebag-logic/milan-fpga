[A681f]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Round 6: hosted `rtl-fast` failed at round 5's head on the TSN stack boundary gate, and this round fixes that.**

- The failing step was `firmware-boundary`'s "Hold the TSN stack boundary over the firmware builders' compiles" (run 40408916714).
- That gate finds by text every Python module and Makefile that names the firmware's tree, and refuses any that `sw/firmware/ctrl/test/ctrl_configs.py` does not classify. It refused six of this harness's files.
- This round classifies them in `ctrl_configs.py`, each with what it compiles, and changes no gate code.
- No firmware, harness code, measurement or published figure changes. The images rebuilt at this head are byte-identical to round 2's.
- Both reviews of round 5 were POSITIVE. This round's change is new, so it needs review.

- The failing step, run locally exactly as `rtl-fast.yml` writes it at this head: `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`. It prints `ctrl_boundary: PASS`, rc 0, with `0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved` over 3084 recorded compiler invocations.
- `firmware-verilator`'s step (`--only verilator`, the pinned Verilator 5.050) also prints `ctrl_boundary: PASS`, rc 0.
- 107 local gates ran one at a time at this head. Every one is rc 0, with the tree clean after it:
  - both boundary runs, and every other step of rtl-fast's firmware jobs: `firmware-unit`, the three mutant shards plus shard 0 (`test_ctrl_firmware: PASS` on each), the store suite (435 tests) and the coverage gates;
  - the bare-metal scope gate (`scripts/check_baremetal_only.py --check`: 0 findings across 1431 files);
  - the docs workflow's check-mode commands and self-tests (the em dash gate: 0 findings over 655 added lines);
  - the harness self-test: 87 checks pass and 62 of 62 mutants are caught, unchanged;
  - the compiler-absent control and the end-station builder gate, each with its one NOT RUN arm, as in round 5;
  - `git diff --check`;
  - behave, 406/406 scenarios.
- The full Verilator sweep ran because a shared file changed: 64 of 64 suites in four shards, 2,190,531 checks, 0 failures.
- The boundary gate is now in the lane's standing gate table. It was missing from rounds 1 to 5, which is how they all passed locally.
- The act runner's self-test is left to CI, which AGENTS.md requires of a candidate's copy.

`665-s2-cpu-budget` -> `dev-soft-core`, head `e0e1b4649ea3af908a8f32eccaad7903fa2cc134` (one commit on round 5's `f58d049b`).

**The baseline for S2b and S2c** is unchanged: arm A's composed maximum over every backlog window, at least 31.32 ms at 1x1 and at least 44.19 ms at 8x8. Those figures are lower bounds, because SRP's load is never released in the bound-talker windows. Compare them window by window, over the same four backlog rows, using the README's composed-window table.

- The figure over released windows only (14.81 / 27.84 ms) is not a baseline. A change that lets SRP be served adds windows to it, so its before and after would cover different windows.
- Neither is a partial figure. A re-measure that leaves out a backlog row names that row, and its figure covers fewer windows than the baseline.

## Linked Issue / roles

Relates to #665 (lane S2). Not every acceptance item is met: the rows miss T_svc, and one RESIDUE item stays with the manager (see Known limitations).
Relates to #397 (re-opened by the Mark II decisions).

Executor: `[A681f]`
Internal cleared-context reviewer: `[R703]`
External reviewer: `[R704]`

## Description

The round-6 assignment is [issuecomment-6435512208](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6435512208).

**The failure.** At `f58d049b` the boundary gate refused six files under `tb/verilator/ctrl_service_budget/` by name:

- the programs `build.py`, `fixture_variant.py`, `runtime_ssp.py` and `selftest.py`;
- the modules `scenario.py` and `split_soc.py`, which compiled nothing in the capture.

The assignment quotes the first refusal only, and only up to PART_OF. The full message also offers OUTSIDE ("compiles none of the firmware's") and SUITES ("compiles only in a suite"). No local gate in rounds 1 to 5 ran this step, which is how all five passed locally. It is in the standing gate table from this round on.

**The change.** `sw/firmware/ctrl/test/ctrl_configs.py` classifies each file by what it actually compiles (`git diff f58d049b`: 26 lines in `OUTSIDE` and `SUITES`, no other code):

| File | Category | What it does, and why that category |
|---|---|---|
| `build.py` | `OUTSIDE` | It delegates every compile of the firmware. Its image goes to `ctrl_srp_image.py`, run unchanged at the shapes (`endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8`), interface counts (1, 2) and AECP composition that the gate runs it at itself (`ctrl_runs.image_runs`). The split layout's reset entry is the one `test_ctrl_memory.py --build-only` compiles in the same capture, and the runtime archives change only the link. A control's planted copy of the firmware tree, outside the checkout, goes to the same builder. A variant arm goes to `fixture_variant.py`, and the runtime to `runtime_ssp.py`. Its own compiles build the test SoC's Verilator model. This is the existing `tb/verilator/milan_dp/Makefile` entry's shape: "delegates firmware builds to the separately captured F5 program; its own compiler recipes build RTL harnesses". |
| `runtime_ssp.py` | `OUTSIDE` | It runs `ctrl_image_runtime.py` (already `OUTSIDE`) with `-fno-stack-protector` added (#723). The bare-metal runtime comes from picolibc's and compiler-rt's sources outside the checkout, with no firmware or stack source. |
| `scenario.py` | `OUTSIDE` | It writes the stimulus and reads `AECP_REGISTRATIONS` from `aecp.h`. It has no subprocess call. |
| `selftest.py` | `OUTSIDE` | The grader self-test. It reads `AECP_REGISTRATIONS` from `aecp.h` and has no subprocess call. It calls only `run.py`'s grading and table functions and `build.py`'s digest and reuse checks. |
| `split_soc.py` | `OUTSIDE` | It exports the test SoC with LiteX, with `compile_software=False` and `compile_gateware=False`. It reads the image's placeholder addresses from `ctrl_build.RV32_FLAGS` and the store's generated headers. It compiles no firmware or stack source. |
| `fixture_variant.py` | `SUITES` | It compiles only in the labelled variant arms (`run.py --variant`): `ctrl_srp_image.py`'s compiles, with the size fixture read from `build.py`'s edited copy outside the checkout. The gate's own builds compile every checkout source it compiles. |

**Why not BUILDERS or PART_OF**, the two options the assignment names:

- **PART_OF** means "runs under another builder". No known builder runs any of these files. Their parent is `run.py`, which names no firmware tree.
- **BUILDERS** obliges a hosted job to run the builder under the gate's capture, and the gate refuses a builder that does not exit 0. No hosted job can run `build.py`:
  - its `firmware()` imports the picolibc and compiler-rt data packages, which no workflow installs;
  - the full build also needs the patched LiteX tree (`sw/litex/litex_pins.txt` says the pins alone cannot elaborate a config) together with Verilator. `firmware-boundary` installs the LiteX pins but has no Verilator, and `firmware-verilator` has Verilator but no LiteX.
- Registering `build.py` as a builder would therefore need an edit under `.github/` and to the CI generators. That is outside this lane's scope, so it is not done here. It is a question for the manager (Known limitations).

**Not weakened.** The gate's code, its controls and its other entries are unchanged.

- Removing any one of the six new entries makes the gate refuse that file by name again. A probe that runs the gate's own `ctrl_configs.held` on a stub capture shows this for all six.
- At `f58d049b` the same probe gives the hosted refusal byte for byte.
- Every firmware compile the harness makes of a checkout source is one the gate already captures and judges, at the same arguments.

**No image or figure change.** `ctrl_configs.py` is read only by the boundary gate (`ctrl_boundary.py`, `ctrl_runs.py`, `ctrl_plants.py`). No image builder reads it.

- Every harness image was rebuilt at this head through `build.firmware` alone: the six arms and three controls.
- Each ELF's sha256 equals the one round 2's `build.json` recorded (A1 and the as-built control `d4c28047…`, A8 `c89a1871…`, B1 `f561a45f…`, B8 `741d33e3…`, S1 `ef7809fe…`, S8 `5d54d5e4…`, the slow-ADP control `367e7f7f…`, the slow-SHUTDOWN control `3818d15f…`).
- One side effect is disclosed: `build.py`'s `tree:firmware` digest covers all of `sw/firmware/ctrl`, `ctrl_configs.py` included. So a build made before this commit is refused for reuse ("reused build is stale: tree:firmware changed"), and a regrade needs a rebuild. The rebuilt images are those above.

The harness README's "The test SoC" section gains the classification and the rule that a new file naming the firmware's tree must be listed (`README.md:107-118`).

Figures (CPU 50 MHz, bus 100 MHz), unchanged from round 5:

| Figure | 1x1, one interface | 8x8, two interfaces |
|---|---|---|
| Paths missing T_svc (instances), arm A | 22 of 81 (58 of 141) | 60 of 129 (102 of 182) |
| Composed maximum over every backlog window, arm A | at least 31.32 ms (backlog-adp), a lower bound | at least 44.19 ms (backlog-adp-refill), a lower bound |
| Over 3 of 4 backlog windows, arm B (`backlog`, `backlog-adp` and `backlog-owed`; `backlog-adp-refill` not run; a partial figure, not the composed maximum; each window released) | 14.81 ms (backlog) | 27.84 ms (backlog) |
| Over the windows that released their load only, arm A (not the composed maximum) | 14.81 ms | 27.84 ms |
| Worst pass, A | 31.32 ms | 59.79 ms |
| SRP's records under the composed load | never released in arm A's bound-talker windows (at least 568 to 628 ms); elsewhere first 66-84 ms, last up to 186 ms | never released likewise (at least 584 to 659 ms); elsewhere first 131-144 ms, last up to 341 ms |
| Every fan-out at capacity, arm A (16 / 32 recipients) | 7.77 to 11.33 ms (SET_NAME the longest) | 12.39 to 22.98 ms (SET_NAME the longest) |
| Every fan-out at capacity, arm B | 7.77 to 14.80 ms (BIND_RX's GET_STREAM_INFO notice the longest) | 12.39 to 32.78 ms (SET_STREAM_INFO on interface 1, over the 24 ms ceiling) |
| A recipient's cost, every fan-out, both arms (arm A in brackets) | 11,818 to 21,875 CPU cycles (11,818 to 20,358) | 11,786 to 22,030 (11,844 to 20,486) |
| A response with 7 frames owed ahead (12 ACMP) | 126.29 ms | 161.10 ms |
| The four commands behind it | none answered | two answered (176.52, 188.27 ms), two never |
| An event behind 15 others | 15.49 ms | 44.65 ms |
| An ACMP command behind a full acmp ring | 63.30 ms | 108.71 ms |
| An ENTITY_AVAILABLE behind the adp ring (observed) | 67.93 ms | 83.51 ms |
| The same, its bucket refilling (observed) | 88.33 ms | 118.81 ms |
| SHUTDOWN -> ENTITY_DEPARTING | 0.58 ms | 0.58 / 1.17 ms |

Decision input:

- **D4 (a)**: per-pass CPU work sets the time.
  - `srp_mbx.c:441-451` admits an SRP record only when no tick is owed and no event is pending. The mailbox ticks every 10 ms. Whenever every pass is over 10 ms, as in arm A after a bind, SRP takes nothing.
  - A notification costs 11,786 to 22,030 CPU cycles a recipient (11,818 to 20,486 in arm A). The notifications go one after another in one pass.
  - The rest is `memset` and `memcpy`, lwSRP's `mrp_mad`, AECP's polls, and software multiply and divide.
  - A cap that keeps passes under the tick also ends SRP's starvation.
- **D4 (b)**: the event, ACMP and MAAP backlogs are bounded by ring room. ADP, AECP and SRP are observed at their burst. Every loaded channel's last record misses T_svc. The ACMP ring's room (12) exceeds the core's owed responses (8).
- **D3**: unchanged. A flash-window read costs 15 to 29 times a block RAM fetch. The hot set is at least 42,080 B (1x1) and 43,060 B (8x8).

## Authoritative references

- `docs/reference/FR_NFR.md` 3.4.1:
  - the markers;
  - "the last required recipient's commit ends a notification fan-out";
  - "backlog ... consume this budget";
  - TX-ring backpressure.
- H-NOTIFY in `FR_NFR.md` 3.4.2.
- `docs/design/MAILBOX_SPLIT.md:495-502`, `:645-657`, `:753-758`.
- `sw/mailbox/mailbox.yaml`: token buckets, ring words, the event ring, and the receive and transmit rings' names. `hdl/milan/mailbox/KL_mbx_rx.sv`: admission.
- `scripts/check_baremetal_only.py`: the bare-metal scope gate (#259), run by `.github/workflows/docs.yml`.
- `sw/firmware/ctrl/test/ctrl_configs.py` (its docstring, BUILDERS, PART_OF, OUTSIDE and SUITES) and `ctrl_boundary.py`: the TSN stack boundary gate (#697), run by `.github/workflows/rtl-fast.yml` in `firmware-boundary` and `firmware-verilator`; `sw/firmware/ctrl/README.md` describes it.
- AECP firmware:
  - `sw/firmware/ctrl/aecp/aecp.h` (`AECP_REGISTRATIONS`);
  - `aecp.c` (`transmit`, the retry);
  - `aecp_commands.c`;
  - `sw/firmware/ctrl/test/ctrl_aecp_image.c` (`a_format`).
- SRP, the loop and ACMP:
  - `sw/firmware/ctrl/srp/srp_mbx.c:441-451`;
  - `sw/firmware/ctrl/loop/ctrl_loop.c` (`service_rx`);
  - tsn-c-stack `acmp.h` (`ACMP_OWED_MAX`) and `acmp.c` (`room`).
- IEEE 1722.1-2021 7.5.2 (unsolicited notifications), 7.4.2.1, 7.4.15.1 and 7.4.45.1; Milan v1.2 5.4.5.2, Table 5.22 and Table 5.26.
- Owner decisions D3, D4 and D5 (issuecomment-6409738976), and the cache-first decision (issuecomment-6421463860).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2-cpu-budget
git submodule update --init third_party/tsn-c-stack third_party/lwSRP
```

Use the capture prerequisites (`tb/verilator/nvm_capture_cpu/README.md#run`):

- the product LiteX tree, with its virtual environment first on `PATH`;
- the pinned RV32 SDK and Verilator;
- `LITEX_ENV_CC_TRIPLE`, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

Keep build directories outside the checkout. The Markdown gates need the pinned renderer (`tools/markdown/requirements.txt`).

## How to validate

```sh
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 scripts/check_baremetal_only.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-ports --variant answering-ports --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-shutdown --variant shutdown-entry --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-shutdown --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --cpu-regions as-built
python3 scripts/docs_check.py
python3 scripts/check_py_idiom.py
python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f
python3 scripts/gen_toc.py --check
cd tests && behave
```

Expected result / pass criteria:

- The first boundary run (`firmware-boundary`'s step) prints `ctrl_boundary: PASS`, rc 0, with `0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved`. It needs the pinned RV32 SDK, and a `python3` with PyYAML and `sw/litex/litex_pins.txt`. At `f58d049b` it refuses the six harness files by name.
- The second (`firmware-verilator`'s step, the pinned Verilator on `PATH`) and every firmware step after it exit rc 0.
- The bare-metal gate prints `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`, rc 0.
- The self-test prints `self-test: 0 failures` with 87 `PASS` and 62 `MUTANT caught` lines, rc 0.
- Run summaries, each rc 0:
  - 1x1 run: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
  - 8x8 run: `17 groups graded, 0 refusals, 102 T_svc misses (102 of 182 probe instances, 60 of 129 paths)`.
  - 1x1 answering-ports run: `8 groups graded, 0 refusals, 41 T_svc misses (41 of 68 probe instances, 18 of 44 paths)`.
  - Shutdown arm: `2 groups graded, 0 refusals, 0 T_svc misses (0 of 2 probe instances, 0 of 1 paths)`.
- Each figure repeats to the cycle. The 1x1 run's `table.md` ends its composed-window table with `Composed maximum over the 4 backlog windows: at least 1,565,803 CPU cycles (31.316 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).`, then the released-only figure, 740,260 (14.805 ms).
- The 1x1 answering-ports run's `table.md` reads `Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 740,260 CPU cycles (14.805 ms), backlog.` Its `results.json` record has `"not_run": ["backlog-adp-refill"]` and `"partial": true`.
- The controls print `CONTROL slow-adp-rx caught`, `CONTROL slow-adp-shutdown caught` and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.
- Each listed docs gate is rc 0; the em dash gate reports 0 findings.
- behave: 14 features, 406 scenarios, 1977 steps passed.

## Known limitations / out of scope

- **`build.py` is OUTSIDE, not a known builder.** Making it one needs a hosted job that can run it under the capture. That job would need the picolibc and compiler-rt data packages and the patched LiteX tree beside Verilator, plus a build-only mode in `build.py`. That is a workflow and generator change, so it is left to the manager, as a possible new Issue.
- A harness build made before this PR's last commit is refused for reuse: the firmware tree digest covers `sw/firmware/ctrl`, and `ctrl_configs.py` is in it. Rebuild instead. The images rebuild byte-identical.
- The rows miss T_svc, and this PR repairs no service path.
  - The [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) puts instruction-cache evaluation (S2c) before firmware-only tuning (S2b, a per-pass work cap in `ctrl_loop` under D4). Both re-base against the composed maximum over every backlog window.
  - The SRP starvation, the ACMP drop and the per-recipient cost are measured and reported here. Whether they become Issues or S2b scope is the manager's decision.
- RESIDUE R703-1 R-4 / R704-3-R1 (one sentence in `docs/testing/TESTING.md`) is not applied. That file is in the release lanes' file map, which split lanes stay out of, so it stays on the residue checklist.
- Arm B runs three of the four backlog rows and was not re-measured with `backlog-adp-refill`, so its figure over the backlog windows is partial, and is labelled so.
- R703-4's suggestions S1 to S3 are optional, outside the round-5 assignment, and not applied:
  - S1: fan-out recipients that commit out of registration order (P6 escapes);
  - S2: a record released on the bus cycle of a later record's commit (P9 escapes);
  - S3: R703-3's S1 to S3, carried (H3 escapes; the idle minimum's exclusion; R703-2's S1 to S3).
- A composed window closes three quiet passes, or 500 ms, after its row is served. A record still unreleased then is reported with the time it had waited by the run's end, a lower bound.
- A record's service ends at the end of its releasing pass; lwSRP may keep a record for replay and finish it later.
- In arm A the fixture's stream observation reports unavailable. So SET_CONFIGURATION, SET_STREAM_INFO, an output map edit and BIND_RX's GET_STREAM_INFO notice complete only in the answering-ports arm. At 8x8 the image's input maps have capacity 0.
- SET_STREAM_FORMAT is refused in both arms, whose format port answers unsupported, so its fan-out is not run.
- The lock expiry's notice (60 s) and the counter pushes are not run.
- The ADP, AECP and SRP backlog rows are observed at their burst; the refill leg is one sample of sustained arrivals.
- SHUTDOWN is measured through a labelled test-only entry. START_STREAMING is not run.
- Ends are mailbox commits: no wire, ingress, egress or network time. Flash erase and program waits are zero. There is no DDR3 and no datapath.
- The linked image addresses placeholder devices; #791 and #723 are open.
- The self-test is portable, but no CI job runs it yet; that registration is a CI change.
- `docs/testing/TESTING.md` and `.github/` are not touched: the release lanes and the CI owner hold them.
- Physical calibration was not run; nothing here is hardware evidence.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
