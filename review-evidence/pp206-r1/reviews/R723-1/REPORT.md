[R723] POSITIVE - exact head e9272b5635e76bf12a69376d59fd21d059cae320

# R723-1: independent review of processor PR #208 (issue #206)

- PR: Mister-M-alt/protocol-processor-control-plane-avb-milan#208, head `e9272b5635e76bf12a69376d59fd21d059cae320`, tree `0482079467bc4e40ebac7997441c9569b4cc4a8f` (I confirmed both in the reviewer clone, and the tree again in a fresh clone from the public remote).
- Base: processor main `097a79875f20c27f0a5987a193c165c5086f3cf5`. Origin: milan-fpga #790, its STOP analysis (option A) and the manager's decision on that issue.
- Scope, as reconstructed from public sources: the issue #206 body ("Required", "Acceptance"), the assignment comment on #206, the PR body, milan-fpga #790 with its STOP and decision comments, and the diff `097a7987..e9272b5`. Evidence came from the public tree milan-fpga `2d5d308a`, `review-evidence/pp206-r1`. The processor repository has no AGENTS.md or CONTRIBUTING.md. Its contributor conventions are `docs/README.md` and `README.md`, and I read both.
- Prior public review findings on PR #208: none. At this head the PR thread holds only two "review started" notices (this round's and another reviewer's), so nothing had to be resolved or retained. I read no other reviewer's report.

## Verdict

POSITIVE. All five lenses are CLEAN. There is no open BLOCKER, MAJOR or MINOR finding. One RESIDUE (prose line wrap) and one SUGGESTION (test strength) are recorded below. Neither affects the verdict.

## What the change does (verified against the source)

`hdl/top/protocol_processor_top.sv` adds the wire `gsi_settled_w`:

- `:3532` declares it.
- `:3563-3564` drives it: `(32'(gsi_desc_index_o) < N_STREAM_IN_P) && (gsi_status_w[7:5] == PB_COMPLETED_C)`.

`gsi_status_w` is `lstn_gsi_status_r[sink]` (`:3550`), the committed listener status that selector 7 returns as pbsta/acmpsta (`:3575`). So the gate reads the same probing-status source as the probing_status field.

Inside `if (gsi_input_w)` (kind 0, STREAM_INPUT), while `!gsi_settled_w` (`:3578-3588`):

- selector 0 is `gsi_data_i & ~0x52000000`;
- selector 2 is 0;
- selector 4 `[63:16]` is 0, and the failure-code byte `[15:8]` stays SRP's.

Selector 6 now reads the same wire (`:3573-3574`), with behaviour identical to the old inline test.

I checked the bit positions in the microprogram. `hdl/aecp/ucode/gen_ucode.py:1440-1456` lays selector 0 as FMT_D (`[31:0]`) at @28 and selector 4 as FMT_Q (`{dmac[63:16], code, resv}`) at @52. The masks match the IEEE 1722.1-2021 GET_STREAM_INFO flags in MSB-first numbering, as the repository's F06.12 also states: STREAM_ID_VALID `0x40000000`, STREAM_DEST_MAC_VALID `0x10000000`, STREAM_VLAN_ID_VALID `0x02000000`. The bench capture in #790 (`0xd6000006`) decodes to exactly these three bits plus FORMAT and BOUND.

Only E_GSTRI gathers selectors 0, 2 and 4. The other kind-0 gathers use selectors 1, 3 and 15 (`gen_ucode.py:1636, 2354-2355, 2391, 2453`). The gate therefore reaches only GET_STREAM_INFO, which covers its solicited, unsolicited and GET_DYNAMIC_INFO record forms.

## Checks requested by the assignment

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | In-range STREAM_INPUT not PROBING_COMPLETED: the three flags clear and stream_id, stream_dest_mac, stream_vlan_id are 0, from the same source as probing_status | holds | RTL above. `receipts/suite-head/gsi-internal.log`: GI GATE steps PROBING, PROBING-SENT, REPROBE, REPROBE-SENT, PASSIVE-STALE, UNBOUND and RESET are graded by name and byte-exact, with pbsta/acmpsta in the same response. 6,373 checks, 0 failures |
| 2 | Settled inputs, every other field and flag, and STREAM_OUTPUT answers unchanged | holds | `gsi_body` (`tb/pp_top/sim_main.cpp:5415-5423`) changes only STREAM_INPUT bodies below COMPLETED. The full default build passes (10,317 checks, 0 failures), and so does the seven-build `make run` (rc 0, 10,872 checks, 0 FAIL, the same as the PR's figure). Reviewer probe P1, the gate leaking to STREAM_OUTPUT, is killed by `G2: STREAM_OUTPUT[1] Milan response byte-exact` (`receipts/suite-probe-out/full.log`). See SUGGESTION R723-1-SUG-01 |
| 3 | The four pp_top cases fail on the base, and the pass-through mutant is killed | holds | Head tests on base RTL: rc 1, 82 FAIL, 32 of them `GI GATE`, covering RESET, PROBING, PROBING-SENT, REPROBE(-SENT), PASSIVE-STALE (flags, stream_id and dest MAC) and UNBOUND (`receipts/suite-base-rtl/`). The settled case passes on the base by design, because the base answer is already correct there. It is the positive control, and the `settled-gate-closed` arm kills it. My 29-arm campaign: rc 0, 29 of 29 killed by their named checks, golden and restored PASS (`receipts/gsi-mutants/`). `settled-gate-removed` (restoring the pass-through) fails `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero`, and its 82 FAIL lines are byte-identical to the base-RTL run (`receipts/base-vs-passthrough-mutant.txt`). Base gsi-internal: 6,254 checks, 0 failures; head 6,373 (+119) (`receipts/suite-base-all/`) |
| 4 | Docs row for GET_STREAM_INFO | holds | 06 §6.2 realization text, F06.12 flags paragraph, F06.13 lineage rows and Reads paragraph; 02 §4.4 row; integrator guide §8; 00 REQ-AEM-010. All state the same rule as the RTL, including the out-of-range case. `make check` at head: rc 0 (`receipts/make-check/`) |
| 5 | Parent consumer gate (with the #202 patch), including the C++ and Python idiom gates | author receipts consistent; independently corroborated without the patch | Author receipts `author-r1/a691c/receipts/parent-static-10bb22af/01-16`: all rc 0, gitlink file records `e9272b5`. `parent-py-idiom-764d1253` shows the earlier `9abb41f` failing `long function 10 > ratchet 9`. Reviewer probe P2 (`receipts/parent-idiom-probe/`) uses parent dev `97aab1d0` without the patch, which is not public, with the gitlink at `097a7987` / `9abb41f` / `e9272b5`. Results: `check_py_idiom.py` rc 0 / 1 (`protocol-processor/tb/pp_top/gsi_mutants.py long function=1`) / 0; `check_cpp_idiom.py` rc 0 at all three pins. `mutations()` is 100 lines and `settled_gate_mutations()` 32. The 29-arm table is identical, in the same order, at `9abb41f` and `e9272b5` (`receipts/mutation-table-compare.txt`). The milan_dp `[GSI]` and parent sweep receipts are the author's, from pin `764d1253` (gitlink `9abb41f`, same RTL and tests). I did not re-run them |
| 6 | No top-level port, parameter or register-map change | holds | Every hdl hunk is inside the module body at `:3532` and later. The module header (729 lines) is byte-identical at base and head. No package, microcode, memory-map or parameter document changed (`receipts/no-port-param-regmap.txt`). Lint rc 0 over 41 modules (`receipts/lint-hdl/`) |

Comment rule: none of the added source lines carries a bench lane label, lane name, round, reviewer ID or issue-comment ID. `A8`/`A15` are the listener action-primitive registry IDs (docs/README §2), and "lane" in `view_lane` means a bit lane. No RESIDUE.

## Findings

### R723-1-RES-01 - RESIDUE - Docs

- Where: `docs/architecture/06_aecp_engine.md:397`.
- Defect: the reflowed paragraph leaves one 133-column source line, "fields and flags while the internal fields still report their state owners. An output's selector 2 stream_id is the integrator's word", inside a paragraph whose other lines are wrapped at 71 to 81 columns. The rendered page and every claim are unchanged. This is source layout only.
- Required outcome: break that line after "owners." so that "An output's selector 2 stream_id is the integrator's word" begins the next wrapped line, then rewrap to the paragraph's width.
- Verification: `awk 'NR>=394 && NR<=401 && length > 90' docs/architecture/06_aecp_engine.md` prints nothing, and the paragraph's words are unchanged.

### R723-1-SUG-01 - SUGGESTION - Tests

- Where: `tb/pp_top/gsi_internal.hpp:694-742` (`settled_gate`).
- Evidence: reviewer probe P1 (`scripts/probe_output_gate.py`) applies the same gate to kind-0 STREAM_OUTPUT selectors 0, 2 and 4. Only one check in the full default build kills it: `G2: STREAM_OUTPUT[1] ... byte-exact`. The `--gsi-internal-only` unit, which the mutant driver runs, passes it with 0 failures (`receipts/suite-probe-out/`).
- Impact: requirement (2), unchanged output answers, is pinned today, but by a single incidental check outside the gate section.
- Suggested outcome: at step PASSIVE-STALE, while sink 0 is unsettled, read STREAM_OUTPUT 0 and check its stream_id, destination MAC and the three flags byte-exact. Optionally add a driver arm that drops the `gsi_input_w` scope.
- Verification: P1 then fails a named `GI GATE` check under `--gsi-internal-only`.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.3.8.5, 5.4.2.10.1 and Table 5.9, Table 5.5; IEEE 1722.1-2021 7.4.16.2 and its flag masks; `pp_acmp_pkg.sv:104-107`; the selector 7 source; out-of-range and unbound behaviour; the #790 capture decoded | R723-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| RTL | CLEAN | `protocol_processor_top.sv:1030-1053, 1918-1944, 3495-3590` (status read `:3550`); `gen_ucode.py:1418-1456` and every other `GSI(n)` user; module header identical; lint rc 0 | R723-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Robustness | CLEAN | Request and wait handshake untouched (`gsi_req_o`, `aecp_gsi_wait_w`); live per-beat reads under the documented F06.13 coherence bound; reset and boot-preload status source; out-of-range index (status 0, so gated); GET_DYNAMIC_INFO records (W8e/W8m/W8m2 graded via `gsi_body`, failing on base); output scope probe P1 | R723-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Tests | CLEAN | `gsi_internal.hpp` settled_gate and helpers; `sim_main.cpp` fold and `gsi_body`; the `gsi_mutants.py` six arms and split; head, base, base-RTL and P1 runs; the 29-arm campaign; seven-build `make run`; mutation-table identity (SUGGESTION SUG-01) | R723-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Docs | CLEAN | 06 §6.2, F06.12, F06.13; 02 §4.4; integrator §8; 00 REQ-AEM-010; `tb/pp_top/README.md`; PR body line references (`:3532`, `:3554-3564`, `:3573-3574`, `:3578-3588`, all exact); `make check` rc 0 (RESIDUE RES-01) | R723-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |

## Reviewer execution (this round)

All runs use the pinned Verilator 5.050 (`receipts/verilator-identity.txt`: rev v5.050, wrapper sha256 `905795b9…e92f`) on disposable clones at exact head. Peak unit memory stayed under the 12 GB cap.

- `make check`: rc 0.
- `scripts/lint_hdl.sh`: rc 0.
- `make -C tb/pp_top run`: rc 0, 10,872 checks.
- Head default build, full and gsi-internal: rc 0 / rc 0.
- Head tests on base RTL: rc 1 (expected), 82 / 89 FAIL lines (gsi-internal / full).
- Base tree gsi-internal: rc 0, 6,254 checks.
- `gsi_mutants.py --jobs 5`: rc 0, 29 of 29 killed.
- Probe P1: killed by G2 only.
- Probe P2 (parent idiom scanners at three pins, unpatched parent): results as in row 5.

Publishing: `MANIFEST.sha256` lists 129 receipts and scripts. The Verilator build logs and the full `make run` transcript embed a local toolchain path, so they are kept local. `receipts/pp-top-make-run/run.summary.txt` carries every tally, check-count and FAIL line of that run, with the path replaced by `<home-path>`. Its rc is in `rc`.

## Limits

- I did not run the processor full sweep (`scripts/run_suites.sh`), `check-req-tags.py --evidence`, the `acmp_mutants.py` arms, any parent bank (sweep, milan_dp `[GSI]`, pp_shadow, `gsi-mutants`), Yosys/OOC or ROM digests. Those figures (1,030,712 checks; 2,190,635 parent checks; +664 LUT / +12 FF on `KL_pp_shadow`; ROM digests equal to `ed211803`) are the author's published receipts and are not reproduced here.
- The #202 wiring patch (`ff5068d2…1275`) is not public. Probe P2 ran on unpatched parent dev, so it isolates the processor's contribution and is not the patched gate itself.
- No manager source bank exists at this head, and none is claimed or inferred. Hosted CI at this head, queried 2026-10-27T10:00Z (`receipts/hosted-check-runs.txt`): `docs-gates` and `portability` completed success on both the push and pull_request runs, and `suites` was still in progress on both, so no conclusion is drawn from it. Hosted/act acceptance is the manager's.
- Physical calibration NOT RUN. No hardware or field evidence exists; skips are not hardware proof.
- Observation outside the delta, not a finding: `docs/architecture/02_interfaces.md:424` (pre-existing) tells the integrator to disarm its RX filter "at teardown" from the binding view. Per this PR's own text, that view keeps the stream identity until unbind. This may deserve a look in the #790 adoption.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `097a7987`, live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`) with the builder and native banks, and link the receipts on the PR.
- Read the hosted `suites` job conclusion at exact head and own hosted/act acceptance.
- Carry R723-1-RES-01 to the residue checklist.
- In the milan-fpga #790 pin adoption: the four `[GSI]` cases in milan_dp/pp_shadow, the `gsi_mutants.py` arm planted on `      if (!gsi_settled_w) begin`, the ROM digest rows, and the parent consumer gate with the #202 patch on the merged pin.
- Merge requires the second independent positive review and the full completion bar.

R723-1 FINISHED
