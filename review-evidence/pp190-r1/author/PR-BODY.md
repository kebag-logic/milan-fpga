[A654] Take the engine-driven DECLARE_TALKER's TSpec MaxFrameSize per source

Refs #190 (part 1 of the ruling in issue comment 6256563927; see "Acceptance" for why this does not close it).

Branch `190-per-source-tspec`, one commit on main `5addf297`:

- `90321bff`: take the engine-driven DECLARE_TALKER's TSpec MaxFrameSize per source.

## What changes

`cfg_tspec_max_frame_i` was one 16-bit value, and every source's engine-driven DECLARE_TALKER
captured it. A device whose Stream Outputs carry different formats therefore declared one
MaxFrameSize for all of them. Issue #190 saw this on the bench: the CRF stream declared the 8-channel
AAF value 217 instead of 29.

IEEE 802.1Q-2018 35.2.2.8.4 a) makes MaxFrameSize the largest frame the talker produces for the
stream. Milan v1.2 4.3.3.2 Table 4.4 sets it by format: 24·N + 25 for an N-channel AAF PCM32 48 kHz
stream, and 28 + 1 = 29 for CRF at one timestamp per PDU.

The port is now per source, as the ruling approved:

- `hdl/top/protocol_processor_top.sv:300-303`: `input wire [N_STREAM_OUT_P*16-1:0] cfg_tspec_max_frame_i`,
  flat `[16*s +: 16]`, the same packing as `cfg_stream_id_i`.
- `hdl/top/protocol_processor_top.sv:2703`: the talker stage (`st_tk_r`) captures
  `cfg_tspec_max_frame_i[32'(tkr_gate_src_w) * 16 +: 16]`, the slot of the source whose gate opened or
  closed. This is the same index the stage already puts in the request.

Nothing else changes: no parameter, no other port, no register map. The service face already carries
MaxFrameSize per request (`svc_max_frame_i`), and the SRP core already stores the TSpec per source.
An integration that drives the same value on every slot, `{N_STREAM_OUT_P{value}}`, behaves exactly
as before.

This is a breaking port change for the integrator: the port is now `N_STREAM_OUT_P` times wider.
The parent's adoption drives every slot with today's value, then drives the CRF slot with 29. That
is part 2 of the ruling, and it is not in this PR.

## Tests (`tb/pp_top`, new section TS)

The main model drives 1024 on every slot, so no existing check moves. Section TS runs a fresh model
of its own. Its eight slots are eight different Table 4.4 values: source 0 the 8-channel AAF value
217, source 1 the CRF value 29, and sources 2 to 7 the AAF value at 2 to 7 channels (73 to 193).

- **TS0**: AECP is released, and a PROBE_TX for every source is answered SUCCESS, so every DA gate is
  open.
- **TS1**, one check per source: the first Talker attribute on the MSRP wire for source *s* declares
  slot *s*. The value is range-matched the way a bridge reads it: FirstValue + k steps the Unique ID
  and the destination_address and carries the TSpec unchanged (802.1Q-2018 35.2.2.8). Sources 0 to 6
  are admitted (74.368 of 75 Mb/s); source 7 is refused and declares Talker Failed, which carries the
  TSpec at the same offset.

`make -C tb/pp_top tspec` runs the section alone (9 checks); the full run runs it last.

Every new check fails under a planted arm. The arms are in `tb/pp_top/acmp_mutants.py`, run with
`--tspec-only`:

| Arm | Defect planted | Named check | Failing checks |
|---|---|---|---|
| `tspec_slot_zero` | every source captures slot 0, the single value the port carried before | `TS1: source 1 declares its own slot's MaxFrameSize` (the CRF slot) | 7 of 9: TS1 for sources 1 to 7, each declaring 217 |
| `tspec_slot_last` | every source captures the last slot | `TS1: source 0 declares its own slot's MaxFrameSize` | 7 of 9: TS1 for sources 0 to 6, each declaring 193 |
| `tspec_no_allocator` | the talker's MAAP request face is tied not-ready | `TS0: AECP is released and every source's PROBE_TX_RESPONSE is SUCCESS` | 9 of 9 |

## Documentation

- `docs/architecture/02_interfaces.md` §4.1: the tspec is per source, with the port and its packing.
  A new anchor, `sec-02-srp`, gives the section a stable link target.
- `docs/guides/integrator.md` §6: the port's width in the SRP row; it joins the per-source vectors,
  and a paragraph says what to drive in each slot.
- `docs/architecture/10_srp_engine.md` §3: each source declares its own slot.
- `docs/architecture/09_verification.md` §8.12 and `tb/pp_top/README.md` section TS: the checks and
  the arms.

## Gates

Every gate and campaign ran at base `5addf297` and at this head `90321bff`, with the pinned
Verilator 5.050 and sv2v 0.0.12, and Yosys 0.33 for the processor's own gates. All are rc 0 at
both. Records are identical after normalizing paths, times and parallel completion order, except
where the table says otherwise.

| Processor gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | 1,030,013 checks, 0 failing | 1,030,022 checks, 0 failing: only `pp_top` moves, 10,519 → 10,528 (TS0 and the eight TS1 checks) |
| `scripts/lint_hdl.sh` | 41 LINT OK | identical |
| `make check` | OK | identical except the link count, 1,196 → 1,200 (the four links this PR adds) |
| `scripts/gen_matrix.py --check` | 94 rows, 0 untested | identical |
| `syn/yosys/run.sh` | every top and the Xilinx engine OK | identical |

The generated ROMs are byte-identical at base and head (`ucode.hex` a3b62cab…bcb3, `ltn_rom.hex`
23cc67ee…e956); no generator input changed.

Campaigns that build a changed file (the top or `tb/pp_top`), rc 0 with the same verdicts at both:

- `tb/pp_top/acmp_mutants.py`: 51 of 51 killed at base; 54 of 54 at head. The three new arms and the
  `--tspec-only` golden are the only difference.
- `make -C tb/pp_top`: `aecp-mutants` (61 killed), `aecp-dispatch-mutants` (54) and `ctr-mutants` (17),
  each with its sources restored.
- `tb/pp_top/gsi_mutants.py` (20 detected), `name_wr_mutant.py` (killed), `notify_mutants.py`
  (109 of 109) and `d3_mutants.py` (110 of 110).
- `make -C tb/adp_engine mutants` (57 killed), `make -C tb/maap mutants` (29) and
  `make -C tb/name_state mutants` (16).
- `make -C tb/elab_guards mutants`: 160 of 160 killed. `tb/elab_guards/guards.py --frontend yosys`:
  93 of 93. Only the top's guard line numbers move, by the three port-comment lines.

Not run, because they build no changed file: the `tb/srp_top`, `tb/srp_admission`, `tb/aecp_cmds` and
`tb/acmp_talker` retry campaigns, and `tb/nvm_port` figures.

Parent consumer gates ran on a scratch parent at dev `e9cbb676`, with the protocol-processor gitlink
staged at each revision. Its working tree carries the two parent patches earlier processor lanes
needed at this processor main: the evidence classification of three processor-main readers, and the
two milan_dp #67 rows. At the head it also carries one more patch. That patch drives the new port
with the old value on every slot (`.cfg_tspec_max_frame_i({N_STREAM_OUT_P{cfg_tspec_max_frame_i}})`
in `hdl/milan/KL_pp_shadow.sv`), so the parent's behaviour does not change.

- 23 of the 24 gates are rc 0 at both base and head: the idiom, naming, evidence, docs, hygiene,
  source-list, SoC-source, TODO-ownership and port-contract checks, `pp_srcs`, the bare-metal
  check, RTL lint, the BDD suite (406 scenarios), the xvlog gate (0 findings), the builder gates
  (all pass but gate 11, not run at either, which needs a build tree not on this host),
  pp_shadow (2,184 checks), nvm_cosim lint and quick, milan_dp_render and milan_dp (10,465 `[ok]`,
  1,127 `[PASS]`, 0 failures). Their records are identical apart from timings, the pin the
  xvlog gate names, and `check_py_idiom.py`'s line total (+20, `acmp_mutants.py`).
- `check_submodule_docs.py` fails identically at both (`documented pin differs from Git`). It fails at
  any pin the parent's docs do not record, so the pin adoption owns it.
- Control: at the head without the every-slot patch, `lint_rtl.py --check` fails on
  `WIDTHEXPAND` at `KL_pp_shadow.sv:1161`: 128 bits expected, 16 driven. So the adoption has to drive
  the per-source port, even if only with today's value on every slot.

## Acceptance

Part 1 of the ruling:

- [x] The port is per source, `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]`, indexed like
  `cfg_stream_id_i`.
- [x] Every engine-driven DECLARE_TALKER, gate open and gate close alike, uses its own source's
  slot. The service face was already per request.
- [x] Suite cases cover sources with different values: all eight, with source 0 the AAF 217 and
  source 1 the CRF 29. Each has a planted arm that fails it: `tspec_slot_zero` fails source 1's
  check, and `tspec_slot_last` fails source 0's.
- [x] The processor gates pass.
- [x] The parent consumer gates pass on the scratch parent that drives every slot with the old value.
  The one exception, `check_submodule_docs`, fails identically at base and is the pin record the
  adoption updates.

Issue #190 itself is not closed by this PR. Its first item, the CRF stream declaring 29, needs part 2
in the parent: drive the CRF slot with 20 + 8 × timestamps_per_pdu + 1, add a suite case against the
PDU length, and fix the stale comment at `KL_crf_tx.sv:206-211`. That rides the next pin adoption.
