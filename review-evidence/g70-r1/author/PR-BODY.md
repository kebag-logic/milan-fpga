[A598]

Closes #70

The out-of-context recipe now gives synthesis its clock. `syn/ooc/engine_ooc.tcl` and `syn/ooc/ucpu_ooc.tcl` each read a new constraints file, `syn/ooc/ooc_clock.xdc`, before anything else and therefore before `synth_design`. That file holds the one clock definition, `create_clock -period 10.000 -name clk [get_ports clk_i]`, with the period unchanged at 10 ns. The `create_clock` that both scripts issued after `synth_design` since the first commit is gone, so the reported slack is now a constrained synthesis result rather than a post-hoc report on an unconstrained netlist.

A new check, `ooc clock order` (`syn/ooc/check_ooc_clock.py`), holds that order in the `make ooc` flow:

- Before Vivado starts, `run.sh` checks both scripts and the XDC. Each script must have exactly one `synth_design`, read `ooc_clock.xdc` before it, and issue no `create_clock`, `create_generated_clock`, `read_xdc` or `source` after it. The XDC must define exactly one 10.000 ns clock on `clk_i`.
- After both syntheses, `run.sh` checks the Vivado logs, which proves the order Vivado actually ran. A `read_xdc` echo of the file must precede `Command: synth_design`, and Vivado must report parsing the file inside synthesis before technology mapping. No constraint command may follow `synth_design completed successfully`.
- The `ooc` make target runs the check's 17-arm self-test first: one clean fixture and sixteen planted defects, with at least one arm per rule that only that rule catches.

No RTL, testbench, bench or repository-script file changes.

## Figures

Re-measured once at main `5dce647a` with each flow. Both used Vivado 2026.1 (lin64, SW Build 6511674) on `xc7a100tfgg484-2` with `synth_design -mode out_of_context` and the default directive, the shipping ROM, and a 10 ns clock on `clk_i`. The unconstrained column is `make ooc` of main itself; the constrained column is `make ooc` at this head.

| Top | Metric | Unconstrained (create_clock after synth_design) | Constrained (XDC read before synth_design) |
|---|---|---:|---:|
| KL_gptp_engine | Slice LUTs | 4,853 | 4,852 |
| KL_gptp_engine | Slice registers | 3,652 | 3,652 |
| KL_gptp_engine | Block RAM tiles | 1.5 | 1.5 |
| KL_gptp_engine | DSPs | 4 | 4 |
| KL_gptp_engine | WNS | +1.773 ns, 0 of 12,254 endpoints failing | +1.773 ns, 0 of 12,254 endpoints failing |
| KL_gptp_ucpu | LUTs / registers / BRAM / DSPs | 1,643 / 733 / 1.5 / 4 | 1,643 / 733 / 1.5 / 4 |
| KL_gptp_ucpu | WNS | +1.941 ns, 0 of 3,165 endpoints failing | +1.941 ns, 0 of 3,165 endpoints failing |

The only difference is one logic LUT inside the engine's microCPU instance. The timing report bodies are identical, with the same critical path and slack. The unconstrained run reproduces exactly the dated figures the manager guide carried (PR #76, 2026-09-24), which confirms they came from the unconstrained flow. The 2.249 ns cited in the issue is the PR #69-era engine figure; PR #76 later moved it to +1.773 ns.

## Documentation

- `docs/HDL_DEVELOPER.md` gains an "Out-of-context measurement" section with the flow, the check, both flows side by side with a Flow column and the tool identity, and a checklist item.
- `docs/MANAGER.md` gives each figure in the latest snapshot its flow. It keeps the PR #76 delta and labels it as the unconstrained flow.
- Every archived page that quotes out-of-context figures gains a flow note under its banner; no archived figure changes.
  - For this line's pages, the note records that `syn/ooc` issued `create_clock` after `synth_design` from the first commit `c99f7a8` through `5dce647a`.
  - For the prototype pages, the order is verified at `c99f7a8` only, because the prototype line's later scripts are not retained.

## Validation

At this head, with Verilator 5.050 first on the path, each command from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `make tb` | 0 | microCPU 768/768; parser 268/268; engine 1,613/1,613 in the shipping, request-seeded and Sync-seeded images; engine mutation arm 34/34; gaskets 81/81 plus 5/5 controls; tsn-gen 288/288 plus 4/4 controls; bench tag test PASS; no skips (fresh build) |
| `make contract` | 0 | PHC interface contract PASS |
| `make lint` | 0 | engine and bench lint clean |
| `make docs` | 0 | diagram check and self-test PASS; docs check PASS (11 current, 17 historical pages) and self-test PASS; source evidence 20 exact, 0 findings, self-test PASS |
| `make ooc` | 0 | `ooc clock order` self-test PASS (17 arms); script check PASS; both syntheses 0 critical warnings and 0 errors; log check PASS; six reports retained; tree clean afterwards |

Both logs show the clock defined before synthesis starts:

```text
ucpu_ooc.log    28:# read_xdc $SPEC/syn/ooc/ooc_clock.xdc   32:Command: synth_design ...   84:Parsing XDC File [.../syn/ooc/ooc_clock.xdc]   372:Start Technology Mapping
engine_ooc.log  28:# read_xdc $SPEC/syn/ooc/ooc_clock.xdc   38:Command: synth_design ...   116:Parsing XDC File [.../syn/ooc/ooc_clock.xdc]  443:Start Technology Mapping
```

Planted controls:

- Static check, run through `make ooc`. Moving `read_xdc` after `synth_design` stops the run before Vivado.
  - In `engine_ooc.tcl`: `ooc clock order: FAIL` with `engine_ooc.tcl: ooc_clock.xdc is not read before synth_design` and `engine_ooc.tcl:23: read_xdc after synth_design`.
  - In `ucpu_ooc.tcl`: the same two findings, ending at `ucpu_ooc.tcl:17`.
  - Restoring main's scripts: `create_clock after synth_design` at `ucpu_ooc.tcl:13` and `engine_ooc.tcl:20`.
  - The unplanted positive control passes the check.
- Log check on real synthesis. Both scripts were planted with `read_xdc` after `synth_design` and synthesized without the static check. The log check failed with six findings, including `engine_ooc.log:545: read_xdc after synth_design`, and that run's figures equal the unconstrained ones. Main's own logs fail the same check with `create_clock after synth_design`.
- Disabling each of the check's ten rules in turn makes its self-test fail: 10 of 10.

## Known limitations

- Out-of-context synthesis is not board timing qualification; no placement or routing was run.
- The microCPU source carries a comment quoting the other repository's 1,070-LUT anchor. This change leaves RTL untouched. The flow behind that anchor is described in the `ucpu_ooc.tcl` header instead.
- Comparing against figures dated before this change needs a run in the old order. The guides label every quoted figure with its flow for that reason.
