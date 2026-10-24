# [A668] processor #200 — HANDOFF

Status: **REVIEW READY** at head `33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33`. Every gate is rc 0. No STOP condition was hit.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `200-avb-info-not-supported` (local only; not pushed, no PR opened)
- Base: processor main `93fb0b2d736b36588ea7321e25fba2f8819ea41f`
- Head: `33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33`, one commit on base, subject
  "Answer GET_AVB_INFO on a non-AVB_INTERFACE descriptor NOT_SUPPORTED with the command echoed (issue #200)"
- Checked before the commit: `git remote get-url origin` was the processor repository and HEAD was 93fb0b2d.
- Public trail: TAKEN is issue #200 comment 6379949872; REVIEW READY is comment 6385280946. No other post, no edit of any
  comment.
- The PR draft is `PR-BODY.md`. Receipts are under `receipts/`, indexed in `receipts/INDEX.md` (generated from the
  files present). Records over 190 KB are in `EXTERNAL-RECORDS.csv`.

## 1. Behaviour

GET_AVB_INFO (AEM 0x0027) at the engine's A_PLD-exit re-dispatch, in order:

1. cdl < 16 answers `BAD_ARGUMENTS` (echo). Unchanged.
2. descriptor_type ≠ AVB_INTERFACE answers **`NOT_SUPPORTED` (11), with the command echoed at its own length**,
   whether or not that descriptor exists. Since #182 this answered `NOT_IMPLEMENTED` (1).
3. An absent AVB_INTERFACE index answers `NO_SUCH_DESCRIPTOR` (E_GAVB's locate miss). Unchanged.
4. Otherwise SUCCESS. Unchanged.

The only synthesised change is one constant, `upc_r <= UPC_NOTIMPL_C` (560) → `UPC_NSUPPE_C` (864), in that arm.
`echo_r` stays 1. E_NSUPPE is the existing command-sized NOT_SUPPORTED echo (SET_STATUS 11, BUILD_HDR, SEND_RESP).
GET_STREAM_INFO's wrong-type arm, ACQUIRE_ENTITY and LOCK_ENTITY on a non-ENTITY target already use it.

## 2. Changes (head file:line, clause)

| File:line (head) | Change | Clause |
|---|---|---|
| `hdl/aecp/KL_aecp_engine.sv:3457` | the wrong-type arm moves from `UPC_NOTIMPL_C` to `UPC_NSUPPE_C`; `echo_r <= 1'b1` kept (:3458) | Table 7-141 status 11 |
| `hdl/aecp/KL_aecp_engine.sv:3443-3453` | arm comment: behaviour and reason, issue and clause IDs only | Milan 5.4.2.23, 5.4.2.2, 5.4.2.9; IEEE 7.4.40.1; Table 7-141 status 1 vs 11 |
| `hdl/aecp/KL_aecp_engine.sv:1300-1307` | the `UPC_NOTIMPL_C` bound is back to TWO assignment sites (the pop default :1337 and the audio-map arm :3354), its pre-#182 text, plus one sentence: GET_AVB_INFO keeps its real M9 body | issues #76, #83 |
| `hdl/aecp/ucode/aecp_commands.json:313,317` | status `SUCCESS, NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS, NOT_SUPPORTED`; entries `GAVB, NSUPPE, BADARG` (both are the pre-#182 text) | command model (#73) |
| `docs/architecture/06_aecp_engine.md:276` | F06.14 row, regenerated with `python3 -B scripts/check_aecp_commands.py --write`; byte-identical to its pre-#182 row | — |
| `docs/architecture/06_aecp_engine.md:997-1013` | §6.10 paragraph rewritten with the issue's clauses and the length → type → existence order | Table 7-141; Milan 5.4.2.23; IEEE 9.3.5.3.3 scope; Milan 5.4.2.2, 5.4.2.9; IEEE 7.4.40.1 |
| `docs/architecture/06_aecp_engine.md:1374` | §8.1 realization row: `NOT_SUPPORTED` with the command echoed (§6.10, issue #200) | — |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:598` | §8 entry for GET_AVB_INFO: the ruling, all four clause groups of the issue, and the unchanged AVB_INTERFACE answers (SUCCESS, NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS) | as in the issue |
| `docs/architecture/09_verification.md:579` | standing-control text: "back on NOT_IMPLEMENTED (issue #200)" | — |
| `tb/aecp_cmds/decode.json:25,159` | re-recorded with `make -C tb/aecp_cmds record`: the engine sha, and 0x0027's wrong-type program `NOTIMPL {1: echo}` → `NSUPPE {11: echo}`, cdl 16-100, floor 16. Nothing else moved | — |
| `tb/aecp_cmds/mutants.py:10,73-79`; `tb/aecp_cmds/README.md:104` | control `gavb-other-type-not-supported` → `gavb-other-type-not-implemented` (plants #182's status) | — |
| `tb/pp_top/sim_main.cpp:5739-5783` | V5's 13 rows expect `AECP_NOT_SUPPORTED` byte-exact echoes; function renamed `v5_..._is_not_supported` (callers :5617, :5635) | Table 7-141 status 11 |
| `tb/pp_top/sim_main.cpp:3429-3432` | M9 comment: the wrong-type answer now differs from M9's in its status byte, and the real AVB_INTERFACE 0 body stays so an unguarded arm runs E_GAVB | — |
| `tb/pp_top/aecp_dispatch_mutants.py:44-66` | arms renamed and retargeted to the NOT_SUPPORTED words; new arm `gavb-other-type-full-body` | — |
| `tb/pp_top/aecp_dispatch_mutations/` | 7 `gavb-*` patches regenerated against the new source (2 renamed), 1 new; `gavb-locate-miss-ignored` and `m9-guard-get-avb-info` unchanged. Every patch in the three mutation directories passes `git apply --check` at head | — |
| `tb/pp_top/README.md:676-679,793-798,1357-1359,1376-1385,1478-1493` | V5 text, the counting-provenance sentence, the arm table (re-measured counts), the arm prose | — |

**Compliance-review numbering.** The issue and the assignment say "section 8, item 12". In
`docs/00_MILAN_COMPLIANCE_REVIEW.md` §8, row 12 is the SET_CONFIGURATION notification decision (#178), and the
GET_AVB_INFO entry #182 added is row **14**. I updated row 14 and left row 12 alone. Please confirm this reading.

**Microcode ROM: byte-identical.** `gen_ucode.py` gives `ucode.hex` sha256
`1f78804e448c385d633ed4355b7d84100ec13b12c77305c3bc11986653a80a8e` (26,624 bytes, 2048 words, 92 programs) at base
and head, and `cmp` agrees. The parent's `ooc.sh --record-rom-digests` recorded the same ucode and latency-ROM
digests at pin 33d3010c as the ledger holds for 93fb0b2d (`receipts/rom-identity.txt`).

## 3. New or changed checks, planted mutants, failing words

V5 (13 checks in `tb/pp_top`, in the main run and in `make aecp-dispatch`):
`V5 GET_AVB_INFO on <row>: NOT_SUPPORTED, the command echoed at cdl <16|20>, byte-exact`. The rows are ENTITY,
CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT, JACK_OUTPUT, CLOCK_SOURCE, CLOCK_DOMAIN 0, CLOCK_DOMAIN 5
(absent), 0x0109, 0x8009 and 0xFFFF at cdl 16, and CLOCK_DOMAIN 0 padded to cdl 20. V1, V1b, V3 (NO_SUCH_DESCRIPTOR)
and V4 (BAD_ARGUMENTS) are unchanged and pass.

Dispatch arms (`tb/pp_top/aecp_dispatch_mutants.py`, target `aecp-dispatch`), all KILLED at head. The counts were
measured before the commit (`receipts/pre/gavb-dispatch-arms.out`), and the full head campaign gave the same counts.

| Arm | Planted | Named failing words | Failing checks |
|---|---|---|---|
| `gavb-other-type-not-implemented` | wrong-type arm on `UPC_NOTIMPL_C` (#182's status) | `V5 GET_AVB_INFO on CLOCK_DOMAIN 0: NOT_SUPPORTED` | 13 (every V5 row) |
| `gavb-other-type-header-only` | `echo_r` 0 on the wrong-type arm | `V5 GET_AVB_INFO on CLOCK_DOMAIN 0 padded: NOT_SUPPORTED, the command echoed at cdl 20` | 13 |
| `gavb-other-type-full-body` (new) | wrong-type arm on `UPC_TIZ8NS_C`, the read-side set's fixed-body NOT_SUPPORTED | the same words | 13 |
| `gavb-type-gate-dropped` | type gate `1'b0` | `V5 GET_AVB_INFO on ENTITY 0: NOT_SUPPORTED` | 13 |
| `gavb-type-low-byte` | gate on descriptor_type[7:0] | `V5 GET_AVB_INFO on type 0x0109: NOT_SUPPORTED` | 2 (0x0109, 0x8009) |
| `gavb-interface-not-supported` | gate inverted | `V1: GET_AVB_INFO byte-exact` | 16 (V1, V1b, V3 and the 13 V5 rows) |
| `gavb-locate-miss-ignored` | E_GAVB's miss branch replaced with NOP | `V3: GET_AVB_INFO on a missing interface refuses NO_SUCH_DESCRIPTOR` | 1 |
| `gavb-padded-refused` | `cdl != 16` | `V1b: GET_AVB_INFO padded to cdl 20 answers V1's SUCCESS, byte-exact` | 2 (V1b, V5 padded) |
| `gavb-floor-14` | floor 14 | `V4: short GET_AVB_INFO answers BAD_ARGUMENTS` | 1 |
| `m9-guard-get-avb-info` | `gavb_w` without `aem_w` | `M9: mt=4 word 0027` | 14 |

Standing control (`tb/aecp_cmds/mutants.py`): `gavb-other-type-not-implemented` →
`FAIL:  decode: GET_AVB_INFO: the table's entries name NSUPPE, which the engine never dispatches AEM 0x0027 to (the fresh sweep)`.

## 4. Base and head records (processor)

Base runs used a clean clone at 93fb0b2d, and head runs a clean clone at 33d3010c (both scratch, outside the lane).
The pre-commit make check and dispatch arms ran in the lane tree, whose ignored build products were removed
afterwards. Each `.rc` file is the command's own exit status, written by a recording wrapper, never through a pipe.
Normalised base-vs-head diffs are `receipts/cmp/*.cmp.diff`, summarised in `receipts/cmp/SUMMARY.txt`. Local tools:
Verilator 5.052 (CI pins 5.050), Yosys 0.66, sv2v 0.0.13, and wavedrom 2.0.3.post3 in a venv outside the tree.

| Processor gate | Base | Head | Base vs head |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,399 checks, 0 failing | rc 0, 1,030,399 | every suite line identical (pp_top 10,741, aecp_cmds 176) |
| `scripts/check-req-tags.py --suites … --evidence …` | rc 0, 231 evidence lines, 14 suites | rc 0 | evidence identical except −1 line offsets in `pp_top/sim_main.cpp` past V5 |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | only `ids: 663 files` → `664 files` (the new patch file) |
| `syn/yosys/run.sh` | rc 0, 43 OK | rc 0 | verdict lines identical |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0, 93 of 93 | rc 0, 93 of 93 | identical |

| Campaign (builds a changed file) | Base | Head | Base vs head |
|---|---|---|---|
| `tb/aecp_cmds/mutants.py --jobs 1` | rc 0, 17 of 17 detected | rc 0, 17 of 17 | only the GET_AVB_INFO control (renamed, now NSUPPE words) |
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 1` | rc 0, 73 of 73 (4 controls, 69 arms) | rc 0, 74 of 74 (70 arms) | only the GET_AVB_INFO arms: two renamed, one new, V5 words NOT_IMPLEMENTED → NOT_SUPPORTED |
| `tb/pp_top/aecp_mutants.py --jobs 1` | rc 0, 67 of 67 | rc 0, 67 of 67 | identical |
| `tb/pp_top/ctr_mutants.py --jobs 1` | rc 0, 18 of 18 | rc 0, 18 of 18 | identical |
| `tb/pp_top/gsi_mutants.py --jobs 1` | rc 0, 23 detected | rc 0, 23 detected | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | identical |
| `tb/pp_top/acmp_mutants.py --jobs 1` | rc 0, 65 of 65 | rc 0, 65 of 65 | identical |
| `tb/pp_top/notify_mutants.py --jobs 1` | not run (see below) | rc 0, 137 of 137 | — |
| `tb/pp_top/d3_mutants.py --jobs 2` | not run (see below) | rc 0, 110 of 110 | — |
| `tb/elab_guards/mutants.py --jobs 1` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical after line normalisation |
| `tb/name_state/mutants.py --jobs 1` | rc 0, 16 KILLED | rc 0, 16 KILLED | identical |

Not run at base: notify and d3. These are comparisons, not gates. At one build per side, d3 alone would have taken
about six hours, so I stopped the base chain to give head d3 two build slots. Both pass at head.

Not run on either side, because they build no changed file: `tb/srp_top`, `tb/maap`, `tb/adp_engine`,
`tb/srp_admission`, `tb/acmp_talker` retry mutants and the `tb/nvm_port` figures. Their suites ran in
`run_suites.sh`.

Void runs, set aside under `receipts/void/` and not used as records:

- The first base aecp_cmds controls hit the foreground time limit and were stopped. They were rerun detached.
- A partial base notify run was stopped as described above.
- A head d3 run at `--jobs 1` was stopped after 10 arms and rerun at `--jobs 2`.

While stopping the first of these, a `pkill -f` pattern also matched its own shell. One orphaned sweep process was
killed by PID and its temporary copy removed. Nothing else was affected.

## 5. Scratch-parent consumer gate

Scratch parent `pp200-parent`: a local clone of milan-fpga dev `a032c6d6e3775f145349d5a495c1e1ad12294936` (a clone
of the trusted dev lane), every submodule initialised. Its push URL is set to an invalid value, and it was never
pushed. Two local commits on branch `scratch-pp200-a668`:

- `c9fe2f84` sets the protocol-processor gitlink to 33d3010c.
- `50e6c0b2` adds the head-pin rows that `syn/yosys/ooc.sh --record-rom-digests` wrote to `syn/yosys/rom_digests.tsv`.
  The digests equal the base pin's.

Its working tree is clean. The base runs used a second clone, `pp200-parent-ctl`, at pristine a032c6d6 with the
processor at 93fb0b2d (`receipts/cons/STATE.txt`). No parent patch was needed for any run below.

| Parent consumer gate | Base (dev, pin 93fb0b2d) | Head (pin 33d3010c, committed) | Base vs head |
|---|---|---|---|
| `make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` | rc 0: 11,630 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]`; tallies 185/185, 185/185, 6/6 | rc 0, same counts | every check line identical (sorted, times normalised; list sha256 f0fbc6b6… at both) |
| `syn/yosys/ooc.sh KL_pp_shadow` (the parent's recipe for the processor) | rc 0: LUT 58,039, LUTRAM 4,236, FF 26,948, RAMB36 15, RAMB18 4, DSP 10, CARRY4 2,394 | rc 0: LUT **58,506**; everything else identical | **+467 LUT (+0.80 %)**, no other resource moved; a rerun gives 58,506 again |
| `ooc.sh protocol_processor_top` (scratch row, `parent-scratch-ooc-pp-top-row.patch`, module defaults) | rc 0: LUT 57,221, LUTRAM 4,076, FF 26,437, RAMB36 16, RAMB18 1, DSP 4, CARRY4 2,369 | rc 0: LUT **57,168**; everything else identical | **−53 LUT (−0.09 %)** |

**Area delta of `protocol_processor_top`: −53 LUT (−0.09 %) out of context at its module defaults, with zero change
in LUTRAM, FF, BRAM, DSP and CARRY4**, so about 0 as expected. Inside the parent's wrapper `KL_pp_shadow`, at the
parent's parameters, the same change maps to +467 LUT (+0.80 %), again with no other resource moving. It is
deterministic. Controls in `pp200-parent-ctl` (scratch commits in its own submodule, never pushed) attribute it:

- Base plus only the constant swap, without the comment edits, gives 58,506, equal to head. The whole delta is the
  one constant.
- Base with the arm pointed at a third existing program, `UPC_BADARG_C` (704), gives 57,986 (−53).

So the LUT count moves by about ±500 with nothing more than which existing program address one mux arm loads. That
is the mapper's sensitivity to the constant, not new logic or state. The summary is `receipts/cons/AREA.txt`.

## 6. Notes for the reviewer

- **Echo length versus the reference controller.** The issue requires NOT_SUPPORTED "echoed at its own length",
  and that is what the head does: cdl 16 for the four-byte command. 06 §6.6 records that the reference controller
  stack accepts a command-length reflection only for NOT_IMPLEMENTED, and sizes every other non-success answer
  against the response form (cdl 32 + 4·N here), so it may report this echo as an incorrect payload size.
  GET_STREAM_INFO's existing wrong-type echo is in the same position. The read-side set answers a wrong target with
  a fixed-body NOT_SUPPORTED instead (E_TIZ8NS and its siblings). I did not choose that form, because the issue
  asks for the echo. The new `gavb-other-type-full-body` arm shows V5 tells the two apart.
- The compliance-review row number (§2): row 14 updated, row 12 untouched.
- Ports, parameters and register maps: unchanged. No top-level port, parameter or register-map change.

## 7. Commands (plain shell)

```
python3 -B scripts/check_aecp_commands.py --write
make -C tb/aecp_cmds record
make check
./scripts/lint_hdl.sh
./scripts/run_suites.sh
python3 -B tb/aecp_cmds/mutants.py --output OUT --verilator verilator --jobs 1
python3 tb/pp_top/aecp_dispatch_mutants.py --output OUT --verilator verilator --jobs 1
make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2
./syn/yosys/ooc.sh --record-rom-digests KL_pp_shadow
./syn/yosys/ooc.sh KL_pp_shadow
```

## 8. Public trail

- TAKEN: issue #200 comment 6379949872.
- REVIEW READY: issue #200 comment 6385280946, head 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33.
- No push, no PR, no merge, no edit or deletion of any comment.
