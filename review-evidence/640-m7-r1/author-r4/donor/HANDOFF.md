# Donor handoff, lane M7

Executor [A587]. Relates to #640 in the parent repository.

## Current continuation state

The earlier STOP is superseded by owner ruling 6162175442 on parent #640.
Donor `e4869fd0c42889b2ac806587cc5c78afb1c33461` and parent
`412e3f6c8c402bce63e94c291d2782b5579aaa1d` are committed and clean, local only.
The three authorized donor corrections are implemented; parent Python/C++
gates pass without budget changes. Clock controls pass 30/30 before and after;
parser passes 337/337 with identical output. All fixture data and expected
clock findings are unchanged. All 33 engine mutants now pass across five disjoint batches, with every original clean control passing. All other donor constituents pass. The final batch audit confirms complete coverage without duplicates. REVIEW READY on both heads.
The [current parent handoff](../HANDOFF.md#round-4-continuation) owns complete
commands, receipts, failure-attempt history and final campaign results.

## Round 4 initial STOP record

**STOP at parent integration gates.** The local donor merge is committed and
clean; the parent merge remains resolved/staged and uncommitted.

| Identity | Value |
|---|---|
| Donor branch | `640-m7` |
| Donor HEAD | `6b5a4282586a3851117674891d1955253e3de452` |
| First parent | `18dd997b2459699e41e5ce9bceca1181e41fa5fe` |
| Second parent | `61d486e9dfbff80739d7ce8cbac587b6f011648d` |
| Parent HEAD | `354f781828d8b4d73037129f297b072320a10f9c` |
| Parent MERGE_HEAD | `fa8209889411e8ca95757174c981f720dbcd95a2` |
| Parent staged tree | `3112cc103cfa17756ee0b5ede78aa0bdc9a46627` |

The merge contains both `18dd997b` and `7dda9c3b`. No push occurred. Commit
subject is `Merge main into 640-m7 and preserve both measurement histories`;
the configured local identity was used, with no body or trailers.

### Changes and conflict resolution

- `docs/MANAGER.md:29`: retain incoming constrained/unconstrained measurements,
  clock-order explanation and PR #76 comparison.
- `docs/MANAGER.md:72`: retain the M7 timer-storage table and comparison under a
  separate subsection. Explicitly identify the then-unconstrained flow and
  measured lane head `18dd997b`. This was the only donor conflict.
- `hdl/common/KL_gptp_timer.sv:80`, `:89`, `:107`: existing M7 deadline RAM
  conversion survives unchanged. It keeps its indexed write and combinational
  sweep read, with reset-backed validity in the existing armed bits.
- Incoming parser error handling, servo microcode, clock-order gate and docs
  are merged unchanged. Against `61d486e9`, only the timer conversion and the
  retained M7 measurement subsection differ.

### Gate table and planted defects

All commands ran with pinned Verilator 5.050 and GNU make 4.3, `MAKEFLAGS=w`.
Build parallelism was capped at two. Prepared Python environment was 3.12.3.

| Command / target | Result | Defect checked |
|---|---|---|
| `make contract lint docs` | rc 0 | PHC contract; engine/Arty lint; 9 diagram assets; docs 11 current/17 historical; 20 exact source anchors. Diagram/docs/source self-tests: 10/10/7 controls against changed assets and stale evidence. |
| `python3 syn/ooc/check_ooc_clock.py` | rc 0 | Clock must be loaded before synthesis with the required period/source. |
| `python3 syn/ooc/check_ooc_clock.py --selftest` | rc 0; 30 arms | Late/missing/wrong clock, missing log evidence, wrong port, unclocked registers and critical warnings. |
| `make -j8 tb`, microCPU constituent | 768/768 passes | Instruction/state-port behavior. |
| Same invocation, parser constituent | 337/337; 8/8 mutants caught | Error-at-every-byte, rejected-frame writes and contamination of the next accepted frame. |
| Same invocation, engine constituent | 1,613/1,613 at each of three seeds; 33/33 mutants caught | Protocol/servo, pairing, publication, timeout and result faults named by the campaign. |
| Same invocation, gaskets constituent | 81/81; 4/4 mutants caught | Byte transport/gasket faults. |
| `make -j8 -C tb/tsngen` | rc 0; 288/288; 3/3 mutants caught | Zeroed received sequence, discarded grandmaster identity, early EOF. |
| `make -j8 -C bench/arty test` | rc 0 | Simulated RX/TX tag transport; no hardware access. |
| Default ROM generator to scratch | rc 0; 1,016 real words, 13,312 bytes | Default image matches the parent re-record and incoming #621 image. |
| Parent Python/C++ idiom gates | **rc 1 each** | Exact sites below. |

The initial aggregate `make tb` returned **2**, because its interpreter lacked
PyYAML when it reached tsngen. All four earlier targets passed; tsngen and the
remaining Arty target were subsequently run separately to rc 0. All six targets
therefore have passing evidence, but no aggregate rc-0 receipt is claimed.
The donor campaigns catch 48 planted defects (8+33+4+3).

### Integration blockers

| Gate | Result | Exact imported source |
|---|---|---|
| `python3 scripts/check_py_idiom.py` | rc 1: long function 10 > 9; undocumented public function 1 > 0 | `gptp-processor/syn/ooc/check_ooc_clock.py:269`: `selftest` is 120 lines; `:370`: nested `findings` has no docstring |
| `python3 scripts/check_cpp_idiom.py` | rc 1: multi-declarator declaration 4 > 0 | `gptp-processor/tb/verilator/parser/sim_main.cpp:275`, `:1343`, `:1421`, `:1491` |

The two files equal incoming `61d486e9` byte-for-byte. At parent dev's donor
`7dda9c3b`, the parser has zero such findings and the clock checker is absent.
No ratchet was raised. Round 4's merge-only scope prevents unrequested cleanup.
The parent table mutation driver also requires a committed parent gitlink and
has no Round 4 verdict while the parent merge is stopped.

Additional inherited mismatch: `docs/MANAGER.md:103` says 1,008 words and `:111`
says `FUTO@13`; the generator reports 1,016 and `FUTO@249`. The incoming paragraph
was left unchanged and disclosed. The donor docs gate does not catch it.

### Primitive and resource before/after

Historical timer mapping: 256 FF plus read mux -> 5 RAM32M + 2 RAM32X1D.
Historical donor OOC engine: 4,853 -> 4,748 LUT; 3,652 -> 3,396 FF; unchanged
1.5 BRAM tiles and 4 DSP. WNS +1.773 -> +2.249 ns in the old unconstrained
flow. These are the two historical M7 comparison points, not a measurement
of this merge. The incoming constrained measurement remains separately listed.

Parent M0s recipe (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`) historical route:
LUT 50,267 -> 49,898; FF 54,413 -> 53,220; RAMB36/RAMB18 74/27 -> 74/25;
WNS +0.299 -> +0.122 ns; WHS +0.031 -> +0.019 ns. Route complete, every
then-recorded gate endpoint passed. Full primitive/route receipts are retained
in the parent HANDOFF.md, sections 5 and 6.

The incoming parser and microcode can alter engine/plane area and timing.
Clock-before-synthesis also changes the OOC flow. Parent dev adds other area
lanes, counters and SoC inputs. No new measurement was made after STOP and
none of the historical figures qualifies the merged head. Acceptance
re-recording remains M9's responsibility under D7.

### Receipts

Logs stay in `$VALIDATION_STORAGE/640m7-a587/r4/`; only hashes/sizes are copied here.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `donor-static.log` | 4270 | `9952220737bab66e7193481a4ea88053455f06c34f700226caba19a7e5fb7246` |
| `donor-tb.log` | 38731 | `59ba61deda6383547ee9322b5972f664e36651179d808943bb04a1eb3b59c5d5` |
| `donor-tsngen.log` | 1877 | `59c7abe36fba88cbbe46f805b37166199df9fbf88b67c23125a1e18c292f48ff` |
| `donor-arty.log` | 5041 | `192588704bf206c42b057e1eab8f3f9d34a303c80b38984a55d9375349fe3d84` |
| `donor-clock.log` | 68 | `95d7509d88fb0432367164d91a04052eea11195787c8cd4b986997967557c02f` |
| `donor-clock-self.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-rom.log` | 296 | `096cd71d0b654495a5c9ddd97b0e91567dcfc8df9464ee9832d96ad511745e5c` |
| `py-idiom.log` | 250 | `e67ee4daf8e2a54d14c8c6fc9fc59aa15887aee0e6047a4b4d88371d7556d1fc` |
| `cpp-idiom.log` | 133 | `a9d036222c8b7cabdfff022696286ce415728e909e3a87fb807055eb31a10e12` |
| `stop-provenance.log` | 1257 | `56f200227bfcf901fd339365e36ac64b89dba9420f9ee290b3185a3ae3097037` |
| `final-state.log` | 680 | `c0c3443a4d8d07403ae7748f4642b4486115ef91fed17deff48bacad8d51d5b8` |

Next step needs an assignment for the imported findings, without increasing
budgets. Then rerun the affected checks and resume the parent's staged merge.
No independent review of this merged head has been claimed.

Public STOP receipt: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162158855

Public REVIEW READY receipt: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162686301
