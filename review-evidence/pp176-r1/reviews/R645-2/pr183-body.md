[A629] SET_STREAM_INFO: accept exactly the IEEE 1722.1-2013 48-byte body and the 2021 84-byte body, answer in the 2021 form

Refs #176 (see "Acceptance" below for why this does not close it by itself).

Branch `176-ssi-2013-body`, three commits on main `f0b1b9d8`:

- `29f58ad3`: accept the 2013 body (round 1);
- `e59804d8`: merge of processor main `f0b1b9d8` (PR #180);
- `bee33ff2`: refuse every other length, longer ones included, and pin the 2021 ip-block echo (round 2).

## What changes

SET_STREAM_INFO on a Stream Output accepts exactly two bodies:

- the IEEE 1722.1-2021 body (Figure 7-40, 84 payload bytes, cdl 96), as before;
- the IEEE 1722.1-2013 body (Figure 7.46, 48 payload bytes, cdl 60), new.

Every other length is refused, shorter or longer. Neither IEEE 1722.1-2021 7.4.15.1 nor Milan v1.2
5.4.2.9 defines a longer body. The refusal is the one a short body already got: BAD_ARGUMENTS at
cdl 96, `{descriptor_type, descriptor_index}` over a zero body, and no offset write. Before this PR a
body longer than 84 bytes was accepted and echoed at its own length.

The 2013 body is the 2021 body's first 48 bytes. The only difference: 2021 turns the reserved word at
@70 into `ip_flags` and appends the ports and the two IP addresses. So `flags` (@28) and
`msrp_accumulated_latency` (@48) sit at the same offsets in both.

Both accepted bodies take the same routes, in the same order:

| Case | Answer |
|---|---|
| Stream Input target | NOT_SUPPORTED |
| streaming Stream Output | STREAM_IS_RUNNING |
| flags not exactly MSRP_ACC_LAT_VALID (another flag, or none) | NOT_SUPPORTED, nothing applied |
| latency bit 31 set | BAD_ARGUMENTS, nothing applied |
| foreign lock / no such descriptor | ENTITY_LOCKED / NO_SUCH_DESCRIPTOR |
| otherwise | SUCCESS, the latency becomes the presentation-time offset |

Every response is the 2021 form, cdl 96:

- a 2021 command keeps its byte-exact echo, ip block included;
- a 2013 command gets its own @24..@69 echoed, then zeros from @70 to @107. Those are the fields it
  does not carry: `ip_flags`, both ports, both addresses. Its reserved word at @70 is not carried into
  `ip_flags`;
- any other length gets the zero-body BAD_ARGUMENTS stub above.

A body is recognised only at exactly its cdl with all of its bytes in the RX slot.

Observed at the merged base and at this head, one valid MSRP_ACC_LAT_VALID body per length on Stream
Output 0, latency 600000 + cdl, in this order:

| cdl | Merged base `e59804d8`: status / response cdl / offset row | Head `bee33ff2` |
|---|---|---|
| 59 | BAD_ARGUMENTS / 96 / unset | BAD_ARGUMENTS / 96 / unset |
| 60 | SUCCESS / 96 / 600060 | SUCCESS / 96 / 600060 |
| 61 | BAD_ARGUMENTS / 96 / 600060 | BAD_ARGUMENTS / 96 / 600060 |
| 95 | BAD_ARGUMENTS / 96 / 600060 | BAD_ARGUMENTS / 96 / 600060 |
| 96 | SUCCESS / 96 / 600096 | SUCCESS / 96 / 600096 |
| 97 | SUCCESS / 97 / 600097 | BAD_ARGUMENTS / 96 / 600096 |
| 100 | SUCCESS / 100 / 600100 | BAD_ARGUMENTS / 96 / 600096 |
| 140 | SUCCESS / 140 / 600140 | BAD_ARGUMENTS / 96 / 600096 |

## How (`hdl/aecp/KL_aecp_engine.sv`)

- `si13_w`: the command is a SET_STREAM_INFO of exactly cdl 60, walked whole (48 bytes).
- `si21_w`: the command is a SET_STREAM_INFO of exactly cdl 96, walked whole (84 bytes).
- The dispatch arm sends every SET_STREAM_INFO that is neither to E_SIBAD. Every later route is shared.
- At A_RUN an echoed answer to a 2013 command is lengthened to 84 bytes (`SI21_PLD_C`).
- `frame_byte` zeroes a 2013 command's echo past @69 (`si13_pad_w`).
- No microprogram changes. The generated ROM is byte-identical to main's
  (sha256 `a3b62cabe2cb091383f999bf58b830ff2d3ab63cd8699b95d2529dbf4d02bcb3`); only comments in
  `gen_ucode.py` change.
- No register-map, top-level port or parameter change. The five new names are module-internal
  localparams (`SI21_CDL_C`, `SI21_PLD_C`, `SI13_CDL_C`, `SI13_PLD_C`, `SI13_ECHO_C`).

## Command model and records

- `aecp_commands.json`: SET_STREAM_INFO declares `floor: 60`, the same field ACQUIRE_ENTITY and
  REGISTER_UNSOLICITED_NOTIFICATION use. F06.14 (regenerated) says it accepts exactly the 2021 body
  (cdl 96) and the 2013 body (cdl 60), and gives the 2021-form answer in Resp. size.
- The field registry text and its two generated copies name SET_STREAM_INFO among the
  floor-declaring commands.
- `tb/aecp_cmds` sweeps the valid MSRP_ACC_LAT_VALID templates (with and without bit 31 of the
  latency) at cdl 60, 96, 97 and 100. `decode.json` is re-recorded. For AEM 0x000E:
  - SINFO, SIRUN, BADARG and NSUPPE only at cdls "60, 96", each answering cdl 96;
  - SIBAD at "12-59, 61-95, 97-100", answering cdl 96.
  - READ_DESCRIPTOR's swept lengths gain 60 and 97, because the template lengths reach every opcode.
- 06 F06.14, §6.3 and §8.1, and 09 §8.1 and §8.11, record the contract.

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
- W24n / W24n1 and W24o / W24o1 (new): a valid MSRP_ACC_LAT_VALID body one byte longer (cdl 97) and
  44 bytes longer (cdl 140) than the 2021 body, with a non-zero tail, is refused BAD_ARGUMENTS at
  cdl 96, `{type, index}` over a zero body, byte-exact, and its latency is not applied.
- W24a3 (new): a 2021 body whose ip block (@70..@107) is non-zero is echoed byte-exact.
- W25b3: a 2013 body on a really streaming output is STREAM_IS_RUNNING, byte-exact in the 2021
  form, and writes nothing.

The 2013 stimulus puts a non-zero pattern in every field it carries, and A5A5 in the reserved
word at @70.

The 2013 rows live in `w24g_the_2013_body_and_a_body_of_neither_length()` and the longer bodies in
`w24n_bodies_longer_than_the_2021_body()`, both called from W24 between W24f and W24h. Separate
functions keep W24 under the reference platform's 100-line C++ function rule. The ENTITY_LOCKED
route is not graded separately in the 2013 form: it shares E_SINFO's echo with the locate miss that
W24l grades.

Every new check fails under at least one planted mutant (default build, 10,004 checks; recorded as
M38-M46 in `tb/pp_top/README.md`):

| Mutant | Failing checks |
|---|---|
| 2013 body refused again | W24g, W24g1, W24g2, W24i-W24l, W25b3 |
| answer keeps the command's length | W24g, W24g2, W24i-W24l, W25b3 |
| bytes past @69 echo the slot | W24g, W24i-W24l, W25b3 |
| reserved word echoed into ip_flags | W24g, W24i-W24l, W25b3 |
| any body of 48 bytes or more taken as 2013 | W24m, W24m1, W24m2, W24n, W24n1, W24o, W24o1, W24a3 (+ W24h2, W25b2, W25b3 collateral) |
| 2013 latency never captured | W24g1, W24g2, W24k, W24l2 (+ collateral) |
| flag gate forced open | W24j, W24l2 (+ W24d-W24f and collateral) |
| upper bound reopened (`si21_w` compares `>=`) | W24n, W24n1, W24o, W24o1 (+ W24h2, W25b2, W25b3 collateral) |
| 2013 zero tail widened to every SET_STREAM_INFO | W24a3 |

The unpatched control passes 10,004 of 10,004 and `tb/aecp_cmds` 176 of 176. Under the
upper-bound arm, `tb/aecp_cmds` also fails on AEM 0x000E's recorded SINFO, NSUPPE, BADARG and SIBAD
lengths.

## Gates

Every gate and campaign ran at the merged base `e59804d8` and at this head `bee33ff2`, with the
pinned Verilator 5.050 and sv2v 0.0.12. All are rc 0 at both. Records are identical after
normalizing paths, times, digests, the source line numbers the added lines shift, and parallel
completion order.

| Processor gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | 1,029,982 checks, 0 failing | 1,029,987 checks, 0 failing: only `pp_top` moves, 10,501 → 10,506 (W24a3, W24n, W24n1, W24o, W24o1) |
| `scripts/lint_hdl.sh` | 41 LINT OK | identical |
| `make check` | OK (231 of 231 planted command-model defects caught) | identical |
| `scripts/gen_matrix.py --check` | 94 rows, 0 untested | identical |
| `syn/yosys/run.sh` | 42 tops + the Xilinx engine OK, under Yosys 0.66 and under 0.33 | identical |

Campaigns that build a changed file, all rc 0 with identical verdicts at both:

- `make -C tb/aecp_cmds mutants`: 16 of 16 controls detected.
- `make -C tb/pp_top`:
  - `aecp-dispatch-mutants`, `aecp-mutants` and `ctr-mutants`: all killed, and each source restored.
  - `gsi_mutants.py`: 20 detected.
  - `name_wr_mutant.py`: killed.
  - `acmp_mutants.py`: 51 of 51 killed.
  - `notify_mutants.py`: 98 of 98 killed.
  - `d3_mutants.py`: 110 of 110 killed, run in four chunks.
- `make -C tb/adp_engine mutants`, `make -C tb/maap mutants` and `make -C tb/name_state mutants`: all
  killed.
- `make -C tb/elab_guards mutants`: 160 of 160 killed.

Parent consumer gates: the parent at dev `e9cbb676`, the protocol-processor gitlink staged at each
revision, with two parent patches in the working tree. One is the evidence classification of
three processor-main readers. The other is the two-row milan_dp #67 change below.

- 22 of the 23 gates are rc 0 at both base and head, with identical check lines: the idiom, naming,
  evidence, docs, hygiene, source-list and port-contract checks, the builder gates, RTL lint, the BDD
  suite, the xvlog gate, pp_shadow (2,184 checks), nvm_cosim lint and quick, milan_dp_render and
  milan_dp.
- `check_submodule_docs.py` fails identically at both (`documented pin differs from Git`). It fails
  at any pin the parent's docs do not record, and passes at dev's own pin.

Which parent rows each patch is needed for, each measured by running without that patch:

| Patch | Rows that fail without it, at base and at head |
|---|---|
| evidence classification | `measure_test_evidence.py --check`: `FAIL: 3 unexplained DUT-source reader(s)` (`tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py`, `tb/elab_guards/mutants.py`, all on processor main before this branch). At dev's own pin it passes without the patch |
| milan_dp #67 | `make -C tb/verilator/milan_dp`: `[FAIL] #67 the 2013-length SET_STREAM_INFO refuses at cdl 96 got=0x0 exp=0x1` and `[FAIL] #67 no refusal moved the stored offset got=0x0 exp=0xb71b0`, then the pool stops the later legs. These rows pin the 2013 refusal that round 1 removed, and the parent's 2013 probe carries latency 0, which is now applied. The patch expects SUCCESS at cdl 96 and sends the stored 750000, so the next row is unchanged. With it, both rows pass in every leg and milan_dp is rc 0 |

The idiom gates that read the patched files (`check_cpp_idiom.py`, `check_py_idiom.py`) pass
without them as well. Round 2 changes neither row's verdict, because the #67 rows send only
a 2013 body and a 2021 body, and both are answered as in round 1.

## Acceptance

- [x] The 2013 48-byte body and the 2021 84-byte body are accepted with the same field semantics, the
  same MSRP_ACC_LAT_VALID-only rule, the same refusal while streaming, and BAD_ARGUMENTS for a bad value.
- [x] Every other length, shorter or longer, is refused BAD_ARGUMENTS at cdl 96 with the zero-body
  stub and no offset write (W24m, W24n, W24o; the `tb/aecp_cmds` record from cdl 12 to 100).
- [x] The response always uses the 2021 form, cdl 96, whatever the command's length.
- [x] Suite cases cover each length, including a shorter and two longer bodies that are neither form.
- [x] The processor's suites pass.
- [ ] The parent's consumer gates pass. Not by this PR alone, so it says "Refs #176". At the new pin
  the parent needs the two-row milan_dp #67 change above, and its pin documentation must record the
  pin. With that change and the evidence classification applied, every other consumer gate is rc 0
  at this head. These parent changes belong to the pin adoption.

## Round 2

Round 1's head `29f58ad3` accepted any SET_STREAM_INFO of 84 bytes or more as the 2021 body, and
echoed it at its own length. Round 2 merges processor main `f0b1b9d8` (`e59804d8`; the textual merge
was clean) and adds `bee33ff2`:

- R645-1-F1 (the ruling's contract): exactly cdl 60 and 96 are accepted (`si21_w` beside `si13_w`).
  Every other length is refused with the short-body stub. Added: W24n/W24n1 (cdl 97) and W24o/W24o1
  (cdl 140), from a valid MSRP_ACC_LAT_VALID template with a non-zero tail. Added: the `tb/aecp_cmds`
  sweep at cdl 97 and 100, the re-recorded `decode.json`, F06.14, §6.3 and §8.1, and the probe table
  above. Added: mutant M45 (`si21_w` compares `>=`), which fails W24n, W24n1, W24o and W24o1 by name.
- R644-1-F1: W24a3 sends a 2021 body with a non-zero ip block and grades its echo byte-exact. Mutant
  M46 (`si13_pad_w` widened to every SET_STREAM_INFO) fails it.
- R644-1-R1: 09 §8.1 says "W24h-W24m".
- R645-1-F2: the comment anchors cite `issue #176, REQ-AEM-009` and no test labels. Function names,
  assertion strings and the findings tables are unchanged.

No register-map, top-level port or parameter change: the new name `SI21_CDL_C` is a module-internal
localparam.
