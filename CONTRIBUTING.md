# Contributing — house rules that keep this repo shippable

Short version: SystemVerilog only, banner-documented, one-line commits,
lane-per-worktree, every change grows the test suite, and nothing merges on
"looks right" — TB numbers or silicon numbers.

## 1. HDL house style (Cemal Dogan / Oguz Kahraman school)

- **SystemVerilog only** for new HDL. Python (migen/LiteX) is SoC *glue*,
  never new datapath logic.
- File head: SPDX line + banner comment stating what the module is and the
  one design decision that matters. `` `default_nettype none `` at the top,
  `` `default_nettype wire `` at the bottom.
- Ports documented **inline with `//!`** — the port list IS the spec.
- Naming: `_r` registered, `_w` wire/comb, `_p` one-cycle pulse, `_S` FSM
  states, `_C`/`_P` params. Named `always_ff`/`always_comb` blocks
  (`begin : name … end : name`).
- Reset: synchronous, active-low `rst_n`, every register reset. 2-space
  indent.
- CDC: only via the blessed primitives (`cdc_pulse`, `cdc_handshake`,
  toggle+sync); **clock-liveness observers must be `reset_less`** — never
  place an observer inside a reset cone its consumer drives (the 07-24
  link-guard deadlock).

## 2. Workflow

- **One lane = one worktree = one branch = one PR** (`~/milan-avb-multiwork`
  pattern). Copy (`cp -r`), never symlink, `third_party/` into a worktree —
  a symlink escapes to the main repo and builds silently stale RTL; then
  delete the copied submodule's `.git` file.
- **Commits: one line, no trailers.** Say CERT, never the A-word.
- PRs use the template: Status / Description / how-to-reproduce / how-to-
  validate / DoD. **Self-test results go in a PR comment** — a comment is
  evidence, not approval. Maintainer merges by default.
- `tests/steps/tsn_gen_steps.py` `LAYOUTS` merges are **semantic, never
  marker-union**: rebuild each command's block from its owning commit
  verbatim (naive unions broke main twice; a third time gets you named in
  this file).

## 3. Verification bar

- Every functional RTL change ships with a self-checking Verilator harness
  under `tb/verilator/<name>/` (`make` = build+run, exit code is the gate).
  See `docs/testing/TESTING.md` for the suite index and tiers.
- Coverage-matrix rows (`docs/testing/`) only move ✅ with a runnable test.
  Prefer real-wiring-path tests over unit mocks.
- **Measure, don't assume**: no number from a comment or model drives a
  decision. HW counter first; measure before AND after; a TB-green
  integration change still owes a datapath-regression run
  (`tb/verilator/milan_dp`).
- Timing claims need the full cell recipe (config + directive + seed); a
  bare WNS number is not reproducible. 3×32-thread Vivado discipline:
  single configs become 3-directive sweeps, keep best WNS.

## 4. Bench discipline (the expensive lessons)

- AX boot probes need **≥ 8 min** windows (power→network ≈ 7 min); a probe
  timeout is not a dead board.
- Never freeze the PCM ring mid-stream and plain re-enable (resume desync);
  full reset-reprogram.
- QSPI: never overwrite a slot without the current content dumped to disk
  first; DTB changes go through the **OpenSBI FW_FDT_PATH embed** (the dtb
  flash slot is not what the kernel boots on); regenerate the DTB from the
  build's `csr.csv` on ANY gateware block-set change (CSR-rot rule,
  `docs/integration/QSPI_FLASHBOOT.md`).
