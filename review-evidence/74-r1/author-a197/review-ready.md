[A197] REVIEW READY
Commit: `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` (branch `74-junction-chatter`, one commit on `dev` `ede8d48e`). **Not pushed from this lane.** Pushing and opening the PR are left to the maintainer; the PR body is prepared with `Relates to #74`.

Changed:
- `KL_media_grid_align`: the lock-phase keep-off. The engagement capture is clamped `DIV_C/128` (1/128 sample) clear of both ticks through the new defaulted `LOCK_KEEPOFF_CYC_P`. A non-raced engagement is bit-identical.
- `KL_chan_map_capture`: in the `2'b11` coincidence branch the tick now takes the pending marker, and the coincident marker pends in its place. The KNOWN CAVEAT is replaced by the law.
- `tb/verilator/media_grid_align`:
  - The wrap runs the real `KL_chan_map_capture` on the loop's marker and tick.
  - New arms: [G7] a lock raced ON the tick, with one edge of delivery jitter, 8 x 0.2 s, plus a held and a surplus frame at that lock; [G8] a lock raced from below; [G9] one free-running passage each way.
  - New mutants `MGA_MUT_NO_KEEPOFF` and `MGA_MUT_COIN`.
- `tb/verilator/chmap_capture`: [T0] gains 3 directed coincidence checks.
- Docs: the `REGISTER_MAP.md` `SLIP_TDM` paragraph (the "never a hidden slip" claim was false), a `TIME_SYNC.md` row, the `TESTING.md` row, and the bench README.

Validation (head, Verilator 5.050, at most 8 jobs):
- `make -C tb/verilator/media_grid_align`: 45/45. `MGA_MUT_U_SIGN` fails [G2], `MGA_MUT_NO_KEEPOFF` fails [G7] (5203 dups), and `MGA_MUT_COIN` fails [G9] (11 dups for 1 slip).
- `make -C tb/verilator/chmap_capture`: 204/204, plus netlist 20/20.
- `make -C tb/verilator/milan_dp aclk`: 139/139. The output is byte-identical to the same leg built with the two base RTL files.
- Base RTL with the branch harnesses: 13/45 and 3/204 fail, exactly the new checks. The G7 windows at base are {0, 0, 771, 2351, 2431, 1980, 1694, 1701} dups. [G9] at base counts 10 dups for one slip, and 0 skips with 9 dups for the mirrored slip. G0-G6 print identical results at base and head.
- Gates:
  - `lint_rtl --check`: 90<=90.
  - `check_sv_idiom`, `measure_naming --check`, `check_port_contracts`, `check_cpp_idiom`, `measure_test_evidence --check`, `check_hygiene --check`: pass.
  - `xvlog_gate --check`: PASS, 0 findings in `hdl/`.
  - `docs_check`, `gen_toc --check`, `check_doc_style`: pass.
  - `check_em_dash --base ede8d48e`: 0 findings over 35 added lines.
  - `git diff --check`: clean.

Acceptance criteria (item 2):
- **Met: no phantom dups at a slip-free raced lock.** [G7]/[G8] count 0 dups and 0 skips at lock, with the marker at least 14 cycles off every tick. At base the same lock counts thousands per window.
- **Met: a real slip still counts exactly once.** At the raced lock, a held frame is 1 dup and a surplus frame is 1 skip. A free-running passage is 1 dup or 1 skip, in its direction.
- **Met: the mutation.** Removing the keep-off fails [G7], and reverting the coincidence branch fails [G9].
- Counters, CSR words, `mr` triggers, CLOCK behaviour, shape and pins are unchanged, and every existing test population is kept. `milan_datapath.sv` and `milan_csr.sv` are untouched.

Open risks/questions:
- **Scope, for the reviewer.** The DECISION ships the keep-off plus a one-line counter-law repair; neither half suffices alone. If the repair is judged out of item 2's scope, say so here.
- **Acquisition counts.** An acquisition that starts within the loop's transient reach of a tick crosses it and comes back. With jitter, those crossings count balanced dup/skip pairs during acquisition ([G8]: 84/84). The lock itself counts none.
- **Jitter model.** The root's marker jitter is modelled as 0 or 1 edge. Its silicon width is unmeasured (bench items 1 and 4).
- **VERSION.** VERSION is not bumped, because it lives in `milan_csr.sv`. `SLIP_TDM` now counts a free-running slip once, in its direction; it used to count about a dozen dups per slip, so the next release note should say so.
- **Not run here.** Full parent, protocol-processor, gPTP, Yosys and builder banks, act, and hosted CI were not run in this lane.
