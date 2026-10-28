[A692]

## Contents

- **[Status](#status)** -- STOP: one required fast-gate job needs a register-map decision; every other gate result is listed.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, related issues and roles.
- **[Description](#description)** -- The gitlink, the source-stream-ID wiring, the #790 cases, the updated models and documents.
- **[Authoritative references](#authoritative-references)** -- The clauses and the processor changes.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane did not change, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**STOP** at `f67a4ca1b32f2b247b772007e9731f26d2a82440`; `799-adopt-processor-f65c8ff7` -> `dev` (from `97aab1d0`, still the live dev tip).
Not ready for review until the decision below is taken.

- **Blocking: the `publication-census` job of `rtl-fast` fails.** `sw/mailbox/publication_census.py` (#665, ruling
  6088423771, decision 2 (a)) requires every read of a class-D output of `KL_pp_shadow` to be named. A read that
  reaches the wire must be carried by a field of the mailbox publication block (`sw/mailbox/mailbox.yaml`), which
  the split placement's firmware writes in place of the processor. The #202 wiring makes the AAF and CRF frames
  stamp `src_stream_id_o`, and the block has no per-source Stream ID field. Adding one is a register-map change
  beyond the `src_stream_id_o` routing, the assignment's STOP condition. Census at this head: 5 findings. With the
  two edits that need no decision (`src_stream_id_o` in `CLASS_D_PORTS`; the GET_STREAM_INFO selector-2 read as a
  `processor` row), 3 remain, all on the two stamps.
- **The resource gate refuses all three endpoints** against the eleventh record; route-1x1 LUT +753 (+1.47 %, below
  the assignment's 2 % STOP). Accepting it is an owner decision; the record is not re-baselined here.
- Every other gate the issue names passes (table below).

## Linked Issue / roles

Relates to #799
Relates to #790

Not "Closes": the acceptance is not met. The census job above fails, and the in-house qualification re-runs on the
built image (with the gPTP adoption) cannot happen in this lane.

Processor PRs #204 (#202), #207 (#205) and #208 (#206) are the donor changes adopted here.

Executor: `[A692]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Commit | Change |
|---|---|
| `a7235498` | `protocol-processor` gitlink `ed211803` -> `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8` (processor main). FPGA-gPTP stays at `55680bff` |
| `ed07eea3` | Pin-derived records, each through its generator: ROM ledger rows (both equal to the `ed211803` rows), boundary diagram, pin table row |
| `18444ac6` | The #202 source-stream-ID wiring, reviewed and finished as milan-fpga code, with two MAAP-conflict recovery legs |
| `fbc0723a` | #790 in milan_dp: `[GSI]` G11, three processor-copy arms in `gsi_mutants.py`, the datapath's GET_STREAM_INFO ledger restated |
| `897459bc` | #790 in pp_shadow: the `[GSI]` group |
| `9e1c8741` | The torture plan's MAAP conflict entry, which expected the old two-LeaveAll wait |
| `05b26476` | Testing guide, compliance matrix, register map notes, MAAP fabric page |
| `aabfd834`, `c0b7ebe0` | milan_dp README: G11 and the measured #790 arms |
| `856797ed`, `3ee2d969`, `f67a4ca1` | Pin page adoption section with the measured resources, CHANGELOG section, written to the audience style limits |
| `6ab0adc5` | Two register-map rows the change touched, without the em dash |
| `1f7420d1` | `sw/firmware/ctrl/README.md`: 171 tsn-c-stack pin controls (the four new sidmove targets) |

**The wiring (processor #202).** After a MAAP conflict the processor moves a declared source to a new Stream ID
and publishes each source's current ID on `src_stream_id_o`. `KL_pp_shadow` passes it out. In `milan_datapath`:

- the AAF framer stamps it for every talker (`KL_aaf_packetizer` `SID_PP_P = 1`), so a TCTX unique ID no longer
  reaches the wire; the stamp wire is declared ahead of its first reader (#193);
- the CRF Media Clock Output stamps its source's current ID where the shape has one;
- an output's GET_STREAM_INFO stream_id (selector 2) is the current ID (IEEE 1722.1-2021 7.4.16.2).

Two legs drive a real conflict, a peer ANNOUNCE from a lower MAC (IEEE 1722-2016 B.3.6.4): `obj_sidmove` (the
shipping 1x1 shape, AAF talker and CRF output) and `obj_sidmove8` (8x8, a named TCTX unique ID). The wire, the
PROBE_TX answer, GET_STREAM_INFO and the Talker Advertise name one ID before and after the move.

**#790 (processor #206).** An input's stream_id, stream_dest_mac and stream_vlan_id, and their three Table 5.9
flags, are reported only while it is settled (Milan v1.2 5.4.2.10.1). Four named cases in milan_dp `[GSI]` G11 and
in pp_shadow's `[GSI]` group: bound and probing before the first answer; settled; back in PROBING_PASSIVE after
TMR_NO_TK with the settled stream still in the binding view (5.5.3.5.18, 5.5.3.5.36); unbound.

| Planted in the processor copy (`make gsi-mutants`) | Named check that fails | Failures |
|---|---|---|
| selectors 0, 2 and 4 pass through while unsettled | G11 sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: stream_id is zero | 3 of 499 |
| selector 0's three flags pass through | the same case: the three flags clear | 1 of 499 |
| selector 4's stream_dest_mac passes through | the same case: stream_dest_mac is zero | 1 of 499 |

The campaign returns 0: the clean leg passes 499 / 499 and all 14 arms are caught by name. In pp_shadow the same
pass-through, planted in a scratch clone (not committed), fails 3 of 651: the stale case's flags read `0x52`,
stream_id `0x0200000000020790` and stream_dest_mac `0x91E0F0002A90`. That is #790's bench capture.

**#205.** No parent test, model or document expected the old zeroed listener fields. The split firmware's ACMP
already echoes them.

**Models and documents expecting the old behaviour.** The torture plan's MAAP conflict entry asserted a two-LeaveAll
wait; it now grades the move to another Stream ID (Milan v1.2 Table 5.3, IEEE 802.1Q-2018 35.2.2.8), with a new
assertion that the wire and the answers name the new ID. The testing guide's ordinary-command inventory, the
compliance matrix, the MAAP fabric page and the register map (the STRMW talker SID words keep a source's first ID;
the TCTX unique ID is no longer stamped) are updated.

**Resources** (Vivado 2026.1, the recipe's flows, at `05b26476`, the final RTL; against the eleventh record):

| Endpoint | Figure | Record | Head | Delta | Tolerance | Gate |
|---|---|---:|---:|---:|---:|---|
| `route-1x1` | LUT / FF / SLICE | 51,259 / 53,208 / 15,835 | 52,012 / 53,707 / 15,780 | +753 / +499 / -55 | 500 / 600 / 80 | LUT refused |
| | WNS / WHS ns | 0.236 / 0.028 | 0.440 / 0.036 | +0.204 / +0.008 | 0.25 fall | ok |
| `ooc-1x1` | LUT / FF | 23,828 / 20,000 | 24,346 / 20,404 | +518 / +404 | 250 / 250 | refused |
| `ooc-8x8` | LUT / FF | 32,467 / 28,220 | 34,156 / 29,782 | +1,689 / +1,562 | 316 / 339 | refused |

RAMB36, RAMB18 and DSP are unchanged. Route complete, 0 routing errors; slow corners WNS +0.440 ns, WHS +0.074 ns;
fast corners WNS +1.660 ns, WHS +0.036 ns. Of the route's +753 LUTs, +712 are inside the processor (its SRP talker's
owed-Leave copy, the ACMP talker's move and quarantine); the parent's wiring and everything outside the processor
are about +41.

**Gates** (clean clones; each rc is the command's own):

| Gate | Head | Result |
|---|---|---|
| Full sweep, four shard units | `3ee2d969` | 64 / 64 suites, 2,191,637 checks, 0 in-suite failures, 0 timed out; tally rc 0 |
| milan_dp | `3ee2d969` | 18 legs, 13,723 checks, 0 failures (notify 499 with G11, sidmove 50, sidmove8 52, the gptp and gptp-lat legs) |
| pp_shadow | `3ee2d969` | base 651, vid73 651, crf 691, pending 317 checks, 0 failures |
| milan_dp_gptp, physical | `3ee2d969` | PASS, 1 / 1 suite, 209 checks, 0 failures, not timed out (the physical leg 155, the two accounting verifiers 14 and 14; 5,412 s) |
| `make gsi-mutants` | `fbc0723a` | rc 0: clean 499 / 499, 14 / 14 arms caught by name |
| Firmware gate set, 8 commands | `3ee2d969` | all rc 0 |
| rtl-fast replica | `3ee2d969` | 11 / 12 `needs:` jobs success; `publication-census` failure (the STOP) |
| behave | `3ee2d969` | 14 features, 406 scenarios, 1,979 steps passed |
| Yosys `syn/yosys/run.sh` | `3ee2d969` | 60 / 60 tops; tied-input and tap-purity PASS |
| lint, xvlog, both idiom gates, source lists, port contracts, measures, pin records, builder bank | `3ee2d969` | 22 / 22 rc 0 (lint 89 <= 89; xvlog 0 findings; ROM digests re-record with no diff) |
| Docs gates, GNU Make 4.3 | `f67a4ca1` | 42 steps rc 0 (2 skipped by rule); LiteX leg, markdown on CPython 3.12.3 and the no-git step rc 0 |
| Resource gate, route-1x1 / ooc-1x1 / ooc-8x8 | `05b26476` | MATERIAL REGRESSION at all three (above) |

`git diff 05b26476 f67a4ca1` is Markdown only, and `git diff 3ee2d969 f67a4ca1` is `CHANGELOG.md` and the pin page.

## Authoritative references

- Milan v1.2 5.3.7.5 and Table 5.3 (the PAAD "may decide to use the same Stream ID as before, or another Stream ID").
- Milan v1.2 5.4.2.10.1 and Table 5.9; 5.3.8.5 and Table 5.5; 5.5.3.5.18 and 5.5.3.5.36.
- Milan v1.2 5.5.4.1 (PROBE_TX) and 5.5.4.3 with Tables 5.46 and 5.47 (GET_TX_STATE).
- IEEE 1722-2016 4.4.4.8 (stream_id) and Annex B (MAAP, B.3.6.4 compare_MAC).
- IEEE 1722.1-2021 7.4.16 (GET_STREAM_INFO; 7.4.16.2 "the current id of the stream") and 8.2.4.2.5 (txResponse).
- IEEE 802.1Q-2018 35.2.2.8 (no FirstValue change for an existing StreamID).
- Processor PRs #204, #207 and #208 and their merge bars; #790 and its STOP analysis.
- `syn/ooc/pp_resource_baseline.json`, the eleventh record; `docs/design/AREA_BUDGET.md`.
- `sw/mailbox/publication_census.py` and `sw/mailbox/mailbox.yaml` (#665).

## How to get into the same state

Set `REPO` to the candidate checkout. Point `VERILATOR`, `MAKE43_BIN`, `RV32_SDK`, `LITEX_PYTHON`, `GTEST_1_14`,
`CLANG_18_BIN` and `VIVADO_BIN` at the local dependencies. Before any command inside a submodule, check its own
top-level directory.

```sh
cd "$REPO"
git remote get-url origin
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
test "$(git -C gptp-processor rev-parse --show-toplevel)" = "$PWD/gptp-processor"
git submodule status protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination "$RV32_SDK"
python3 scripts/ci_rv32_sdk.py --destination "$RV32_SDK" --verify-only
export VERILATOR VERILATOR_JOBS=2 PYTHON_CPU_COUNT=4 PYTHONHASHSEED=0
export MILAN_RV32_CC="$RV32_SDK/bin/riscv32-linux-gcc"
export PKG_CONFIG_PATH="$GTEST_1_14/lib/pkgconfig" LD_LIBRARY_PATH="$GTEST_1_14/lib"
export PATH="$MAKE43_BIN:$CLANG_18_BIN:$VIVADO_BIN:$PATH"
```

The expected state: origin `https://github.com/kebag-logic/milan-fpga.git`, head `f67a4ca1b32f2b247b772007e9731f26d2a82440`, processor
`f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`, gPTP `55680bff3b287b9a7b0c759f51471fa617c17335`, GNU Make 4.3,
Verilator 5.050, Yosys 0.66, sv2v v0.0.12.

## How to validate

```sh
python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
make -C tb/verilator/milan_dp gsi-mutants
make -C tb/verilator/milan_dp sidmove
make -C tb/verilator/milan_dp sidmove8
make -C tb/verilator/pp_shadow
python3 syn/ooc/pp_resource_gate.py check-baseline
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 scripts/check_submodule_docs.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs" --wait
python3 scripts/suite_tally.py "$suite_logs" --quiet --expect-suite-root tb/verilator
syn/yosys/run.sh
(cd tests && behave --no-capture -f plain)
python3 sw/builder/test_builder.py
```

Expected today: the census exits 1 with the three stamp findings (the STOP); every other command exits 0. The
resource gate's `check` at each endpoint reports MATERIAL REGRESSION until the record is re-baselined.

## Known limitations / out of scope

- **The census decision** (the STOP). (A) a per-source current-Stream-ID publication register in the mailbox
  contract, the stamps mapped to it, and the CRF stamp's read made shape-independent; or (B) an owner ruling that
  the split placement stamps the configured ID, with a census exclusion for it.
- **The resource record** is not re-baselined; route-1x1, ooc-1x1 and ooc-8x8 exceed their tolerances.
- **8x8 and 4x4 shapes:** the datapath's maap-face source index is one bit narrower than the processor's, so the CRF
  output's ALLOC_DA and conflict arrive as source 0's. Processor PR #204 noted it for this adoption; it is outside
  #799's Required list. The shipping 1x1 shape is unaffected. A new issue is recommended.
- The STRMW talker SID words (`0x814`, `0x818`) keep a source's first ID; making them follow the move would change
  the register map.
- The in-house qualification re-runs need the built image and the gPTP adoption.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the census job fails; the qualification re-runs are owed)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the census job fails)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (the census decision)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
