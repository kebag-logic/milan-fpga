# R239-1 reproduction scripts (issue #372 / PR #518, head 60c5225f)

Every script is read-only on the review clone. Builds, probes and scratch
mutants live in the R239 scratch tree. Raw outputs are in `../raw/`.

| Script | What it does | Receipt(s) |
|---|---|---|
| `verify_tool_mtree.py <layer>` | Hashes every regular file listed in the layer's pacman mtree for `verilator-5.050-1` | `raw/tool-mtree.txt`, `raw/tool-identity.txt` |
| (inline, see REPORT) | `gpgv` of the cached package, archive `.MTREE` vs layer mtree | `raw/tool-package-chain.txt` |
| `export_head.sh` | `git archive` of the exact head plus the pinned `verilog-axis` bytes into scratch; blob proof 857/857 | `raw/export-proof.txt` |
| `run_focused_suite.sh` | `make -C tb/verilator/ptp_ts VERILATOR=<pinned 5.050>` in the export; `suite_tally.py --verdict` and the directory tally | `raw/focused-*` |
| `probes/build_probe.sh` + `probes/probe_reset.cpp` | Real mux + real checker + real bind, Makefile flags verbatim, driven through reset edge cases R1-R3 | `raw/probe-reset-*.log` |
| `probes/build_variants.sh` | Through `make mux-sva-build`: no `--assert`, bind omitted, bind with a width warning, instance-path bind | `raw/variant-*` |
| `probes/xprobe.sv`, `probes/pastprobe.sv`, `probes/assumeprobe.sv` | Two-state X, `$past`/`$stable` at the first edge, `cover`, `assume` on 5.050 | `raw/xprobe-*`, `raw/pastprobe-*`, `raw/assumeprobe-*` |
| `probes/r239_extra_mutants.py` | Eight extra scratch mutants judged by the campaign's own `detection()` | `raw/extra-mutants.txt` |
| `run_static_subset.sh` | Eleven docs-workflow gates, as `docs.yml` invokes them, in a scratch git clone at the head | `raw/static/` |
| `verify_clone_integrity.py` | Final review-clone identity, index, blob, kind/mode, hidden-flag and required-submodule proof | `raw/clone-integrity.txt` |

Default-error-limit probe (inline):
`<export>/tb/verilator/ptp_ts/obj_dir_mux_sva_w8/Vmux_sva +scenario=single_beats +stimulus_fault=s0_drop_tvalid`
-> `raw/probe-default-errlimit.log`.
