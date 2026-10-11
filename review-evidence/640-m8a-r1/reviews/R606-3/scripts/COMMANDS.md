# R606-3 commands

`$CHECKOUT` is the exact-head clone (`ce10328c3d89d81509e47836fa4a48b22ecdbc20`), `$PACKET` this packet,
`$VENV` a CPython 3.12 venv holding only `pyyaml` and `sw/litex/litex_pins.txt` (`receipts/venv_freeze.txt`),
prepared as `elaborate.yml` does (`scripts/ci_litex_env.py`, then `PYTHON=python3 sw/litex/patches/apply.sh`).
`$VERILATOR` is the scoped Verilator 5.050 (`receipts/verilator_identity.txt`). Every run was foreground or
waited on by a foreground parent; each log has an `.rc` beside it.

Exact-head gates (from `$CHECKOUT`, `$VENV/bin` and `$VERILATOR` first on `PATH`):

```sh
python3 -I scripts/ci_scope.py --selftest                       # receipts/ci_scope_selftest.*
echo docs/design/SPLIT_CONTROL_MEMORY.md | python3 -I scripts/ci_scope.py
python3 -I scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md   # receipts/ci_scope_classify.*
python3 -I scripts/ci_events.py --check                         # receipts/ci_events_check.*
python3 -I scripts/ci_events.py --selftest                      # receipts/ci_events_selftest.*
python3 -I sw/litex/test_ctrl_memory.py                         # receipts/test_ctrl_memory.*
scripts/run_litex_sims.sh --selftest                            # receipts/litex_sims_selftest.*
scripts/run_litex_sims.sh <logs>                                # receipts/litex_sims_aggregate.*
<markdown-venv>/python3 scripts/docs_check.py                   # receipts/docs_check.*
<markdown-venv>/python3 scripts/check_em_dash.py --base 76605880a20005cbc2acad1b23ba2ccebde64ca8
<markdown-venv>/python3 scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86
<markdown-venv>/python3 scripts/gen_toc.py --check
python3 scripts/check_doc_style.py
git diff --check 76605880a20005cbc2acad1b23ba2ccebde64ca8 HEAD
```

Controls at the round-2 head (`git archive 76605880` into scratch, the three populated submodules linked in):

```sh
python3 -I scripts/ci_scope.py --selftest                       # receipts/control_76605880_ci_scope_selftest.*
python3 <R607-2>/probe_elf_loads.py <tree-76605880> <out>       # receipts/control_76605880_r607-2_probe_elf_loads.*
python3 $PACKET/scripts/probe_segments.py <tree-76605880> <out> # receipts/control_76605880_probe_segments.*
```

The external round's probes, unmodified (published at `b68338bf`, `review-evidence/640-m8a-r1/reviews/R607-2/`):

```sh
python3 probe_load_soc.py $CHECKOUT <out>    # receipts/r607-2_probe_load_soc.*  (rc 1 = no longer reproduces)
python3 probe_elf_loads.py $CHECKOUT <out>   # receipts/r607-2_probe_elf_loads.*
```

Reviewer probes:

```sh
python3 $PACKET/scripts/probe_segments.py $CHECKOUT <out>       # receipts/probe_segments_head.*
```

Four shipped split images, relinked (head archive copy with `third_party/lwSRP` cloned at its gitlink):

```sh
# runtime: sw/firmware/ctrl/test/ctrl_image_runtime.py plus -fno-stack-protector (receipts/runtime_tool.diff)
python3 ctrl_image_runtime.py --picolibc <picolibc data> --compiler-rt <compiler_rt data> \
  --litex-software $VENV/.../litex/soc/software --output <runtime>
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/<shape>.yaml --interfaces <1|2> \
  --with-aecp --layout split --output <out> --libc <runtime>/libc.a --compiler-runtime <runtime>/libcompiler_rt.a
python3 $PACKET/scripts/plan_images.py <tree> <riscv32 objcopy> <out>/split-*/ctrl_app.elf   # head and 76605880
```

Control with the SoC child's include hook removed (`receipts/control_no_include_hook.diff`, scratch copy):

```sh
python3 -I sw/litex/test_ctrl_memory.py      # receipts/control_no_include_hook.*
```

Trial merge with live dev, no checkout: `git merge-tree --write-tree --name-only HEAD 6bfeeb13...`.
Final clone check: `python3 $PACKET/scripts/verify_clone.py $CHECKOUT <head> <tree>`.
