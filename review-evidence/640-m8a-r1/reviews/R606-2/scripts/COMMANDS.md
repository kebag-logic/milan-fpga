# R606-2 reproduction commands

Placeholders: `$HEAD` is a clone at `76605880a20005cbc2acad1b23ba2ccebde64ca8` with
`third_party/lwSRP`, `protocol-processor`, `gptp-processor` and `third_party/verilog-axis`
initialised; `$BASE` is `git archive ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` plus the
same four submodules (identical gitlinks), each made a git repository; `$PKT` is this
packet; `$LX` is a LiteX interpreter installed from `sw/litex/litex_pins.txt` with
`sw/litex/patches/apply.sh` applied; `$SDK` is the pinned Bootlin SDK installed with
`scripts/ci_rv32_sdk.py --destination $SDK --archive <archive>` (archive sha256
`d42680e9...`); `$PICO` is a `PYTHONPATH` naming checkouts of
`pythondata-software-picolibc` and `pythondata-software-compiler_rt`.

## Classifier self-test (finding F1)

    cd $HEAD && python3 -I scripts/ci_scope.py --selftest            # rc 1 at head
    cd $BASE && python3 -I scripts/ci_scope.py --selftest            # rc 0 at ac2c5e77
    cd $HEAD && python3 -I scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md   # false

## Lane test and LiteX aggregate (finding F2)

    # pinned elaborate interpreter as installed by elaborate.yml (no firmware data packages)
    cd $HEAD/sw/litex && MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc $LX test_ctrl_memory.py
    cd $HEAD && PYTHONPATH= MILAN_LITEX_PYTHON=$LX MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc \
        PATH=<pinned verilator 5.050 dir>:$PATH scripts/run_litex_sims.sh <logdir>     # 6/7, rc 1
    # same, with the firmware data packages importable
    PYTHONPATH=$PICO ... (same two commands)                                            # PASS; 7/7

## Firmware images (four points, split and flat)

    # runtime: ctrl_image_runtime.py needs -fno-stack-protector with the pinned SDK (pre-existing)
    sed 's/"-fno-common", /"-fno-common", "-fno-stack-protector", /' \
        $HEAD/sw/firmware/ctrl/test/ctrl_image_runtime.py > <tmp>/ctrl_image_runtime_nossp.py
    PYTHONPATH=$HEAD/sw/firmware/ctrl/test:$HEAD/sw/firmware/gtest MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc \
        python3 -B <tmp>/ctrl_image_runtime_nossp.py --picolibc <picolibc data> \
        --compiler-rt <compiler_rt data> --litex-software <litex>/soc/software --output $RT
    for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do for i in 1 2; do for lay in split flat; do
      MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py \
        --config configs/$cfg.yaml --interfaces $i --with-aecp --layout $lay --output <out>/$lay-$cfg-if$i \
        --libc $RT/libc.a --compiler-runtime $RT/libcompiler_rt.a
    done; done; done

## Exports (default digest, split CSR map)

    PYTHONHASHSEED=0 PYTHONPATH=$PICO $LX $PKT/scripts/export_soc.py <tree> <config-stem> <out> [--ctrl-mailbox [--ctrl-firmware ELF]]
    python3 -I $PKT/scripts/compare_exports.py <export-a> <tree-a> <export-b> <tree-b>

Run exports one at a time when a new CPU argument set must be generated: concurrent
generator runs in one VexiiRiscv checkout fail.

## ELF edge probe (suggestions S1, S2)

    python3 -I $PKT/scripts/probe_elf_edges.py $HEAD <scratch>
