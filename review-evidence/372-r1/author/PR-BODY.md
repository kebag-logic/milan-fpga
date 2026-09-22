[A170]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN on author evidence at `5bbf2953ea747403217aeeda020df6a6e5ff27f9`, reviews pending. `ptp_ts` reports 495 checks and 0 failures; the SVA campaign passes 62 of 62 rows. Branch `372-bound-axis-assertions` -> `dev`.

## Linked Issue / roles

Closes #372

Executor: `[A170]`
Internal cleared-context reviewer: `[R239]`
External reviewer: `[R240]`
Manager: `[A10]`

## Description

This adds the first assertion-based verification to the tree, as the bounded rollout settled in #372, and leaves the product RTL untouched. A simulation-only checker is bound by module name to the real `hdl/common/axis_mux_rr_2in_1out.sv`. A direct harness then grades the mux at TDATA_WIDTH 8 and 64, and a campaign shows that every property fails on a defect written against it.

| Piece | What it does |
|---|---|
| `tb/common/sva/axis_stream_source_sva.sv` | Reusable AXI4-Stream source obligations (IHI0051A 2.2): TVALID held, and TDATA, TKEEP and TLAST stable, from the first stalled edge to the handshake. The instance name says whose obligation it is (`u_<port>_stimulus` or `u_<port>_dut`). Width guard at elaboration. |
| `tb/common/sva/axis_mux_rr_2in_1out_sva.sv` | Three interface instances, plus concurrent laws for legal state, grant only to a requester, ownership held until TLAST, released after TLAST, and reset releases the owner. Deferred-immediate laws cover grant exclusivity, TREADY equal to "owner and sink ready", TVALID forwarding and payload forwarding on transfer. |
| `tb/common/sva/axis_mux_rr_2in_1out_bind.sv` | Module-name bind. Ownership is read as `state == IDLE` and so on, in the mux's own scope. |
| `tb/verilator/ptp_ts/mux_sva_main.cpp` | Compliant sources and a sink, and a scoreboard that never reads the checker: every beat once, in order, never interleaved, with round-robin alternation under saturation. A DPI witness ledger requires every checker scope to exist. Non-vacuous counts must equal the harness's own port counts where the antecedent is visible on the ports. There are 8 scenarios. |
| `tb/verilator/ptp_ts/sva_campaign.py` | 62 rows: clean runs, 16 stimulus faults, 14 DUT mutants on scratch copies, a scoreboard mutant, an elaboration-guard row, and 4 lost-coverage controls whose faults must go undetected. Raw logs stay in `obj_dir_sva_campaign/`. |
| `tb/verilator/ptp_ts/Makefile` | Default is `run mux-sva sva-campaign`. `run` is byte-identical and one `mux-sva-build` recipe builds every shape. `--assert` is explicit, `-j 8`, and there is no `-Wno-fatal`. |
| `scripts/measure_test_evidence.py` | One reader disposition, classifying the campaign as a mutation campaign. |
| `docs/testing/ASSERTIONS.md` | The guidelines: files and naming, binding, enabling, reset and past state, witnesses, proving failure and reproduction. It lists the pinned 5.050 behaviour measured and the limits. The page is linked from the documentation indexes. |

Pinned-tool facts that shaped the design, each measured on Verilator 5.050:
- Assertions are on by default since 5.038, and `--no-assert` removes them.
- A bind to a nonexistent module builds silently.
- A pass action runs on vacuous edges too, so the harness counts only a `$past`-flagged non-vacuous report.
- The simulation is two-state.

## Authoritative references

- #372 decision: https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5776353888
- `REQUIREMENTS.md` REQ-VER-01, REQ-VER-02, REQ-VER-04
- `CONTRIBUTING.md` sections 1-3; `docs/development/CODE_QUALITY.md` Rules 6, 8 and 10 to 12
- Arm IHI0051A section 2.2 (AXI4-Stream handshake and stability)
- Verilator v5.050 `docs/guide/languages.rst` (bind by module name, unknown states) and `docs/guide/exe_verilator.rst` (`--no-assert`)

## How to get into the same state

```sh
git fetch origin
git switch 372-bound-axis-assertions        # head 5bbf2953ea747403217aeeda020df6a6e5ff27f9
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# needs Verilator 5.050 (the CI pin), a C++17 compiler and python3
```

## How to validate

```sh
logs=$(mktemp -d)
make -C tb/verilator/ptp_ts VERILATOR=<verilator 5.050> > "$logs/ptp_ts.log" 2>&1; echo "make rc=$?"
python3 scripts/suite_tally.py --verdict "$logs/ptp_ts.log"; echo "verdict rc=$?"
python3 scripts/suite_tally.py "$logs"
python3 tb/verilator/ptp_ts/sva_campaign.py --list
python3 scripts/measure_test_evidence.py --check
```

Expected result and pass criteria:
- make exits 0, and the verdict exits 0.
- There are four tallies: `ptp_ts: 92 checks, 0 failures` (unchanged), `ptp_ts mux sva w8: 170`, `w64: 171` and `sva campaign: 62`, all with 0 failures.
- The campaign prints 62 `[PASS]` rows, and each row's build and run logs are under `tb/verilator/ptp_ts/obj_dir_sva_campaign/<row>/`.
- The evidence gate reports 0 unexplained readers.

## Known limitations / out of scope

- The simulation is two-state, so X and Z propagation is not established.
- One clock, so no CDC.
- No formal tool was run.
- Zero-delay, so nothing is claimed about timing closure.
- One module: the mux instance inside `ptp_ts_top` is not bound, because the original leg is unchanged.
- No functional coverage (`covergroup`/`cover`).
- No product RTL, firmware, submodule pin, workflow, CI-policy or budget change.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (author evidence in the REVIEW READY comment; reviewers to confirm)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (author ran the focused suite and every relevant gate; the manager owns the full bar)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

🤖 Generated with [Claude Code](https://claude.com/claude-code)
