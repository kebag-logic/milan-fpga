# Virtual E2E — test procedure and verification record

Status: **2026-08-01.** What tests exist for the boardless validation tier, the
exact commands to run them, what PASS/FAIL/BLOCKED mean, and the recorded
result against the current commit. Read with `VIRTUAL_E2E_HOWTO.md` (operator
guide), `VIRTUAL_E2E_QEMU.md` (roadmap), `TRUE_E2E_REQUIREMENTS.md` (requirement
IDs). **A green run here is a simulation result, never a hardware claim.**

## 1. The test set (what runs, and what each gate proves)

| gate | command | proves | typical time |
|---|---|---|---|
| T0 env-check | `./scripts/virtual-e2e.sh env-check` | host toolchain + RV32/RV64 artifacts present, hashed, on PATH | seconds |
| T1 M-A2 boot | `./scripts/virtual-e2e.sh t1` | real softcore boots real BIOS, reaches real `milan_datapath` RTL CSRs, reads `ID='MILN'` | ~100 s (cached) / few min (cold) |
| T2-prep | `./scripts/virtual-e2e.sh t2-prep` | RV32 image-boot prerequisites (kernel/rootfs/firmware/oracle source) | seconds (gate only) |
| T3-prep | `./scripts/virtual-e2e.sh t3-prep` | machine-to-machine prerequisites (QEMU, co-sim bridge headers, datapath RTL) | seconds (gate only) |
| all | `./scripts/virtual-e2e.sh all` | the full dependency graph in order, with honest BLOCKED semantics | ~100 s |

## 2. Exact commands (post-rebase verification run)

Run from the repo root `/home/alex/milan-fpga-hermes`:

```sh
# 0. Capture the baseline (what commit is under test?)
git rev-parse --short HEAD        # 55a68a45  (rebased onto 3c82068d)
git status --short

# 1. Invalidate the stale pre-rebase sim model.
#    The cached Vsim was built from pre-rebase sources; milan_sim.py changed in
#    the rebase (audio cd wiring + VERILATOR_THREADS hook), so it is NOT evidence.
mv sw/litex/build_milan_sim /tmp/build_milan_sim.pre-rebase

# 2. Syntax gates (cheap, no sim).
bash -n scripts/virtual-e2e.sh
python3 -m py_compile sw/litex/milan_sim.py scripts/ma2_sim_driver.py

# 3. Clean rebuild + boot proof, with the new threading hook exercised.
source /home/alex/litex-milan/venv/bin/activate     # REQUIRED (BIOS build shells out to python3 -m litex)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
VERILATOR_THREADS=auto python scripts/ma2_sim_driver.py \
  --repo /home/alex/milan-fpga-hermes --log /tmp/ma2_post_rebase.log

# 4. The tier gates.
./scripts/virtual-e2e.sh env-check
./scripts/virtual-e2e.sh t1
./scripts/virtual-e2e.sh all        # full graph; expected exit 2 (BLOCKED) today
```

## 3. Recorded result against commit `55a68a45`

| gate | result | key evidence |
|---|---|---|
| baseline | HEAD `55a68a45` ("virtual e2e: runner, sim driver, docs, evidence"), rebased onto `3c82068d` (listener counters / lwSRP walker) | `git log` |
| stale-cache invalidation | pre-rebase `build_milan_sim/` archived to `/tmp/build_milan_sim.pre-rebase` | mv |
| syntax | `bash -n` OK; `py_compile` OK | stdout |
| clean rebuild + boot (threading opt-in) | **PASS** — `M-A2: PASS prompt_reached=True dump_seen=True`, driver exit 0 | `/tmp/ma2_post_rebase.log` |
| T0 env-check | **PASS** — 19 PASS / 0 FAIL / 0 SKIP / 0 BLOCKED | `evidence/virtual-e2e-env-check-2026-08-01.md` |
| T1 M-A2 | **PASS** — 22 PASS / 0 FAIL / 0 SKIP / 0 BLOCKED; `t1.ma2.boot` + `t1.ma2.id-magic` both PASS | `evidence/virtual-e2e-t1-2026-08-01.md` |
| all (full graph) | **BLOCKED (exit 2)** — 35 PASS / 0 FAIL / 1 SKIP / 4 BLOCKED | `evidence/virtual-e2e-all-2026-08-01.md` |

The decisive ID dump (CPU reached the real RTL CSRs):

```
0x90000000  4e 4c 49 4d 21 00 01 00 05 7f 40 00 00 00 00 00  NLIM!.....@.....
```
`4e 4c 49 4d` = `NLIM` = **'MILN'** little-endian.

## 4. What the rebase changed (and why re-verification was required)

The rebase committed the virtual-E2E tier as `55a68a45` on top of a new RTL
base (`3c82068d`). Two changes touch the sim build, so the pre-rebase cached
`Vsim` could not be trusted:

1. **`sw/litex/milan_sim.py`** — added the `cd_audio` clock-domain wiring (the
   datapath's audio clock driven from `sys`) and the `VERILATOR_THREADS` /
   `VERILATOR_JOBS` hook (the LiteX sim toolchain's own `threads=`/`jobs=`,
   single-threaded default preserved). RV32 made the explicit default;
   `--xlen=64` kept supported.
2. **`sw/litex/milan_soc.py`** — `abspath` normalization of the RTL source base
   (a literal `./` in `__file__` used to eat one `dirname` level).

Re-verification therefore used a **clean rebuild**, not the cached model.

## 5. Verdict semantics (how to read any run)

| verdict | meaning |
|---|---|
| `PASS` | the assertion was observed to hold this run |
| `FAIL` | something that should work did not — the run is red on purpose |
| `SKIP` | optional item absent; does not gate |
| `BLOCKED` | a genuine prerequisite is absent; exit 2, **never** a pass |

`t2-prep` / `t3-prep` are **prerequisite gates, not tier passes.** A tier is
`PASS` only when its own acceptance criteria (with a working negative control)
have run. Today T2 is BLOCKED on the Linux-image boot (RAM sim model + wire
attachment) and T3 is BLOCKED on the two-node bridge, virtual L2, independent
AVDECC oracle, and negative control.

## 6. Honest boundaries (unchanged by the rebase)

- The RV32 OpenSBI firmware exists (`milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin`,
  verified DTB strings) but is a **custom LiteX-map** OpenSBI — it boots the
  Verilator exact-hardware lane and likely **not** stock
  `qemu-system-riscv32 -machine virt`. QEMU remains the orchestration lane.
- Hardware-only properties (PHY/RGMII timing, analog audio, Vivado-vs-Verilator
  differences, real gPTP timestamp quality) are `BLOCKED` in the virtual tier.
- Nothing here retires the bench.

## 7. Regression suites affected by the rebase base (RUN — recorded)

The new base `3c82068d` touches listener counters / lwSRP walker RTL. The
virtual-E2E gates above do not cover that; the corresponding suites were run as
a separate recorded gate on 2026-08-01 against `55a68a45`:

```sh
for s in lwsrp lwsrp_ctx lwsrp_rx lwsrp_switchpdu lwsrp_tx; do
  make -C "tb/verilator/$s" clean >/dev/null && make -C "tb/verilator/$s" -j"$(nproc)"
done
cd tests && behave -f plain
```

**Result: all PASS** — lwsrp_ctx 43 / lwsrp_rx 143 / lwsrp_tx 445 / lwsrp_switchpdu 7
checks with 0 failures; behave **520 scenarios passed, 0 failed**. Recorded in
`evidence/REBASE-REGRESSION-2026-08-01-55a68a45.md`. This is a *targeted* rebase
regression, not the full 55-suite sweep (`scripts/run_all_suites.sh` for that).

## 8. The virtual switch decision (B)

The switch architecture for T2/T3 is decided in
[`VIRTUAL_SWITCH_RESEARCH.md`](VIRTUAL_SWITCH_RESEARCH.md): a deterministic
userspace L2 switch (`virtwire`) as the primary CI backend, Linux bridge + `tc`
as a secondary wall-clock lane, P4 deferred. Raw-socket (`AF_PACKET`) is the
attachment point with a documented fidelity boundary (no PHY/FCS/preamble
validation). Implementation phases T2.0–T2.3 and the T3 machine-to-machine plan
are there.
