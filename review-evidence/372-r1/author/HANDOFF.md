# #372 author handoff: [A170]

Bounded assertion rollout on `hdl/common/axis_mux_rr_2in_1out.sv`, as settled in
<https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5776353888>.
TAKEN: <https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5776503391>.
REVIEW READY: <https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5777604896>
(text identical to `REVIEW-READY.md`). The author stops at head `5bbf2953`.

## 1. State

| Item | Value |
|---|---|
| Worktree | `$CANDIDATE` |
| Branch | `372-bound-axis-assertions` (manager-created with `gh issue develop 372`) |
| Base | dev `88e9276b2a220c716f64a843f7e1eb8f9265e896` (= `git merge-base origin/dev HEAD`) |
| Head | `5bbf2953ea747403217aeeda020df6a6e5ff27f9` |
| Tree | `fee8638e957b1a4076da67cb7c1f368336f1a46c` |
| Commits | one, direct child of the base |
| Message | `Bind SVA checkers to axis_mux_rr_2in_1out with witnessed positives and a detection campaign (#372)` (one line, no trailer; `git cat-file -p HEAD` shows no body) |
| Worktree status | clean (`git status --short` empty; build dirs are `obj_dir_*`, already ignored) |
| Pushed | **no**. The author does not push; the head exists in this worktree only |
| Superseded local head | `8edd2ba671239add40188a8cdcb2341839a9b7c6`, never pushed or published, amended to add the elaboration-guard row; its logs are kept as `logs/superseded-*` |

Files (12 changed, 2256 insertions, 7 deletions):

| File | Change |
|---|---|
| `tb/common/sva/axis_stream_source_sva.sv` | new: reusable AXI4-Stream source-obligation checker (4 concurrent properties + elaboration guard) |
| `tb/common/sva/axis_mux_rr_2in_1out_sva.sv` | new: mux checker, 3 interface instances + 5 concurrent + 4 deferred-immediate laws |
| `tb/common/sva/axis_mux_rr_2in_1out_bind.sv` | new: `bind axis_mux_rr_2in_1out ... u_sva` |
| `tb/verilator/ptp_ts/mux_sva_main.cpp` | new: direct mux harness (8 scenarios, scoreboard, witness ledger), built at 8 and 64 bits |
| `tb/verilator/ptp_ts/sva_campaign.py` | new: 62-row detection campaign |
| `tb/verilator/ptp_ts/Makefile` | `all: run mux-sva sva-campaign`; `run` recipe byte-identical; new `mux-sva-build`, `mux-sva`, `sva-campaign`; `clean` extended |
| `scripts/measure_test_evidence.py` | +1 `DUT_READER_DISPOSITIONS` entry for the campaign (classification; unexplained-reader budget stays 0) |
| `docs/testing/ASSERTIONS.md` | new guideline page (generated Contents, hand descriptions) |
| `docs/README.md`, `docs/testing/TESTING.md`, `tb/verilator/README.md`, `docs/guides/VERIFICATION_DEVELOPER.md` | index rows/links |

Unchanged, verified by `git diff 88e9276b..HEAD -- <paths> | wc -l` = 0:
`tb/verilator/ptp_ts/sim_main.cpp`; `hdl sw protocol-processor gptp-processor third_party external .github configs syn constraints .gitmodules .gitignore`; every `scripts/*.budget`. Submodule pins unchanged.

## 2. Tool identity (pinned Verilator 5.050)

- Host `PATH` `verilator` is **5.052** (2026-09-05). It was NOT used for evidence.
- Evidence tool: the Arch package `verilator-5.050-1` present in a local
  container image layer (no container was started, nothing installed):
  `$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/bin/verilator`
  (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`; `verilator_bin` sha256
  `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`).
  The wrapper resolves its own `VERILATOR_ROOT` (`$RealBin/../share/verilator`).
- Provenance: `probes/verify_verilator_5050_mtree.py <layer>` hashes every
  installed file against the package's own mtree: `files=127 ok=123 mismatch=0
  missing=4`; the 4 missing are the man pages (`probes/verify_verilator_5050_mtree.txt`).
- Used as `make ... VERILATOR=<that path>` and `sva_campaign.py --verilator <that path>`;
  the campaign prints the identity line in every run.
- C++: host `g++ (GCC) 16.2.1 20260810`; `-j 8` on an 8-core host.
- Pinned documentation read: `docs/guide/exe_verilator.rst` and
  `docs/guide/languages.rst` at tag `v5.050` (copies in `probes/`).

## 3. Pinned behaviour measured (synthetic probes)

Sources in `probes/p1..p9`, re-run script `probes/rerun.sh <verilator>`, output
`probes/rerun-output.txt` (rc=0). Every claim in `docs/testing/ASSERTIONS.md`
"What the pinned Verilator does with assertions" traces to one of these:

| Fact | Probe evidence |
|---|---|
| assertions on by default (5.038+) | p1 `noassert` build (no flag) still fires `ap_hold` |
| `--no-assert` removes concurrent + immediate + action blocks | p2 `noassert` drop mode rc=0 silent; p5 `noassert` no witness |
| bind to a nonexistent module builds silently under `-Wall` | p2 `badbind` build: no `%` line, rc=0 |
| failure line + `Verilog $stop` + exit 1 | p1 drop mode, p8 |
| `disable iff` abandons at both ends | p1 `reset_after`/`reset_before` rc=0 |
| pass action runs every passing edge; `$assertvacuousoff` inert | p4: 12 calls/14 edges with and without `VAC_OFF` |
| `$past` in pass action gives an exact non-vacuity flag | p6: 15 calls, 4 non-vacuous = harness count 4 |
| `cover` needs `--coverage-user` | p1 `covuser`, p5 `covuser` vs `assert` |
| `assume property` checked, reports `Assertion failed` | p3 `ab` |
| `assert final` in `always_comb` works | p3 `bone` |
| DPI scope exists only with a live DPI call | p7 `assert` found vs `noassert` NULL |
| `+verilator+error+limit+N` reports all fails at an edge | p8 second run |
| two-state: `$isunknown(1'bx)` = 0 | p8 |
| `__Dpi.h` generated even with a mistyped bind | p9 |

## 4. Commands and exits

Baseline at the base (unchanged suite), pinned 5.050:

```
make -C tb/verilator/ptp_ts VERILATOR=<5.050>      -> rc=0   (logs/baseline-ptp_ts-88e9276b.log)
python3 scripts/suite_tally.py --verdict <that log> -> rc=0   "ptp_ts: 92 checks, 0 failures"
```

Final at head `5bbf2953`, pinned 5.050, from a `make clean` tree:

```
make -C tb/verilator/ptp_ts VERILATOR=<5.050>       -> rc=0, 111 s   (logs/ptp_ts-5bbf2953....log)
python3 scripts/suite_tally.py --verdict <that log>  -> rc=0
python3 scripts/suite_tally.py <dir holding it as ptp_ts.log> -> rc=0  "checks: 495   in-suite failures: 0" (4 tallies)
make -C tb/verilator/ptp_ts run (original leg only)  -> rc=0, 5 s, "ptp_ts: 92 checks, 0 failures"
```

Gates at head (all rc=0; output `logs/gates-5bbf2953....txt`):
`docs_check.py`; `check_em_dash.py --base 88e9276b` (0 findings over 292 added
lines in 5 pages) and `--selftest`; `check_doc_style.py` and `--selftest`;
`check_gptp_docs.py`; `check_doc_paths.py`; `gen_toc.py --check` and
`--verify-anchors`; `check_feature_status.py --self-test`;
`check_solution_docs.py`; `check_submodule_docs.py`; `check_diagram_pngs.py`;
`docs/DOC_MAP.gen.py --check`; `docs/traceability/gen_module_matrix.py --check`
(69 modules, unchanged); `check_baremetal_only.py --check`; `check_archive.py`;
`pp_srcs.py --check --selftest`; `check_rtl_source_lists.py` and `--selftest`;
`measure_naming.py --check`; `check_port_contracts.py`;
`measure_fail_fast.py --check`; `check_todo_ownership.py`;
`measure_test_evidence.py --check` (74 <= 77 unarmed, 0 unexplained readers,
3 <= 3 wall-clock) and `--selftest` (101/101); `check_hygiene.py --check`;
`check_sv_idiom.py`; `check_cpp_idiom.py`; `check_py_idiom.py`;
`check_sh_idiom.py`; `suite_tally.py --selftest`; `suite_shards.py --selftest`;
`lint_rtl.py --check` with the pinned 5.050 first on PATH (90 <= 90, unchanged).

Robustness only, NOT evidence: the same suite with the host PATH Verilator 5.052
also passes (rc=0, campaign 62/62; `logs/ptp_ts-host-verilator-5052-probe.log`,
taken on the amended tree before the commit).

## 5. Counts: original and new

| Tally line in the suite log | Base `88e9276b` | Head `5bbf2953` |
|---|---:|---:|
| `ptp_ts: N checks, 0 failures` (original `ptp_ts_top` harness) | 92 | 92 |
| `== ptp_ts mux sva w8: checks: N   failures: 0 ==` | - | 170 |
| `== ptp_ts mux sva w64: checks: N   failures: 0 ==` | - | 171 |
| `== ptp_ts sva campaign: checks: N   failures: 0 ==` | - | 62 |
| suite total (`suite_tally.py`) | 92 | 495 |

What a check is: harness checks are graded verdicts (4 scope checks, one per
output packet delivered intact, per-scenario drain/open-packet checks, reset
checks, the alternation check, 21 witness checks). Campaign checks are one per
row. No assertion evaluation, pass action or clock edge is counted anywhere.
w8 and w64 differ by one because the random scenario's seed is per width
(3728 and 3784, printed in each run's first line).

## 6. Witnesses at head (non-vacuous passes vs the harness's own port count)

| Property | w8 checker / harness | w64 checker / harness | Relation |
|---|---|---|---|
| `u_s0_stimulus.*` (4 rules) | 563 / 563 | 625 / 625 | equal |
| `u_s1_stimulus.*` (4 rules) | 608 / 608 | 689 / 689 | equal |
| `u_m_dut.*` (4 rules) | 172 / 172 | 228 / 228 | equal |
| `ap_state_legal` | 1081 / 1081 | 1192 / 1192 | equal |
| `ap_reset_releases_owner` | 10 / 10 | 12 / 12 | equal |
| `ap_owner_released_after_tlast` | 120 / 120 | 121 / 121 | equal |
| `ap_owner_held_until_tlast_handshake` | 787 / 379 | 896 / 403 | at least (internal state) |
| `ap_grant_only_to_requester` | 123 / 123 | 123 / 123 | at least (internal state) |
| `ai_grants_mutually_exclusive` | 1514 / 677 | 1668 / 723 | both above zero (immediate) |
| `ai_ready_only_for_owner_and_ready_sink` | 1514 / 677 | 1668 / 723 | both above zero |
| `ai_tvalid_forwarded` | 1468 / 674 | 1689 / 754 | both above zero |
| `ai_payload_forwarded_on_transfer` | 1098 / 500 | 1201 / 524 | both above zero |

## 7. Every property and trigger, with independent evidence

Campaign at head: 62 rows, 0 failures (`logs/ptp_ts-5bbf2953....log`; raw build
and run logs and scratch sources per row in `logs/campaign-raw-5bbf2953.../`).
Detection = build ok, exit 3 (harness assertion stop, run with
`+verilator+error+limit+1000`), and an `Assertion failed in <path>` line naming
the expected path; stimulus rows also require `stimulus fault injected`.

| Property | Instance(s) | Trigger rows (all PASS) | Mutation / fault |
|---|---|---|---|
| `ap_tvalid_held_until_handshake` | s0, s1 stimulus | `stimulus-s{0,1}_drop_tvalid-w{8,64}` (4) | withdraw TVALID one edge after the first stall, payload held |
| same | `u_m_dut` | `mutant-released_while_tlast_stalled-w64` | `if (s0_tvalid && s0_tlast && m_tready)` -> `if (s0_tvalid && s0_tlast)`; co-fires m payload rules and `ap_owner_held...` (release to IDLE zeroes m) |
| `ap_tdata_stable_until_handshake` | s0, s1 stimulus | `stimulus-s{0,1}_flip_tdata-w{8,64}` (4) | TDATA bit 0 flipped for one stalled edge |
| same | `u_m_dut` | `mutant-tdata_hidden_while_stalled-w8` | `m_tdata  = s1_tdata;` -> `& {TDATA_WIDTH{m_tready}}` |
| `ap_tkeep_stable_until_handshake` | s0, s1 stimulus | `stimulus-s{0,1}_flip_tkeep-w{8,64}` (4) | TKEEP bit 0 flipped |
| same | `u_m_dut` | `mutant-tkeep_hidden_while_stalled-w64` | `m_tkeep  = s0_tkeep;` -> `& {(TDATA_WIDTH/8){m_tready}}` |
| `ap_tlast_stable_until_handshake` | s0, s1 stimulus | `stimulus-s{0,1}_flip_tlast-w{8,64}` (4) | TLAST flipped |
| same | `u_m_dut` | `mutant-tlast_hidden_while_stalled-w8` | `m_tlast  = s1_tlast;` -> `&& m_tready` |
| `ap_state_legal` | `u_sva` | `mutant-illegal_state_reached-w64` | first `next_state = STREAM_1;` -> `state_t'(2'b11)` |
| `ap_grant_only_to_requester` | `u_sva` | `mutant-granted_without_request-w8` | `if (s1_tvalid)` (under `!last_served`) -> `if (1'b1)` |
| `ap_owner_held_until_tlast_handshake` | `u_sva` | `mutant-released_before_tlast_s0-w8`, `mutant-released_before_tlast_s1-w64` | drop `sX_tlast` from the release condition |
| `ap_owner_released_after_tlast` | `u_sva` | `mutant-kept_after_tlast-w8` | STREAM_1 release -> `next_state = STREAM_1;` |
| `ap_reset_releases_owner` | `u_sva` | `mutant-reset_ignored-w64` | `if (!rst_n) state <= IDLE;` -> `if (1'b0)` |
| `ai_grants_mutually_exclusive` | `u_sva` | `mutant-both_sources_ready-w64` | `s1_tready = (state != IDLE) && m_tready`; co-fires the grant law |
| `ai_ready_only_for_owner_and_ready_sink` | `u_sva` | `mutant-ready_ignores_sink-w8` | `s0_tready = (state == STREAM_0)` |
| `ai_tvalid_forwarded` | `u_sva` | `mutant-tvalid_waits_for_tready-w64` | `m_tvalid = s0_tvalid && m_tready` (the defect the mux comment records) |
| `ai_payload_forwarded_on_transfer` | `u_sva` | `mutant-tkeep_from_other_source-w64` | `m_tkeep  = s1_tkeep;` -> `s0_tkeep` |
| scoreboard (round-robin order) | harness | `scoreboard-round_robin_inverted-w8` | `last_served` ternary swapped; no property fires, `simultaneous_offers ... alternate` check fails |
| `gen_guard_tdata_width` | checker | `elaboration-tdata_width_12` | build at width 12 refused with the guard's own message |

Every mutation pattern is required to occur exactly once in the pristine
source; scratch copies live only under the campaign directory. The first
failing edge's full set of named failures is printed per row.

Load-bearing demonstration of the guard row (manual, `/tmp` only): with the
guard deleted from a scratch copy of the checker, the width-12 build still
fails, but on the harness `static_assert`, and the guard message appears 0
times, so the row's rule reports FAIL.

## 8. Lost-coverage controls (the detection check must fail)

| Row | What | Positive run | Faults (8 each) |
|---|---|---|---|
| `coverage-assertions_disabled-w64` | `--no-assert` | exit 1, `[FAIL] checker instance ...u_sva is elaborated with its assertions` (scopes absent), no assertion | all injected, exit 1, no property named: not detected |
| `coverage-bind_target_mistyped-w8` | bind target `axis_mux_rr_2in_1out_mistyped`; build log has 0 warnings | same scope refusal | not detected |
| `coverage-bind_ports_swapped-w64` | s0/s1 and owner flags mirrored in the bind; every law still holds | exit 1, only the 8 per-port stimulus witness checks fail (171 checks, 8 failures), no assertion | each stopped by the MIRRORED instance, so the detection check for the intended instance fails |
| `coverage-unused_path-w8` | clean build, `+scenario=single_beats +grade_witnesses` | exit 1, the 4 `u_m_dut` witnesses and the owner-held floor fail | none |

## 9. Limits (also in `docs/testing/ASSERTIONS.md`)

Two-state only (no X/Z; `$isunknown` inert), one clock (no CDC), simulation
only (no formal tool read the properties; the DPI witnesses would be compiled
out and stimulus instances become assumptions for one), cycle-based zero-delay
(no timing), one module (the mux instance inside `ptp_ts_top` is not bound: the
original `run` leg is unchanged), no functional coverage (`covergroup`/`cover`).
A campaign row proves a property can fail on one defect, not on every defect.

## 10. Open items for the manager (no action taken)

1. `scripts/test_evidence.budget` mutation ratchet reads 77; measured 75 at the
   base and 74 at head (`ptp_ts` is now armed). Not lowered, to avoid editing a
   shared budget file from this lane; lowering it is a normal tightening.
2. The `measure_test_evidence.py` disposition entry is a classification the gate
   requires for every mutation campaign; the unexplained-reader budget stays 0.
3. Suite time: `ptp_ts` goes from about 5 s to about 110 s on this 8-core host
   (18 extra Verilator builds, each `-j 8`); well inside the 1800 s suite budget.
4. Local sweeps on this host use the PATH Verilator 5.052; the suite passes on
   it too, but only the pinned 5.050 run is evidence.
5. The stimulus faults fire at each port's first stall, which is always an
   arbitration wait, so they do not cascade into `u_m_dut`; that isolation is
   deliberate and documented in the campaign.
6. The `u_m_dut` TVALID rule cannot fail alone on this mux with compliant
   sources (it is implied by forwarding, ownership and the source rules); its
   row shows it among the failures of the first failing edge.

No genuine DUT defect was found in the unmodified mux: every property passes
on it at both widths, and every failure seen came from a planted mutant, fault
or control.

## 11. Artifacts (this directory)

- `TAKEN.md`, `REVIEW-READY.md`, `PR-BODY.md`, this file
- `logs/baseline-ptp_ts-88e9276b.log`, `logs/ptp_ts-5bbf2953....log`,
  `logs/gates-5bbf2953....txt`, `logs/campaign-raw-5bbf2953.../`,
  `logs/ptp_ts-host-verilator-5052-probe.log`, `logs/superseded-*`,
  `logs/precommit-iteration{1,2,3}-ptp_ts.log` (uncommitted iteration runs, not evidence)
- `probes/` (p1..p9 sources, `rerun.sh`, `rerun-output.txt`, pinned rst docs,
  mtree script and output)
