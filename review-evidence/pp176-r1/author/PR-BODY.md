[A629] SET_STREAM_INFO: accept the IEEE 1722.1-2013 48-byte body beside the 2021 one, answer in the 2021 form

Refs #176 (see "Acceptance" below for why this does not close it by itself).

Branch `176-ssi-2013-body`, one commit `29f58ad3` on main `22c139a4`.

## What changes

SET_STREAM_INFO on a Stream Output now accepts two bodies:

- the IEEE 1722.1-2021 body (Figure 7-40, 84 payload bytes, cdl 96), as before;
- the IEEE 1722.1-2013 body (Figure 7.46, 48 payload bytes, cdl 60), new.

The 2013 body is the 2021 body's first 48 bytes. The only difference: 2021 turns the reserved
word at @70 into `ip_flags` and appends the ports and the two IP addresses. So `flags` (@28) and
`msrp_accumulated_latency` (@48) sit at the same offsets in both.

Both bodies take the same routes, in the same order:

| Case | Answer |
|---|---|
| Stream Input target | NOT_SUPPORTED |
| streaming Stream Output | STREAM_IS_RUNNING |
| flags not exactly MSRP_ACC_LAT_VALID (another flag, or none) | NOT_SUPPORTED, nothing applied |
| latency bit 31 set | BAD_ARGUMENTS, nothing applied |
| foreign lock / no such descriptor | ENTITY_LOCKED / NO_SUCH_DESCRIPTOR |
| otherwise | SUCCESS, the latency becomes the presentation-time offset |

The response is always the 2021 form, cdl 96:

- a 2021 command keeps its byte-exact echo, as today;
- a 2013 command gets its own @24..@69 echoed, then zeros from @70 to @107. Those are the fields
  it does not carry: `ip_flags`, both ports, both addresses. Its reserved word at @70 is not
  carried into `ip_flags`.

Any other length below cdl 96 is still a truncated command, exactly as today:
BAD_ARGUMENTS at cdl 96, `{descriptor_type, descriptor_index}` over a zero body, nothing applied.
A 2013 body is recognised only at exactly cdl 60 with all 48 bytes in the RX slot.

## How (`hdl/aecp/KL_aecp_engine.sv`)

- `si13_w`: the command is a SET_STREAM_INFO of exactly cdl 60, walked whole.
- The short-command route to E_SIBAD is skipped for it. Every later route is shared with the
  2021 body.
- At A_RUN an echoed answer to it is lengthened to 84 bytes (`SI21_PLD_C`).
- `frame_byte` zeroes its echo past @69 (`si13_pad_w`).
- No microprogram changes. The generated ROM is byte-identical
  (sha256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`); only comments in
  `gen_ucode.py` change.
- No register-map, top-level port or parameter change. The four new names are module-internal
  localparams.

## Command model and records

- `aecp_commands.json`: SET_STREAM_INFO declares `floor: 60`, the same field ACQUIRE_ENTITY and
  REGISTER_UNSOLICITED_NOTIFICATION use. F06.14 (regenerated) names the 2013 body in Scope and
  the 2021-form answer in Resp. size.
- The field registry text and its two generated copies name SET_STREAM_INFO among the
  floor-declaring commands.
- `tb/aecp_cmds` sweeps the SET_STREAM_INFO flag templates at cdl 60 as well as 96.
  `decode.json` is re-recorded:
  - SINFO, SIRUN and BADARG now have floor 60, at cdls "60, 96";
  - SIBAD is "12-59, 61-95";
  - NSUPPE answers cdl 96 to the 2013 body and echoes the rest;
  - READ_DESCRIPTOR's swept lengths gain 60, because the new template length reaches every opcode.
- 06 §6.3, 06 §8.1 and 09 §8.1/§8.11 record the change.

## Tests (`tb/pp_top`, section W)

The old W24g row pinned the 2013 refusal. It is replaced by:

- W24g / W24g1: a 2013 body is SUCCESS, byte-exact against an independent 2021-form expectation,
  and the presentation-offset row publishes its latency.
- W24g2: a second 2013 body sets the offset back.
- W24i, W24j, W24k, W24l: Stream Input, extra flag, bit-31 latency and missing descriptor in the
  2013 form. Each is byte-exact in the 2021 form.
- W24l2: none of those refused 2013 latencies was applied.
- W24m / W24m1 / W24m2: a 72-byte body (cdl 84), which is neither form, is still refused
  BAD_ARGUMENTS at cdl 96 with the zero-body stub, and writes nothing.
- W25b3: a 2013 body on a really streaming output is STREAM_IS_RUNNING, byte-exact in the 2021
  form, and writes nothing.

The 2013 stimulus puts a non-zero pattern in every field it carries, and A5A5 in the reserved
word at @70.

These rows live in `w24g_the_2013_body_and_a_body_of_neither_length()`, called from W24 between W24f and
W24h. A separate function keeps W24 under the reference platform's 100-line C++ function rule. The
ENTITY_LOCKED route is not graded separately in the 2013 form: it shares E_SINFO's echo with the
locate miss that W24l grades.

Every new check fails under at least one planted mutant (default build, 9,985 checks; recorded
as M38-M44 in `tb/pp_top/README.md`):

| Mutant | Failing checks |
|---|---|
| 2013 body refused again | W24g, W24g1, W24g2, W24i-W24l, W25b3 |
| answer keeps the command's length | W24g, W24g2, W24i-W24l, W25b3 |
| bytes past @69 echo the slot | W24g, W24i-W24l, W25b3 |
| reserved word echoed into ip_flags | W24g, W24i-W24l, W25b3 |
| any body of 48 bytes or more taken as 2013 | W24m, W24m1, W24m2 (+ W24h2, W25b2, W25b3 collateral) |
| 2013 latency never captured | W24g1, W24g2, W24k, W24l2 (+ collateral) |
| flag gate forced open | W24j, W24l2 (+ W24d-W24f and collateral) |

The unpatched control passes 9,985 of 9,985. Under three of the arms, `tb/aecp_cmds` also fails,
on the SET_STREAM_INFO decode lines of the recorded sweep.

## Gates (base `22c139a4` / head `29f58ad3`, pinned Verilator 5.050, sv2v 0.0.12)

Every record is rc 0 at base and head, never piped. The base and head records are identical except where
noted.

| Gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | 1,029,951 checks, 0 failing | 1,029,960 checks, 0 failing. Only `pp_top` moves, 10,470 → 10,479 (the 9 new checks) |
| `scripts/lint_hdl.sh` | rc 0 | rc 0, identical |
| `make check` | rc 0 | rc 0, identical |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0, identical |
| `syn/yosys/run.sh` (sv2v 0.0.12, Yosys 0.66) | rc 0, 42 tops + Xilinx engine | rc 0. Identical but for `all.v` line numbers, shifted by the added engine lines |

Every campaign that builds a changed file was run at both revisions: tb/aecp_cmds mutants; tb/pp_top
aecp, aecp-dispatch, ctr, gsi, name-wr, acmp, notify and d3; tb/adp_engine; tb/maap; tb/elab_guards;
tb/name_state. All are rc 0 at both, with identical verdicts (d3: 110 of 110 arms killed). The SRP and
ACMP-talker campaigns build none of the changed files.

## Reference platform (scratch parent at dev `7d79ffb2`, gitlink staged at base and at head)

Twenty-one consumer gates were run. Eighteen are rc 0 at base and head with identical results,
check_cpp_idiom and the BDD conformance suite included.

- `measure_test_evidence.py --check` and `check_submodule_docs.py` fail identically at base and head.
  Both pass with the gitlink at dev's own pin. They report the gap between that pin and processor main:
  three test readers added before this base are not yet classified, and the documented pin differs.
  The pin adoption closes both.
- `tb/verilator/milan_dp` fails at head on exactly the two section #67 rows that pin the old refusal
  ("the 2013-length SET_STREAM_INFO refuses at cdl 96" and the offset row after it). With those two
  rows changed to expect the new answer (a parent-side patch, validated in the scratch parent only), the
  suite passes at head with the same per-leg tallies as base. The adoption must carry that change.

## Acceptance

- [x] The 2013 48-byte body and the 2021 84-byte body are accepted with the same field semantics, the
  same MSRP_ACC_LAT_VALID-only rule, the same refusal while streaming, and BAD_ARGUMENTS for a bad value.
- [x] The response always uses the 2021 form.
- [x] Suite cases cover each length, including a short body that is neither form and is still refused
  (W24m).
- [x] The processor's suites pass.
- [ ] The parent's consumer gates pass. This is met only once the pin adoption updates the parent's
  milan_dp #67 rows, which pin the old refusal, and records the pin. That is why this PR says
  "Refs", not "Closes".
