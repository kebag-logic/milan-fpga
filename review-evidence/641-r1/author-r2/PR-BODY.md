[A573]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 2](#round-2)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Round 2 REVIEW READY: all assigned local commands returned 0. The builder reports one archival calibration arm NOT RUN. Independent re-review and new-head hosted execution remain pending. A transient memory overrun is recorded under limitations.
`641-651-gate-guards` -> `dev`; base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Round 2 candidate: `614b4aa5f408d75673b546ce6efb6ef126437be2`.

## Linked Issue / roles

Closes #641
Closes #651

Executor: `[A573]`
Internal cleared-context reviewer: `[R566]`
External reviewer: `[R567]`

## Description

A stopped make parse could print a partial database and still verify a shape consumer. The inventory now checks the parse result while querying an empty goal, so missing generated products do not obscure a complete parse. Both remaining nested source derivations clear inherited query flags.

Converted elaboration guards could print an error and still map successfully. Both synthesis flows now restore converted error/fatal displays as `$error` tasks before parameter binding and cache lookup. Active guards fail; inactive generate branches remain legal. The existing CI workers invoke the same enforced flow.

The service-budget oracle now derives descriptor and journal sizes through the image generators. Its trace generator checks completed builds, raw log bytes, media and grading before writing the fixture. The simulation adapter returns the inherited builder census so fresh fixture builds can complete. Three fresh traces regenerate the oracle reproducibly, with no mirrored size fields. All three reject a planted byte-count mismatch.

## Round 2

Answers assignment comment 6084524982 and reviews R566-1/R567-1.
Current enforcement claims and both wording residues are corrected.
The fast CI job now schedules the guard self-test.
`pp_shadow` now asserts its nested source command status.
Its new control rejects `MAKE=false` under both Make versions.
Removing the assertion reproduces silent success under both versions.
All 228 shape checks pass with each Make version.
The CI contract passes 1749 items and 2374 mutation arms.
The width-52 example fails under both converter versions.
The legal width-64 control passes under both versions.
All 46 documentation/script commands returned 0.
The builder returned 0; one archival calibration arm remains NOT RUN.
Portability passed all 58 tops and both structural checks.
OOC passed all 18 tops.
The final planting check confirms five usable anchors.
All non-comment RTL bytes match the reviewed Round 1 source.
Tracked bytes, modes and all three required submodule pins are verified.
Generated files were removed; the worktree is clean.
Lint also passed a fresh replay with four workers.
Optional diagnostic preservation remains unchanged; its limitation is documented.
New commits only; publication and re-review remain manager duties.

## Authoritative references

- #641: all three acceptance items and assignment comments 6081334020/6084524982.
- PR #699: R566-1 and R567-1 findings and adopted suggestions.
- #651: both flow refusals, planted controls and inherited CI enforcement.
- #634: nested-make query behavior and the GNU Make 4.3 control method.
- `REQUIREMENTS.md`: REQ-VER-02 and REQ-VER-04.
- `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` and `syn/resmap/sweep_plan.json`: requested refusal points.
- `syn/yosys/README.md`, `docs/testing/CI_WORKFLOWS.md` and `CONTRIBUTING.md`: local and hosted verification contracts.

## How to get into the same state

```sh
git switch 641-651-gate-guards
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Set `WORK` to external scratch storage and export `TMPDIR="$WORK"` and `PYTHONDONTWRITEBYTECODE=1`. Use GNU Make 4.4.1, an isolated GNU Make 4.3 installation, Yosys 0.66, sv2v 0.0.12 and pinned Verilator 5.050. The fixture rebuild additionally needs the documented CPU-capture dependencies and RV32 compiler. `HANDOFF.md` records version and artifact digests and the local package-build caveat.

## How to validate

Run each command directly and require rc 0:

```sh
python3 scripts/check_entity_shape.py --self-test
PATH="$MAKE43_BIN:$PATH" python3 scripts/check_entity_shape.py --self-test
python3 syn/yosys/guard_selftest.py
python3 syn/yosys/ooc_selftest.py
python3 syn/yosys/cache_selftest.py
syn/yosys/check_list_hermetic.sh
sv2v() { "$SV2V12" "$@"; }
export -f sv2v
syn/yosys/run.sh
syn/yosys/ooc.sh
python3 sw/builder/test_builder.py --require-rv32
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 "$PACKET/RUN-ROUND2-GATES.py" "$PACKET/ROUND2-GATES.json" "$WORK/final-gates"
python3 "$PACKET/PLANT-CHECK.py"
python3 "$PACKET/NESTED-CONTROLS.py"
PATH="$MAKE43_BIN:$PATH" python3 "$PACKET/NESTED-CONTROLS.py"
unset -f sv2v
python3 "$PACKET/SWEEP-CONTROLS.py"
python3 "$PACKET/SWEEP-REPLAY.py" --repo . --work "$WORK/docs-example" --sv2v "$SV2V12" --flow-rev HEAD --label sv2v12 --points rx-tdata-52 --jobs 1
python3 "$PACKET/SWEEP-REPLAY.py" --repo . --work "$WORK/docs-example" --sv2v "$SV2V13" --flow-rev HEAD --label sv2v13 --points rx-tdata-52 --jobs 1
python3 "$PACKET/EXAMPLE-CONTROLS.py"
```

Export `SV2V12` as the pinned converter executable, `SV2V13` as the 0.0.13 executable, `MAKE43_BIN` as the isolated make binary directory, `MD_PYTHON` as the Markdown environment's interpreter, and `PACKET` as the handoff directory. The exported converter function retains the pin despite the flow's local executable-directory precedence. The sweep driver additionally needs sv2v 0.0.13 to reproduce converted guards; unset the function for that replay if needed.

To regenerate the trace fixture, build both supported shapes into separate external directories with `PYTHONHASHSEED=0`, `VERILATOR_JOBS=2`, `MAKEFLAGS=-j8` and the documented RV32 environment. Run populated `all` plans on both, plus populated `uart-paced` on the small build, using `--record-budget-findings`. Then run:

```sh
python3 tb/verilator/fw_service_budget/gen_oracle.py   --small-build "$SMALL_BUILD" --large-build "$LARGE_BUILD"
python3 "$PACKET/GENERATOR-CONTROLS.py" --small-build "$SMALL_BUILD"
```

Expected results: 228 shape checks under each make version; 36 guard controls; 75 OOC controls; 58/58 portability tops plus structural checks; 18/18 OOC tops; six expected sweep refusals; all 46 documentation/script commands rc 0, plus the bounded lint replay. The refreshed fixture passes 55 oracle and 14 flash checks; all three generator custody controls pass. The 8x8 trace retains two measured NVM-status budget findings, with no product or budget change.

## Known limitations / out of scope

- The builder bank returns 0 and reports one unavailable archived utilization-report arm as NOT RUN. No physical route was run to recreate that archive.
- Local synthesis used the required Yosys version from a package build with external ABC; byte equality with the hosted bundled-ABC build is not claimed.
- The current builder already refuses the two stream variants. The replay proves that refusal, then bypasses that earlier check only in memory so generated scratch inputs reach the downstream guards.
- The hosted portability result, independent reviews and candidate-merge validation remain pending the manager's publication workflow.
- The only RTL-file change corrects an enforcement comment. All non-comment RTL bytes, firmware, shipping images and submodule revisions are unchanged.
- Optional S2 remains unchanged: converted guard refusals name `$error`, without the original guard message.
- Fixture measurement evidence is retained from Round 1; Round 2 does not rebuild the fixture.
- Parallel validation briefly exceeded the assigned memory ceiling: 10.08 GB peak against 9 GB. No OOM occurred. The remaining heavy jobs finished sequentially, and the four-worker lint replay passed.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes under the assignment; archival-report exception recorded above
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
